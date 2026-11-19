"""State icons for the interface: one set (Lucide), one stroke, one size. Shape and word carry the state; colour is the third cue.

Icon geometry: Lucide v1.75.0 (https://lucide.dev), ISC License, Copyright (c) 2026 Lucide Icons and Contributors.
Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted,
provided that the above copyright notice and this permission notice appear in all copies. (Full text: THIRD_PARTY_NOTICES.md)
Icons used: circle-check (normal), eye (watch), triangle-alert (degraded), circle-help (unknown).
"""

_BODY = {
    "NORMAL": "<circle cx='12' cy='12' r='10' /> <path d='m16 9-5.5 5.5L8 12' />",
    "WATCH": "<path d='M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0' /> <circle cx='12' cy='12' r='3' />",
    "DEGRADED": "<path d='m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3' /> <path d='M12 9v4' /> <path d='M12 17h.01' />",
    "UNKNOWN": "<circle cx='12' cy='12' r='10' /> <path d='M9 9.5a3 2.5 0 016 0c0 2-2 2-3 3.5' /> <path d='M12 17h.01' />",
}


def state_icon(state):
    """Inline SVG for a state, decorative (the state word always sits next to it). Unknown states fall back to UNKNOWN."""
    inner = _BODY.get(state, _BODY["UNKNOWN"])
    return ("<svg class='cs-ico' width='1.15em' height='1.15em' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' "
            "stroke-linecap='round' stroke-linejoin='round' aria-hidden='true' focusable='false'>" + inner + "</svg>")
