import unittest

from block_markdown import (
    BlockType,
    markdown_to_blocks,
    block_to_blocktype,
)


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

# Testing block to blocktype function
    def test_block_to_blocktype(self):
        text1 = "## Some heading"
        self.assertEqual(block_to_blocktype(text1), BlockType.HEADING)

        text2 = "```A block of code```"
        self.assertEqual(block_to_blocktype(text2), BlockType.CODE)

        text3 = "> Some quote\n>\n> containing more\n> than one line"
        self.assertEqual(block_to_blocktype(text3), BlockType.QUOTE)

        text4 = "1. ordered list one\n2. and two\n3. and three"
        self.assertEqual(block_to_blocktype(text4), BlockType.ORLIST)

        text5 = "- something unordered\n- another line"
        self.assertEqual(block_to_blocktype(text5), BlockType.UNLIST)


if __name__ == "__main__":
    unittest.main()