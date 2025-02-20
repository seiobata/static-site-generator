import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()