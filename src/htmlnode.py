class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not isinstance(self.props, object):
            raise TypeError("props should be of type object")
        if not self.props:
            return ""
        attrs = ""
        for key, val in self.props.items():
            attrs = attrs + f" {key}=\"{val}\""

        return attrs

    def __repr__(self):
        return f"HTMLNode(\"{self.tag}\", \"{self.value}\", {self.children}, {self.props})"
