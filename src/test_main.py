import unittest

from main import extract_title


class TestMainFunctions(unittest.TestCase):
    def test_extract_title(self):
        md = "# A Basic Title  "
        self.assertEqual(extract_title(md), "A Basic Title")


    def test_extract_title_multi(self):
        md = """
## Not the title we want

Some paragraph content with a # included

# Actual Title  
"""
        self.assertEqual(extract_title(md), "Actual Title")


if __name__ == "__main__":
    unittest.main()