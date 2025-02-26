import re

from textnode import TextType, TextNode


def text_to_textnodes(text):
    node = [TextNode(text, TextType.NORMAL)]
    list_of_nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
    list_of_nodes = split_nodes_delimiter(list_of_nodes, "_", TextType.ITALIC)
    list_of_nodes = split_nodes_delimiter(list_of_nodes, "`", TextType.CODE)
    list_of_nodes = split_nodes_link(list_of_nodes)
    list_of_nodes = split_nodes_image(list_of_nodes)
    return list_of_nodes

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

# like split_nodes_delimiter but for links
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        try:
            first_half, second_half = node.text.split(f"[{links[0][0]}]({links[0][1]})", 1)
        except ValueError:
            print("invalid Markdown syntax: link not closed; returning as-is")
            new_nodes.append(node)
            continue
        extended_nodes = []
        if first_half.strip(): # statement is true if first_half contains any text
            extended_nodes.append(TextNode(first_half, TextType.NORMAL))
        extended_nodes.append(TextNode(links[0][0], TextType.LINK, links[0][1]))
        if second_half.strip():
            extended_nodes.extend(split_nodes_link([TextNode(second_half, TextType.NORMAL)]))
        new_nodes.extend(extended_nodes)
    return new_nodes

# almost identical to split_nodes_link but for images; maybe worth sharing code
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
        try:
            first_half, second_half = node.text.split(f"![{images[0][0]}]({images[0][1]})", 1)
        except ValueError:
            print("invalid Markdown syntax: image not closed; returning as-is")
            new_nodes.append(node)
            continue
        extended_nodes = []
        if first_half.strip():
            extended_nodes.append(TextNode(first_half, TextType.NORMAL))
        extended_nodes.append(TextNode(images[0][0], TextType.IMAGE, images[0][1]))
        if second_half.strip():
            extended_nodes.extend(split_nodes_image([TextNode(second_half, TextType.NORMAL)]))
        new_nodes.extend(extended_nodes)
    return new_nodes
