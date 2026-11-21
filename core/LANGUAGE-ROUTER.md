# Language Router (R10)

Determine the dominant language of the entire in-scope source (not commands), using its grammar and overall meaning. Route the whole text once; process minority-language material too. Never drop it or route each paragraph separately.

- English: refine English; also translate into Japanese and Simplified Chinese.
- Vietnamese: translate to English, refine it moderately, then also produce Japanese and Simplified Chinese.
- Japanese, Simplified or Traditional Chinese, Korean, French, German, Spanish and other reliably understood languages: translate into English only.
- An explicit target or refine-only request overrides defaults. Use only the requested targets; when Chinese is requested without a script, use Simplified Chinese. Never silently switch to Traditional Chinese.
- If the dominant language or meaning is not reliably identifiable, state the uncertainty briefly and translate only what is supportable, without inventing source material or asserting an unsupported route.
