class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self, props):
        if not props:
            return ""
        return " ".join([f'{key}="{value}"' for key, value in props.items()])

    def __repr__(self):
        return f"{self.__class__.__name__}(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag is None:
            if self.value is None:
                raise ValueError("LeafNode must have either a tag or a value")
            return str(self.value)
        
        props_str = self.props_to_html(self.props)
        if props_str:
            props_str = " " + props_str
        
        if self.value is None:
            return f"<{self.tag}{props_str}>"
        else:
            return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not tag:
            raise ValueError("ParentNode must have a tag")
        if not children:
            raise ValueError("ParentNode must have children")
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        props_str = self.props_to_html(self.props)
        if props_str:
            props_str = " " + props_str
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"

if __name__ == "__main__":
    # Test props_to_html
    print("Testing props_to_html:")
    node = HTMLNode()
    props = {
        "href": "https://www.google.com",
        "target": "_blank",
        "class": "primary"
    }
    print(f"Props HTML: {node.props_to_html(props)}")
    
    # Test LeafNode
    print("\nTesting LeafNode:")
    # Test 1: Basic paragraph
    leaf1 = LeafNode("p", "This is a paragraph of text.")
    print(f"Leaf1 repr: {leaf1}")
    print(f"Leaf1 HTML: {leaf1.to_html()}")
    
    # Test 2: Link with props
    leaf2 = LeafNode(
        "a",
        "Click me!",
        props={"href": "https://www.google.com"}
    )
    print(f"\nLeaf2 repr: {leaf2}")
    print(f"Leaf2 HTML: {leaf2.to_html()}")
    
    # Test 3: Image (self-closing tag)
    leaf3 = LeafNode(
        "img",
        None,
        props={"src": "test.png", "alt": "Test image"}
    )
    print(f"\nLeaf3 repr: {leaf3}")
    print(f"Leaf3 HTML: {leaf3.to_html()}")
    
    # Test 4: Just text
    leaf4 = LeafNode(None, "Hello, world!")
    print(f"\nLeaf4 repr: {leaf4}")
    print(f"Leaf4 HTML: {leaf4.to_html()}")

    # Test ParentNode
    print("\nTesting ParentNode:")
    # Create some leaf nodes
    leaf1 = LeafNode("p", "First paragraph")
    leaf2 = LeafNode("p", "Second paragraph")
    
    # Create a parent node containing these leaf nodes
    parent = ParentNode(
        "div",
        [leaf1, leaf2],
        props={"class": "container"}
    )
    print(f"Parent repr: {parent}")
    print(f"Parent HTML: {parent.to_html()}")
    
    # Test nested structure
    nested = ParentNode(
        "div",
        [
            LeafNode("h1", "Title"),
            ParentNode(
                "section",
                [
                    LeafNode("p", "Section content"),
                    LeafNode("a", "Learn more", props={"href": "#"})
                ]
            )
        ]
    )
    print(f"\nNested structure repr: {nested}")
    print(f"Nested structure HTML: {nested.to_html()}")

