import unittest

from src.parser import split_nodes_delimiter, extract_images, extract_links, text_to_nodes
from src.textnode import TextType, TextNode


class TestParser(unittest.TestCase):
    def test_split_bold(self):
        node = TextNode("Some **bold** text", "plain")
        split_nodes = split_nodes_delimiter(
            [node], "**", TextType.BOLD_TEXTNODE)
        self.assertListEqual(split_nodes, [
            TextNode("Some ", TextType.PLAIN_TEXTNODE),
            TextNode("bold", TextType.BOLD_TEXTNODE),
            TextNode(" text", TextType.PLAIN_TEXTNODE)
        ])

    def test_double_bold(self):
        node = TextNode(
            "Here is text **and some bolded**, with **some more bolded**", "plain")
        split = split_nodes_delimiter([node], "**", "bold")
        self.assertListEqual(split, [
            TextNode("Here is text ", "plain"),
            TextNode("and some bolded", "bold"),
            TextNode(", with ", "plain"),
            TextNode("some more bolded", "bold")
        ])

    def test_italic_bold(self):
        node = TextNode("_This is skewed_.**And this bold**", "plain")
        splits = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXTNODE)
        splits = split_nodes_delimiter(splits, "**", TextType.BOLD_TEXTNODE)
        self.assertListEqual(splits, [
            TextNode("This is skewed", TextType.ITALIC_TEXTNODE),
            TextNode(".", TextType.PLAIN_TEXTNODE),
            TextNode("And this bold", TextType.BOLD_TEXTNODE)
        ])

    def test_extract_image(self):
        md = "This is text with ![An image](https://i.imgur.com/aKaOqIh.gif)"
        self.assertEqual(extract_images(
            md), [('An image', 'https://i.imgur.com/aKaOqIh.gif')])

    def test_extract_link(self):
        md = "This is text with [a link](https://google.com)"
        self.assertEqual(extract_links(md), [('a link', 'https://google.com')])

    def test_extract_images(self):
        md = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(extract_images(md), [
            ('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),
            ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')
        ])

    def test_extract_links(self):
        md = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(extract_links(md), [
            ('to boot dev', 'https://www.boot.dev'),
            ('to youtube', 'https://www.youtube.com/@bootdotdev')
        ])

    def test_image_link(self):
        md = "This is [a link to youtube](https://www.youtube.com) and we also have ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(extract_links(md), [
            ('a link to youtube', 'https://www.youtube.com')
        ])
        self.assertListEqual(extract_images(md), [
            ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')
        ])

    def test_text_to_plain_node(self):
        text = "This is plain text"
        self.assertListEqual(text_to_nodes(text), [TextNode(
            "This is plain text", "plain")])

    def test_text_with_link(self):
        text = "This text has [a link](https://google.com) inside of it"
        self.assertListEqual(text_to_nodes(text), [
            TextNode("This text has ", "plain"),
            TextNode("a link", "link", "https://google.com"),
            TextNode(" inside of it", "plain")
        ])

    def test_multi_delimiter(self):
        text = "This text is both **bold** and has `inline code` inside of it"
        self.assertListEqual(text_to_nodes(text), [
            TextNode("This text is both ", "plain"),
            TextNode("bold", "bold"),
            TextNode(" and has ", "plain"),
            TextNode("inline code", "code"),
            TextNode(" inside of it", "plain")
        ])

    def test_full_shbang(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(text_to_nodes(text), [
            TextNode("This is ", "plain"),
            TextNode("text", "bold"),
            TextNode(" with an ", "plain"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "plain"),
            TextNode("code block", "code"),
            TextNode(" and an ", "plain"),
            TextNode("obi wan image", "image",
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", "plain"),
            TextNode("link", "link", "https://boot.dev")
        ])


if __name__ == "__main__":
    unittest.main()
