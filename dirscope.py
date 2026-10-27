
#!/usr/bin/env python3
"""
DirScope - A lightweight directory analysis tool.

Summarizes file types, directory size, and the largest files
without modifying the filesystem.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any


VERSION = "1.0.0"


def format_size(size: int) -> str:
    """Convert bytes into a human-readable size."""
    value = float(size)

    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.1f} {unit}"
        value /= 1024

    return f"{value:.1f} TB"


def analyze_directory(root: Path) -> dict[str, Any]:
    """Collect file statistics recursively without changing any files."""
    if not root.exists():
        raise FileNotFoundError(f"Path does not exist: {root}")

    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    extensions: Counter[str] = Counter()
    extension_sizes: Counter[str] = Counter()
    largest_files: list[dict[str, Any]] = []
    total_files = 0
    total_dirs = 0
    total_bytes = 0
    skipped_entries = 0

    def on_walk_error(_: OSError) -> None:
        nonlocal skipped_entries
        skipped_entries += 1

    for current, dirs, files in os.walk(
        root, followlinks=False, onerror=on_walk_error
    ):
        # Do not traverse directory symlinks.
        current_path = Path(current)
        dirs[:] = [
            name for name in dirs
            if not (current_path / name).is_symlink()
        ]
        total_dirs += len(dirs)

        for filename in files:
            file_path = current_path / filename

            try:
                if file_path.is_symlink():
                    continue

                stat = file_path.stat()
                if not file_path.is_file():
                    continue

                size = stat.st_size
                extension = file_path.suffix.lower() or "[no extension]"

                total_files += 1
                total_bytes += size
                extensions[extension] += 1
                extension_sizes[extension] += size

                largest_files.append({
                    "path": str(file_path.relative_to(root)),
                    "size_bytes": size,
                })

            except (OSError, ValueError):
                skipped_entries += 1

    largest_files.sort(key=lambda item: item["size_bytes"], reverse=True)

    return {
        "root": str(root.resolve()),
        "summary": {
            "total_files": total_files,
            "total_directories": total_dirs,
            "total_size_bytes": total_bytes,
            "total_size": format_size(total_bytes),
            "skipped_entries": skipped_entries,
        },
        "file_types": [
            {
                "extension": ext,
                "count": count,
                "size_bytes": extension_sizes[ext],
                "size": format_size(extension_sizes[ext]),
            }
            for ext, count in extensions.most_common()
        ],
        "largest_files": largest_files,
    }


def print_report(report: dict[str, Any], top: int) -> None:
    """Display a readable terminal report."""
    summary = report["summary"]

    print("\nDirScope — Directory Analysis")
    print("=" * 38)
    print(f"Location     : {report['root']}")
    print(f"Files        : {summary['total_files']:,}")
    print(f"Directories  : {summary['total_directories']:,}")
    print(f"Total size   : {summary['total_size']}")
    print(f"Skipped      : {summary['skipped_entries']:,}")
    print()

    print("FILE TYPES")
    print("-" * 52)
    print(f"{'Extension':<20} {'Count':>8} {'Total size':>14}")

    for item in report["file_types"][:top]:
        print(
            f"{item['extension']:<20} "
            f"{item['count']:>8,} "
            f"{item['size']:>14}"
        )

    if not report["file_types"]:
        print("No readable files found.")

    print("\nLARGEST FILES")
    print("-" * 52)

    for index, item in enumerate(report["largest_files"][:top], 1):
        print(
            f"{index:>2}. {format_size(item['size_bytes']):>10}  "
            f"{item['path']}"
        )

    if not report["largest_files"]:
        print("No files found.")

    print("\nAnalysis complete. No files were modified.\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dirscope",
        description="Inspect a directory and generate a file statistics report.",
        epilog="Example: python dirscope.py ./project --top 10",
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Directory to analyze (default: current directory)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        metavar="N",
        help="Number of entries to show per section (default: 10)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output the full report as JSON",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.top < 1:
        parser.error("--top must be at least 1")

    root = Path(args.path).expanduser()

    try:
        report = analyze_directory(root)
    except (OSError, ValueError) as exc:
        print(f"dirscope: error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report, args.top)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
