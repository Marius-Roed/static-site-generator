from .htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is missing from parentnode")

        if not self.children:
            raise ValueError(
                "Children is missing from parentnode.\nConsider making it a leaf node if no children are present")

        props = self.props_to_html() if self.props else ""

        output = f"<{self.tag}{props}>"

        for child in self.children:
            output += child.to_html()

        output += f"</{self.tag}>"

        return output
