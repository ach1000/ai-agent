import unittest
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import available_functions


class TestFunctionSchemas(unittest.TestCase):
    def test_available_functions_contains_all_declarations(self):
        """All four function declarations should be present in available_functions"""
        names = {d.name for d in available_functions.function_declarations}
        self.assertEqual(
            names,
            {"get_files_info", "get_file_content", "run_python_file", "write_file"},
        )

    def test_schema_get_files_info_structure(self):
        """get_files_info schema should have the correct name and a 'directory' parameter"""
        self.assertEqual(schema_get_files_info.name, "get_files_info")
        props = schema_get_files_info.parameters.properties
        self.assertIn("directory", props)
        self.assertEqual(props["directory"].type, types.Type.STRING)
        # 'directory' is optional — no required list
        self.assertFalse(schema_get_files_info.parameters.required)

    def test_schema_get_file_content_structure(self):
        """get_file_content schema should require file_path as a STRING"""
        self.assertEqual(schema_get_file_content.name, "get_file_content")
        props = schema_get_file_content.parameters.properties
        self.assertIn("file_path", props)
        self.assertEqual(props["file_path"].type, types.Type.STRING)
        self.assertIn("file_path", schema_get_file_content.parameters.required)

    def test_schema_run_python_file_structure(self):
        """run_python_file schema should require file_path and have an optional args ARRAY"""
        self.assertEqual(schema_run_python_file.name, "run_python_file")
        props = schema_run_python_file.parameters.properties
        self.assertIn("file_path", props)
        self.assertEqual(props["file_path"].type, types.Type.STRING)
        self.assertIn("file_path", schema_run_python_file.parameters.required)
        # args is optional
        self.assertNotIn("args", (schema_run_python_file.parameters.required or []))
        self.assertIn("args", props)
        self.assertEqual(props["args"].type, types.Type.ARRAY)
        self.assertEqual(props["args"].items.type, types.Type.STRING)

    def test_schema_write_file_structure(self):
        """write_file schema should require both file_path and content as STRINGs"""
        self.assertEqual(schema_write_file.name, "write_file")
        props = schema_write_file.parameters.properties
        self.assertIn("file_path", props)
        self.assertIn("content", props)
        self.assertEqual(props["file_path"].type, types.Type.STRING)
        self.assertEqual(props["content"].type, types.Type.STRING)
        required = schema_write_file.parameters.required
        self.assertIn("file_path", required)
        self.assertIn("content", required)

    def test_all_schemas_have_descriptions(self):
        """Every schema and each of its parameters should have a non-empty description"""
        schemas = [
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
        for schema in schemas:
            with self.subTest(schema=schema.name):
                self.assertTrue(schema.description, f"{schema.name} is missing a description")
                for param_name, param in schema.parameters.properties.items():
                    self.assertTrue(
                        param.description,
                        f"{schema.name}.{param_name} is missing a description",
                    )


if __name__ == "__main__":
    unittest.main()
