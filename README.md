# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the listings for items that match a description, with an optional size and price ceiling.
- **Inputs:** `description` (str), `size` (str or None), `max_price` (float or None)
- **Returns:** A list of matching listing dicts, best match first, at most 10 results. Each dict includes: id, title, description, category, style_tags (list), size, condition, price (float), colors (list), brand (str or None), platform.
- **When it has nothing:** It returns an empty list when nothing matches — an empty list, not None, and not an exception.
- **Size rule:** The requested size has to equal one whole option in the listing's size, ignoring case. "S/M" counts as S and M, and notes in brackets are ignored ("XL (oversized)" is XL). It's never a substring test, so "L" doesn't match "XL" and "S" doesn't match "US 9". "One Size" listings only match a request for "one size".

### `suggest_outfit`

- **What it does:** Uses the AI model to suggest one or two outfits that pair a thrifted item with pieces the user already owns.
- **Inputs:** `new_item` (dict): the listing the user is thinking about buying; `wardrobe` (dict): the user's clothes in an `items` list, which may be empty
- **Returns:** A non-empty string with one or two outfit suggestions that name pieces from the user's wardrobe.
- **When it has nothing:** With an empty wardrobe, it returns general styling advice for the item, instead of raising an error or returning an empty string.

### `create_fit_card`

- **What it does:** Uses the AI model to write a short caption someone would actually post about the find.
- **Inputs:** `outfit` (str): the outfit suggestion from `suggest_outfit`; `new_item` (dict): the listing for the item
- **Returns:** A string with a 2–4 sentence caption that reads like a real post. It mentions the item, price, and platform.
- **When it has nothing:** If `outfit` is empty or whitespace, it returns a message explaining the outfit is missing, instead of raising an error.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**
If search_listings returns an empty list, put a message in session["error"] naming what the user could change, and return the session without calling suggest_outfit. Otherwise take the first result, put it in session["selected_item"], and continue.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->
Regex, not a model call. It costs nothing and gives the same answer every time and the mistakes are easy to trace (through patterns). Wording that won't be recognized: "nothing over thirty dollars", it gives no price.

**What moves through the session:** <!-- which fields, in what order -->

- `query` — new_session — what the user typed
- `wardrobe` — new_session — the user's clothes
- `parsed` — parse_query — description, size, max_price
- `search_results` — search_listings — the matching listings
- `error` — the branch — a message is set here if the search came up empty, and the loop stops
- `selected_item` — the loop — the first search result
- `outfit_suggestion` — suggest_outfit — the outfit text
- `fit_card` — create_fit_card — the caption


---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30, size M'
[1] parse_query
      in:  vintage graphic tee under $30, size M
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 8 items: Y2K Baby Tee — Butterfly Print, Mesh Long-Sleeve Top — Black, 90s Silk Slip Dress — Floral, Midi Length … +5 more
      →    8 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Hey there! That Y2K baby tee is an absolute steal, and you are going to get so much wear out of it. Here are t…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Obsessed with this little butterfly tee I just scored on depop for eighteen bucks. Paired it with baggy jeans …

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Hey there! That Y2K baby tee is an absolute steal, and you are going to get so much wear out of it. Here are two super fun ways to style it using pieces you already own!

Outfit one is all about that classic early 2000s contrast. Pair the baby tee with your baggy straight-leg jeans, dark wash. Tuck the tee in and add your chunky white sneakers to keep it casual and comfy. Throw on the black crossbody bag to finish the look.

Outfit two leans into a cool grunge mix. Layer your vintage black denim jacket right over the baby tee, and pair them with your wide-leg khaki trousers. Lace up your black combat boots to give the sweet butterfly print a nice edgy finish.

  Fit card: Obsessed with this little butterfly tee I just scored on depop for eighteen bucks. Paired it with baggy jeans and chunky sneakers for the ultimate cozy y2k day. 🦋✨

