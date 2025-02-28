from contextlib import nullcontext
import faulthandler
import importlib.metadata
from typing import Optional, Annotated

import typer.rich_utils
from uphy.device import gui
from uphy.device import api
import logging
import typer
from pathlib import Path
from rich.logging import RichHandler
from rich.table import Table
from rich import print
import importlib.metadata
import importlib.util
import importlib.resources
import psutil
import upgen.model.uphy as uphy_model
from uphy.cli import VERBOSE_OPTION, configure_logging

from . import (
    get_device_handler,
    get_sample_model,
    DeviceError,
    run_client,
    run_client_and_server,
    run_server,
    Protocol,
    LOGGER,
)

from .server import server_binary_path

faulthandler.enable()

APP_HELP="""
U-Phy Device tools with support for controlling and executing a U-Phy server for simulation and execution of a fieldbus device inside a python program.
"""

app = typer.Typer(
    pretty_exceptions_enable=False,
    no_args_is_help=True,
    name="device",
    help=APP_HELP,
)

INTERFACES = psutil.net_if_addrs()

def _model_parser(path: Path) -> uphy_model.Root:
    try:
        return uphy_model.Root.parse_file(str(path))
    except Exception as exception:
        raise typer.BadParameter(str(exception)) from exception

def _interface_parser(interface: str) -> str:
    interfaces = list(INTERFACES.keys())
    if interface.isnumeric():
        index = int(interface)
        try:
            return interfaces[index]
        except IndexError:
            pass

    if interface in INTERFACES:
        return interface

    raise typer.BadParameter(
        f"Interface '{interface}' not found in {interfaces}",
    )

def _interface_prompt_list():
    def _interface_describer(name: str, addresses: list[tuple]):
        addresses_str = ", ".join(
            f"{address[1]}"
            for address in addresses
        )
        return f"{name} ({addresses_str})"
    return "\n".join(
        f"[{idx}] {_interface_describer(name, interface)}"
        for idx, (name, interface) in enumerate(INTERFACES.items())
    )

INTERFACE_HELP = "The network interface to run the server on. NOTE: This should not be your main network card, but a secondary card used for protocol data."
INTERFACE_PROMPT = f"""
The tool needs to know which network interface to run the protocol stack on.

NOTE: This preferably should not be your main network card,
      but a secondary card used for protocol data. Some protocols
      (profinet, ...) may need to reconfigure the network
      configuration to run properly.

{_interface_prompt_list()}

Select interface"""

INTERFACE_OPTION = typer.Option(
    help=INTERFACE_HELP,
    metavar="INTERFACE",
    parser=_interface_parser,
    prompt=INTERFACE_PROMPT,
)
TRANSPORT_HELP = "The target transport to connect to the running server. 'tcp://' for network localhost access, '/dev/uphyX' or 'COMX') for serial connection to device."
MODEL_HELP = "Path to a U-Phy device model json file. If no model is specified a default built in model will be used."
MODEL_OPTION = typer.Option(help=MODEL_HELP, parser=_model_parser, metavar="MODEL")
HANDLER_HELP = "Path to custom device handler python script. A template file can be generated using 'uphy-device export-handler'."


def server_print_path(value: bool):
    if value:
        typer.echo(server_binary_path())
        exit(0)

SERVER_PRINT_PATH_HELP = "Print path for server only"
SERVER_PRINT_PATH_OPTION = typer.Option(is_eager=True,callback=server_print_path, allow_dash=True, help=SERVER_PRINT_PATH_HELP)

configure_logging(level=logging.INFO)

