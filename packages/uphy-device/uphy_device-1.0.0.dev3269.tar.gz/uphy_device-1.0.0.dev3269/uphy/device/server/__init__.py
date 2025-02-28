import importlib.resources
import logging
from pathlib import Path
import subprocess
import sys
import typer

if sys.platform == "win32":
    server_name = "server.exe"
else:
    server_name = "server"

LOGGER = logging.getLogger(__name__)

def server_binary_path() -> Path:
    with importlib.resources.as_file(importlib.resources.files(__name__)) as base:
        if (path := base / "bin" / server_name).exists():
            return path
        raise Exception("Can't find server binary")

def server_binary() -> Path:
    path = server_binary_path()
    if sys.platform == "linux":
        setcap_check(path)
    return path

def setcap_permissions() -> str:
    return "cap_net_raw,cap_net_admin,cap_net_bind_service+ep"

def setcap_check(path: Path):
    update = ["setcap", setcap_permissions(), str(path)]
    check = ["setcap", "-v", setcap_permissions(), str(path)]
    try:
        subprocess.check_output(check)
    except subprocess.CalledProcessError:
        LOGGER.warning(
            "You need to allow raw sockets and binding to low port numbers for server to function."
        )
        confirm = typer.confirm("Do you wish automatically adjust permissions using policy kit")
        if confirm:
            try:
                subprocess.check_output(["pkexec", *update])
                return
            except subprocess.CalledProcessError:
                LOGGER.error("Failed to adjust permissions")

        typer.echo()
        typer.echo("Run the following as root or privileged user:")
        typer.echo()
        typer.echo(" ".join(update))
        typer.echo()
        exit(-1)
    except FileNotFoundError:
        # System does not support setcap, could be widows for example
        pass
