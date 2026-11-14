# Social Post Studio: a Claude Agent Skill

> One article in → a ready-to-post **content pack** for LinkedIn, Instagram, TikTok, YouTube Shorts and X, each written for its platform and **validated against real limits**.

![skill](https://img.shields.io/badge/Claude-Agent%20Skill-D97757) ![python](https://img.shields.io/badge/python-3.10%2B-3776AB) ![license](https://img.shields.io/badge/license-MIT-green)

## What it does

| Step | Who |
|---|---|
| Pulls the key message, facts and call to action from your source | Claude |
| Writes a platform-native post for each network (hook, length, hashtags, link rules) | Claude |
| Checks every post: length (X counts URLs as 23), hashtag count/format, links where they don't work, YouTube title | `scripts/validate_posts.py` |
| Fixes errors and re-checks before answering | Claude |

It never invents statistics or quotes that aren't in the source.

## Install

```bash
git clone https://github.com/SameerD2logix/claude-skill-social-post-studio ~/.claude/skills/social-post-studio
```
Ask Claude: *"Turn this article into posts for LinkedIn, Instagram and X: <link or text>"*.

## Validator

```bash
$ python scripts/validate_posts.py examples/pack.json
[WARNING] post 1 (instagram): 248 characters, best range is 300-1000
0 error(s), 1 warning(s)
```
- Errors = would be rejected or broken (exit code 1). Warnings = works, but not best practice.
- `--json` for automation (n8n, CI, Claude Code hooks).
- Standard library only.

## Layout

```
SKILL.md                    workflow + platform playbook
reference/platforms.md      limits and best practice per platform
scripts/validate_posts.py   validator
examples/pack.json          a full example pack
tests/                      pytest suite
```

## Tests

```bash
pip install pytest && pytest -q
```

## Author

**Sameer Hussain**, [D2Logix](https://d2logix.com). Built while making an automated news-to-social-media pipeline.
