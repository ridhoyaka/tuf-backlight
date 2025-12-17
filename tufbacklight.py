#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
import time

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.align import Align
from rich.text import Text
from rich.box import ROUNDED

LED_PATH = "/sys/class/leds/asus::kbd_backlight/kbd_rgb_mode"
BRIGHTNESS_DEFAULT = "1"

MODES = {
    "0": "Static",
    "1": "Breathing",
    "2": "Color Cycle",
    "3": "Strobing",
}

SPEEDS = {
    "0": "Slow",
    "1": "Medium",
    "2": "Fast",
}

BACK_CODE = "00"
EXIT_CODE = "99"

console = Console()

def check_root():
    if os.geteuid() != 0:
        console.print("[bold red]Please run this tool with sudo[/bold red]")
        sys.exit(1)

def figlet_text(font: str, text: str) -> str:
    try:
        result = subprocess.run(
            ["figlet", "-f", font, text],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout.rstrip()
    except FileNotFoundError:
        pass
    return text

def header():
    console.clear()
    term_width = shutil.get_terminal_size((80, 20)).columns
    title_art = figlet_text("smkeyboard", "TUF BACKLIGHT")

    title = Text()
    for line in title_art.splitlines():
        title.append(line.center(term_width) + "\n", style="bold orange1")

    subtitle = Align.right(
        Text(
            "\n"
            "v1.0 coded by akaY\n"
            "https://github.com/ridhoyaka",
            style="white",
        )
    )

    console.print(
        Panel(
            Align.center(Group(title, subtitle)),
            border_style="orange3",
            padding=(1, 2),
            box=ROUNDED,
        )
    )

def select_mode() -> str:
    table = Table(box=ROUNDED)
    table.add_column("Key", justify="center", style="bold orange1", min_width=3, max_width=4)
    table.add_column("Mode", style="white")

    for k, v in MODES.items():
        table.add_row(k, v)

    table.add_row(EXIT_CODE, "[bold red]Exit[/bold red]")

    console.print(
        Panel(
            table,
            title="Main Menu",
            border_style="orange3",
            box=ROUNDED,
        )
    )

    return Prompt.ask(
        "[orange1]Choose mode[/orange1]",
        choices=list(MODES.keys()) + [EXIT_CODE],
    )

def select_speed() -> str:
    table = Table(box=ROUNDED)
    table.add_column("Key", justify="center", style="bold orange1", min_width=3, max_width=4)
    table.add_column("Speed", style="white")

    for k, v in SPEEDS.items():
        table.add_row(k, v)

    table.add_row(BACK_CODE, "[yellow]Back[/yellow]")

    console.print(
        Panel(
            table,
            title="Speed Selection",
            border_style="orange3",
            box=ROUNDED,
        )
    )

    return Prompt.ask(
        "[orange1]Choose speed[/orange1]",
        choices=list(SPEEDS.keys()) + [BACK_CODE],
    )

def rgb_back_menu():
    table = Table(box=ROUNDED, show_header=False)
    table.add_column("Key", justify="center", style="bold orange1", min_width=3)
    table.add_column("Action", style="white")

    table.add_row("00", "[yellow]Back[/yellow]")

    console.print(
        Panel(
            table,
            border_style="orange3",
            box=ROUNDED,
        )
    )

def input_rgb():
    while True:
        header()
        rgb_back_menu()

        r = Prompt.ask("[orange1]Red (0–255)[/orange1]", default="255")
        if r == BACK_CODE:
            return BACK_CODE

        g = Prompt.ask("[orange1]Green (0–255)[/orange1]", default="255")
        b = Prompt.ask("[orange1]Blue (0–255)[/orange1]", default="255")

        try:
            r, g, b = int(r), int(g), int(b)
            for v in (r, g, b):
                if not 0 <= v <= 255:
                    raise ValueError
            return r, g, b
        except ValueError:
            console.print("[bold red]RGB values must be between 0 and 255[/bold red]")
            time.sleep(1)

def apply_setting(mode: str, r: int, g: int, b: int, speed: str):
    command = f"{BRIGHTNESS_DEFAULT} {mode} {r} {g} {b} {speed}\n"

    try:
        with open(LED_PATH, "w") as f:
            f.write(command)

        console.print(
            Panel(
                Align.center(Text("Applied Successfully!", style="bold green")),
                title="Status",
                border_style="orange3",
                box=ROUNDED,
            )
        )
    except OSError as e:
        console.print(f"[bold red]Failed to apply setting:[/bold red] {e}")

    Prompt.ask("[orange3]Press Enter to return to menu[/orange3]", default="")

def main():
    check_root()

    while True:
        header()
        mode = select_mode()

        if mode == EXIT_CODE:
            console.clear()
            console.print(
                Panel(
                    Align.center(Text("Goodbye 👋", style="bold orange1")),
                    border_style="green",
                    box=ROUNDED,
                )
            )
            sys.exit(0)
        
        r, g, b = 255, 255, 255
        if mode in ("0", "1", "3"):
            header()
            rgb = input_rgb()
            if rgb == BACK_CODE:
                continue
            r, g, b = rgb
        
        speed = "0"
        if mode in ("1", "2", "3"):
            header()
            speed = select_speed()
            if speed == BACK_CODE:
                continue

        header()
        apply_setting(mode, r, g, b, speed)
#https://github.com/ridhoyaka
if __name__ == "__main__":
    main()
