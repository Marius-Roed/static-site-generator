import unittest

from src.htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode("div", "Hello World!", None, {
                        "class": "greeting", "href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(),
                         ' class="greeting" href="https://boot.dev"')

    def test_values(self):
        node = HTMLNode("div", "Let me read")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Let me read")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode("p", "What a strange world",
                        None, {"class": "primary"})
        self.assertEqual(node.__repr__(
        ), 'HTMLNode("p", "What a strange world", None, {\'class\': \'primary\'})')


if __name__ == "__main__":
    unittest.main()
