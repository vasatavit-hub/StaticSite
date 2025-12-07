import unittest

from textnode import *
from node_create import *
from text_to_nodes import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is a bold text node", TextType.BOLD)
        node3 = TextNode("This is different",TextType.TEXT,"www.google.com")
        node4 = TextNode("This is different",TextType.BOLD,"www.google.com")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        html_node = text_node_to_html_node(node)



        self.assertNotEqual(node4, node3)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_create(self):
        text = TextNode("text", TextType.TEXT)
        bold = TextNode("bold", TextType.BOLD)
        italic = TextNode("italic", TextType.ITALIC)
        node = TextNode("text**bold**", TextType.TEXT)
        node2 = TextNode("text_italic_", TextType.TEXT)
        node3 = TextNode("text**bold**text**bold**text", TextType.TEXT)
        test = split_nodes_delimiter(node, "**", TextType.BOLD)
        self.assertEqual(test[0], text)
        self.assertEqual(test[1], bold)
        test = split_nodes_delimiter(node2, "_", TextType.ITALIC)
        self.assertEqual(test[0], text)
        self.assertEqual(test[1], italic)
        test = split_nodes_delimiter(node3, "**", TextType.BOLD)
        self.assertEqual(test[0], text)
        self.assertEqual(test[1], bold)
        self.assertEqual(test[2], text)
        self.assertEqual(test[3], bold)
        self.assertEqual(test[4], text)

    def test_extract(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

        matches = extract_markdown_links(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)



        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        node =  TextNode("obi wan image",TextType.IMAGE,"https://i.imgur.com/fJRm4Vk.jpeg")
        nodes2=[
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ]       
        self.assertListEqual(nodes,nodes2)


    def test_markdown_to_blocks(self):
        md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        with open('src/markdown.txt') as file:
            markdown = file.read()
            blocks = markdown_to_blocks(markdown)
            for block in blocks:
                block_type = block_to_block_type(block)

  

    def test_paragraphs(self):
        print("paragraphs ...")
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
        print("paragraphs OK")
    def test_codeblock(self):
        print("codeblock ...")
        md = """
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        print("codeblock OK")


if __name__ == "__main__":
    unittest.main()
    