import click
import os
from cloudcli.utils import context_path, architecture

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def list_components(component_type):
    if component_type == "datacenters":
        click.echo("Datacenters:")
        for datacenter in architecture.values():
            click.echo(f"- {datacenter['name']}")
    elif component_type == "rooms" and len(context_path) >= 1:
        datacenter_name = context_path[0]
        if datacenter_name in architecture:
            click.echo(f"Rooms in datacenter '{datacenter_name}':")
            for room in architecture[datacenter_name]['rooms']:
                click.echo(f"- {room['name']}")
        else:
            click.echo("No rooms found. Make sure you are in the correct datacenter.")
    elif component_type == "bays" and len(context_path) >= 2:
        datacenter_name, room_name = context_path[0], context_path[1]
        if datacenter_name in architecture:
            room = next((r for r in architecture[datacenter_name]['rooms'] if r['name'] == room_name), None)
            if room:
                click.echo(f"Bays in room '{room_name}' (datacenter '{datacenter_name}'):")
                for bay in room['bays']:
                    click.echo(f"- {bay['name']}")
            else:
                click.echo("No bays found. Make sure you are in the correct room.")
        else:
            click.echo("No bays found. Make sure you are in the correct room.")
    elif component_type == "devices" and len(context_path) >= 3:
        datacenter_name, room_name, bay_name = context_path[0], context_path[1], context_path[2]
        if datacenter_name in architecture:
            room = next((r for r in architecture[datacenter_name]['rooms'] if r['name'] == room_name), None)
            if room:
                bay = next((b for b in room['bays'] if b['name'] == bay_name), None)
                if bay:
                    click.echo(f"Devices in bay '{bay_name}' (room '{room_name}', datacenter '{datacenter_name}'):")
                    for device in bay['devices']:
                        click.echo(f"- {device['name']} ({device['type']})")
                else:
                    click.echo("No devices found. Make sure you are in the correct bay.")
            else:
                click.echo("No devices found. Make sure you are in the correct room.")
        else:
            click.echo("No devices found. Make sure you are in the correct bay.")
    else:
        click.echo(f"Unsupported component type or wrong context: {component_type}")

def handle_alt_command(command):
    parts = command.split()
    if not parts:
        return
    cmd = parts[0]
    args = parts[1:]

    if cmd in ["clear", "clr"]:
        clear_screen()
    elif cmd in ["list", "ls"] and len(args) == 1:
        list_components(args[0])
    else:
        click.echo("Invalid command or incorrect number of arguments. Type 'help' for a list of commands.")
