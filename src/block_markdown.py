from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes
from htmlnode import ParentNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNLIST = "unordered list"
    ORLIST = "ordered list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        new_block = block.strip()
        if new_block.strip():
            new_blocks.append(new_block)
    return new_blocks


def block_to_blocktype(block):
    lines = block.split("\n")
    if block.startswith("#"):
        header = ""
        for char in block:
            if char == "#":
                header += "#"
            else:
                break
        if len(header) <= 6 and block.startswith(header + " "):
            return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith("> "):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNLIST
    if block.startswith("1. "):
        count = 1
        for line in lines:
            if not line.startswith(f"{count}. "):
                return BlockType.PARAGRAPH
            count += 1
        return BlockType.ORLIST
    return BlockType.PARAGRAPH

# This is the main function of this file
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        block_type = block_to_blocktype(block)
        html_node = block_to_html_node(block, block_type)
        child_nodes.append(html_node)
    return ParentNode("div", child_nodes, None)


def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return make_paragraph_node(block)
        case BlockType.HEADING:
            return make_heading_node(block)
        case BlockType.CODE:
            return make_code_node(block)
        case BlockType.QUOTE:
            return make_quote_node(block)
        case BlockType.UNLIST:
            return make_unlist_node(block)
        case BlockType.ORLIST:
            return make_orlist_node(block)
        case _:
            raise ValueError("invalid block type")

# converts inline markdown to list of LeafNodes
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    child_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        child_nodes.append(html_node)
    return child_nodes


def make_paragraph_node(block):
    lines = block.split("\n")
    new_block = " ".join(lines)
    return ParentNode("p", text_to_children(new_block))


def make_heading_node(block):
    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break
    new_block = block[count + 1:]
    return ParentNode(f"h{count}", text_to_children(new_block))


def make_code_node(block):
    new_block = block[4:-3]
    code_node = text_node_to_html_node(TextNode(new_block, TextType.NORMAL))
    code_node = ParentNode("code", [code_node])
    return ParentNode("pre", [code_node])


def make_quote_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip("> "))
    new_block = " ".join(new_lines)
    return ParentNode("blockquote", text_to_children(new_block))


def make_unlist_node(block):
    lines = block.split("\n")
    new_block = []
    for line in lines:
        new_lines = text_to_children(line[2:])
        new_block.append(ParentNode("li", new_lines))
    return ParentNode("ul", new_block)


def make_orlist_node(block):
    lines = block.split("\n")
    new_block = []
    for line in lines:
        list_num = line.find(". ")
        if list_num != -1:
            new_lines = text_to_children(line[list_num + 2:])
            new_block.append(ParentNode("li", new_lines))
        else:
            raise ValueError("invalid ordered list")
    return ParentNode("ol", new_block)
