---
name: social-post-studio
description: Turn an article, news link, product update or idea into ready-to-post content for Instagram, LinkedIn, TikTok, YouTube Shorts and X, each within that platform's limits. Use when the user asks for social media posts, captions, a content pack or "post this everywhere".
---

# Social Post Studio

Write one source into a **content pack**: a separate post per platform, written for how people
use that platform, and validated against its hard limits.

## Workflow

1. **Read the source** and pull out: the one key message, 2–3 supporting facts, and the call to action.
   If facts are unclear, say so instead of inventing numbers.
2. **Ask only if needed:** which platforms (default: Instagram, LinkedIn), language, brand voice.
3. **Write the pack** as JSON in this shape (one object per platform):
   ```json
   {"posts": [
     {"platform": "linkedin", "text": "...", "hashtags": ["#AI"], "link": "https://..."},
     {"platform": "instagram", "text": "...", "hashtags": ["#AI", "#Tech"]}
   ]}
   ```
4. **Validate** before answering:
   ```bash
   python scripts/validate_posts.py pack.json
   ```
   Fix every error (too long, too many hashtags, link where links don't work) and re-run.
5. **Present** each post under a platform heading, ready to copy.

## Platform playbook

Details and limits: `reference/platforms.md`. In short:

| Platform | Hook | Length | Hashtags | Links |
|---|---|---|---|---|
| LinkedIn | Insight or lesson in line 1 | 600–1,300 chars | 3–5 | OK |
| Instagram | Emotion/benefit in line 1 | 300–1,000 chars | 5–15 | Not clickable: say "link in bio" |
| TikTok | First 2 seconds matter | caption < 300 chars | 3–5 | No |
| YouTube Shorts | Title < 60 chars | description < 1,000 | 3–5 | OK in description |
| X | One sharp line | < 280 chars | 1–2 | OK (counts as 23) |

## Quality bar

- Never invent statistics, quotes or dates that are not in the source.
- Each post must make sense **without** reading the others.
- One clear call to action per post.
