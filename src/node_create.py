from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    #If old_nodes is a list ...
    if isinstance(old_nodes,list): 
        check = False
        #Check if delimiter in the list
        for node in old_nodes:      
            if delimiter in node.text:
                check = True
        if check == False:
            return old_nodes
        
        #Split nodes by delimiter as long as delimiter remains. Odd are TEXT, even are text_type, last is TEXT
        for node in old_nodes:
            if node.text_type != TextType.TEXT:
                result.extend([node])
            else:
                l2=node.text
                while delimiter in l2:
                    l1,l2=l2.split(delimiter,1)
                    if len(l1)>0:
                        result.extend([TextNode(l1,TextType.TEXT)])
                    l1,l2=l2.split(delimiter,1)
                    result.extend([TextNode(l1,text_type)])
                if len(l2)>0:
                    result.extend([TextNode(l2,TextType.TEXT)])
        
        return result


    else:                  
        #If old_nodes is not a list ..
        #Check if delimiter in the list
        if delimiter not in old_nodes.text:
            return old_nodes

        if old_nodes.text_type != TextType.TEXT:
                return old_nodes

        l2=old_nodes.text
        #Split node by delimiter as long as delimiter remains. Odd are TEXT, even are text_type, last is TEXT
        while delimiter in l2:
            l1,l2=l2.split(delimiter,1)
            if len(l1)>0:
                result.extend([TextNode(l1,TextType.TEXT)])
            l1,l2=l2.split(delimiter,1)
            result.extend([TextNode(l1,text_type)])
        if len(l2)>0:
            result.extend([TextNode(l2,TextType.TEXT)])

        return result

def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)",text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)",text)
    return matches

def split_nodes_image(old_nodes):
    result = []
    #If old_nodes is a list ...
    if not isinstance(old_nodes,list):
        old_nodes = [old_nodes]

    for node in old_nodes:
        images = extract_markdown_images(node.text)
        l2 = node.text
        for image in images:
            l1,l2=l2.split(f"![{image[0]}]({image[1]})",1)
            if len(l1)>0 or l1!=None:
                result.extend([TextNode(l1,node.text_type)])
            result.extend([TextNode(image[0],TextType.IMAGE,image[1])])
        if len(l2)>0 or l2!=None:
            result.extend([TextNode(l2,node.text_type,node.url)])
    return result



def split_nodes_link(old_nodes):
    result = []
    #If old_nodes is a list ...
    if not isinstance(old_nodes,list):
        old_nodes = [old_nodes]

    for node in old_nodes:
        links = extract_markdown_links(node.text)
        l2 = node.text
        for link in links:
            l1,l2=l2.split(f"[{link[0]}]({link[1]})",1)
            if len(l1)>0:
                result.extend([TextNode(l1,node.text_type)])
            result.extend([TextNode(link[0],TextType.LINK,link[1])])
        if len(l2)>0:
            result.extend([TextNode(l2,node.text_type,node.url)])
    return result