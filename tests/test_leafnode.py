import unittest

from src.leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_to_hmtl(self):
        node = LeafNode("p", "This is a text node")
        self.assertEqual(node.to_html(), "<p>This is a text node</p>")

    def test_values(self):
        node = LeafNode("a", "link text", {"href": "#"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "link text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {'href': '#'})

    def test_props_to_str(self):
        node = LeafNode("span", "underline me", {"class": "underline"})
        self.assertEqual(node.props_to_html(), " class=\"underline\"")

    def test_val_err(self):
        node = LeafNode("div", None, {"class": "card"})
        self.assertRaises(ValueError, lambda: node.to_html())

    def test_empty_str(self):
        node = LeafNode("p", "", {})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_empty_props(self):
        node = LeafNode("p", "This is my very awesome text", {})
        self.assertEqual(node.to_html(), "<p>This is my very awesome text</p>")


if __name__ == "__main__":
    unittest.main()
