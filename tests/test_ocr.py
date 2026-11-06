import io
import unittest

from PIL import Image

from services.ocr import (
    DocumentError,
    KTP_FIELDS,
    MAX_UPLOAD_BYTES,
    prepare_document_image,
    validate_extraction,
)


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


class UploadValidationTests(unittest.TestCase):
    def test_rejects_empty_and_oversized_uploads(self):
        with self.assertRaises(DocumentError):
            prepare_document_image("empty.png", b"")
        with self.assertRaises(DocumentError):
            prepare_document_image("large.png", b"x" * (MAX_UPLOAD_BYTES + 1))

    def test_accepts_image_and_returns_jpeg(self):
        source = Image.new("RGB", (40, 30), color="white")
        buffer = io.BytesIO()
        source.save(buffer, format="PNG")
        image_bytes, preview = prepare_document_image("sample.png", buffer.getvalue())
        self.assertTrue(image_bytes.startswith(b"\xff\xd8\xff"))
        self.assertEqual(preview.size, (40, 30))

    def test_rejects_unsupported_or_invalid_image(self):
        with self.assertRaises(DocumentError):
            prepare_document_image("bad.jpg", b"not an image")


if __name__ == "__main__":
    unittest.main()
