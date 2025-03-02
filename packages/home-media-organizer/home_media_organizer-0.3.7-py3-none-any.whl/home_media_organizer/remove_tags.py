import argparse
import logging

from .home_media_organizer import iter_files
from .media_file import MediaFile


#
# remove tags to media files
#
def remove_tags(args: argparse.Namespace, logger: logging.Logger | None) -> None:
    cnt = 0
    # find only files with these tags
    if args.with_tags is None:
        args.with_tags = args.tags
    #
    for item in iter_files(args, logger=logger):
        MediaFile(item).remove_tags(args.tags, args.confirmed, logger)
        cnt += 1
    if logger is not None:
        logger.info(f"[blue]{cnt}[/blue] files untagged.")


def get_remove_tags_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "remove-tags",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="Remove tags associated with media files",
    )
    parser.add_argument("--tags", nargs="+", help="Tags to be removed from medis files")
    parser.set_defaults(func=remove_tags, command="remove_tags")
    return parser
