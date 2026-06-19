#!/usr/bin/env python3
"""Export visible LinkedIn message cards without sending anything.

This script is intentionally read-only. It does not accept credentials, does not
log in, does not send messages, and does not click send/apply controls. The
operator must provide a Playwright user-data directory that is already logged in.

Example:
  python tools/linkedin_message_export.py --user-data-dir /path/to/profile --output .local/linkedin-messages.json
"""

from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.async_api import async_playwright


JS_GET_CONVERSATIONS = r"""
() => {
  const items = document.querySelectorAll('.msg-conversation-listitem, [data-test-id="conversation-list-item"]');
  return Array.from(items).map((item, index) => {
    const nameEl = item.querySelector('.msg-conversation-card__participant-names, [data-test-id="conversation-name"]');
    const previewEl = item.querySelector('.msg-conversation-card__message-snippet, [data-test-id="conversation-preview"]');
    const timeEl = item.querySelector('.msg-conversation-card__timestamp, time');
    return {
      index,
      name: nameEl?.textContent?.trim() || '',
      preview: previewEl?.textContent?.trim() || '',
      time: timeEl?.textContent?.trim() || timeEl?.dateTime || '',
      unread: item.classList.contains('msg-conversation-listitem--unread') || item.classList.contains('unread')
    };
  }).filter(c => c.name || c.preview);
}
"""


async def export_messages(user_data_dir: Path, limit: int, headless: bool) -> dict:
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=headless,
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = await context.new_page()
        try:
            await page.goto("https://www.linkedin.com/messaging/", wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(5000)
            for _ in range(5):
                await page.evaluate("() => window.scrollBy(0, 1200)")
                await page.wait_for_timeout(500)
            conversations = await page.evaluate(JS_GET_CONVERSATIONS)
            return {
                "exported_at": datetime.now(timezone.utc).isoformat(),
                "source": "linkedin-messaging-visible-cards",
                "count": len(conversations[:limit]),
                "conversations": conversations[:limit],
            }
        finally:
            await context.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only export of visible LinkedIn messaging cards.")
    parser.add_argument("--user-data-dir", type=Path, required=True, help="Existing logged-in Playwright/Chromium profile")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()

    if not args.user_data_dir.exists():
        raise SystemExit(f"user data directory does not exist: {args.user_data_dir}")
    result = asyncio.run(export_messages(args.user_data_dir, args.limit, args.headless))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "count": result["count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
