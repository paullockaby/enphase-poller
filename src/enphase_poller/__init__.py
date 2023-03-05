import argparse
import logging
import os
import sys
from typing import List

from enphase_poller.poller import get_version, run

# calculate what version of this program we are running
__version__ = get_version()


def parse_arguments(arguments: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="welwick")

    parser.add_argument(
        "--api-url",
        dest="api_url",
        default=os.environ.get("ENPHASE_LOCAL_API_URL"),
        help="url for the enphase proxy",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="send verbose output to the console",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="return the version number and exit",
    )
    return parser.parse_args(arguments)


def main() -> None:
    args = parse_arguments(sys.argv[1:])

    logging.basicConfig(
        format="[%(asctime)s] %(levelname)-8s - %(message)s",
        level=logging.DEBUG if args.verbose else logging.INFO,
        stream=sys.stdout,
    )

    run(
        args.api_url,
    )


if __name__ == "__main__":
    main()
