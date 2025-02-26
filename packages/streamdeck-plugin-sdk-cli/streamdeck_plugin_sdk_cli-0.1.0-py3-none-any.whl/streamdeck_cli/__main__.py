import typer

from streamdeck_cli.commands.create import create
from streamdeck_cli.commands.pack import pack
from streamdeck_cli.commands.validate import validate


cli = typer.Typer()

# Typer doesn't currently have a better way of registering individual command
# functions than through its command decorator.
cli.command()(create)
cli.command()(pack)
cli.command()(validate)



if __name__ == "__main__":
    cli()
