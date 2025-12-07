class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.props = props
        if not isinstance(children,list):
            self.children = [children]
        else:
            self.children = children
    
    def to_html(self):
        return

    def props_to_html(self):
        if self.props == None:
            return ""
        if self.props =="":
            return ""
        result = ""
        for text in self.props:
            result += text+"="+ '"'+self.props[text]+'"' + " "
        
        return result[0:-1]

    def __repr__(self):
        return f"tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag,value,None,props)
    
    def to_html(self):
        if self.tag == None or self.tag == "":
            return self.value
        if self.tag == "a":
            return '<a href="'+self.props["href"]+'">'+self.value+'</a>'
        if self.tag == "img":
            return '<img src="'+self.props["src"]+'" alt="'+self.props["alt"]+'">'  
        return "<"+self.tag+">"+self.value+"</"+self.tag+">"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag,None,children,props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("All parent nodes must have a tag")
    
        if self.children == None:
            raise ValueError("All parent nodes must have children")

        result = "<"+self.tag+">"
        for child in self.children:
            result += child.to_html()

        result += "</"+self.tag+">"
        return result
        

