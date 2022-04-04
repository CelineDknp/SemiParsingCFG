from .Node import Node
from Utils.config import *
from Utils.utils import *
import re


class ConditionNode(Node):

    def __init__(self, depth, type, regex):
        super().__init__(depth, type, regex)
        if self.type != NODE_COND_START:
            self.condition = ""

    def __str__(self):
        if self.type == NODE_COND_START:
            return self.depth * "\t" + f"Node {self.regex} {self.condition}"
        else:
            return super().__str__()

    def is_anchor(self, input, anchors):
        for val in anchors:
            res = re.search(val, input)
            if res != None:
                return True
        return False

    def find_condition(self, input, pos, delimiter):
        res = delimiter.search(input[pos:].upper())
        if res is None:
            return self.find_condition_simple(input, pos)
        else:
            return self.find_condition_delimiter(input, pos, delimiter)

    def find_condition_delimiter(self, input, pos, delimiter):
        res = delimiter.search(input[pos:].upper())
        end_cond = input.upper().find(res.group(0), pos)
        self.condition = input[pos:end_cond].strip()
        return end_cond+1

    def find_condition_simple(self, input, pos):
        go = True
        cond = ""
        new_line = input.upper().find("\n", pos)
        new_spaces = input.upper().find("   ", pos)
        if new_spaces < new_line:
            next_line = input[pos:new_spaces]
        else:
            next_line = input[pos:new_line]
        first = True
        while go:
            if not first:
                # print(f"Current cond is: {cond}")
                # print(f"Looking at next line: {next_line}")
                if self.is_anchor(next_line.upper(), [r"\sIF(\s)+", "ELSE", "END-IF", "WHEN", "EXEC SQL", r"\*"]):
                    # print("saw anchor")
                    go = False
                elif re.search(r'^(\s)*(\S)+(\s)*$',
                               next_line.upper()):  # Special case of just one thing to finish the line
                    # print("saw signe element")
                    if any(x in next_line.upper() for x in ["MOVE", "WHEN", "DISPLAY", "CONTINUE"]):
                        # print("saw move")
                        go = False
                    else:
                        # print("condition kept going")
                        cond += next_line.lstrip()
                        pos = new_line + 1
                elif any(x in next_line.upper() for x in [">", "<", " IS ", " NOT ", " OR ", " AND ", " NUMERIC "]):
                    cond += next_line.strip() + " "
                    pos = new_line + 1
                else:
                    # print("Saw nothing of interest, stop")
                    go = False
            else:
                cond += next_line.strip() + " "
                pos = new_line + 1
            first = False
            new_line = input.find("\n", pos)
            next_line = input[pos:new_line]
        self.condition = cond.strip()
        # print(self.condition)
        return pos

    def set_condition(self, cond):
        self.condition = cond

    def get_condition(self):
        return self.condition