@app.command(no_args_is_help=True, rich_help_panel="Run")
def client(
    protocol: Protocol,
    transport: Annotated[
        str,
        typer.Option(help=TRANSPORT_HELP),
    ],
    model: Annotated[Optional[uphy_model.Root], MODEL_OPTION] = None,
    verbose: Annotated[bool, VERBOSE_OPTION] = False,
    handler: Annotated[Optional[str], typer.Option(help=HANDLER_HELP)] = None,
    gui_arg: Annotated[gui.Gui, typer.Option("--gui")] = gui.Gui.dear,
):
    """Run a client on this system, connecting to a server over an RPC transport protocol"""

    try:
        if model is None:
            model = get_sample_model()

        up = get_device_handler(protocol, model, handler)
        with up.gui(gui_arg):
            run_client(up, transport)

    except (DeviceError, api.ApiError) as exception:
        LOGGER.error(str(exception))
        LOGGER.debug("", exc_info=True)
    except gui.GuiExit:
        pass


@app.command(no_args_is_help=True, rich_help_panel="Run")
def mono(
    protocol: Protocol,
    interface: Annotated[
        str,
        INTERFACE_OPTION,
    ],
    model: Annotated[Optional[uphy_model.Root], MODEL_OPTION] = None,
    verbose: Annotated[bool, VERBOSE_OPTION] = False,
    handler: Annotated[Optional[str], typer.Option(help=HANDLER_HELP)] = None,
    gui_arg: Annotated[gui.Gui, typer.Option("--gui")] = gui.Gui.dear
):
    """Run a client and server on same system."""
    try:
        if model is None:
            model = get_sample_model()

        up = get_device_handler(protocol, model, handler)
        with up.gui(gui_arg):
            run_client_and_server(up, interface)

    except (DeviceError, api.ApiError) as exception:
        LOGGER.error(str(exception))
        LOGGER.debug("", exc_info=True)
    except gui.GuiExit:
        pass


@app.command()
def build():
    """Start building your device model"""

    print("To start building your device you need to create a model of your device describing its inputs and outputs.")
    print("This is done using RT-Labs device builder at https://devicebuilder.rt-labs.com/")
    print()
    print("After you have configured your model, download the model file into a known location")
    print()
    print()
    if typer.confirm(
        "Start a web browser navigating to this location?"
    ):
        typer.launch("https://devicebuilder.rt-labs.com/")


@app.command()
def export_handler(file: Annotated[typer.FileBinaryWrite, typer.Argument(mode="xb")]):
    """Export a template handler to file"""
    with importlib.resources.open_binary(__package__, "handler.py") as template:
        file.write(template.read())


@app.command(no_args_is_help=True, rich_help_panel="Run")
def server(
    interface: Annotated[
        str,
        INTERFACE_OPTION,
    ],
    verbose: Annotated[bool, VERBOSE_OPTION] = False,
    print_path: Annotated[bool, SERVER_PRINT_PATH_OPTION]=False
):
    """Start a u-phy server on your local system. This will listen to connections from client instances to run the u-phy system."""
    try:
        run_server(interface)
    except (DeviceError, api.ApiError) as exception:
        LOGGER.error(str(exception))
        LOGGER.debug("", exc_info=True)


@app.command(rich_help_panel="Extra")
def discover():
    """Tries to discovery locally attached u-phy servers"""
    import serial.tools.list_ports

    table = Table("ID", "Serial Number", "Subsystem", title="Serial ports")
    for port in serial.tools.list_ports.comports():
        LOGGER.debug(port.usb_info())
        if port.vid != 0x04D8 or port.pid != 0x1301:
            continue
        index = port.location.split(".")[-1]
        if index == "0":
            system = "server"
        elif index == "2":
            system = "console"
        else:
            system = "unkown"
        table.add_row(port.name, port.serial_number, system)

    print(table)


@app.command(rich_help_panel="Extra")
def readme():
    """Open browser at main documentation site"""

    print("The main documentation site for U-Phy is located at https://docs.rt-labs.com/u-phy.")
    if typer.confirm(
        "Start a web browser navigating to site?"
    ):
        typer.launch("https://docs.rt-labs.com/u-phy")


if __name__ == "__main__":
    app()
