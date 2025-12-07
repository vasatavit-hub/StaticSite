from text_to_nodes import markdown_to_html_node, extract_title
import os

def generate_page(from_path, template_path, dest_path):
    #Read from from_path
    with open(from_path) as file:
        markdown = file.read()
    print(f"Reading form {from_path}")
    #Read from template_path
    with open(template_path) as file2:
        template = file2.read()
    print(f"Reading from {template_path}")
    #Transform from_path to html
    print(f"Creating HTML Code from {from_path}")
    content = markdown_to_html_node(markdown)
    #Extract h1 from from_path
    title = extract_title(markdown)
    #Replace {{ Title }}
    template = template.replace('{{ Title }}',title)
    #Replace {{ Content }}
    print(f"Inserting HTML Code to template")
    template = template.replace('{{ Content }}',content.to_html())
    #Check if dest_path exist
    #Create dir if necessary
    dir_path =os.path.dirname(dest_path)
    if dir_path != "":
        os.makedirs(dir_path, exist_ok=True)
    #Create new html at dest_path
    print(f"Creating {dest_path}")
    with open(dest_path,"w") as file3:
        file3.write(template)

def generate_pages_recursively(source,template,destination):
    files = os.listdir(source)
    print(f"files {files}")
    for file in files:
        path = os.path.join(source,file)
        dest = os.path.join(destination,file)
        if os.path.isfile(path):
            dest = dest.replace(".md",".html")
            generate_page(path, template, dest)
        else:
            generate_pages_recursively(path,template,dest)