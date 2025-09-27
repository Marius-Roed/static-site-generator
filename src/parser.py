import re
from .textnode import TextNode, TextType, text_node_to_html
from .block import get_block_type
from .parentnode import ParentNode


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
    nodes = [TextNode(text, TextType.PLAIN_TEXTNODE)]
    nodes = split_node_to_link(nodes)
    nodes = split_node_to_image(nodes)
    for text_type, symbol in delimiters.items():
        nodes = split_nodes_delimiter(nodes, symbol, text_type)

    return nodes


def markdown_to_blocks(text):
    blocks = []
    sections = text.split("\n\n")
    for block in sections:
        block = block.strip()
        if block != "":
            blocks.append(block)
    return blocks


def get_heading_tag(text):
    m = re.match(r"^\s?#{1,6}", text)
    if not m:
        return 'p'
    return 'h' + str(len(m[0]))


def text_to_children(text, text_type=None):
    nodes = []
    match(text_type):
        case "heading":
            text = " ".join(text.split("\n"))
            nodes.append(ParentNode(
                get_heading_tag(text), text_to_nodes(text)))
        case "quote":
            text = text[1:]
            text = " ".join(text.split("\n"))
            nodes.append(ParentNode('blockquote', text_to_nodes(text)))
        case "ordered_list" | "unordered_list":
            items = []
            li = text.split("\n")
            for item in li:
                item = item[2:]
                print(item)
                items.append(ParentNode('li', text_to_nodes(item)))

            tag = 'ol' if text_type == "ordered_list" else 'ul'
            nodes.append(ParentNode(tag, items))
        case "code":
            nodes.append(ParentNode(
                'code', [TextNode(text.replace("```", ""), 'code')]))
        case _:
            nodes.append(ParentNode('p', text_to_nodes(text)))

    return nodes


def markdown_to_html(md):
    nodes = []
    output = ""
    blocks = markdown_to_blocks(md)
    for block in blocks:
        block_type = get_block_type(block)
        children = text_to_children(block, block_type)
        nodes.extend(children)

    for node in nodes:
        if isinstance(node, TextNode):
            output += text_node_to_html(node)
            continue
        output += node.to_html()

    return output
