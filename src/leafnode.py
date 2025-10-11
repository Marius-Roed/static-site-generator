from .htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value and self.tag == "img":
            return f"<{self.tag}{self.props_to_html()} />"
        elif not self.value:
            raise ValueError("Value is missing in leafnode")

        if not self.tag:
            return self.value

        if self.tag == "li":
            print(self)
            self.value = self.value.strip()
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
