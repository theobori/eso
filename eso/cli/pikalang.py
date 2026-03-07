"""The pikalang CLI module."""

import sys

from typing import NoReturn

from eso import Pikalang
from eso.cli._helper import cli_create_base_parser, cli_esolang_run
from eso.exceptions import EsoError
from eso.metadata import get_metadata_sentence


def cli_pikalang() -> NoReturn:
    """Function supposed to be used when creating Python executable scripts."""

    description = get_metadata_sentence(Pikalang.metadata)
    parser = cli_create_base_parser(description)
    args = parser.parse_args()

    pikalang = Pikalang()

    try:
        cli_esolang_run(pikalang, args.file, args.destination_binary)
    except EsoError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
