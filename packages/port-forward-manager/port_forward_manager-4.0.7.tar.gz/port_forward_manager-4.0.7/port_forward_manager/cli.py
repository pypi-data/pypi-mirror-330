from importlib.metadata import version as current_version
import os.path
import rich
from rich.prompt import Confirm
from sshconf import read_ssh_config
import time
import typer
import yaml

from port_forward_manager.core import models, tools, forward_sessions
from port_forward_manager.core import autocomplete
from port_forward_manager import cli_group, cli_schema, cli_session, cli_ssh_group
from port_forward_manager.core.normalisation import import_settings, export_settings

app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False)
app.add_typer(cli_group.app, name="group", help="Group management")
app.add_typer(cli_schema.app, name="schema", help="Schema management")
app.add_typer(cli_session.app, name="session", help="Session management")
app.add_typer(cli_ssh_group.app, name="ssh_group", help="SSH group management")
tools.load_settings()


@app.command()
def shutdown():
    """
    Stop all active sessions
    """

    settings = tools.settings()

    forward_sessions.update_state()
    for schema in models.Schema.index():
        for session in schema.sessions:
            if session.connected:
                forward_sessions.stop(session)
            session.active = False
        schema.active = False

    time.sleep(settings.wait_after_stop)
    models.db_session.commit()
    forward_sessions.show_active_sessions()


@app.command()
def status(
    schema: str = typer.Option(None, shell_complete=autocomplete.sc_schemas),
    host: str = typer.Option(None, shell_complete=autocomplete.sc_hosts),
    port: int = None,
    json: bool = typer.Option(False, "--json", "-j", help="Output JSON"),
):
    """
    Show active sessions
    """
    sessions = models.Session.get_active()
    if json:
        return yaml.dump(sessions, default_flow_style=False)

    forward_sessions.show_active_sessions(sessions)


@app.command()
def state():
    """
    Show current state in JSON format
    """

    ssh_config = read_ssh_config(os.path.expanduser("~/.ssh/config"))
    ssh_hosts = []
    for host in ssh_config.hosts():
        if "*" in host:
            continue
        hosts = host.split(" ")
        for hostname in hosts:
            ssh_hosts.append(hostname)

    forward_sessions.refresh_state()
    time.sleep(0.5)
    forward_sessions.update_state()
    current_state = {
        "groups": models.Group.get_state(),
        "schemas": models.Schema.get_state(),
        "sessions": models.Session.get_state(),
        "ssh_groups": models.SSHGroup.get_state(),
        "ssh_hosts": ssh_hosts
    }

    print(yaml.dump(current_state))
    # print(simplejson.dumps(current_state, indent=2))


@app.command()
def version():
    """
    Show PFM version
    """
    version_string = current_version("port_forward_manager")
    rich.print(f"Port Forward Manager [bold white]v{version_string}[/]")


@app.command()
def db_wipe():
    """Wipe the whole database clean"""
    if not Confirm.ask(
        "This action will wipe all groups, schemas and sessions, are you sure?"
    ):
        rich.print("Nothing was done.")

    models.reset_database()
    models.init_database()


@app.command()
def yaml_export(
    export_path: str = typer.Argument(None, help="YAML configuration file")
):
    """Import groups, schemas and sessions from configuration file"""
    export_data = export_settings()

    yaml_string = yaml.dump(export_data)
    if export_path:
        tools.write_file(export_path, yaml_string)
    else:
        print(yaml_string)


@app.command()
def yaml_import(
    export_path: str = typer.Argument(..., help="YAML configuration file"),
    wipe: bool = typer.Option(False, help="Wipe DB"),
    force: bool = typer.Option(False, help="Force wipe"),
    prune: bool = typer.Option(False, help="Prune missing entries"),
):
    """Import groups, schemas and sessions from configuration file"""
    settings = tools.load_yaml_file(export_path)

    if settings.get("export_format") != "db_dump":
        rich.print("[red]Invalid export file format[/]")
        exit()

    wipe_database = False

    if wipe and not force:
        if Confirm.ask("This action will wipe all groups, schemas and sessions, are you sure?"):
            wipe_database = True
    elif wipe and force:
        wipe_database = True

    if wipe_database:
        models.reset_database()
        models.init_database()

    change_count = import_settings(settings, prune)

    if change_count == 0:
        rich.print("No changes...")
    else:
        rich.print("There were {} items imported.".format(change_count))


def run():
    app()

