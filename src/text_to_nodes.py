from textnode import *
from node_create import *
from htmlnode import *
import re

def text_to_textnodes(text):
    b = False
    i = False
    c = False

    if "**" in text:
        b = True
    if "_" in text:
        i = True
    if "`" in text:
        c = True

    input = [TextNode(text,TextType.TEXT)]
    if b:
        input = split_nodes_delimiter(input, "**", TextType.BOLD)
    if i:
        input = split_nodes_delimiter(input, "_", TextType.ITALIC)
    if c:
        input = split_nodes_delimiter(input, "`", TextType.CODE)
    
    input = split_nodes_image(input)
    input = split_nodes_link(input)

    return input

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        msg = ""
        lines = block.split("\n")
        for line in lines:
            line = line.strip()
            if line != "":
                msg += line + "\n"
        result.extend([msg[:-1]])
    return result

class BlockType(Enum):
    PAR ="paragraph"
    HEAD ="header"
    CODE ="code"
    QUOTE ="quote"
    U_LIST = "unordered_list"
    O_LIST = "ordered_list"

def block_to_block_type(block):
    #Header --> ###### 
    n = 0
    for i in range (0,min(len(block),8)):
        if block[i]!="#":
            n = i
            break
    if n > 0 and n <7:
        if block[n]== " ":
            return BlockType.HEAD

    #Code --> ```
    if block[0:3]=="```" and block[-3:] == "```":
        return BlockType.CODE
    #Quote --> \n>
    #U_List --> \n -
    #O_List --> \n 1.
    lines = block.split("\n")
    Quote = True
    U_List= True
    O_List= True
    n = 1
    for line in lines:
        if len(line)==0:
            Quote = False
            U_List= False
            O_List= False
            break
        if line[0] != ">":
            Quote = False
        if line[0] != "-" or line[1] != " ":
            U_List = False

        num_str = str(n)
        prefix = f"{num_str}. "
        if not line.startswith(prefix):
            O_List = False
            break
        n += 1
        
    if Quote:
        return BlockType.QUOTE
    if U_List:
        return BlockType.U_LIST
    if O_List:
        return BlockType.O_LIST
    
    return BlockType.PAR

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        if len(block)==0 or block == None:
            continue
        block_type = block_to_block_type(block)
        tag1, tag2 = block_type_tags(block_type,block)
        nodes.extend([block_to_nested_nodes(block,tag1,tag2)])
    parent = ParentNode("div",nodes)
    return parent

def block_to_nested_nodes(block,tag1,tag2=None):
    block = strip_tags(block)
    block = block.strip()
    if tag1=="li":
        return block_to_nested_nodes2(block,tag1,tag2)
    elif tag1=="code":
        return block_to_nested_nodes3(block,tag1,tag2)
    return block_to_nested_nodes1(block,tag1)

def block_to_nested_nodes1(block,tag1):
    TextChildren = text_to_textnodes(block.replace("\n"," "))
    HTMLChildren = []
    for child in TextChildren:
        HTMLChildren.extend([text_node_to_html_node(child)])
    
    return ParentNode(tag1, HTMLChildren)


def block_to_nested_nodes2(block,tag1,tag2):
    Lines = block.split("\n")
    parents = []
    for line in Lines:
        TextChildren = text_to_textnodes(line)
        HTMLChildren = []
        for child in TextChildren:
            HTMLChildren.extend([text_node_to_html_node(child)])
        
        parents.extend([ParentNode(tag1, HTMLChildren)])
    
    return ParentNode(tag2,parents)

def block_to_nested_nodes3(block,tag1,tag2):
    child = LeafNode(tag1,block[4:-3])
    return ParentNode(tag2,child)

def block_type_tags(block_type,block):
    tag1=None
    tag2=None
    match block_type:
        case BlockType.PAR:
            tag1 = "p"
        case BlockType.CODE:
            tag2="pre"
            tag1="code"
        case BlockType.QUOTE:
            tag1="blockquote"
        case BlockType.U_LIST:
            tag2="ul"
            tag1="li"
        case BlockType.O_LIST:
            tag2="ol"
            tag1="li"
        case BlockType.HEAD:
            n=0
            while block[n]=="#":
                n +=1
            tag1=f"h{n}"
    return tag1,tag2

def strip_tags(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PAR:
            return block
        case BlockType.CODE:
            return block
        case BlockType.QUOTE:
            result = block.replace("\n>","\n")
            return result[2:]
        case BlockType.U_LIST:
            result = block.replace("\n- ","\n")
            return result[1:]
        case BlockType.O_LIST:
            n = 1
            result = ""
            lines = block.split("\n")
            for line in lines:
                num_str = str(n)
                prefix = f"{num_str}. "
                result += line[len(prefix):]+"\n"
            return result[:-1]

        case BlockType.HEAD:
            n=0
            while block[n]=="#":
                n +=1
            return block[n:]

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        if len(block)==0:
            continue
        block_type = block_to_block_type(block)
        tag1, tag2 = block_type_tags(block_type,block)
        if tag1 == "h1":
            result = block_to_nested_nodes(block,tag1,tag2)
            return result.children[0].value
    raise Exception("h1 title missing!")