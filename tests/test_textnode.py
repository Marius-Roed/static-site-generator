import unittest

from src.textnode import TextNode, TextType, text_node_to_html


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXTNODE)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXTNODE)
        self.assertEqual(node, node2)

    def test_two(self):
        node = TextNode("A", "plain")
        node2 = TextNode("A", TextType.PLAIN_TEXTNODE)
        self.assertEqual(node, node2)

    def test_three(self):
        node = TextNode("A", TextType.PLAIN_TEXTNODE)
        node2 = TextNode("a", TextType.PLAIN_TEXTNODE)
        self.assertNotEqual(node, node2)

    def test_four(self):
        plain = TextNode("Some test text", TextType.PLAIN_TEXTNODE)
        bold = TextNode("Some test text", TextType.BOLD_TEXTNODE)
        self.assertNotEqual(plain, bold)

    def test_five(self):
        text = TextNode("Click me", TextType.PLAIN_TEXTNODE)
        link = TextNode("Click me", TextType.LINK_TEXTNODE,
                        "https://google.com")
        self.assertNotEqual(text, link)

    def test_six(self):
        link1 = TextNode("Bootdev", "link", "https://boot.dev/")
        link2 = TextNode("Bootdev", "link", "https://boot.dev/")
        self.assertEqual(link1, link2)


class TextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXTNODE)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE_TEXTNODE,
                        "https://www.boot.dev")
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD_TEXTNODE)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


if __name__ == "__main__":
    unittest.main()
