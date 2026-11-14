import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from validate_posts import main, validate  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def levels(findings):
    return [(f.platform, f.level) for f in findings]


def test_example_pack_has_no_errors():
    pack = json.loads((ROOT / "examples" / "pack.json").read_text(encoding="utf-8"))
    assert not [f for f in validate(pack) if f.level == "error"]


def test_x_counts_urls_as_23_chars():
    # 250 + space + a 60-char URL counted as 23 = 274: fits, although the raw text is 311 chars.
    long_url = "https://example.com/" + "p" * 40
    ok = validate({"posts": [{"platform": "twitter", "text": "a" * 250 + " " + long_url}]})
    assert not [f for f in ok if f.level == "error"]
    too_long = validate({"posts": [{"platform": "x", "text": "a" * 260 + " " + long_url}]})
    assert ("x", "error") in levels(too_long)


def test_instagram_link_is_an_error():
    findings = validate({"posts": [{"platform": "instagram", "text": "See https://d2logix.com"}]})
    assert any("link in bio" in f.message for f in findings)


def test_bad_hashtags_and_unknown_platform():
    findings = validate({"posts": [
        {"platform": "linkedin", "text": "x" * 700, "hashtags": ["#ok", "not ok"]},
        {"platform": "myspace", "text": "hi"},
    ]})
    assert ("linkedin", "error") in levels(findings)
    assert any("Unknown platform" in f.message for f in findings)


def test_youtube_needs_title(tmp_path):
    p = tmp_path / "p.json"
    p.write_text(json.dumps({"posts": [{"platform": "youtube", "text": "desc"}]}), encoding="utf-8")
    assert main([str(p)]) == 1
