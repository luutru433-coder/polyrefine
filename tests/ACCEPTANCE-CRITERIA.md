# Acceptance Criteria

Run all 60 cases on the Portable Pack (both Project and compact entry points) and the plugin. Use a fresh conversation per test, except for the ordered turns within one test. Record channel, version, account plan, client, date, case ID, result and any discrepancy; evaluate every turn with the expected route, except where a case explicitly targets the subsequent turn. For uncertain or optional results, apply the specified invariant, not exact phrasing. JA and Chinese outputs need native review by the requester.

- Pass 100% of critical subject, negation, tense, obligation and certainty checks.
- Preserve all numbers and identifiers exactly.
- Pass all routing and formatting checks.
- Report no cross-task context leakage or unauthorized rewrites.
- Report no Soft Alternative that changes assertion strength; omission is valid if no faithful softening exists.
- Verify readability and copy/paste on desktop web and mobile.
- Verify setup and use on an actual ChatGPT Free account. For the plugin, after publication, verify discovery, installation and use separately on web and mobile. Record plan, region or workspace limitations rather than advertising availability.

These requirements apply to the acceptance suite, not all possible model outputs. A packaging pass does not mean language behavior, publication, or Free availability has been verified. Do not mark the public release ready if a gate remains open. The Portable Pack may be released before the plugin once its own gates pass.
