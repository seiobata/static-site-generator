import unittest

from htmlnode import HTMLNode


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
