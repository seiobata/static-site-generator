import unittest

from textnode import TextType, TextNode
from text_extraction import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links
)


class TestInlineMarkdown(unittest.TestCase):

# Testing split nodes delimiter function
    def test_split_nodes_italics(self):
        node1 = TextNode("This contains *some italics*", TextType.NORMAL)
        node2 = TextNode("another *italics* string but *more*", TextType.NORMAL)
        node3 = TextNode("no italics here", TextType.NORMAL)
        nodes = [node1, node2, node3]
        self.assertListEqual(
            split_nodes_delimiter(nodes, "*", TextType.ITALIC),
            [
                TextNode("This contains ", TextType.NORMAL),
                TextNode("some italics", TextType.ITALIC),
                TextNode("another ", TextType.NORMAL),
                TextNode("italics", TextType.ITALIC),
                TextNode(" string but ", TextType.NORMAL),
                TextNode("more", TextType.ITALIC),
                TextNode("no italics here", TextType.NORMAL)
            ]
        )
    
    def test_split_nodes_bold_and_italic(self):
        node = TextNode("This has **both bold** and *italics*", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This has ", TextType.NORMAL),
                TextNode("both bold", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("italics", TextType.ITALIC)
            ]
        )

# Testing extract markdown images function
    def test_extract_markdown_images(self):
        text = "an image ![an image](https://an.image.here)"
        self.assertEqual(
            extract_markdown_images(text),
            [('an image', 'https://an.image.here')]
        )
    
# Testing extract markdown links function
    def test_extract_markdown_links(self):
        text = "![an image](https:/an.image.here) and [a link](https://a.link.here)"
        self.assertEqual(
            extract_markdown_links(text),
            [('a link', 'https://a.link.here')]
        )


if __name__ == "__main__":
    unittest.main()