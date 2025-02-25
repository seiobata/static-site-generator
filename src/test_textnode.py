import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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


if __name__ == "__main__":
    unittest.main()