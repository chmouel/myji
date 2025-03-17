import datetime
import os
import subprocess
import sys
import webbrowser

import click

from myji import defaults  # Third-party imports next


def make_osc8_link(text, url):
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"


def make_full_url(ticket, server=None):
    if server is None:
        server = os.getenv("JIRA_SERVER", "issues.redhat.com")
    return f"https://{server}/browse/{ticket}"


def browser_open_ticket(ticket, server=None):
    if not ticket:
        webbrowser.open(
            f"https://{server}/projects/{os.getenv('JIRA_PROJECT', 'SRVKP')}"
        )
        return

    try:
        webbrowser.open(make_full_url(ticket, server))
    except Exception as e:
        click.secho(f"Failed to open URL {ticket}: {e}", fg="red", err=True)


def log(message, level="INFO", verbose_only=False, verbose=False, file=sys.stdout):
    """
    Log a message with color-coded level prefix.

    Args:
        message (str): The message to log.
        level (str): The log level (e.g., INFO, WARNING, ERROR).
        verbose_only (bool): Only log if verbose mode is enabled.
        verbose (bool): Whether verbose mode is enabled.
        file (file): The file to write to.
    """
    if verbose_only and not verbose:
        return

    color = defaults.LOG_LEVELS.get(level, "reset")
    prefix = f"[{level}] " if level else ""

    if file == sys.stderr:
        click.secho(f"{prefix}{message}", fg=color.lower(), err=True)
    else:
        click.secho(f"{prefix}{message}", fg=color.lower())


def colorize(color, text):
    """Colorize text with Click's style function"""
    return click.style(text, fg=color.lower())


def show_time(s):
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d")


def parse_email(s):
    return s.split("@")[0].split("+")[0]


def get_pass_key(s):
    cmd = ["pass", s]
    try:
        return subprocess.check_output(cmd, text=True).strip()
    except subprocess.CalledProcessError:
        click.secho(f"Failed to retrieve password for {s}", fg="red", err=True)
        return None
