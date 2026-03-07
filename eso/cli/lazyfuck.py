"""The lazyfuck CLI module."""

import sys

from typing import NoReturn

from eso import Lazyfuck
from eso.cli._helper import cli_create_base_parser, cli_esolang_run
from eso.exceptions import EsoError
from eso.metadata import get_metadata_sentence


def cli_lazyfuck() -> NoReturn:
    """Function supposed to be used when creating Python executable scripts."""

    description = get_metadata_sentence(Lazyfuck.metadata)
    parser = cli_create_base_parser(description)
    args = parser.parse_args()

    lazyfuck = Lazyfuck()

    try:
        cli_esolang_run(lazyfuck, args.file, args.destination_binary)
    except EsoError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
