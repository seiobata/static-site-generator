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
            raise ValueError("invalid Markdown syntax: no closing syntax")
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

# like split_nodes_delimiter but for images
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        first_half, second_half = node.text.split(f"![{images[0][0]}]({images[0][1]})", 1)
        extended_nodes = []
        if first_half.strip():
            extended_nodes.append(TextNode(first_half, TextType.NORMAL))
        extended_nodes.append(TextNode(images[0][0], TextType.IMAGE, images[0][1]))
        if second_half.strip():
            extended_nodes.extend(split_nodes_image([TextNode(second_half, TextType.NORMAL)]))
        new_nodes.extend(extended_nodes)
    return new_nodes

# almost identical to split_nodes_image; maybe worth sharing code
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        link = extract_markdown_links(node.text)
        if len(link) == 0:
            new_nodes.append(node)
            continue
        first_half, second_half = node.text.split(f"[{link[0][0]}]({link[0][1]})", 1)
        extended_nodes = []
        if first_half.strip():
            extended_nodes.append(TextNode(first_half, TextType.NORMAL))
        extended_nodes.append(TextNode(link[0][0], TextType.LINK, link[0][1]))
        if second_half.strip():
            extended_nodes.extend(split_nodes_link([TextNode(second_half, TextType.NORMAL)]))
        new_nodes.extend(extended_nodes)
    return new_nodes
