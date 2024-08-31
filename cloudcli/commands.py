import click
from cloudcli.utils import save_architecture, architecture, context_path
from cloudcli.help import show_manual, display_help

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
    if not context_path or context_path[0] not in architecture:
        click.echo("You must be in a datacenter to create a room.")
        return
    datacenter_name = context_path[0]
    name = args[0]
    room = {
        'name': name,
        'bays': []
    }
    architecture[datacenter_name]['rooms'].append(room)
    save_architecture()
    click.echo(f"Room '{name}' created in datacenter '{datacenter_name}'.")

def create_bay(args):
    if len(context_path) < 2:
        click.echo("You must be in a room to create a bay.")
        return
    datacenter_name, room_name = context_path
    room = next((r for r in architecture[datacenter_name]['rooms'] if r['name'] == room_name), None)
    if not room:
        click.echo(f"Room '{room_name}' not found in datacenter '{datacenter_name}'.")
        return
    bay_name, size_in_u = args
    bay = {
        'name': bay_name,
        'size_in_u': int(size_in_u),
        'devices': []
    }
    room['bays'].append(bay)
    save_architecture()
    click.echo(f"Bay '{bay_name}' of size {size_in_u}U created in room '{room_name}'.")

def create_device(args):
    if len(context_path) < 3:
        click.echo("You must be in a bay to create a device.")
        return
    datacenter_name, room_name, bay_name = context_path
    room = next((r for r in architecture[datacenter_name]['rooms'] if r['name'] == room_name), None)
    bay = next((b for b in room['bays'] if b['name'] == bay_name), None)
    if not bay:
        click.echo(f"Bay '{bay_name}' not found in room '{room_name}'.")
        return
    name, device_type, bay_position = args
    device = {
        'name': name,
        'type': device_type,
        'position_in_bay': int(bay_position)
    }
    bay['devices'].append(device)
    save_architecture()
    click.echo(f"Device '{name}' of type '{device_type}' created at position {bay_position} in bay '{bay_name}'.")

def use_component(args):
    global context_path
    if args[0] == "..":
        if context_path:
            context_path.pop()
    else:
        component_name = args[0]
        if not context_path:
            if component_name in architecture:
                context_path.append(component_name)
            else:
                click.echo(f"Datacenter '{component_name}' not found.")
        elif len(context_path) == 1:
            datacenter_name = context_path[0]
            room = next((r for r in architecture[datacenter_name]['rooms'] if r['name'] == component_name), None)
            if room:
                context_path.append(component_name)
            else:
                click.echo(f"Room '{component_name}' not found in datacenter '{datacenter_name}'.")
        elif len(context_path) == 2:
            datacenter_name, room_name = context_path
            room = next((r for r in architecture[datacenter_name]['rooms'] if r['name'] == room_name), None)
            bay = next((b for b in room['bays'] if b['name'] == component_name), None)
            if bay:
                context_path.append(component_name)
            else:
                click.echo(f"Bay '{component_name}' not found in room '{room_name}'.")
        else:
            click.echo("You cannot go deeper than a bay.")
    click.echo(f"Current path: {' / '.join(context_path) if context_path else 'root'}")

def handle_command(command):
    parts = command.split()
    if not parts:
        return
    cmd = parts[0]
    args = parts[1:]

    if cmd == "help":
        display_help()
    elif cmd == "man" and args:
        show_manual(args[0])
    elif cmd in ["create_datacenter", "cda"] and len(args) == 3:
        create_datacenter(args)
    elif cmd in ["create_room", "crm"] and len(args) == 1:
        create_room(args)
    elif cmd in ["create_bay", "cby"] and len(args) == 2:
        create_bay(args)
    elif cmd in ["create_device", "cde"] and len(args) == 3:
        create_device(args)
    elif cmd in ["use", "use"] and len(args) == 1:
        use_component(args)
    else:
        click.echo("Invalid command or incorrect number of arguments. Type 'help' for a list of commands.")
