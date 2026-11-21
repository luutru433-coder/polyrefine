import argparse
import io
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit
from zipfile import BadZipFile, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
PROJECT_LIMIT = 8_000
MAX_ZIP_BYTES = 100_000_000
RULES = (
    "MASTER-RULES.md",
    "REWRITE-DETECTION.md",
    "CONTEXT-ISOLATION.md",
    "SEMANTIC-LOCK.md",
    "PRONOUN-HANDLING.md",
    "LANGUAGE-ROUTER.md",
    "SOFT-ALTERNATIVE.md",
    "OUTPUT-CONTRACT.md",
)
DIST_RULE = "DISTRIBUTION.md"
LISTING_RESTRICTION = re.compile(
    r"\b(?:free|portable pack|pricing|paid plan|subscription)\b", re.IGNORECASE
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


def text_field(value, limit, label, *, multiline=False):
    require(
        isinstance(value, str) and value.strip() and len(value) <= limit,
        f"{label} must be nonempty and at most {limit} characters",
    )
    require(
        all(not unicodedata.category(c).startswith("C")
            or (multiline and c == "\n") for c in value),
        f"{label} contains unsupported characters",
    )


def validate_manifest(manifest, version):
    require(manifest["$schema"] == SCHEMA, "Incorrect Agent Plugins schema")
    require(manifest["name"] == "polyrefine", "Incorrect plugin name")
    number = r"(?:0|[1-9][0-9]*)"
    identifier = r"[0-9A-Za-z-]+"
    semver = rf"{number}\.{number}\.{number}(?:-({identifier}(?:\.{identifier})*))?(?:\+{identifier}(?:\.{identifier})*)?"
    match = re.fullmatch(semver, version)
    require(
        match and len(version) <= 64
        and all(not (part.isdigit() and len(part) > 1 and part.startswith("0"))
                for part in (match[1] or "").split("."))
        and manifest["version"] == version,
        "Manifest version must match the repository SemVer",
    )
    text_field(manifest["description"], 1_024, "description")
    require(not LISTING_RESTRICTION.search(manifest["description"]), "Restricted listing text")

    extension = manifest["extensions"]["com.openai"]
    require(set(extension) == {"interface"}, "Only listing metadata is allowed")
    listing = extension["interface"]
    require(listing["displayName"] == "PolyRefine Translator", "Incorrect display name")
    require(listing["category"] == "Productivity", "Incorrect listing category")
    for key, limit in (("displayName", 30), ("shortDescription", 30), ("longDescription", 4_000)):
        text_field(listing[key], limit, key, multiline=key == "longDescription")
        require(not LISTING_RESTRICTION.search(listing[key]), f"Restricted text in {key}")

    for key in ("supportURL", "privacyPolicyURL"):
        text_field(listing[key], 2_048, key)
        url = urlsplit(listing[key])
        require(url.scheme == "https" and url.hostname, f"{key} must be an HTTPS URL")

    prompts = listing["defaultPrompt"]
    require(isinstance(prompts, list) and 1 <= len(prompts) <= 3, "Use 1–3 starter prompts")
    normalized = set()
    for prompt in prompts:
        text_field(prompt, 128, "starter prompt")
        require("@" not in prompt and not LISTING_RESTRICTION.search(prompt), "Restricted starter prompt")
        normalized.add(" ".join(unicodedata.normalize("NFKC", prompt).casefold().split()))
    require(len(normalized) == len(prompts), "Duplicate starter prompts")


def make_zip(plugin):
    buffer = io.BytesIO()
    with ZipFile(buffer, "w") as archive:
        for path, data in sorted(plugin.items()):
            member = ZipInfo(f"public-plugin/{path}")
            member.create_system = 3
            member.external_attr = 0o100644 << 16
            archive.writestr(member, data)
    return buffer.getvalue()


def validate_zip(data, plugin, version):
    require(len(data) <= MAX_ZIP_BYTES, "ZIP exceeds 100 MB")
    expected = {f"public-plugin/{path}": contents for path, contents in plugin.items()}
    with ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        require(
            len(names) == len(expected) and set(names) == set(expected),
            "ZIP must contain only the expected files under one public-plugin root",
        )
        require(archive.testzip() is None, "ZIP has a corrupted member")
        manifest = json.loads(archive.read("public-plugin/plugin.json"))
        validate_manifest(manifest, version)
        require(all(archive.read(path) == contents for path, contents in expected.items()),
                "ZIP contents differ from the current skill or listing")


def build_outputs():
    version = read("VERSION").strip()
    manifest = json.loads(read("templates/plugin.json"))
    manifest["version"] = version
    validate_manifest(manifest, version)
    rules = {name: read(f"core/{name}") for name in (*RULES, DIST_RULE)}
    skill = read("templates/SKILL.md")
    require(skill.startswith("---\nname: polyrefine\ndescription: "), "Invalid skill frontmatter")
    require(set(re.findall(r"\(references/([^()]+)\)", skill)) == set(rules),
            "Skill must reference every canonical rule document")

    plugin = {
        "plugin.json": (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode(),
        "skills/polyrefine/SKILL.md": skill.encode(),
        **{f"skills/polyrefine/references/{name}": value.encode() for name, value in rules.items()},
    }

    project = "\n\n".join(rules[name].strip() for name in RULES) + "\n"
    require(len(project) <= PROJECT_LIMIT, f"Project instructions exceed {PROJECT_LIMIT} characters")
    # The priority list and executable rules cover the same decisions as the conflict table.
    compact = "\n".join(
        re.sub(r"^#+\s+", "", line).replace("**", "")
        for line in project.splitlines() if line.strip() and not line.startswith("|")
    ) + "\n"
    pack = {
        "QUICK-START.md": read("templates/QUICK-START.md").encode(),
        "PROJECT-INSTRUCTIONS.md": project.encode(),
        "COMPACT-PROMPT.txt": compact.encode(),
        "TEST-EXAMPLES.md": read("templates/TEST-EXAMPLES.md").encode(),
        "VERSION.md": f"# PolyRefine Translator {version}\n\nUses the same versioned rules as the skills-only distribution.\n".encode(),
    }
    zip_path = f"dist/polyrefine-{version}.zip"
    data = make_zip(plugin)
    validate_zip(data, plugin, version)
    outputs = {zip_path: data}
    for directory, files in (("public-plugin", plugin), ("free-portable-pack", pack), ("dist/portable-pack", pack)):
        outputs.update({f"{directory}/{name}": contents for name, contents in files.items()})
    return version, zip_path, plugin, outputs


def managed_files(root):
    files = set()
    for directory in ("public-plugin", "free-portable-pack", "dist/portable-pack"):
        files.update(p.relative_to(root).as_posix() for p in (root / directory).rglob("*") if p.is_file())
    files.update(p.relative_to(root).as_posix() for p in (root / "dist").glob("polyrefine-*.zip") if p.is_file())
    return files


def materialize(root, outputs, *, check):
    extras = managed_files(root) - outputs.keys()
    if check:
        stale = extras | {
            path for path, data in outputs.items()
            if not (root / path).is_file() or (root / path).read_bytes() != data
        }
        require(not stale, "Stale generated files; run python3 build.py:\n" + "\n".join(sorted(stale)))
        return
    for path in extras:
        (root / path).unlink()
    for path, data in outputs.items():
        destination = root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)


def main():
    parser = argparse.ArgumentParser(description="Build or verify the PolyRefine distributions.")
    parser.add_argument("--check", action="store_true", help="Fail without writing if generated files are stale.")
    args = parser.parse_args()
    try:
        version, zip_path, plugin, outputs = build_outputs()
        materialize(ROOT, outputs, check=args.check)
        validate_zip((ROOT / zip_path).read_bytes(), plugin, version)
    except (BadZipFile, KeyError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"{'Verified' if args.check else 'Built and validated'} PolyRefine {version}: {zip_path}")
    for name in ("PROJECT-INSTRUCTIONS.md", "COMPACT-PROMPT.txt"):
        count = len(outputs[f"free-portable-pack/{name}"].decode())
        print(f"{name}: {count:,} characters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
