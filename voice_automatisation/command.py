import subprocess
from dataclasses import dataclass
from typing import Callable


@dataclass
class Keyword:
    synonyms: tuple[str]
    weight: float


@dataclass
class Command:
    identifier: str
    keywords: tuple[Keyword]
    callback: Callable


example_commands = [
    Command(
        "play/pause",
        (
            Keyword(("wiedergabe",), 5),
            Keyword(("pause", "pausieren", "weiter", "fortführen"), 1),
        ),
        callback=lambda: subprocess.call(["xdotool", "key", "XF86AudioPlay"]),
    )
]
