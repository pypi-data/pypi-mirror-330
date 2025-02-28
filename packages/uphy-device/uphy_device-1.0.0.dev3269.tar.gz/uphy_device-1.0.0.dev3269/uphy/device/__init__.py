from collections.abc import Generator
from contextlib import contextmanager
from functools import partial
import importlib
from threading import Thread
import time
from typing import Optional
from uphy.device.api import (
    Up,
    ApiError,
    Device,
    SignalInfos,
    ProfinetConfig,
    EthercatDevice,
    ModbusDevice,
)
from yarl import URL
import logging
from time import sleep
from .server import server_binary
from .gui import Gui, GuiExit, UpdateProtocol
import subprocess
from abc import ABC, abstractmethod

from uphy.device import api
import upgen.model.uphy as uphy_model
from enum import Enum
import importlib.util
import importlib.resources
import sys

LOGGER = logging.getLogger(__name__)


class Protocol(str, Enum):
    ETHERCAT = "ethercat"
    PROFINET = "profinet"
    MODBUS = "modbus"
    ETHERNETIP = "ethernetip"


class DeviceError(Exception):
    pass


class UnsupportedError(DeviceError):
    pass


class DeviceHandlerBase(Up, ABC):
    _update: UpdateProtocol
    _status: str

    def __init__(
        self,
        device: Device,
        vars: SignalInfos,
        busconf: ProfinetConfig | EthercatDevice | ModbusDevice,
    ):
        LOGGER.debug(device)
        LOGGER.debug(vars)
        LOGGER.debug(busconf)

        super().__init__(device=device, vars=vars, busconf=busconf)
        self._init()

    def set_update_callback(self, update: UpdateProtocol):
        self._update = update

    @contextmanager
    def gui(self, gui_arg: Gui) -> Generator[None, None, None]:
        with gui.get(gui_arg, self.device) as update:
            self.set_update_callback(update)
            yield

    @abstractmethod
    def _init():
        """Handler started"""
        pass

    @abstractmethod
    def _set_outputs():
        """System initialized."""
        pass

    @abstractmethod
    def _get_inputs():
        """Update data."""
        pass

    def _error_ind(self, error_code) -> None:
        LOGGER.error("ERROR: error_code=%s", error_code)
        self._status = f"Error: {error_code}"

    def _avail(self) -> None:
        LOGGER.debug("AVAIL")
        self.read_outputs()
        self._set_outputs()

    def _sync(self) -> None:
        LOGGER.debug("SYNC")
        self._get_inputs()
        self.write_inputs()

    def _status_ind(self, status: int) -> None:
        LOGGER.info("STATUS: %s", status)
        self._status = str(status)

    def _profinet_signal_led_ind(self) -> None:
        LOGGER.info("PROFINET LED SIGNAL")

    def _poll_ind(self) -> None:
        LOGGER.debug("POLL")

        self.read_outputs()
        self._set_outputs()

        self._get_inputs()
        self.write_inputs()

        if self._update:
            self._update(status=self._status)


def get_sample_model() -> uphy_model.Root:
    try:
        with importlib.resources.as_file(importlib.resources.files(__name__)) as base:
            if (path := base / "share" / "digio.json").exists():
                return uphy_model.Root.parse_file(str(path))
    except Exception as exception:
        raise DeviceError(str(exception)) from exception
    else:
        raise DeviceError("Can't find sample model")

def _get_handler(handler: Optional[str]):
    if handler:
        spec = importlib.util.spec_from_file_location("uphy.device.handler", handler)
        device_handler_module = importlib.util.module_from_spec(spec)
        sys.modules["uphy.device.handler"] = device_handler_module
        spec.loader.exec_module(device_handler_module)
    else:
        from . import handler as device_handler_module

    return device_handler_module.DeviceHandler


def get_device_config(model: uphy_model.Root, protocol: Protocol):
    root = model
    device = api.Device(root, root.devices[0])
    vars = api.SignalInfos.from_slots(device.slots.values())

    if protocol == Protocol.ETHERCAT:
        config = api.EthercatDevice(root, root.devices[0])
    elif protocol == Protocol.PROFINET:
        config = api.ProfinetConfig(root, root.devices[0])
    elif protocol == Protocol.MODBUS:
        config = api.ModbusDevice(root, root.devices[0])
    elif protocol == Protocol.ETHERNETIP:
        config = api.EthernetIPConfig(root, root.devices[0])
    else:
        raise UnsupportedError(f"Unsupported protocol: {protocol}")

    return device, config, vars


def get_device_handler(
    protocol: Protocol, model: uphy_model.Root = None, handler: Optional[str] = None
) -> DeviceHandlerBase:
    """Create a device handler from protocol and model information."""
    device_handler = _get_handler(handler)
    device, config, vars = get_device_config(model, protocol)
    return device_handler(device=device, vars=vars, busconf=config)


def init_transport_url(up: Up, transport: str):
    url = URL(transport)
    if url.scheme == "tcp":
        up.tcp_transport_init(
            url.host if url.host else "localhost", url.port if url.port else 5150
        )
    elif url.scheme == "":
        up.serial_transport_init(transport)
    else:
        raise ApiError(f"Unknown transport {transport}")


def run_client_blocking(up: Up, transport: str):
    try:
        LOGGER.info("Starting transport")
        init_transport_url(up, transport)

        up.rpc_init()

        while True:
            LOGGER.info("Starting application")

            up.rpc_start()
            up.init_device()

            up.start_device()

            up.write_inputs()

            up.enable_watchdog(True)

            while up.worker():
                pass

            LOGGER.info("Restarting application")
    except ApiError as exception:
        LOGGER.error(exception)
    except GuiExit:
        pass


def run_client(
    up: Up,
    transport: str,
):
    # Run off main thread to make sure main thread can handle signals
    runner = Thread(
        target=partial(run_client_blocking, up, transport),
        name="Device Runner",
        daemon=True,
    )
    runner.start()
    while runner.is_alive():
        sleep(1)


def run_client_and_server(up: Up, interface: str):
    server = server_binary()

    server_runner = subprocess.Popen([server, interface])
    time.sleep(1)
    try:
        client_runner = Thread(
            target=partial(run_client_blocking, up, "tcp://localhost"),
            name="Device Runner",
            daemon=True,
        )
        client_runner.start()

        while client_runner.is_alive():
            sleep(1)

    finally:
        server_runner.kill()
        server_runner.wait()


def run_server(interface: str):
    server = server_binary()
    subprocess.run([server, interface])
