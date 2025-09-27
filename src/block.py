from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def get_block_type(block):
    if re.match(r"^#{1,6}", block):
        return BlockType.HEADING.value
    elif block.startswith('```') and block.endswith('```'):
        return BlockType.CODE.value
    elif re.match(r"^\>", block):
        return BlockType.QUOTE.value
    elif re.match(r"^\s?\-\s", block):
        return BlockType.UNORDERED_LIST.value
    elif re.match(r"^\s?[0-9]\.", block):
        return BlockType.ORDERED_LIST.value

    return BlockType.PARAGRAPH.value
