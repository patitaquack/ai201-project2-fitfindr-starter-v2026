"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
    {
        # Criterion 3 — state. Any normal query works; what gets checked is
        # that session["selected_item"] is the item suggest_outfit received.
        "name": "selected item reaches suggest_outfit",
        "query": "black denim jacket under $60",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # Criterion 4 — the fit card. The same query five times, so the same
        # item ($35 Knit Cardigan) goes to create_fit_card five times.
        "name": "fit card mentions the price",
        "query": "knit cardigan under $45",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Criterion 5 — model unavailable. A matching query with a key Gemini
        # will reject. run_eval.py swaps the key in for this scenario only.
        "name": "invalid API key names GEMINI_API_KEY",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 5,
        "env": {"GEMINI_API_KEY": "invalid-key-for-testing"},
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
