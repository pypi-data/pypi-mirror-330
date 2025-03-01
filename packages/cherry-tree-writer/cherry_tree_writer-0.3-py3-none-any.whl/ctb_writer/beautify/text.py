"""
This file allows to add beautify text to cherrytree
"""
import re
import warnings
import xml.etree.ElementTree as ET
from ctb_writer.styles import styles
from .text_parser import Tokenizer

COLOR_RE = re.compile(r"#[0-9a-f]{6}", re.I)

def get_color(color):
    """
    Return a color from input hex or name

    :raises ValueError: If the color is not valid
    """
    if isinstance(color, bytes):
        color = color.decode()

    resolved_color = styles.get(color.lower())
    if resolved_color:
        return resolved_color

    if not re.match(COLOR_RE, color):
        raise ValueError("A color with the format '#af45df' is expected") from None

    return color

def color(func):
    """
    Check that args given is a color
    """
    def wrapper_is_color(*args, **kwargs):
        new_args = []
        for i, arg in enumerate(args):
            if isinstance(arg, str) or isinstance(arg, bytes):
                arg = get_color(arg)
            new_args.append(arg)

        for key, arg in kwargs.items():
            if isinstance(arg, str) or isinstance(arg, bytes):
                kwargs[key] = get_color(arg)

        return func(*new_args, **kwargs)
    return wrapper_is_color


def parse(text):
    """
    Parse a given text and return a list of usable tuples
    """
    result = []
    tokens = Tokenizer.tokenize(text)

    escaped = []
    style_in_use = ""
    current_position = 0
    for token in tokens:
        if token.type == "ESCAPE":
            escaped.append(token)

        elif token.type == "START":
            result.append((style_in_use, text[current_position:token.column]))
            style_in_use = token.value[2:-2]
            current_position = token.column + len(token.value)

        elif token.type == "END":
            text_to_add = ""
            while escaped:
                token_to_escape = escaped.pop(0)
                text_to_add += text[current_position: token_to_escape.column] + token_to_escape.value[1:-1]
                current_position += len(token_to_escape.value)

            text_to_add += text[current_position:token.column]

            result.append((style_in_use, text_to_add))
            style_in_use = ""
            current_position = token.column + len(token.value)
    if current_position < len(text):
        result.append((style_in_use, text[current_position:]))
    return result

class CherryTreeRichtext:
    """
    Class allowing some operations on text, such as:
     - Adding bold
     - Colors
     - Other style
    """
    def __init__(self, text, bold=False, underline=False, size=None, fg=None, bg=None):
        self.text = text
        self.bold = bold
        self.underline = underline
        self.size = size
        self.fg = fg
        self.bg = bg

    @property
    def fg(self):
        return self._fg

    @fg.setter
    @color
    def fg(self, color):
        """
        Check if the value given is a color

        :raises ValueError: If colors does not match a regex

        :param color: The color to check
        :type color: str
        """
        self._fg = color

    @property
    def bg(self):
        return self._bg

    @bg.setter
    @color
    def bg(self, color):
        """
        Check if the value given is a color
        """
        self._bg = color

    def get_xml(self):
        """
        Get the text on cherry tree format
        """
        text_attributes = {}
        if self.bold:
            text_attributes["weight"] = "heavy"

        if self.fg:
            text_attributes["foreground"] = self.fg

        if self.bg:
            text_attributes["background"] = self.bg

        if self.underline:
            text_attributes["underline"] = "single"

        if self.size:
            if not re.match(r"h[1-3]", self.size, re.I):
                warnings.warn(f"Unknown size: {self.size}, use h1-3")
            else:
                text_attributes["scale"] = self.size.lower()

        richtext = ET.Element("rich_text", attrib=text_attributes)
        richtext.text = self.text
        return richtext

    @classmethod
    def from_style(cls, text, style):
        """
        Parse a style and return the text
        """
        attrib = {}
        for text_style in style.split("|"):
            if text_style == "bold":
                attrib["bold"] = True

            elif text_style == "underline":
                attrib["underline"] = True

            elif ":" in text_style:
                style_name, style_val = text_style.split(":")
                if style_name == "fg" or style_name == "bg":
                    attrib[style_name] = get_color(style_val)
                else:
                    attrib[style_name] = style_val

        return cls.from_attributes(text, attrib)

    @classmethod
    def from_attributes(cls, text, attributes):
        """
        Build a class instance from the attributes

        :param text: The text to use
        :type text: str

        :param attributes: The attributes for the text style
        :type attributes: Dict[str, str]
        """
        return cls(text,
                   bold=attributes.get("bold", False),
                   underline=attributes.get("underline", False),
                   size=attributes.get("size"),
                   fg=attributes.get("fg"),
                   bg=attributes.get("bg"))
