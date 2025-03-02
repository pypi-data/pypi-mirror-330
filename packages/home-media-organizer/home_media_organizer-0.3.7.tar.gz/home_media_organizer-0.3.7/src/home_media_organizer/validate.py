import argparse
import logging
import os
from multiprocessing import Pool
from pathlib import Path
from typing import Tuple

import rich
from PIL import Image, UnidentifiedImageError
from tqdm import tqdm  # type: ignore

from .home_media_organizer import iter_files
from .utils import cache, calculate_file_hash, clear_cache, get_response, manifest

try:
    import ffmpeg  # type: ignore
except ImportError:
    ffmpeg = None


@cache.memoize(tag="validate")
def jpeg_openable(file_path: str) -> bool:
    try:
        with Image.open(file_path) as img:
            img.verify()  # verify that it is, in fact an image
            return True
    except UnidentifiedImageError:
        return False


@cache.memoize(tag="validate")
def mpg_playable(file_path: str) -> bool:
    if not ffmpeg:
        rich.print("[red]ffmpeg not installed, skip[/red]")
        return True
    try:
        # Try to probe the file using ffmpeg
        probe = ffmpeg.probe(file_path)

        # Check if 'streams' exist in the probe result
        if "streams" in probe:
            video_streams = [s for s in probe["streams"] if s["codec_type"] == "video"]
            if len(video_streams) > 0:
                return True
        return False
    except ffmpeg.Error:
        return False


#
# check jpeg
#
def check_media_file(item: Path) -> Tuple[Path, str, bool]:
    return (
        item,
        calculate_file_hash(item),
        (item.suffix in (".jpg", ".jpeg") and not jpeg_openable(item))
        or (item.suffix.lower() in (".mp4", ".mpg") and not mpg_playable(item)),
    )


def validate_media_files(args: argparse.Namespace, logger: logging.Logger | None) -> None:
    if args.no_cache:
        clear_cache(tag="validate")

    if args.confirmed is not None or not args.remove:
        with Pool(args.jobs or None) as pool:
            # get file size
            for item, new_hash, corrupted in tqdm(
                pool.imap(check_media_file, iter_files(args)),
                desc="Validate media",
                disable=not args.progress,
            ):
                existing_hash = manifest.get_hash(item, None)
                if existing_hash is not None and existing_hash != new_hash:
                    if logger is not None:
                        logger.warning(f"[red][bold]{item}[/bold] is corrupted.[/red]")
                    continue
                if corrupted:
                    if logger is not None:
                        logger.info(f"[red][bold]{item}[/bold] is not playable.[/red]")
                    continue
                if args.manifest:
                    manifest.set_hash(item, new_hash)
    else:
        for item in iter_files(args):
            _, new_hash, corrupted = check_media_file(item)
            existing_hash = manifest.get_hash(item, None)
            if existing_hash is not None and existing_hash != new_hash:
                if logger is not None:
                    logger.warning(f"[red][bold]{item}[/bold] is corrupted.[/red]")
                if args.remove:
                    if args.confirmed is False:
                        if logger is not None:
                            logger.info(f"[green]DRYRUN[/green] Would remove {item}.")
                    elif args.confirmed or get_response("Remove it?"):
                        if logger is not None:
                            logger.info(f"[red][bold]{item}[/bold] is removed.[/red]")
                        os.remove(item)
                continue
            if corrupted:
                if logger is not None:
                    logger.warning(f"[red][bold]{item}[/bold] is not playable.[/red]")
                if args.remove:
                    if args.confirmed is False:
                        if logger is not None:
                            logger.info(f"[green]DRYRUN[/green] Would remove {item}.")
                    elif args.confirmed or get_response("Remove it?"):
                        if logger is not None:
                            logger.info(f"[red][bold]{item}[/bold] is removed.[/red]")
                        os.remove(item)
                continue
            if args.manifest:
                manifest.set_hash(item, new_hash)


def get_validate_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "validate",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="Identify corrupted media files",
    )
    parser.add_argument("--remove", action="store_true", help="If the file if it is corrupted.")
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="invalidate cached validation results and re-validate all files again.",
    )
    parser.set_defaults(func=validate_media_files, command="validate")
    return parser
