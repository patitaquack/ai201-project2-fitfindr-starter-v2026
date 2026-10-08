"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re

import config
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    listings = load_listings()

    if max_price is not None:
        listings = [item for item in listings if item["price"] <= max_price]

    if size:
        listings = [item for item in listings if _size_matches(size, item["size"])]

    keywords = _keywords(description)
    scored = []
    for item in listings:
        score = _keyword_score(keywords, item)
        if score > 0:
            scored.append((score, item))

    # sorted() is stable, so equal scores keep the order they had in the file.
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in scored[: config.SEARCH_RESULT_LIMIT]]


# Words that say nothing about the item. Without this, "looking for a tee"
# matches every listing whose description contains "for" or "a".
_STOPWORDS = {
    "a", "an", "and", "the", "for", "with", "in", "on", "of", "to", "or",
    "i", "im", "i'm", "my", "me", "some", "something", "looking", "want",
    "need", "find", "any", "that", "this", "is", "it",
}


def _keywords(text: str) -> set[str]:
    """Lowercase words from the query, minus stopwords."""
    words = re.findall(r"[a-z0-9']+", (text or "").lower())
    return {w for w in words if w not in _STOPWORDS}


def _keyword_score(keywords: set[str], item: dict) -> int:
    """
    How many query keywords appear as whole words in the listing.

    Whole words, not substrings, so "tee" doesn't match "steel". A trailing
    "s" is ignored on both sides so "tees" and "tee" count as the same word.
    """
    fields = [
        item.get("title"),
        item.get("description"),
        item.get("category"),
        item.get("brand"),  # None for most listings
        " ".join(item.get("style_tags") or []),
        " ".join(item.get("colors") or []),
    ]
    text = " ".join(f for f in fields if f).lower()
    listing_words = {w.rstrip("s") for w in re.findall(r"[a-z0-9']+", text)}
    return sum(1 for k in keywords if k.rstrip("s") in listing_words)


def _size_matches(wanted: str, listed: str) -> bool:
    """
    Size rule: the requested size has to equal one whole option in the
    listing's size, ignoring case.

    A listing size is split on "/" into options, and notes in brackets are
    dropped: "S/M" offers S and M, "XL (oversized)" offers XL. Multi-part
    sizes also match on each part, so "W30 L30" matches a request for "W30".
    Never a substring test: "L" does not match "XL", and "S" does not match
    "US 9". "One Size" listings only match a request for "one size".
    """
    wanted = " ".join(wanted.upper().split())
    for option in (listed or "").upper().split("/"):
        option = " ".join(re.sub(r"\(.*?\)", "", option).split())
        if wanted == option or wanted in option.split():
            return True
    return False


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    items = (wardrobe or {}).get("items") or []
    item_text = _describe_item(new_item)

    if not items:
        prompt = (
            f"Someone is thinking about buying this secondhand item:\n{item_text}\n\n"
            "They haven't saved any of their own clothes yet. Suggest one or two "
            "outfits built around this item, describing the kinds of pieces that "
            "would go with it (colors, cuts, shoes, layers). Keep it under 120 words."
        )
    else:
        closet = "\n".join(
            f"- {w.get('name')} ({w.get('category')}; colors: "
            f"{', '.join(w.get('colors') or [])}"
            + (f"; note: {w['notes']}" if w.get("notes") else "")
            + ")"
            for w in items
        )
        prompt = (
            f"Someone is thinking about buying this secondhand item:\n{item_text}\n\n"
            f"Here is what they already own:\n{closet}\n\n"
            "Suggest one or two outfits that pair the new item with specific pieces "
            "from their wardrobe, naming those pieces exactly as listed. Only use "
            "pieces from the list. Keep it under 120 words."
        )

    response = generate(prompt, system=_STYLIST_SYSTEM).strip()
    if not response:
        # The model came back empty — still honour "never return an empty string".
        return f"Try the {new_item.get('title', 'item')} with simple basics in neutral colors."
    return response


_STYLIST_SYSTEM = (
    "You are a friendly thrift-store stylist. Give practical, specific outfit "
    "ideas in plain text. No markdown headings."
)


def _describe_item(item: dict) -> str:
    """The listing fields the model needs, one per line."""
    lines = [
        f"Title: {item.get('title')}",
        f"Category: {item.get('category')}",
        f"Description: {item.get('description')}",
        f"Colors: {', '.join(item.get('colors') or [])}",
        f"Style: {', '.join(item.get('style_tags') or [])}",
        f"Size: {item.get('size')}",
        f"Condition: {item.get('condition')}",
        f"Price: ${item.get('price')}",
        f"Platform: {item.get('platform')}",
    ]
    if item.get("brand"):
        lines.append(f"Brand: {item['brand']}")
    return "\n".join(lines)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    if not outfit or not outfit.strip():
        return (
            "No fit card: there was no outfit suggestion to write a caption about. "
            "Run suggest_outfit first and pass its result in."
        )

    prompt = (
        f"Here is a secondhand find:\n{_describe_item(new_item)}\n\n"
        f"Here is how it will be styled:\n{outfit}\n\n"
        "Write a 2 to 4 sentence caption someone would actually post about this "
        "find. Mention the item, its price, and the platform once each, and be "
        "specific about the vibe of the outfit. It should read like a real post, "
        "not a product description. Return only the caption."
    )
    return generate(prompt, system=_CAPTION_SYSTEM).strip()


_CAPTION_SYSTEM = (
    "You write short, casual social media captions about thrifted outfits. "
    "Plain text, at most two emojis, no hashtags."
)
