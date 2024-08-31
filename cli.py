from cloudcli.commands import handle_command
from cloudcli.alt_commands import handle_alt_command
from cloudcli.utils import load_architecture, get_prompt
import click

@click.command()
def cli():
    load_architecture()
    click.echo("Welcome to CloudCLI. Type 'help' for a list of commands.")
    while True:
        command = click.prompt(get_prompt(), type=str)
        if command in ["exit", "quit"]:
            click.echo("Exiting CloudCLI.")
            break
        if command.split()[0] in ["list", "ls", "clear", "clr"]:
            handle_alt_command(command)
        else:
            handle_command(command)

if __name__ == '__main__':
    cli()
