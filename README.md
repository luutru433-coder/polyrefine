# PolyRefine Translator

PolyRefine refines English without silently changing who did what, how certain it is, or when it happened. It turns English or Vietnamese into **Refined English**, **Japanese** and **Simplified Chinese**, and translates other supported source languages into **English Translation** by default. You can also name a target language or ask for a revision of a previous result.

## Try it in ChatGPT

- **Any chat:** copy the full [Compact Prompt](free-portable-pack/COMPACT-PROMPT.txt) into a fresh ChatGPT conversation, then send `I need your help.`
- **Your own Project:** follow the [Quick Start](free-portable-pack/QUICK-START.md), using the supplied [Project Instructions](free-portable-pack/PROJECT-INSTRUCTIONS.md).
- Compare your response with the [test examples](free-portable-pack/TEST-EXAMPLES.md). A translation ZIP upload and an external API key are not needed to use the Portable Pack.

PolyRefine does not disable platform Memory or guarantee translation accuracy. Review high-stakes translations before using them. See the [privacy policy](PRIVACY.md) or ask a question via [Issues](https://github.com/luutru433-coder/polyrefine/issues).

## Build from source

With Python 3.10 or newer (no dependencies):

```sh
python3 build.py
python3 build.py --check
python3 -m unittest discover -s tests
```

[core/](core/) is the only rule source. The build creates [public-plugin/](public-plugin/), [free-portable-pack/](free-portable-pack/), a copy at `dist/portable-pack/`, and the versioned ZIP. Edit rules in `core/`, not in generated files. Run the build again after making changes. `--check` compares the files with the current sources and validates the ZIP without writing files.

## Submit the skills-only plugin

Download [polyrefine-1.2.0.zip](dist/polyrefine-1.2.0.zip); use the ZIP as built, not the repository's “Download ZIP” archive.

1. Follow [OpenAI's submission instructions](https://developers.openai.com/plugins/deploy/submission) using your verified OpenAI Platform organization and a role with Apps Management Write.
2. Choose the skills-only submission path and upload the ZIP. Confirm the listing and support/privacy links, resolve any validation or scanning issues, and submit for review.
3. After approval, publish from the submission portal. For subsequent updates, update `VERSION` and the changelog, rebuild and submit the new ZIP.

Offline validation does not confer Directory approval. The listing describes the fixed semantic checks and rewrite/output workflow that distinguish PolyRefine from generic translation, but [guideline §1.1a](https://developers.openai.com/plugins/plugin-guidelines) remains subject to review. Plugin installation on ChatGPT Free has not been verified. Live use, desktop/mobile checks and Japanese/Chinese native review are tracked in the [acceptance criteria](tests/ACCEPTANCE-CRITERIA.md).

MIT licensed.
