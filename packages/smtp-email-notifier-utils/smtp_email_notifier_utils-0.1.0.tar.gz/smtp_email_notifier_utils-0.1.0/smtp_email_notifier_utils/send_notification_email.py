"""Send notification email to the recipient."""

import click
import logging
import os
import pathlib
import sys

from datetime import datetime
from rich.console import Console

from smtp_email_notifier_utils import constants
from smtp_email_notifier_utils.notifier import send_notification

DEFAULT_OUTDIR = os.path.join(
    constants.DEFAULT_OUTDIR_BASE,
    os.path.splitext(os.path.basename(__file__))[0],
    constants.DEFAULT_TIMESTAMP,
)

error_console = Console(stderr=True, style="bold red")

console = Console()


def validate_verbose(ctx, param, value):
    """Validate the validate option.

    Args:
        ctx (Context): The click context.
        param (str): The parameter.
        value (bool): The value.

    Returns:
        bool: The value.
    """

    if value is None:
        click.secho(
            "--verbose was not specified and therefore was set to 'True'", fg="yellow"
        )
        return constants.DEFAULT_VERBOSE
    return value


@click.command()
@click.option("--logfile", help="The log file")
@click.option("--message", help="The short message to send in the body of the email.")
@click.option(
    "--outdir",
    help=f"The default is the current working directory - default is '{DEFAULT_OUTDIR}'",
)
@click.option("--recipient", help="The email address of the recipient.")
@click.option("--subject", help="The subject of the notification email.")
@click.option(
    "--verbose",
    is_flag=True,
    help=f"Will print more info to STDOUT - default is '{constants.DEFAULT_VERBOSE}'.",
    callback=validate_verbose,
)
def main(
    logfile: str, message: str, outdir: str, recipient: str, subject: str, verbose: bool
):
    """Send notification email to the recipient."""

    error_ctr = 0

    if recipient is None:
        error_console.print("--recipient was not specified")
        error_ctr += 1

    if message is None:
        error_console.print("--message was not specified")
        error_ctr += 1

    if subject is None:
        error_console.print("--subject was not specified")
        error_ctr += 1

    if error_ctr > 0:
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        console.print(
            f"[yellow]--outdir was not specified and therefore was set to '{outdir}'[/]"
        )

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        console.print(f"[yellow]Created output directory '{outdir}'[/]")

    if logfile is None:
        logfile = os.path.join(
            outdir, os.path.splitext(os.path.basename(__file__))[0] + ".log"
        )
        console.print(
            f"[yellow]--logfile was not specified and therefore was set to '{logfile}'[/]"
        )

    logging.basicConfig(
        filename=logfile,
        format=constants.DEFAULT_LOGGING_FORMAT,
        level=constants.DEFAULT_LOGGING_LEVEL,
    )

    success = send_notification(recipient, subject, message)
    if success:
        print("Notification sent successfully!")
    else:
        print("Failed to send notification")

    if verbose:
        print(f"The log file is '{logfile}'")
        console.print(
            f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]"
        )


if __name__ == "__main__":
    main()
