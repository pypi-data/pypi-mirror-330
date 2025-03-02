#!/usr/bin/env python3
import click
import sys
from . import parse
from .filters import rebreak_lines


@click.command()
@click.argument("in_file_path")
@click.option("--filter", "filter_arg", default="")
@click.option(
    "--out-format",
    type=click.Choice([v.name for v in parse.OutputFormat]),
    default="srt",
)
def main(in_file_path: str, filter_arg: str, out_format: str):
    # Encoding utf-8-sig to handle BOM, which Aegisub seems to generate
    # when exporting to SRT. This works fine even if there is no BOM.
    with open(in_file_path, encoding="utf-8-sig") as f:
        text = f.read()
    srt = parse.SRT.from_str(text)

    for filter_name in filter_arg.split():
        match filter_name:
            case "rebreak_lines":
                filter_module = rebreak_lines
            case unknown:
                raise InvalidFilterError(unknown)
        srt.events = [filter_module.filter(event) for event in srt.events]

    sys.stdout.write(srt.to_output_format(parse.OutputFormat[out_format]))


class InvalidFilterError(Exception):
    pass


if __name__ == "__main__":
    main()
