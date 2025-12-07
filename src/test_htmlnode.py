import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p","Hello World",None,{
                "href": "https://www.google.com",
                "target": "_blank", 
        })
        node2 = LeafNode("p","Hello World!",{
                "href": "https://www.google.com",
                "target": "_blank",
                "href": "https://www.google.com",
                "target": "_blank", 
        })
        node3 = HTMLNode("p","Hello World",None,{
                "a": "A",
                "b": "B",
                "c": "C",
                "d": "?", 
        })
        node4 = HTMLNode()
        self.assertEqual(node2.to_html(),"<p>Hello World!</p>")


    def test_parent_child(self):
        ch_n0 = LeafNode("b","bold")
        ch_n1 = LeafNode("","normal")
        ch_n2 = LeafNode("i","italic")
        p_n0 = ParentNode("p",ch_n0)
        p_n1 = ParentNode("h",[ch_n1,ch_n2])
        p_n2 = ParentNode("html",[p_n0,p_n1])


if __name__ == "__main__":
    unittest.main()
    