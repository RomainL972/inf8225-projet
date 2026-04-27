import sys
import shutil
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python separate.py <build_dir>")
    sys.exit(1)

build_dir = Path(sys.argv[1]).expanduser().resolve()

if not build_dir.exists():
    print(f"Error: build dir does not exist: {build_dir}")
    sys.exit(1)

if not build_dir.is_dir():
    print(f"Error: not a directory: {build_dir}")
    sys.exit(1)

matches = sorted(
    p for p in build_dir.rglob("*") if p.is_dir() and p.name == "interference_graphs"
)

if not matches:
    print("No interference_graphs subdirectories found.")
    sys.exit(-1)

sorted_root = build_dir / "sorted_graphs"
sorted_root.mkdir(parents=True, exist_ok=True)


def regclass_from_filename(path: Path):
    stem = path.name.rsplit(".", 1)[0]
    if "_" not in stem:
        return None
    return stem.rsplit("_", 1)[1]


def unique_destination_path(dst_dir: Path, filename: str):
    candidate = dst_dir / filename
    if not candidate.exists():
        return candidate

    base, dot, ext = filename.rpartition(".")
    base = base if dot else filename
    ext = f".{ext}" if dot else ""

    i = 1
    while True:
        candidate = dst_dir / f"{base}_{i}{ext}"
        if not candidate.exists():
            return candidate
        i += 1


moved = 0
skipped = 0

for src_root in matches:
    for src_file in sorted(p for p in src_root.rglob("*") if p.is_file()):
        regclass = regclass_from_filename(src_file)
        if not regclass:
            skipped += 1
            print(f"Skipping (cannot parse REGCLASS): {src_file}")
            continue

        dst_dir = sorted_root / regclass
        dst_dir.mkdir(parents=True, exist_ok=True)

        dst_file = unique_destination_path(dst_dir, src_file.name)
        shutil.copy2(str(src_file), str(dst_file))
        moved += 1

print(f"Moved {moved} file(s) into {sorted_root}")
if skipped:
    print(f"Skipped {skipped} file(s) with no underscore in filename stem")
