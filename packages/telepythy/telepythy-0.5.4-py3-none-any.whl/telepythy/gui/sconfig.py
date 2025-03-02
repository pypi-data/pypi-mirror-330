import os
import datetime
from enum import Enum
from typing import Type, Any

import platformdirs
from msgspec import Struct, field, yaml, to_builtins
from qtpy import QtGui, QtWidgets

import strictyaml

from ..lib import utils

class Profile(Struct):
    class Type(Enum):
        command = "command"
        connect = "connect"
        serve = "serve"

    name: str
    type: Type
    value: str

class Startup(Struct):
    source_path: str = field(default_factory=lambda: get_config_path('startup.py'))
    show_tips: bool = True

class Style(Struct):
    theme: str = "dark"
    syntax: str = "gruvbox-dark"
    font: QtGui.QFont = QtGui.QFont("monospace", 12)

class View(Struct):
    menu: bool = True

class Window(Struct):
    view: View = field(default_factory=lambda: View())
    size: tuple[int, int] = field(default_factory=lambda: default_window_size())

class Config(Struct):
    startup: Startup = field(default_factory=lambda: Startup())
    style: Style = field(default_factory=lambda: Style())
    window: Window = field(default_factory=lambda: Window())
    profiles: list[Profile] = field(default_factory=lambda: [
        Profile("default", Profile.Type.command, utils.DEFAULT_COMMAND)
    ])

def get_config_path(*names):
    cfg_dir = platformdirs.user_config_dir('telepythy', False)
    return os.path.join(cfg_dir, *names)

def default_window_size():
    size = QtWidgets.QApplication.primaryScreen().availableSize()
    return (int(size.width() / 2.5), int(size.height() / 1.5))

def enc_hook(obj: Any) -> Any:
    if isinstance(obj, QtGui.QFont):
        return f"{obj.family()},{obj.pointSize()}"
    else:
        raise NotImplementedError(f"Objects of type {type(obj)} are not supported")

def dec_hook(type: Type, obj: Any) -> Any:
    if type is QtGui.QFont:
        family, size = obj.split(',')
        return QtGui.QFont(family.strip(), int(size.strip()))
    else:
        raise NotImplementedError(f"Objects of type {type} are not supported")

def test():
    app = QtWidgets.QApplication()
    cfg = Config()

    x = to_builtins(
        cfg,
        builtin_types=(datetime.datetime, datetime.date),
        enc_hook=enc_hook,
    )

    print(strictyaml.YAML(x).as_yaml())

    # print(yaml.encode(cfg, enc_hook=enc_hook).decode())

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
