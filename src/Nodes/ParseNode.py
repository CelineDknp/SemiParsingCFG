from Nodes.Node import Node
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

    def __init__(self, depth, node_type):
        super().__init__(depth, node_type)
        self.SQLL = MySqlLexer
        self.SQLP = MySqlParser

    def __str__(self):
        return f"Node {self.type} ({self.parsable})"

    def find_parse_text(self, input_str, pos):
        self.parsable = input_str[pos + 8:input_str.lower().find("end-exec", pos)].strip()
        return input_str.lower().find("end-exec", pos) + 8

    def parse(self):
        input_stream = InputStream(input)
        lexer = self.SQLL(input_stream)
        stream = CommonTokenStream(self.CaseChangingStream(lexer, True))
        parser = self.SQLP(stream)
        tree = parser.root()
        return tree
