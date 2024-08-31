
import json
import os

BASE_DIR = os.path.join(os.getcwd(), "architecture")
context_path = []
architecture = {}

def save_architecture():
    for name, datacenter in architecture.items():
        with open(os.path.join(BASE_DIR, f"{name}.json"), 'w') as f:
            json.dump(datacenter, f, indent=4)

def load_architecture():
    if os.path.exists(BASE_DIR):
        for filename in os.listdir(BASE_DIR):
            if filename.endswith(".json"):
                with open(os.path.join(BASE_DIR, filename), 'r') as f:
                    datacenter = json.load(f)
                    architecture[datacenter['name']] = datacenter

def get_prompt():
    return f"CloudCLI [{' / '.join(context_path)}]$: " if context_path else "CloudCLI$: "
