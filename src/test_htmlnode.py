import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("<p>", "Testing HTML node", None, None)
        node2 = HTMLNode("<p>", "Testing HTML node")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("<a>", "Providing some link", None, {"href": "https://google.com/"})
        node2 = HTMLNode("<a>", "Providing some link", None, '"href": "https://google.com/"')
        self.assertNotEqual(node, node2)
    
    def test_props_to_html(self):
        node = HTMLNode(
            "<a>", 
            "Test props to html method", 
            None, 
            {"href": "https://github.com/seiobata/", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), 
            ' href="https://github.com/seiobata/" target="_blank"'
        )
    
    def test_repr(self):
        node = HTMLNode("<p>", "Add some text here", None, {"href": "https://google.com"})
        self.assertEqual(
            "HTMLNode(<p>, Add some text here, None, {'href': 'https://google.com'})", repr(node)
        )

# Testing LeafNode
    def test_to_html(self):
        node = LeafNode("a", "Click Me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click Me!</a>')

    def test_to_html_no_child(self):
        node = LeafNode("p", "Just some string")
        self.assertEqual(node.to_html(), "<p>Just some string</p>")

# Testing ParentNode
    def test_parent_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("i", "Italic text"),
                LeafNode(None, "normal text"),
                LeafNode("a", "inner link", {"href": "https://www.google.com"}),
            ],
            {"target": "_blank"}
        )
        self.assertEqual(
            node.to_html(),
            '<p target="_blank"><i>Italic text</i>normal text<a href="https://www.google.com">inner link</a></p>'
        )
    def test_nested_parent(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "h1",
                    [
                        LeafNode("img", "some image", {"src": "url/of/image.jpg", "alt": "image description"})
                    ]
                ),
                ParentNode(
                    "ol",
                    [
                        LeafNode("li", "item 1"),
                        LeafNode("li", "item 2"),
                    ]
                ),
            ]
        )
        self.assertEqual(
            node.to_html(), 
            '<p><h1><img src="url/of/image.jpg" alt="image description">some image</img></h1><ol><li>item 1</li><li>item 2</li></ol></p>'
        )


if __name__ == "__main__":
    unittest.main()