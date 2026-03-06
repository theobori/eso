"""The aaa CLI module."""

import sys

from typing import NoReturn

from eso import AAA
from eso.cli._helper import cli_create_base_parser, cli_esolang_run
from eso.exceptions import EsoError
from eso.metadata import get_metadata_sentence


def cli_aaa() -> NoReturn:
    """Function supposed to be used when creating Python executable scripts."""

    description = get_metadata_sentence(AAA.metadata)
    parser = cli_create_base_parser(description)
    args = parser.parse_args()

    aaa = AAA()

    try:
        cli_esolang_run(aaa, args.file, args.destination_binary)
    except EsoError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
