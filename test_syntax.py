"""Vérification légère de la syntaxe du fichier principal."""
import pathlib
import py_compile
import unittest


ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT / "Pandoraga.py"


class SyntaxTests(unittest.TestCase):
    def test_main_file_compiles(self):
        self.assertTrue(SOURCE.is_file(), "Pandoraga.py est absent")
        py_compile.compile(str(SOURCE), doraise=True)


if __name__ == "__main__":
    unittest.main()
