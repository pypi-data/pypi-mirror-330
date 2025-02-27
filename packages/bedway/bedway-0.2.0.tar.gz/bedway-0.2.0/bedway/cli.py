import asyncio
from functools import wraps

import click
import uvicorn

from .app import app


@click.command()
@click.option("--host", type=click.STRING, default="0.0.0.0")
@click.option("--port", type=click.INT, default=9128)
def serve(host, port):
    """
    Start the server.
    """
    uvicorn.run(app, host=host, port=port)


@click.group()
def cli():
    pass


cli.add_command(serve)
