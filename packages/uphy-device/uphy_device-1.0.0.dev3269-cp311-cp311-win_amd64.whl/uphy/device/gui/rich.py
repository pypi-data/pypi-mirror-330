from uphy.device import api
from functools import partial
from rich.live import Live
from rich.table import Table
from contextlib import contextmanager


@contextmanager
def gui(device: api.Device):
    def signals_table(signals: list[api.Signal]):
        signals_table = Table(show_header=False, expand=True, box=None)
        signals_table.add_column("Signal", width=25)
        signals_table.add_column("Value", width=5)
        for signal in signals:
            signals_table.add_row(
                signal.name, str(signal.value) if signal.value is not None else "NONE"
            )
        return signals_table

    def slots_table(device: api.Device):
        table = Table(show_lines=True)
        table.add_column("Slot")
        table.add_column("Inputs")
        table.add_column("Outputs")

        for slot in device.slots:
            table.add_row(
                slot.name, signals_table(slot.inputs), signals_table(slot.outputs)
            )

        return table

    with Live(
        get_renderable=partial(slots_table, device), refresh_per_second=4, screen=True
    ):

        def _render(*, status=""):
            pass

        yield _render
