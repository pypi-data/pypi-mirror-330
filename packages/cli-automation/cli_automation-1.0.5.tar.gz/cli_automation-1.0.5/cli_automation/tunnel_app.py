# Manage SOCK5 Tunnel with Bastion Host
# Ed Scrimaglia

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ".")))
import typer
from typing_extensions import Annotated
from .progress_bar import ProgressBar
from .enums_srv import Logging
import asyncio
from .tunnel_srv import SetSocks5Tunnel
from . import logger

app = typer.Typer(no_args_is_help=True)

@app.command("setup", short_help="Setup SOCKS5 tunnel to the Bastion Host", no_args_is_help=True)
def set_tunnel(
        bastion_user: Annotated[str, typer.Option("--user", "-u", help="bastion host username", rich_help_panel="Tunnel Parameters", case_sensitive=False)],
        bastion_host: Annotated[str, typer.Option("--bastion", "-b", help="bastion name or ip address", rich_help_panel="Tunnel Parameters", case_sensitive=False)],
        local_port: Annotated[int, typer.Option("--port", "-p", help="local port", rich_help_panel="Tunnel Parameters", case_sensitive=False)] = 1080,
        verbose: Annotated[int, typer.Option("--verbose", "-v", count=True, help="Verbose level",rich_help_panel="Additional parameters", max=2)] = 0,
        log: Annotated[Logging, typer.Option("--log", "-l", help="Log level", rich_help_panel="Additional parameters", case_sensitive=False)] = Logging.info.value,
    ):

    async def process():
        set_verbose = {"verbose": verbose, "logging": log.value if log != None else None, "logger": logger, "bastion_host": bastion_host, "bastion_user":bastion_user ,"local_port": local_port}
        tunnel = SetSocks5Tunnel(set_verbose)
        await tunnel.set_tunnel()

    progress = ProgressBar()
    asyncio.run(progress.run_with_spinner(process))


@app.command("kill", short_help="Kill SOCKS5 tunnel to the bastion Host")
def kill_tunnel(
        verbose: Annotated[int, typer.Option("--verbose", "-v", count=True, help="Verbose level",rich_help_panel="Additional parameters", max=2)] = 0,
        log: Annotated[Logging, typer.Option("--log", "-l", help="Log level", rich_help_panel="Additional parameters", case_sensitive=False)] = Logging.info.value,
    ):
   
    async def process():
        set_verbose = {"verbose": verbose, "logging": log.value if log != None else None, "logger": logger}
        tunnel = SetSocks5Tunnel(set_verbose)
        await tunnel.kill_tunnel()
        
    progress = ProgressBar()
    asyncio.run(progress.run_with_spinner(process))


@app.callback(invoke_without_command=True, short_help="Manage SOCKS5 tunnel with Bastion Host")
def callback(ctx: typer.Context):
    """
    Sometimes, the machine running CLA doesn’t have direct access to the devices and must go through a Bastion Host or Jump Host. To connect via a Bastion Host, 
    you can either configure SSH specifically or set up a tunnel. Personally, I think creating a tunnel is more efficient since it avoids SSH configuration, 
    specially when using `cla telnet` commands. 
    Using `cla tunnel`, you can create or remove a SOCKS5 tunnel. For cla tunnel to function properly, the host running CLA must have easy access to the 
    Bastion Host (it should be listed in the Bastion Host's known_hosts file). CLA constantly monitors the tunnel’s status, but you can also manually check it using 
    the Linux command `lsof -i:{local_port}`.
    """
    typer.echo(f"-> About to execute {ctx.invoked_subcommand} sub-command")
    

# if __name__ == "__main__":
#     app()