0 model calls this session, 2 served from cache
```

**The three tools, tested one at a time**


Grab those Vintage Levi's 501 Jeans and tuck in your white ribbed tank top. Add the brown leather belt to define your waist, slip on your chunky white sneakers, and throw your vintage black denim jacket over top for a casual, effortless look. Finish it off with your black crossbody bag for running errands.

For a cozier vibe, layer your oversized grey crewneck sweatshirt right over the jeans. Pair this relaxed combination with your black combat boots for a tough, streetwear-inspired edge, and wear your black crossbody bag to keep your hands free.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Scored these vintage Levi's 501 jeans on Depop for just $38 and I am obsessed. Threw them on with my favorite white sneakers for the ultimate effortless weekend fit. The knee fading gives them the best lived-in streetwear vibe. 👖👟
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**
 After writing the criteria, I asked claude to check it for me and to correct me if I didn't have the right understanding and explanations for each one.

-

**Moment 2**

I had claude help me understand better the ste- by -step practice the agent follows after a query. As I got confused with what the end goal was and how each function works.

**Unit 4, Moment 1**

I asked Claude to help diagnose my run log. It said `black denim jacket under $60` picked a light-wash jacket because the search let "denim" and "jacket" outscore "black". When it checked the listings data, that turned out to be wrong: there's no black denim jacket under $60. Three listings tie at 2 of 3 keywords, and file order picks the winner. I kept the corrected version in my diagnosis. What I took from it: a confident explanation isn't a diagnosis until it's checked against the data.

**Unit 4, Moment 2**

Claude committed its changes to my repo without asking during the first three milestones. Because the commit history is part of my grade, I told it to stop committing, and to tell me which files it changed so I can review them before I commit them myself.



<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. `selected_item` id equals the id `suggest_outfit` received | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. The fit card mentions the item's price | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. An invalid key gives a message naming GEMINI_API_KEY, no crash | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Source: `python run_eval.py --label before`, caching off, 45 real model calls. The full output is in [results/run_2026-10-19_0935_before.md](results/run_2026-10-19_0935_before.md). The scenarios are in `scenarios.py`, one per criterion, plus an empty-wardrobe diagnostic run that isn't one of the five.

How I scored each try:
- **1:** `session["error"]` is None and `session["fit_card"]` is a non-empty string.
- **2:** `session["error"]` names what to change, `suggest_outfit` was never called, and `fit_card` is None.
- **3:** I wrapped `agent.suggest_outfit` to record the `id` of the item it was actually called with, then compared that to `session["selected_item"]["id"]`. It was `lst_007` both times, on every try.
- **4:** the card contains the price as a number (`$35` for the $35.0 Knit Cardigan). All five cards were different, so these were real calls, not cached answers.
- **5:** no exception, `session["error"]` contains `GEMINI_API_KEY`, and `fit_card` is None. The bad key was set for this scenario only, through its `env` key in `scenarios.py`.

**Real output from one try** (Try 1 of each), pasted as text, naming the file and function that produced it:

**Criterion 1:** `agent.py::run_agent`, trace from `trace.py`. The fit card is from `tools.py::create_fit_card`.

```
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)

fit_card: Just scored this little butterfly baby tee on Depop for $18 and I am obsessed. Styled it with baggy denim and chunky sneakers for the ultimate Y2K throwback moment. 🦋✨
```

**Criterion 2:** `agent.py::run_agent`, with the message from `agent.py::_nothing_found_message`.

```
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
      →    0 match(es)
[3] branch
      →    search returned []: stopping before suggest_outfit

error: Nothing in the listings matched description 'designer ballgown', size XXS, under $5.
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.
fit_card: None
```

**Criterion 3:** `agent.py::run_agent` (the session), with what `tools.py::suggest_outfit` was actually called with.

```
[3] select_item
      out: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
[4] suggest_outfit
      in:  Denim Jacket — Light Wash, Cropped ($42.0, poshmark)

session["selected_item"]["id"]: lst_007
id received by suggest_outfit:  lst_007
```

**Criterion 4:** `tools.py::create_fit_card`, for the Knit Cardigan, Chunky Brown ($35.0, depop).

```
Living in this chunky brown cardigan from Depop now that it’s finally sweater weather. For just $35, it throws the ultimate cozy, earth-toned vibe over my favorite white tank and baggy jeans. Grabbed my trusty coffee and I'm ready to take on the day ☕️🤎
```

**Criterion 5:** `agent.py::run_agent`, in the `except ModelUnavailable` handler. The text from the service is from `generate.py::_explain`.

```
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] model unavailable
      →    stopping, search results kept

