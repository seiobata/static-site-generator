import unittest

from block_markdown import (
    BlockType,
    markdown_to_blocks,
    block_to_blocktype,
    markdown_to_html_node,
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

# Testing markdown to html function
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        )


    def test_heading(self):
        md = """
## this is an h2 heading

some paragraph in the middle

# another h1 heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>this is an h2 heading</h2><p>some paragraph in the middle</p><h1>another h1 heading</h1></div>"
        )


    def test_quote(self):
        md = """
> some multi line
> blockquote with

a paragraph too
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>some multi line blockquote with</blockquote><p>a paragraph too</p></div>"
        )


    def test_multi_list(self):
        md = """
1. one and
2. two and
3. buckle my shoe

- roses are red
- violets are blue
- this is item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>one and</li><li>two and</li><li>buckle my shoe</li></ol><ul><li>roses are red</li><li>violets are blue</li><li>this is item 3</li></ul></div>"
        )


if __name__ == "__main__":
    unittest.main()