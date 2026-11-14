#!/usr/bin/env python3
"""Validate a social media content pack against each platform's limits.

Usage:
    python validate_posts.py pack.json        # human-readable report
    python validate_posts.py pack.json --json # machine-readable report

Input shape: {"posts": [{"platform": "...", "text": "...", "hashtags": [...], "link": "...", "title": "..."}]}
Exit code 0 = no errors (warnings allowed), 1 = at least one error. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass

URL = re.compile(r"https?://\S+")
HASHTAG = re.compile(r"^#[\w\d_]+$", re.UNICODE)

# Hard limits (error) and soft best practice (warning). Characters, not bytes.
RULES: dict[str, dict] = {
    "linkedin": {"max_chars": 3000, "best": (600, 1300), "hashtags": (0, 5), "links": True},
    "instagram": {"max_chars": 2200, "best": (300, 1000), "hashtags": (0, 30), "best_tags": 15, "links": False},
    "tiktok": {"max_chars": 2200, "best": (0, 300), "hashtags": (0, 10), "best_tags": 5, "links": False},
    "youtube": {"max_chars": 5000, "best": (0, 1000), "hashtags": (0, 15), "best_tags": 5, "links": True,
                "title_max": 100, "title_best": 60},
    "x": {"max_chars": 280, "best": (0, 280), "hashtags": (0, 3), "best_tags": 2, "links": True, "url_weight": 23},
}
ALIASES = {"twitter": "x", "youtube_shorts": "youtube", "shorts": "youtube", "ig": "instagram"}


@dataclass
class Finding:
    index: int
    platform: str
    level: str  # "error" | "warning"
    message: str


def counted_length(post: dict, rule: dict) -> int:
    """Length the platform counts: text + hashtags line (+ link), X counts every URL as 23."""
    body = post.get("text", "")
    tags = " ".join(post.get("hashtags", []))
    full = "\n\n".join(p for p in (body, tags, post.get("link", "")) if p)
    if "url_weight" in rule:
        full = URL.sub("x" * rule["url_weight"], full)
    return len(full)


def validate(pack: dict) -> list[Finding]:
    out: list[Finding] = []
    posts = pack.get("posts")
    if not isinstance(posts, list) or not posts:
        return [Finding(-1, "-", "error", 'Expected {"posts": [...]} with at least one post')]

    for i, post in enumerate(posts):
        name = ALIASES.get(str(post.get("platform", "")).lower(), str(post.get("platform", "")).lower())
        rule = RULES.get(name)
        add = lambda level, msg: out.append(Finding(i, name or "?", level, msg))  # noqa: E731
        if not rule:
            add("error", f"Unknown platform '{post.get('platform')}'. Use one of: {', '.join(RULES)}")
            continue
        if not str(post.get("text", "")).strip():
            add("error", "Post text is empty")

        n = counted_length(post, rule)
        lo, hi = rule["best"]
        if n > rule["max_chars"]:
            add("error", f"{n} characters, limit is {rule['max_chars']}")
        elif n > hi or n < lo:
            add("warning", f"{n} characters, best range is {lo}-{hi}")

        tags = post.get("hashtags", [])
        bad = [t for t in tags if not HASHTAG.match(t)]
        if bad:
            add("error", f"Invalid hashtags (need #word, no spaces): {bad}")
        if len(set(t.lower() for t in tags)) != len(tags):
            add("warning", "Duplicate hashtags")
        if len(tags) > rule["hashtags"][1]:
            add("error", f"{len(tags)} hashtags, max is {rule['hashtags'][1]}")
        elif "best_tags" in rule and len(tags) > rule["best_tags"]:
            add("warning", f"{len(tags)} hashtags, {rule['best_tags']} or fewer usually performs better")

        has_link = bool(post.get("link")) or bool(URL.search(post.get("text", "")))
        if has_link and not rule["links"]:
            add("error", f"Links are not clickable on {name}: remove it and say 'link in bio'")

        if name == "youtube":
            title = post.get("title", "")
            if not title:
                add("error", "YouTube needs a title")
            elif len(title) > rule["title_max"]:
                add("error", f"Title is {len(title)} characters, limit is {rule['title_max']}")
            elif len(title) > rule["title_best"]:
                add("warning", f"Title is {len(title)} characters, under {rule['title_best']} shows fully on phones")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    with open(args.file, encoding="utf-8") as fh:
        pack = json.load(fh)
    findings = validate(pack)
    errors = [f for f in findings if f.level == "error"]
    if args.json:
        print(json.dumps([asdict(f) for f in findings], indent=2, ensure_ascii=False))
    else:
        for f in findings:
            print(f"[{f.level.upper():7}] post {f.index} ({f.platform}): {f.message}")
        print(f"{len(errors)} error(s), {len(findings) - len(errors)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
