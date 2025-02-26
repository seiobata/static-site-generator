import unittest

from block_markdown import markdown_to_blocks


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
        )

    def test_excessive_newlines(self):
        md ="""

\n\n

- We add text
- Not a ton

# Some heading



## Another heading


"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "- We add text\n- Not a ton",
                "# Some heading",
                "## Another heading",
            ]
        )


if __name__ == "__main__":
    unittest.main()