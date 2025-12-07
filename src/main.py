from textnode import *
from static_to_public import *
from text_to_nodes import *
from generate_page import generate_pages_recursively

static_to_public()

generate_pages_recursively("content","template.html","public")

