# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
Users could use keywords that will not match,  the item might be there but the search might not find it because the words are different. This path makes two model calls thatb call to Gemini and either can fail. An api could also hit its rate limit and have a network problem or timeout.
---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
suggest_outfit and returns a message naming what to change — 5 of 5 tries.

**Why this target:**


This path doesn't use Gemini, so the result is the same every time. If it doesn't work  that can be a bug on my code.
---

## 3. Something about state

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->



**Why this target:**

Given a query that matches at least one listing, the `id` of session["selected_item"] is the same as the `id` of the item  suggested_outfit  received — in  5  of 5 tries.

**Why this target:**  Because this dosn't call Gemini, it should return the same every time.

---

## 4. Something about the fit card

Given a query that matches at least one listing, the fit card mentions the item's price — in 4 of 5 tries.






**Why this target:** The fit card calls Gemini, so the wording changes each time and I allow one miss. Gemini might leave the price out once, even though the prompt asks for it. If it's missing more than once, that means my prompt isn't clear enough.



---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->

Given a query that matches at least one listing and an invalid GEMINI_API_KEY, the agent shows a message naming GEMINI_API_KEY instead of crashing — in 5 of 5 tries.

With a fake key Gemini rejects you every single time, it isn't random so 5 of 5 works best for this case.



**Why this target:**
With a fake key Gemini rejects you every single time, it isn't random,and handling the rejection is my own code, so if it ever crashes, that's a bug in my error handling.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
