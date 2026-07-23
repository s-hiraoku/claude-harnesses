# Before / after examples

Calibration set for `SKILL.md` — read once per session when the skill activates. Each pair shows the cut line: what goes, what must survive. Note in every example: the "after" is *shorter and carries more*, and no fact/caveat from the "before" is missing.

## 1. Investigation report opening

**Before (slop):**
> In this report, I will summarize the results of my investigation into the login timeout issue. This was a very interesting problem that required looking at several different parts of the codebase. After a thorough analysis, I believe the root cause is `SessionStore.refresh()` re-acquiring the DB lock it already holds at `session/store.py:142`, which means that under load the second acquisition waits out the 30 s timeout. It should also be noted that I ruled out token expiry because the logs show valid tokens at failure time, and I ruled out the LB health check because the failure is identical when the LB is bypassed. This is an important finding.

**After:**
> The login timeout is caused by `SessionStore.refresh()` re-acquiring the DB lock it already holds (`session/store.py:142`); under load the second acquisition waits out the 30 s timeout. Two other suspects were ruled out: token expiry (logs show valid tokens at failure time) and the LB health check (fails identically with LB bypassed).

Why: the after removes the announcement, self-commentary, and repeated emphasis while preserving the cause, location, mechanism, timing, and eliminated alternatives.

## 2. PR description

**Before (slop):**
> This PR makes some improvements to the validation logic. Three issues were found and fixed: empty-string emails passed `validateEmail` in `validators.ts:18`, phone numbers over 15 digits were silently truncated at line 34, and `null` addresses threw instead of returning a field error at line 51. The code now handles these edge cases appropriately and is more robust. A regression test was added for each fix, and `pnpm test validators` passes all 41 tests. Please review when you have a chance!

**After:**
> Fixes three validation gaps: empty-string emails passed `validateEmail` (`validators.ts:18`), phone numbers over 15 digits were silently truncated (`:34`), and `null` addresses threw instead of returning a field error (`:51`). Each fix has a regression test; `pnpm test validators` passes (41 tests).

Why: the after deletes vague summaries and the ritual closing, stating each fix, location, regression test, command, and result once.

## 3. Recommendation with caveat (preservation test)

**Before (slop):**
> Based on my analysis, I would generally recommend migrating to the new API, as it removes the per-request authentication round-trip, which we measured at 80–120 ms per call. It could potentially be worth considering that there may be a compatibility concern with clients on SDK versions below 2.3 because they cannot parse the new pagination cursor. Those clients will need to be pinned or upgraded before the cutover, but this should not be a major issue.

**After:**
> Recommend migrating to the new API: it removes the per-request auth round-trip (measured 80–120 ms per call). One compatibility caveat: clients on SDK < 2.3 cannot parse the new pagination cursor and will need pinning or upgrading before the cutover.

Why: the after removes reflexive hedges while preserving the measured reason, affected SDK versions, failure mode, and required mitigation. Deleting the caveat would be omission.

## 4. Structure over substance

**Before (slop):**
> ## Summary
> - The 120-line `processData` function, which had cyclomatic complexity 14, was refactored
>
> ## Details
> - **What changed**: The function was split into `parse`, `validate`, and `persist`
> - **Why**: The function was hard to read
> - **Impact**: Behavior is unchanged, and the existing 12 tests still cover it
>
> ## Conclusion
> In conclusion, this refactoring improves the readability of the code.

**After:**
> Split `processData` (was 120 lines, cyclomatic complexity 14) into `parse`, `validate`, and `persist`; behavior unchanged, covered by the existing 12 tests.

Why: three headings, three bullets, and a conclusion repeat the same point. The after preserves the size, complexity, split, behavior, and test coverage in one sentence.
