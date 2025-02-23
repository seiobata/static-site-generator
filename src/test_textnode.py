import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("Another text node", TextType.ITALIC, None)
        node2 = TextNode("Another text node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("Some text node", TextType.NORMAL)
        node2 = TextNode("Some text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_not_eq2(self):
        node = TextNode("One more text node", TextType.CODE)
        node2 = TextNode("one more text node", TextType.CODE)
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("Test repr method", TextType.NORMAL, "https://github.com/seiobata/")
        self.assertEqual(
            "TextNode(Test repr method, normal, https://github.com/seiobata/)", repr(node)
        )

# Testing textnode to htmlnode converter
    def test_text_to_html(self):
        node = TextNode("Some bold text", TextType.BOLD)
        self.assertEqual(repr(text_node_to_html_node(node)), 'LeafNode(b, Some bold text, None)')

    def test_text_to_html_image(self):
        node = TextNode("This should be alt text", TextType.IMAGE, "a/url/image.jpg")
        self.assertEqual(
            text_node_to_html_node(node).to_html(),
            '<img src="a/url/image.jpg" alt="This should be alt text"></img>'
        )
    
    def test_text_to_html_link(self):
        node = TextNode("A simple link", TextType.LINK, "https://somewhere-fake.dontclick")
        self.assertEqual(
            text_node_to_html_node(node).to_html(),
            '<a href="https://somewhere-fake.dontclick">A simple link</a>'
        )

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


if __name__ == "__main__":
    unittest.main()