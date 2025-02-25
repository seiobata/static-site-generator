import re

from textnode import TextType, TextNode


# takes a complex TextNode and splits it based on TextType
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        new_texts = node.text.split(delimiter)
        extended_nodes = []
        if len(new_texts) % 2 == 0:
            raise ValueError("invalid Markdown syntax, no closing syntax")
        for i, text in enumerate(new_texts):
            if text == "":
                continue
            if i % 2 == 0:
                extended_nodes.append(TextNode(text, TextType.NORMAL))
            else:
                extended_nodes.append(TextNode(text, text_type))
        new_nodes.extend(extended_nodes)
    return new_nodes

# regex pattern says "capture all instances of all text
# between ![ ] and ( ) but not including brackets."
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

# same as above except (?<!!) means "any groups that start
# with ! should be excluded" because those are images
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
