import click

def display_help():
    click.echo("Available commands:")
    click.echo(f"{'Command'.ljust(20)}{'Alias'.ljust(10)}Description")
    click.echo("-" * 50)
    click.echo(f"{'create_datacenter'.ljust(20)}{'cda'.ljust(10)}Create a new datacenter")
    click.echo(f"{'create_room'.ljust(20)}{'crm'.ljust(10)}Create a new room in a datacenter")
    click.echo(f"{'create_bay'.ljust(20)}{'cby'.ljust(10)}Create a new bay in a room")
    click.echo(f"{'create_device'.ljust(20)}{'cde'.ljust(10)}Create a new device in a bay")
    click.echo(f"{'use'.ljust(20)}{'use'.ljust(10)}Enter a datacenter, room, or bay")
    click.echo(f"{'clear'.ljust(20)}{'clr'.ljust(10)}Clear the screen")
    click.echo(f"{'architecture'.ljust(20)}{'arch'.ljust(10)}Show the structure of a datacenter or device")
    click.echo(f"{'list'.ljust(20)}{'ls'.ljust(10)}List components like datacenters, rooms, bays, and devices")
    click.echo(f"{'exit'.ljust(20)}{'quit'.ljust(10)}Exit CloudCLI")

def show_manual(command):
    manual_path = f"manuals/{command}.txt"
    try:
        with open(manual_path, 'r') as f:
            click.echo(f.read())
    except FileNotFoundError:
        click.echo(f"No manual entry for '{command}'")
