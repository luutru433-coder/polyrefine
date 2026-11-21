import io
import json
import re
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

import build


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.version, cls.zip_path, cls.plugin, cls.outputs = build.build_outputs()

    def test_pack_has_same_runtime_rules_and_limits(self):
        prefix = "free-portable-pack/"
        project = self.outputs[prefix + "PROJECT-INSTRUCTIONS.md"].decode()
        compact = self.outputs[prefix + "COMPACT-PROMPT.txt"].decode()
        self.assertLess(len(compact), len(project))
        self.assertLessEqual(len(project), build.PROJECT_LIMIT)
        for name in build.RULES:
            rule = build.read(f"core/{name}")
            self.assertIn(rule.strip(), project)
            self.assertEqual(self.plugin[f"skills/polyrefine/references/{name}"], rule.encode())
        for path in self.outputs:
            if path.startswith(prefix):
                self.assertEqual(self.outputs[path], self.outputs[path.replace(prefix, "dist/portable-pack/", 1)])

    def test_zip_rejects_sibling(self):
        data = io.BytesIO(self.outputs[self.zip_path])
        with ZipFile(data, "a") as archive:
            archive.writestr("README.md", "Not part of the plugin")
        with self.assertRaisesRegex(ValueError, "one public-plugin root"):
            build.validate_zip(data.getvalue(), self.plugin, self.version)

    def test_zip_excludes_maintainer_distribution_rules(self):
        self.assertTrue((build.ROOT / "core/DISTRIBUTION.md").is_file())
        with ZipFile(io.BytesIO(self.outputs[self.zip_path])) as archive:
            self.assertNotIn(
                "public-plugin/skills/polyrefine/references/DISTRIBUTION.md",
                archive.namelist(),
            )

    def test_zip_rejects_restricted_text_in_nested_reference(self):
        path = "skills/polyrefine/references/MASTER-RULES.md"
        for text in (b"Available for FrEe.", b"An unPoRtAbLe example."):
            with self.subTest(text=text):
                plugin = self.plugin | {path: text}
                message = f"Restricted text in plugin file: public-plugin/{path}"
                with self.assertRaisesRegex(ValueError, re.escape(message)):
                    build.validate_zip(build.make_zip(plugin), plugin, self.version)

    def test_zip_accepts_free_as_part_of_a_word(self):
        plugin = self.plugin | {"skills/polyrefine/references/MASTER-RULES.md": b"Freedom"}
        build.validate_zip(build.make_zip(plugin), plugin, self.version)

    def test_listing_rejects_excessive_short_description(self):
        manifest = json.loads(self.plugin["plugin.json"])
        manifest["extensions"]["com.openai"]["interface"]["shortDescription"] = "x" * 31
        with self.assertRaisesRegex(ValueError, "shortDescription"):
            build.validate_manifest(manifest, self.version)

    def test_check_detects_stale_files_without_overwriting(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build.materialize(root, self.outputs, check=False)
            build.materialize(root, self.outputs, check=True)
            changed = root / "free-portable-pack/COMPACT-PROMPT.txt"
            changed.write_text("stale", encoding="utf-8")
            obsolete = root / "public-plugin/obsolete.md"
            obsolete.touch()
            with self.assertRaises(ValueError) as context:
                build.materialize(root, self.outputs, check=True)
            self.assertIn(changed.name, str(context.exception))
            self.assertIn(obsolete.name, str(context.exception))
            self.assertEqual(changed.read_text(encoding="utf-8"), "stale")

    def test_acceptance_suite_has_all_cases_and_results(self):
        cases = build.read("tests/TEST-CASES.md")
        results = build.read("tests/EXPECTED-RESULTS.md").split(
            "## Draft target-language candidates", 1
        )[0]
        sections = re.split(r"^## .+ \((\d+)\)$", cases, flags=re.MULTILINE)
        self.assertEqual(sections[1::2], ["10", "10", "8", "8", "8", "6", "6", "4"])
        for count, section in zip(sections[1::2], sections[2::2]):
            self.assertEqual(len(re.findall(r"^\*\*Test (\d+)", section, re.MULTILINE)), int(count))
        expected = [f"{number:02}" for number in range(1, 61)]
        self.assertEqual(sorted(re.findall(r"^\*\*Test (\d+)", cases, re.MULTILINE)), expected)
        self.assertEqual(sorted(re.findall(r"^\| (\d+) \|", results, re.MULTILINE)), expected)
