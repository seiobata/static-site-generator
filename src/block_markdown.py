from enum import Enum


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
