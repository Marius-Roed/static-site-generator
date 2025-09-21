import re
from .textnode import TextNode, TextType


def split_nodes_delimiter(nodes, delimiter, new_type):
    new_nodes = []
    for node in nodes:
        if node.text_type != TextType.PLAIN_TEXTNODE:
            new_nodes.append(node)
            continue
        split = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, unclosed section")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split.append(TextNode(sections[i], TextType.PLAIN_TEXTNODE))
            else:
                split.append(TextNode(sections[i], new_type))
        new_nodes.extend(split)
    return new_nodes


def split_node_to_image(nodes):
    new_nodes = []
    for node in nodes:
        if node.text_type != TextType.PLAIN_TEXTNODE:
            new_nodes.append(node)
            continue
        text = node.text
        images = extract_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            sections = text.split(f"![{image[0]}]({image[1]})")
            if len(sections) != 2:
                raise ValueError(
                    "Invalid markdown, there is an unclosed image")
            if sections[0] != "":
                new_nodes.append(
                    TextNode(sections[0], TextType.PLAIN_TEXTNODE))
            new_nodes.append(
                TextNode(image[0], TextType.IMAGE_TEXTNODE, image[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.PLAIN_TEXTNODE))
    return new_nodes


def split_node_to_link(nodes):
    new_nodes = []
    for node in nodes:
        if node.text_type != TextType.PLAIN_TEXTNODE:
            new_nodes.append(node)
            continue
        text = node.text
        links = extract_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})")
            if len(sections) != 2:
                raise ValueError("Invalid markdown, there is an unclosed link")
            if sections[0] != "":
                new_nodes.append(
                    TextNode(sections[0], TextType.PLAIN_TEXTNODE))
            new_nodes.append(
                TextNode(link[0], TextType.LINK_TEXTNODE, link[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.PLAIN_TEXTNODE))
    return new_nodes


def extract_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def text_to_nodes(text):
    delimiters = {"bold": "**", "italic": "_", "code": "`"}
    nodes = TextNode(text, TextType.PLAIN_TEXTNODE)
    nodes = split_node_to_link([nodes])
    if not isinstance(nodes, list):
        nodes = [nodes]
    nodes = split_node_to_image(nodes)
    if not isinstance(nodes, list):
        nodes = [nodes]
    for text_type, symbol in delimiters.items():
        nodes = split_nodes_delimiter(nodes, symbol, text_type)

    return nodes
