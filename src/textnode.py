from .leafnode import LeafNode
from enum import Enum


class TextType(Enum):
    PLAIN_TEXTNODE = "plain"
    BOLD_TEXTNODE = "bold"
    ITALIC_TEXTNODE = "italic"
    CODE_TEXTNODE = "code"
    LINK_TEXTNODE = "link"
    IMAGE_TEXTNODE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, o):
        if not isinstance(o, TextNode):
            return False
        return (self.text_type == o.text_type and self.text == o.text and self.url == o.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html(node):
    ntype = node.text_type
    match(ntype):
        case TextType.PLAIN_TEXTNODE:
            return LeafNode(None, node.text)
        case TextType.BOLD_TEXTNODE:
            return LeafNode("b", node.text)
        case TextType.ITALIC_TEXTNODE:
            return LeafNode("i", node.text)
        case TextType.CODE_TEXTNODE:
            return LeafNode("pre", node.text)
        case TextType.LINK_TEXTNODE:
            return LeafNode("a", node.text, {"href": node.url})
        case TextType.IMAGE_TEXTNODE:
            return LeafNode("img", "", {"src": node.url, "alt": node.text})
        case _:
            raise ValueError(f"Invalid type error: {node.text_type}")
