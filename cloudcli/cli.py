# cloudcli/cli.py

import os
import json
import click

BASE_DIR = "architecture"
MANUALS_DIR = "manuals"

# Load existing architecture when the script starts
architecture = {}

if os.path.exists(BASE_DIR):
    for filename in os.listdir(BASE_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(BASE_DIR, filename), 'r') as f:
                datacenter = json.load(f)
                architecture[datacenter['name']] = datacenter

# Helper function to save the current state of the architecture
def save_architecture():
    for name, datacenter in architecture.items():
        with open(os.path.join(BASE_DIR, f"{name}.json"), 'w') as f:
            json.dump(datacenter, f, indent=4)

# Display the manual for a given command
def show_manual(command):
    manual_path = os.path.join(MANUALS_DIR, f"{command}.txt")
    if os.path.exists(manual_path):
        with open(manual_path, 'r') as f:
            click.echo(f.read())
    else:
        click.echo(f"No manual entry for '{command}'")

# Command implementations
def create_datacenter(args):
    name, location, number_of_rooms = args
    datacenter = {
        'name': name,
        'location': location,
        'number_of_rooms': int(number_of_rooms),
        'rooms': []
    }
    architecture[name] = datacenter
    save_architecture()
    click.echo(f"Datacenter '{name}' created at location '{location}' with {number_of_rooms} rooms.")

def create_room(args):
    name, datacenter_name = args
    if datacenter_name not in architecture:
        click.echo(f"Datacenter '{datacenter_name}' does not exist.")
        return
    room = {
        'name': name,
        'bays': []
    }
    architecture[datacenter_name]['rooms'].append(room)
    save_architecture()
    click.echo(f"Room '{name}' created in datacenter '{datacenter_name}'.")

def create_bay(args):
    size_in_u, room_name, datacenter_name = args
    if datacenter_name not in architecture:
        click.echo(f"Datacenter '{datacenter_name}' does not exist.")
        return
    rooms = architecture[datacenter_name]['rooms']
    room = next((r for r in rooms if r['name'] == room_name), None)
    if not room:
        click.echo(f"Room '{room_name}' does not exist in datacenter '{datacenter_name}'.")
        return
    bay = {
        'size_in_u': int(size_in_u),
        'devices': []
    }
    room['bays'].append(bay)
    save_architecture()
    click.echo(f"Bay of size {size_in_u}U created in room '{room_name}' at datacenter '{datacenter_name}'.")

def create_device(args):
    size_in_u, name, device_type, bay_position, room_name, datacenter_name = args
    if datacenter_name not in architecture:
        click.echo(f"Datacenter '{datacenter_name}' does not exist.")
        return
    rooms = architecture[datacenter_name]['rooms']
    room = next((r for r in rooms if r['name'] == room_name), None)
    if not room:
        click.echo(f"Room '{room_name}' does not exist in datacenter '{datacenter_name}'.")
        return
    bays = room['bays']
    if int(bay_position) >= len(bays):
        click.echo(f"Bay position {bay_position} is invalid in room '{room_name}'.")
        return
    device = {
        'size_in_u': int(size_in_u),
        'name': name,
        'type': device_type,
        'position_in_bay': int(bay_position)
    }
    bays[int(bay_position)]['devices'].append(device)
    save_architecture()
    click.echo(f"Device '{name}' of type '{device_type}' created at position {bay_position} in bay, in room '{room_name}', datacenter '{datacenter_name}'.")

# Command handler
def handle_command(command):
    parts = command.split()
    if not parts:
        return
    cmd = parts[0]
    args = parts[1:]

    if cmd == "help":
        click.echo("Available commands: create_datacenter, create_room, create_bay, create_device, help, man")
    elif cmd == "man" and args:
        show_manual(args[0])
    elif cmd == "create_datacenter" and len(args) == 3:
        create_datacenter(args)
    elif cmd == "create_room" and len(args) == 2:
        create_room(args)
    elif cmd == "create_bay" and len(args) == 3:
        create_bay(args)
    elif cmd == "create_device" and len(args) == 6:
        create_device(args)
    else:
        click.echo("Invalid command or incorrect number of arguments. Type 'help' for a list of commands.")

# Interactive command prompt
@click.command()
def cli():
    os.system('clear')
    click.echo("Welcome to CloudCLI. Type 'help' for a list of commands.")
    while True:
        command = click.prompt("> ", type=str)
        if command in ["exit", "quit"]:
            click.echo("Exiting CloudCLI.")
            break
        handle_command(command)

if __name__ == '__main__':
    cli()
