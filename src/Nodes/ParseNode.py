from .Node import Node
from antlr4 import *
from AntlrParser.MySqlLexer import MySqlLexer
from AntlrParser.MySqlParser import MySqlParser
import re


class ParseNode(Node):
    class CaseChangingStream:
        def __init__(self, stream, upper):
            self._stream = stream
            self._upper = upper

        def __getattr__(self, name):
            return self._stream.__getattribute__(name)

        def LA(self, offset):
            c = self._stream.LA(offset)
            if c <= 0:
                return c
            return ord(chr(c).upper() if self._upper else chr(c).lower())

    def __init__(self, depth, node_type, regex):
        super().__init__(depth, node_type, regex)
        self.SQLL = MySqlLexer
        self.SQLP = MySqlParser
        self.parse_tree = None

    def __str__(self):
        return f"Node {self.type} ({self.parsable})"

    def find_parse_text(self, input_str, pos):
        end_pattern = re.compile("END-EXEC", flags=re.MULTILINE|re.IGNORECASE)
        res = end_pattern.search(input_str[pos + 8:])
        self.parsable = input_str[pos + 8:input_str.find(res.group(0), pos)].strip()
        self.parse_tree = self.parse()
        return input_str.find(res.group(0), pos) + 8

    def set_parse_text(self, value):
        self.parsable = value

    def parse(self):
        input_stream = InputStream(self.parsable)
        lexer = self.SQLL(input_stream)
        stream = CommonTokenStream(self.CaseChangingStream(lexer, True))
        parser = self.SQLP(stream)
        tree = parser.root()
        return tree
