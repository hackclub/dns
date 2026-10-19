import contextlib
import importlib.machinery
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest

from ruamel.yaml import YAML


ROOT = Path(__file__).resolve().parents[1]
LOADER = importlib.machinery.SourceFileLoader("sort_zones", str(ROOT / "bin/sort-zones"))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
sorter = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(sorter)


class SortZonesTests(unittest.TestCase):
    def assert_sort(self, source, expected):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "zone.yaml"
            path.write_bytes(source.encode())
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertFalse(sorter.sort(path, check_only=True))
            self.assertIn("out of order", output.getvalue())
            self.assertEqual(path.read_bytes(), source.encode())
            self.assertFalse(sorter.sort(path))
            self.assertEqual(path.read_bytes(), expected.encode())
            before, after = YAML().load(source), YAML().load(expected)
            self.assertEqual(dict(before), dict(after))
            self.assertEqual(list(after), sorted(before, key=sorter.KEYGEN))
            self.assertTrue(sorter.sort(path, check_only=True))
            self.assertTrue(sorter.sort(path))
            self.assertEqual(path.read_bytes(), expected.encode())

    def test_formatting_preamble_and_comments(self):
        preamble = "# Zone header\n---\n\n"
        z = ('"z": # inline owner\n'
             '  - type: TXT\n'
             '    value: \'quoted value\'  # keep spacing\n'
             '\n')
        a = ('# Owner of a\n\n# More context for a\n'
             'a:\n'
             '  type: TXT\n'
             '  values: ["one", \'two\']\n')
        self.assert_sort(preamble + z + a, preamble + a + z)

    def test_nested_comments_and_multiline_scalars(self):
        z = 'z:\n  type: TXT\n  value: |+\n    text\n    # literal content\n\n'
        a = '# Owner of a\na: {type: A, value: 192.0.2.1}\n'
        self.assert_sort(z + a, a + z)

    def test_crlf_and_unicode(self):
        z = 'z: {type: TXT, value: "café"}\r\n'
        a = '# a owner\r\na: {type: TXT, value: "☃"}\r\n'
        self.assert_sort(z + a, a + z)

    def test_missing_final_newline(self):
        self.assert_sort('z: 1\na: 2', 'a: 2\nz: 1')

    def test_explicit_document_markers(self):
        self.assert_sort(
            '%YAML 1.2\n---\nz: 1\na: 2\n...\n# Footer\n',
            '%YAML 1.2\n---\na: 2\nz: 1\n...\n# Footer\n',
        )

    def test_natural_reversed_domain_and_special_keys(self):
        blocks = {
            '""': '"": {type: A, value: 192.0.2.1}\n',
            'null': 'null: {type: TXT, value: null-key}\n',
            '3': '3: {type: TXT, value: numeric-key}\n',
            'a10': 'a10: {type: TXT, value: ten}\n',
            'a2': 'a2: {type: TXT, value: two}\n',
            'child.parent': 'child.parent: {type: TXT, value: child}\n',
            'parent': 'parent: {type: TXT, value: parent}\n',
        }
        source = ''.join(reversed(list(blocks.values())))
        by_key = {next(iter(YAML().load(block))): block for block in blocks.values()}
        expected = ''.join(by_key[key] for key in sorted(by_key, key=sorter.KEYGEN))
        self.assert_sort(source, expected)

    def test_sorted_empty_and_comment_only_files_are_unchanged(self):
        for source in ('', '# Header only\n', '---\n# Header\na: 1\nz: 2'):
            with self.subTest(source=source), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'zone.yaml'
                path.write_bytes(source.encode())
                self.assertTrue(sorter.sort(path))
                self.assertTrue(sorter.sort(path, check_only=True))
                self.assertEqual(path.read_bytes(), source.encode())

    def test_flow_mapping_is_rejected_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'zone.yaml'
            source = b'{z: 1, a: 2}\n'
            path.write_bytes(source)
            with self.assertRaisesRegex(ValueError, 'top-level block mapping'):
                sorter.sort(path)
            self.assertEqual(path.read_bytes(), source)

    def test_single_record_addition_to_every_real_zone(self):
        # Append one deliberately out-of-order record. The result must be exactly
        # that record plus the existing source, not a reserialization of it.
        addition = '# Regression test owner\n"": {type: TXT, value: regression-test}\n'
        for zone in sorted(ROOT.glob('*.yaml')):
            with self.subTest(zone=zone.name):
                source = zone.read_bytes().decode()
                if not source.endswith('\n'):
                    source += '\n'
                data = YAML().load(source)
                # Use a key that sorts before every existing key, including apex.
                key = ''
                while key in data:
                    key = '!' + key
                record = addition.replace('""', repr(key))
                keys = list(data) + [key]
                expected_keys = sorted(keys, key=sorter.KEYGEN)
                # Existing zones are sorted. Insert at its semantic position,
                # using the parser's source location rather than rewriting YAML.
                position = expected_keys.index(key)
                lines = source.splitlines(keepends=True)
                if position < len(data):
                    line = data.lc.key(expected_keys[position + 1])[0]
                else:
                    line = len(lines)
                # Avoid separating the fixed header or comments from a record.
                if position > 0:
                    cursor = line - 1
                    while cursor >= 0:
                        if lines[cursor].startswith('#'):
                            line = cursor
                        elif lines[cursor].strip():
                            break
                        cursor -= 1
                expected = ''.join(lines[:line]) + record + ''.join(lines[line:])
                self.assert_sort(source + record, expected)


if __name__ == '__main__':
    unittest.main()