error: The model couldn't be reached, so the outfit and caption steps didn't run. The search worked — 10 listing(s) were found. Check GEMINI_API_KEY in your .env, then run the same query again.
What the service said: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | A matching query completes all three tools and returns a fit card | 4 of 5 | MET (5/5) | All 5 tries ended with `session["error"]` None and a non-empty `fit_card`. The 5 cards were all different, so these were real model calls, not cached. |
| 2 | An impossible query stops before `suggest_outfit` and names what to change | 5 of 5 | MET (5/5) | All 5 tries set `session["error"]` with the "Things to change" list. `suggest_outfit` was never called and `fit_card` stayed None. |
| 3 | The `id` of `session["selected_item"]` equals the `id` of the item `suggest_outfit` received | 5 of 5 | MET (5/5) | A wrapper on `agent.suggest_outfit` recorded the id it was actually called with: `lst_007` every time, the same as `selected_item`. |
| 4 | The fit card mentions the item's price | 4 of 5 | MET (5/5) | All 5 cards contained `$35` for the $35.0 Knit Cardigan. I only counted the price written as a number. |
| 5 | An invalid `GEMINI_API_KEY` gives a message naming `GEMINI_API_KEY`, with no crash | 5 of 5 | MET (5/5) | All 5 tries returned a session with no exception. `session["error"]` contained `GEMINI_API_KEY`, and `fit_card` was None. |

**Diagnoses**

Nothing missed, so there's no miss to diagnose. I read each verdict plainly: every PASS cell meets the criterion as written, with no generous reading needed.

**Were my targets low?** Partly, yes.

- **Criteria 2, 3 and 5 are deterministic.** No model output affects them, so 5 of 5 was the only honest target. Meeting them shows the branch, the session and the error handler work. It doesn't show the agent is good.
- **Criterion 1's 4 of 5** left room for a rate limit or a timeout. Neither happened in 45 real calls, and `generate.py` retries rate limits. 4 of 5 was cautious, but it's tied to a real way the run can fail, so I'd keep it.
- **Criterion 4 is the one I'd tighten.** I set 4 of 5 to allow one miss, but the miss never had a chance. I tested one item, five times, and that item has a round price and a brand. The prompt in `tools.py::create_fit_card` says to mention the price outright, so 4 of 5 on a single item was an easy bar. A tighter version: *"For 5 different matching items, including at least two with `brand` None, each fit card states the item's exact price as a number, in 5 of 5."* This tests the prompt across items instead of repeating one lucky case. It's also stricter about format: in an earlier run, `suggest_outfit` wrote the price as "eighteen bucks", so the model doesn't always use a number.

**A pattern the criteria didn't catch:** every criterion checks that a step ran, or that something was passed on correctly. None of them check how good a match the item is. In the criterion 3 run, `black denim jacket under $60` picked `Denim Jacket — Light Wash, Cropped`. No listing in the data matches all three words. `tools.py::_keyword_score` gives one point per matching keyword, and three listings tie at 2 of 3: the light-wash denim jacket (denim + jacket), `Straight Leg Black Jeans` (black + denim) and `90s Leather Bomber — Black` (black + jacket, but $75, so the price filter drops it). Two problems follow:

1. **The tie is broken by file order.** `sorted()` is stable, so whichever listing comes first in the data wins. Here that gave a sensible pick, a jacket. But nothing in the code prefers the item's type ("jacket") over its color ("black"), so a different data order could have recommended jeans.
2. **The loop treats a partial match as a full match.** The branch only checks whether the list is empty. So the user asked for black, got light blue, and nothing told them that "black" wasn't matched.

