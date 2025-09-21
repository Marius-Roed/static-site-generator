from .textnode import TextNode, text_node_to_html


def main():
    node = TextNode("Bold text", "bold")

    print(text_node_to_html(node).to_html())


if __name__ == "__main__":
    main()
