import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import schema  # noqa: E402

BASE = "https://goodcodereview.com"
SITE = Path(__file__).resolve().parent.parent / "site"


class SchemaTest(unittest.TestCase):
	def setUp(self):
		self.schema = schema.json_schema(BASE)
		self.data = json.loads((SITE / "cards.json").read_text())

	def test_built_files_match_the_schema(self):
		for name in ("cards.json", "cards-drafts.json"):
			data = json.loads((SITE / name).read_text())
			self.assertEqual(schema.check(self.schema, data), [], name)

	def test_a_missing_key_fails(self):
		del self.data["cards"][0]["rule"]
		self.assertIn("missing 'rule'", " ".join(schema.check(self.schema, self.data)))

	def test_a_value_outside_the_enum_fails(self):
		self.data["cards"][0]["severity"] = "urgent"
		self.assertTrue(schema.check(self.schema, self.data))

	def test_an_unknown_key_fails(self):
		self.data["cards"][0]["extra"] = 1
		self.assertIn("unexpected 'extra'", " ".join(schema.check(self.schema, self.data)))

	def test_pass_is_a_json_key_not_pass_underscore(self):
		self.assertIn("pass", self.data["cards"][0])
		self.assertNotIn("pass_", self.data["cards"][0])


if __name__ == "__main__":
	unittest.main()
