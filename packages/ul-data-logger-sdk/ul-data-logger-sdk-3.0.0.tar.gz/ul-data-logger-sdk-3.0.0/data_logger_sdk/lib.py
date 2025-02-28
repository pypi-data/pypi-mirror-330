from pathlib import Path

filename = "dag.yml"

current_file = Path(__file__).resolve()
CONFIG_FILE = current_file.parent / filename
