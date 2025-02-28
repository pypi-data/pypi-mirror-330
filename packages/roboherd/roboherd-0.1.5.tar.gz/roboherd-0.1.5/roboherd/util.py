import click
import logging

from urllib.parse import urlparse
from almabtrieb import Almabtrieb


logger = logging.getLogger(__name__)


def parse_connection_string(connection_string: str) -> dict:
    """
    Parse a connection string into a dictionary of connection parameters.

    ```pycon
    >>> parse_connection_string("ws://user:pass@host/ws")
    {'host': 'host',
        'port': 80,
        'username': 'user',
        'password': 'pass',
        'websocket_path': '/ws'}

    >>> parse_connection_string("wss://user:pass@host/ws")
    {'host': 'host',
        'port': 443,
        'username': 'user',
        'password': 'pass',
        'websocket_path': '/ws'}

    ```
    """

    parsed = urlparse(connection_string)

    default_port = 80 if parsed.scheme == "ws" else 443

    return {
        "host": parsed.hostname,
        "port": parsed.port or default_port,
        "username": parsed.username,
        "password": parsed.password,
        "websocket_path": parsed.path,
    }


def create_connection(ctx):
    connection_string = ctx.obj["connection_string"]
    base_url = ctx.obj["base_url"]

    if not connection_string:
        click.echo("ERROR: No connection string provided")
        click.echo(
            "either provide one through --connection_string or set it in your configuration file"
        )
        exit(1)

    if not base_url:
        click.echo("ERROR: No base url for cows provided")
        click.echo(
            "either provide one through --base_url or set it in your configuration file"
        )
        exit(1)

    ctx.obj["connection"] = Almabtrieb.from_connection_string(
        connection_string, echo=ctx.obj["settings"].get("echo", False)
    )
