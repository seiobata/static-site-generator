import unittest

from textnode import TextType, TextNode
from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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

# Testing split nodes image function
    def test_split_image(self):
        nodes = [
            TextNode("this has ![an image](https://in.here/)", TextType.NORMAL),
            TextNode(
                "another ![second image](https://second.image) and ![third image](https://third.here)",
                TextType.NORMAL
            )
        ]
        self.assertListEqual(
            split_nodes_image(nodes),
            [
                TextNode("this has ", TextType.NORMAL),
                TextNode("an image", TextType.IMAGE, "https://in.here/"),
                TextNode("another ", TextType.NORMAL),
                TextNode("second image", TextType.IMAGE, "https://second.image"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("third image", TextType.IMAGE, "https://third.here")
            ]
        )

# Testing split nodes link function
    def test_split_link(self):
        node1 = TextNode("no links here", TextType.NORMAL)
        node2 = TextNode("[start link](https://first.half/) with more text", TextType.NORMAL)
        self.assertListEqual(
            split_nodes_link([node1, node2]),
            [
                TextNode("no links here", TextType.NORMAL),
                TextNode("start link", TextType.LINK, "https://first.half/"),
                TextNode(" with more text", TextType.NORMAL)
            ]
        )

# Testing text to textnodes function
    def test_text_to_textnode(self):
        text = "[start link](https://here.link) some** big words** followed by _slanted words_ and last ![nice pic](https://very.nice)"
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("start link", TextType.LINK, "https://here.link"),
                TextNode(" some", TextType.NORMAL),
                TextNode(" big words", TextType.BOLD),
                TextNode(" followed by ", TextType.NORMAL),
                TextNode("slanted words", TextType.ITALIC),
                TextNode(" and last ", TextType.NORMAL),
                TextNode("nice pic", TextType.IMAGE, "https://very.nice"),
            ]
        )

    def test_text_to_textnode_no_normal(self):
        text = "![wow pic](https://very.wow)** more big word**` code here `[lazy url](https://just.testing)"
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("wow pic", TextType.IMAGE, "https://very.wow"),
                TextNode(" more big word", TextType.BOLD),
                TextNode(" code here ", TextType.CODE),
                TextNode("lazy url", TextType.LINK, "https://just.testing"),
            ]
        )


if __name__ == "__main__":
    unittest.main()