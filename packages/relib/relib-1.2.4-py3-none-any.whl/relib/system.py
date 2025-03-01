import json
import os
from pathlib import Path
from typing import Any

def read_json(path: Path) -> Any:
  with path.open("r") as f:
    return json.load(f)

def write_json(path: Path, obj: Any) -> None:
  with path.open("w") as f:
    return json.dump(obj, f)

def clear_console() -> None:
  os.system("cls" if os.name == "nt" else "clear")

def console_link(text, url) -> str:
  return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"
