#!/usr/bin/env python3
"""Install engg-reviews PE skills into a chosen workspace folder.

Stdlib only. Discovers every skills/engg-reviews/*/SKILL.md and symlinks them
into {target}/.agents/skills/. Optionally copies helpers from templates/.

Examples:
  python3 install_engg_reviews.py --target ~/ws/pe-workspace
  python3 install_engg_reviews.py --target ./pe-workspace --ref pe-rc-2 --force

After tag pe-rc-2 is published:
  curl -fsSL https://raw.githubusercontent.com/drivestream-lab/prayog-skills/pe-rc-2/scripts/install_engg_reviews.py \\
    -o /tmp/install_engg_reviews.py
  python3 /tmp/install_engg_reviews.py --target /path/to/pe-workspace --ref pe-rc-2
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_REPO = "https://github.com/drivestream-lab/prayog-skills.git"
DEFAULT_REF = "pe-rc-2"
DEFAULT_CACHE = Path.home() / ".cache" / "prayog-skills-engg-reviews"


def run(cmd: list[str], *, cwd: Path | None = None) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def discover_skills(engg_root: Path) -> list[Path]:
    skills: list[Path] = []
    for child in sorted(engg_root.iterdir()):
        if not child.is_dir():
            continue
        if child.name in {"references", "templates"}:
            continue
        if (child / "SKILL.md").is_file():
            skills.append(child)
    return skills


def ensure_repo(cache: Path, repo: str, ref: str) -> Path:
    cache.parent.mkdir(parents=True, exist_ok=True)
    if (cache / ".git").is_dir():
        run(["git", "remote", "set-url", "origin", repo], cwd=cache)
        run(["git", "fetch", "--tags", "--force", "origin"], cwd=cache)
        run(["git", "checkout", "--force", ref], cwd=cache)
        # Prefer annotated/lightweight tag; else branch tip on origin
        for candidate in (ref, f"refs/tags/{ref}", f"origin/{ref}"):
            probe = subprocess.run(
                ["git", "rev-parse", "--verify", candidate],
                cwd=cache,
                capture_output=True,
                text=True,
            )
            if probe.returncode == 0:
                run(["git", "reset", "--hard", candidate], cwd=cache)
                break
        else:
            raise SystemExit(f"Cannot resolve ref {ref!r} in {cache}")
    else:
        if cache.exists():
            shutil.rmtree(cache)
        run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--branch",
                ref,
                repo,
                str(cache),
            ]
        )
    return cache


def link_skill(src: Path, dest: Path, *, force: bool) -> None:
    if dest.is_symlink() or dest.exists():
        if not force:
            raise SystemExit(
                f"Refusing to overwrite existing skill link/dir: {dest}\n"
                f"Re-run with --force to replace."
            )
        if dest.is_symlink() or dest.is_file():
            dest.unlink()
        else:
            shutil.rmtree(dest)
    dest.symlink_to(src.resolve())
    print(f"  linked {dest.name} -> {src}")


def copy_helpers(templates: Path, target: Path, *, force: bool) -> None:
    bin_dir = target / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)

    refresh_src = templates / "refresh-graph.sh"
    refresh_dst = bin_dir / "refresh-graph.sh"
    if refresh_src.is_file():
        shutil.copy2(refresh_src, refresh_dst)
        refresh_dst.chmod(refresh_dst.stat().st_mode | 0o111)
        print(f"  copied {refresh_dst.relative_to(target)}")

    mapping = [
        ("fleet.yaml.example", "fleet.yaml.example"),
        ("env.example", ".env.example"),
        ("README-ENGG-REVIEWS.md", "README-ENGG-REVIEWS.md"),
    ]
    for src_name, dst_name in mapping:
        src = templates / src_name
        if not src.is_file():
            continue
        dst = target / dst_name
        if dst.exists() and not force and dst_name != "fleet.yaml.example":
            print(f"  keep existing {dst_name}")
            continue
        shutil.copy2(src, dst)
        print(f"  copied {dst_name}")

    fleet_example = target / "fleet.yaml.example"
    fleet = target / "fleet.yaml"
    if fleet_example.is_file() and not fleet.exists():
        shutil.copy2(fleet_example, fleet)
        print("  created fleet.yaml from example (edit meta/repos)")


def write_pin(target: Path, cache: Path, ref: str, skills: list[str]) -> None:
    pin = target / ".engg-reviews-pin"
    pin.write_text(
        "\n".join(
            [
                f"ref={ref}",
                f"cache={cache}",
                f"skills={','.join(skills)}",
                "contract=engg-reviews/v1",
                "gate_coupled=false",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"  wrote {pin.name}")


def main() -> int:
    p = argparse.ArgumentParser(
        description="Install engg-reviews PE skills into a workspace folder."
    )
    p.add_argument(
        "--target",
        required=True,
        type=Path,
        help="Workspace folder to instrument (Cursor cwd for PE)",
    )
    p.add_argument("--ref", default=DEFAULT_REF, help=f"Git ref (default: {DEFAULT_REF})")
    p.add_argument("--repo", default=DEFAULT_REPO, help="Git remote URL")
    p.add_argument(
        "--cache",
        type=Path,
        default=DEFAULT_CACHE,
        help=f"Clone cache dir (default: {DEFAULT_CACHE})",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help="Replace existing skill symlinks / overwrite helpers",
    )
    p.add_argument(
        "--no-helpers",
        action="store_true",
        help="Only link skills; skip bin/fleet/.env templates",
    )
    p.add_argument(
        "--local-source",
        type=Path,
        default=None,
        help="Use an existing prayog-skills checkout instead of cloning",
    )
    args = p.parse_args()

    target: Path = args.target.expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    (target / "graphs").mkdir(exist_ok=True)
    (target / "out" / "reports").mkdir(parents=True, exist_ok=True)

    if args.local_source:
        source = args.local_source.expanduser().resolve()
        if not (source / "skills" / "engg-reviews").is_dir():
            raise SystemExit(f"--local-source missing skills/engg-reviews: {source}")
        print(f"Using local source: {source}")
        cache = source
    else:
        print(f"Fetching {args.repo} @ {args.ref}")
        cache = ensure_repo(args.cache.expanduser().resolve(), args.repo, args.ref)

    engg = cache / "skills" / "engg-reviews"
    if not engg.is_dir():
        raise SystemExit(f"No skills/engg-reviews in {cache} (ref={args.ref})")

    skills = discover_skills(engg)
    if not skills:
        raise SystemExit(f"No SKILL.md packages under {engg}")

    skills_dir = target / ".agents" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    print(f"Linking {len(skills)} skill(s) into {skills_dir}")
    for skill in skills:
        link_skill(skill, skills_dir / skill.name, force=args.force)

    if not args.no_helpers:
        templates = engg / "templates"
        if templates.is_dir():
            print("Copying helpers")
            copy_helpers(templates, target, force=args.force)
        else:
            print("WARN: no skills/engg-reviews/templates — helpers skipped")

    write_pin(target, cache, args.ref, [s.name for s in skills])

    print()
    print("Install complete.")
    print(f"  target:  {target}")
    print(f"  ref:     {args.ref}")
    print(f"  skills:  {', '.join(s.name for s in skills)}")
    print()
    print("Next:")
    print(f"  1. Open Cursor on: {target}")
    print("  2. Edit fleet.yaml (meta_path + repos)")
    print("  3. Optional: cp .env.example .env  # for --with-docs Graphify")
    print("  4. ./bin/refresh-graph.sh <repo>")
    print("  5. /ensure-repo-graph → /prd-codebase-map")
    print("     → optional /review-product-questions → /post-product-questions")
    print()
    print("Does NOT touch SDD gates, profiles, or impact-map-* labels.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"Command failed with exit {exc.returncode}", file=sys.stderr)
        raise SystemExit(exc.returncode) from exc
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        raise SystemExit(130) from None
