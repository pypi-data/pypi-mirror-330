from enum import Enum
from contextlib import contextmanager
from typing import Protocol, Generator


class UpdateProtocol(Protocol):
    def __call__(self, **kwargs) -> None: ...


class GuiExit(Exception):
    pass


class Gui(str, Enum):
    rich = "rich"
    dear = "dear"
    none = "none"


@contextmanager
def none_gui(_):
    def update(*_, **__):
        pass

    yield update


@contextmanager
def get(gui: Gui, update: UpdateProtocol) -> Generator[UpdateProtocol, None, None]:
    if gui == Gui.rich:
        from . import rich

        gui_obj = rich.gui
    elif gui == Gui.dear:
        from . import dear

        gui_obj = dear.gui
    elif gui == Gui.none:
        gui_obj = none_gui
    else:
        raise Exception("Invalid gui")

    with gui_obj(update) as gui:
        yield gui