Criterion 1 still passes, because something matched and the run finished. This is a gap in what I chose to measure, not a criterion that was measured wrongly, so I've noted it here rather than revising one of the five.



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
[1] parse_query
      in:  looking for a vintage graphic tee under $30
      out: {'description': 'looking for a vintage graphic tee', 'size': None, 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'looking for a vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    10 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Hey there! That Y2K baby tee is an absolute steal, and you are going to get so much wear out of it. Here are t…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Obsessed with this little butterfly tee I just scored on depop for eighteen bucks. Paired it with baggy jeans …
```

**Empty search**

```
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
      →    0 match(es)
[3] branch
      →    search returned []: stopping before suggest_outfit
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

I moved `search_listings` onto MCP. In `mcp_server.py` it's registered with `@mcp.tool()` and the same typed inputs as the Tool Inventory: `description: str`, `size: str | None`, `max_price: float | None`. Its description gives units (US dollars, inclusive), explains the size rule, and states the empty case (`[]`, not null or an error). `python mcp_client.py` lists the tool with `description: string`, `size: string (optional)`, `max_price: number (optional)`.

In `agent.py`, `_search()` now calls `call_tool("search_listings", {...})` instead of calling the function directly, and falls back to the direct call if MCP can't be reached. Nothing behaved differently afterwards. I compared MCP and direct results for three queries (a match, an empty search, and a size-filtered search), and they were `==` equal every time: same list of dicts, same order, and `[]` stays a list rather than turning into `None` or a string. So the empty-list branch still fires over MCP. One thing to watch: the fallback means a broken server would fail silently. That's why I checked equality directly instead of only checking that a query still produced output.

### Failure modes, triggered on purpose

I triggered each failure separately, using a new query each time so nothing came from the cache. None of them crashed, hung or went silent, so I didn't need a new handler. The handlers were already in place: the empty-list branch in `run_agent`, the empty-wardrobe prompt in `suggest_outfit`, and the `except ModelUnavailable` around the loop.

**1. Empty search:** `python app.py ask 'sequined astronaut suit size XXS under $3'`

The run stopped after the search (3 trace steps, versus 5 on the happy path), and `suggest_outfit` was never called. What the agent said:

```
Nothing in the listings matched description 'sequined astronaut suit', size XXS, under $3.
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $3.
```

**2. Empty wardrobe:** `python app.py ask 'black denim jacket under $60' --empty-wardrobe`

The trace shows `0 wardrobe item(s)` going into `suggest_outfit`, and it still returned a real suggestion, not a crash or an empty string. It suggested general pieces to pair with the jacket (a black ribbed tank, parachute cargo pants, a floral midi dress) instead of claiming items the user owns. What the agent said, first lines:

```
Hey there! A cropped Wrangler jacket with structured shoulders is such a fun find. Here are two easy ways to style it.

Outfit one leans into that cool streetwear vibe. Throw the jacket over a fitted black ribbed tank top and baggy gray parachute cargo pants. ...
```

**3. Model unavailable:** `GEMINI_API_KEY=<bad key> python app.py ask 'cozy wool cardigan under $45'` (a new query, so the cache didn't answer it)

The search and item selection still ran, because they don't need the model. Then the loop stopped at `[4] model unavailable` and kept the search results, without a stack trace or a hang. What the agent said:

```
The model couldn't be reached, so the outfit and caption steps didn't run. The search worked — 2 listing(s) were found. Check GEMINI_API_KEY in your .env, then run the same query again.
What the service said: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.
```

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

**No criterion is still missed:** all five were MET (5/5) in the before run. That doesn't mean nothing is broken. These are the problems I know about that my criteria don't catch:

1. **Ties in search are broken by file order.** `black denim jacket under $60` has no full match, and three listings tie at 2 of 3 keywords. `tools.py::search_listings` keeps whichever comes first in the data. *What I'd do:* break ties by whether the listing's `category` matches a query word, so "jacket" beats "black" when the user names an item type. Then add a criterion: for 5 queries naming a category, the selected item's category matches in 5 of 5.
2. **A partial match is shown as if it were a full match.** The branch in `agent.py::run_agent` only checks whether the result list is empty, so the user who asked for black got light blue without being told. *What I'd do:* record which query words the selected item didn't match, and say so in the output ("no black denim jackets; this is the closest").
3. **Criterion 4 was tested on one item.** I passed it 5 of 5, but always with the same $35 cardigan, which has a brand. I'd re-run it on 5 different items, including at least two with `brand` None, before trusting it.
4. **The model-unavailable message only helps a developer.** "Check GEMINI_API_KEY in your .env" means nothing to someone using the app, and it says the search found listings without showing them. *What I'd do:* show the found listings, with a plain message that styling suggestions are unavailable right now.
5. **The MCP fallback is silent.** If `mcp_server.py` breaks, `agent.py::_search` quietly calls `search_listings` directly, and the trace still says "via MCP". *What I'd do:* make the trace record which path actually ran.

**Why I stopped here:** none of these made a criterion miss, and the unit asks for one improvement, measured properly. I kept the rest as a list rather than fixing several things at once and not being able to tell which change did what.

**On the MCP move:** I moved `search_listings` behind `mcp_server.py` and changed `agent.py::_search` to call `call_tool("search_listings", ...)`. Nothing behaved differently: the MCP and direct calls returned `==` equal results for a matching query, an empty one and a size-filtered one, including `[]` for no match. The details are under Loop Trace.



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
