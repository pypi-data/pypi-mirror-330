"""
U-Phy Device handler

Run with uphy-device --handler [PATH_TO_FILE]
"""

import logging
from uphy.device import DeviceHandlerBase
import math
import time

LOGGER = logging.getLogger(__name__)


class DeviceHandler(DeviceHandlerBase):
    def _init(self) -> None:
        """System initialized."""

    def _set_outputs(self) -> None:
        """Update signal data."""

        # print(self.device.slots[0].outputs[0].values)

    def _get_inputs(self) -> None:
        """Update signal data."""

        # Example sinus plot on all inputs
        for slot in self.device.slots.values():
            for input in slot.inputs.values():
                values = [
                    round(60 + 60 * math.sin(time.time() + (ix * 2 * math.pi / input.values_len)))
                    for ix in range(input.values_len)
                ]
                input.values = values


if __name__ == "__main__":
    """
    Example for running without commandline helpers.
    it's recommended to use uphy-device --handler [PATH_TO_FILE]
    instead of running directly.
    """
    from uphy.device import Protocol, get_device_config, run_client_and_server
    from uphy.device.gui import Gui

    device, config, vars = get_device_config("path/to/model.json", Protocol.MODBUS)
    up = DeviceHandler(device, vars, config)
    with up.gui(Gui.dear):
        run_client_and_server(up, "eth0")
