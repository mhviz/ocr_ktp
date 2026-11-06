import unittest

from services.ocr import DocumentError, KTP_FIELDS, validate_extraction


class ExtractionValidationTests(unittest.TestCase):
    def test_returns_all_fields_and_ignores_unknown_fields(self):
        result = validate_extraction('{"nik":"001234","nama":"Siti","unexpected":"value"}')
        self.assertEqual(result["nik"], "001234")
        self.assertEqual(result["nama"], "Siti")
        self.assertEqual(result["provinsi"], "")
        self.assertEqual(len(result), len(KTP_FIELDS))

    def test_accepts_markdown_json_fence(self):
        result = validate_extraction('```json\n{"nama":"Siti"}\n```')
        self.assertEqual(result["nama"], "Siti")

    def test_rejects_non_object_and_non_string_values(self):
        with self.assertRaises(DocumentError):
            validate_extraction('["not", "an object"]')
        with self.assertRaises(DocumentError):
            validate_extraction('{"nik":123}')

    def test_rejects_invalid_json(self):
        with self.assertRaises(DocumentError):
            validate_extraction("not JSON")


if __name__ == "__main__":
    unittest.main()
