"""Validate the FASTQ file."""

import click
import gzip
import logging
import os
import pathlib
import re
import sys


from rich.console import Console

from fastq_file_utils import constants
from fastq_file_utils.file_utils import check_infile_status


DEFAULT_OUTDIR = os.path.join(
    constants.DEFAULT_OUTDIR_BASE,
    os.path.splitext(os.path.basename(__file__))[0],
    constants.DEFAULT_TIMESTAMP,
)


error_console = Console(stderr=True, style="bold red")

console = Console()


def detect_phred_encoding(quality_scores: str) -> str:
    """Detects whether the quality scores are in Phred+33 or Phred+64 encoding.

    Args:
        quality_scores (str): A string of quality scores from a FASTQ file.

    Returns:
        str: 'Phred+33', 'Phred+64', or 'Unknown'.
    """
    min_qual = min(ord(c) for c in quality_scores)

    if min_qual >= 33 and min_qual <= 74:
        return "Phred+33"
    elif min_qual >= 64 and min_qual <= 105:
        return "Phred+64"
    return "Unknown"


def validate_fastq(file_path: str) -> tuple:
    """Validates a FASTQ file, detects Phred encoding, and counts total records.

    Args:
        file_path (str): Path to the FASTQ file.

    Returns:
        bool: True if valid, False otherwise.
        str: Validation message.
        str: Detected Phred encoding.
        int: Total number of FASTQ records.
    """
    open_func = gzip.open if file_path.endswith(".gz") else open
    detected_encoding = None
    record_count = 0

    try:
        with open_func(file_path, "rt", encoding="utf-8") as f:
            while True:
                header = f.readline().strip()
                sequence = f.readline().strip()
                separator = f.readline().strip()
                quality = f.readline().strip()

                if not header:
                    break  # End of file

                record_count += 1

                if not (header.startswith("@") and separator.startswith("+")):
                    return (
                        False,
                        f"Error in record {record_count}: Invalid header or separator format.",
                        None,
                        record_count,
                    )

                if len(sequence) != len(quality):
                    return (
                        False,
                        f"Error in record {record_count}: Sequence and quality lengths do not match.",
                        None,
                        record_count,
                    )

                if not re.fullmatch(r"^[ATCGN]+$", sequence, re.IGNORECASE):
                    return (
                        False,
                        f"Error in record {record_count}: Invalid characters in sequence.",
                        None,
                        record_count,
                    )

                if not re.fullmatch(r"^[!-~]+$", quality):  # Printable ASCII
                    return (
                        False,
                        f"Error in record {record_count}: Invalid characters in quality scores.",
                        None,
                        record_count,
                    )

                # Detect Phred encoding from the first quality string
                if detected_encoding is None:
                    detected_encoding = detect_phred_encoding(quality)

        return (
            True,
            f"Valid FASTQ file with {record_count} records.",
            detected_encoding,
            record_count,
        )

    except Exception as e:
        return False, f"Error reading file: {e}", None, record_count


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
@click.option("--infile", help="The input FASTQ file.")
@click.option("--logfile", help="The log file.")
@click.option(
    "--outdir",
    help=f"The default is the current working directory - default is '{DEFAULT_OUTDIR}'.",
)
@click.option("--outfile", help="The output final report file")
@click.option(
    "--verbose",
    is_flag=True,
    help=f"Will print more info to STDOUT - default is '{constants.DEFAULT_VERBOSE}'.",
    callback=validate_verbose,
)
def main(infile: str, logfile: str, outdir: str, outfile: str, verbose: bool):
    """Validate the FASTQ file."""

    error_ctr = 0

    if infile is None:
        error_console.print("--infile was not specified")
        error_ctr += 1

    if error_ctr > 0:
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    check_infile_status(infile, "fastq")

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

    is_valid, message, phred_encoding, record_count = validate_fastq(infile)

    print(message)

    if is_valid:
        print(f"Detected Phred Encoding: {phred_encoding}")
        print(f"Total Records: {record_count}")

    if verbose:
        print(f"The log file is '{logfile}'")
        console.print(
            f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]"
        )


if __name__ == "__main__":
    main()
