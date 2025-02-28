import dearpygui.dearpygui as dpg
import math
import logging
from uphy.device import api
from threading import Thread, Event
from contextlib import contextmanager
from collections import deque
from time import time
from . import GuiExit

LOG = logging.getLogger(__name__)

datatype_to_min_max = {
    api.UP_DTYPE_INT8: (-(2**7), 2**7 - 1),
    api.UP_DTYPE_INT16: (-(2**15), 2**15 - 1),
    api.UP_DTYPE_INT32: (-(2**31), 2**31 - 1),
    api.UP_DTYPE_UINT8: (0, 2**8 - 1),
    api.UP_DTYPE_UINT16: (0, 2**16 - 1),
    api.UP_DTYPE_UINT32: (0, 2**31 - 1), # Incorrect max but larger values do not work with dpg
    api.UP_DTYPE_REAL32: (-math.inf, math.inf),
}


class SignalPlot:
    x_axis: int | str
    y_axis: int | str
    series: list[int | str]
    x_data: deque[float]
    y_datas: list[deque[int]]
    value_ids: list[int | str]
    signal: api.Signal

    def __init__(self, signal: api.Signal, writable: bool):
        self.signal = signal
        self.value_ids = []

        min_value, max_value = datatype_to_min_max[signal.datatype]


        with dpg.group():
            for index in range(signal.values_len):
                def _update_signal(_, app_data, __):
                    LOG.info("Update signal %s[%d] : %s to %s", signal.name, index, signal.values[index], app_data)
                    signal.values[index] = app_data

                if writable:
                    value_id = dpg.add_input_int(
                        default_value=(
                            signal.values[index] if signal.values[index] is not None else 0
                        ),
                        on_enter=True,
                        callback=_update_signal,
                        user_data=signal,
                        min_value=min_value,
                        max_value=max_value,
                        min_clamped=True,
                        max_clamped=True,
                    )
                else:
                    value_id = dpg.add_text(
                        default_value=(
                            signal.values[index] if signal.values[index] is not None else 0
                        ),
                    )
                self.value_ids.append(value_id)

        with dpg.plot(height=100, no_title=True, no_menus=True, no_child=True):
            maxlen = 1000
            self.x_axis = dpg.add_plot_axis(dpg.mvXAxis, no_tick_labels=True)
            self.y_axis = dpg.add_plot_axis(
                dpg.mvYAxis, no_tick_labels=True, auto_fit=True
            )
            self.x_data = deque(maxlen=maxlen)
            self.x_data.extend(range(maxlen))

            self.series = []
            self.y_datas = []
            for index in range(signal.values_len):
                data = deque(maxlen=maxlen)
                data.extend([math.nan] * maxlen)
                series = dpg.add_line_series(parent=self.y_axis, x=[], y=[])
                self.series.append(series)
                self.y_datas.append(data)

    def update(self):
        values = self.signal.values
        self.x_data.append(time())
        dpg.set_axis_limits(self.x_axis, 0, len(self.x_data))

        for value, series, datas in zip(values, self.series, self.y_datas):
            datas.append(value if value is not None else math.nan)
            dpg.set_value(series, [tuple(range(len(datas))), tuple(datas)])

        for value, value_id in zip(values, self.value_ids):
            dpg.set_value(value_id, value if value is not None else 0)


@contextmanager
def gui(device: api.Device):

    startup = Event()

    plots: list[SignalPlot] = []

    def _gui_init():
        dpg.create_context()
        dpg.create_viewport(title=f"U-PHY: {device.name}")
        dpg.setup_dearpygui()

        def on_key_q(s, a, u):
            if dpg.is_key_down(dpg.mvKey_LControl):
                LOG.info("Exiting")
                dpg.stop_dearpygui()

        def on_key_esc(s, a, u):
            LOG.info("Exiting")
            dpg.stop_dearpygui()

        with dpg.handler_registry(tag="__keyboard_handler"):
            dpg.add_key_press_handler(key=dpg.mvKey_Q, callback=on_key_q)
            dpg.add_key_press_handler(key=dpg.mvKey_Escape, callback=on_key_esc)

        with dpg.window(label=f"U-PHY: {device.name}", tag="signals", autosize=True):

            with dpg.group(indent=10, horizontal=True, horizontal_spacing=10):
                dpg.add_checkbox(
                    label="CONNECTED",
                    enabled=False,
                    tag="is_connected"
                )
                dpg.add_checkbox(
                    label="CONFIGURED",
                    enabled=False,
                    tag="is_configured"
                )
                dpg.add_checkbox(
                    label="RUNNING",
                    enabled=False,
                    tag="is_running"
                )

            for slot in device.slots.values():
                dpg.add_text(f"{slot.name}")
                dpg.add_separator()

                with dpg.group(indent=10), dpg.table(header_row=False):
                    dpg.add_table_column()
                    dpg.add_table_column()
                    dpg.add_table_column()

                    for signal in slot.inputs.values():
                        with dpg.table_row():
                            dpg.add_text(signal.name)
                            plots.append(SignalPlot(signal, True))

                dpg.add_separator()

                with dpg.group(indent=10), dpg.table(header_row=False):
                    dpg.add_table_column()
                    dpg.add_table_column()
                    dpg.add_table_column()

                    for signal in slot.outputs.values():
                        with dpg.table_row():
                            dpg.add_text(signal.name)
                            plots.append(SignalPlot(signal, False))

                dpg.add_separator()

                with dpg.group(indent=10), dpg.table(header_row=False):
                    dpg.add_table_column()
                    dpg.add_table_column()
                    dpg.add_table_column()

                    for param in slot.params.values():
                        min_value, max_value = datatype_to_min_max[signal.datatype]
                        with dpg.table_row():
                            dpg.add_text(param.name)

                            def _update_signal(_, app_data, __):
                                param.values[0] = app_data
                                LOG.info(f"Update param {param.name} : {list(param.values)} to {list(param.values)}")

                            dpg.add_input_int(
                                default_value=(
                                    param.values[0] if param.values is not None else 0
                                ),
                                on_enter=True,
                                callback=_update_signal,
                                min_value=min_value,
                                max_value=max_value,
                                min_clamped=True,
                                max_clamped=True,
                            )

        dpg.set_primary_window("signals", True)
        dpg.show_viewport()

    def _gui_run():
        try:
            try:
                _gui_init()
            finally:
                startup.set()
            dpg.start_dearpygui()
        finally:
            # We should destroy context here, but this crashes with
            # exit() for some reason, causing other shutdown to fail
            # dpg.destroy_context()
            pass

    def _render(*, status=""):
        if not dpg.is_dearpygui_running():
            raise GuiExit()

        status = int(status)
        dpg.set_value("is_running", (status & api.UP_CORE_RUNNING) != 0)
        dpg.set_value("is_configured", (status & api.UP_CORE_CONFIGURED) != 0)
        dpg.set_value("is_connected", (status & api.UP_CORE_CONNECTED) != 0)
        for plot in plots:
            plot.update()

    gui_thread = Thread(target=_gui_run, daemon=True, name="GUI Runner")
    gui_thread.start()
    startup.wait()
    try:
        yield _render
    finally:
        if dpg.is_dearpygui_running():
            dpg.stop_dearpygui()
        gui_thread.join()
