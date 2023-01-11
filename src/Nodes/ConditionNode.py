from .Node import Node
from Utils.config import *
from Utils.utils import *


class ConditionNode(Node):

    def __init__(self, depth, type, regex):
        super().__init__(depth, type, regex)
        if self.type != NODE_COND_START:
            self.condition = ""
        self.statements_starts = [r"\sIF(\s)+", r"ELSE", r"WHEN", r"EXEC\sSQL", r"\*", r"PERFORM", r"GO(\s)*TO", "MOVE", "DISPLAY", "CONTINUE", "EXIT"]
        self.statements_str = [r"IF", r"ELSE", r"WHEN", r"EXEC SQL", r"\*", r"PERFORM", r"GOTO", r"GO TO", "MOVE", "DISPLAY", "CONTINUE", "EXIT"]


    def __str__(self):
        #if self.type == NODE_COND_START:
        #   return self.depth * "\t" + f"Node {self.regex} {self.condition}"
        #else:
        return super().__str__()

    def is_anchor(self, input):
        if not any(substring in input for substring in self.statements_str):
            return -1
        for val in self.statements_starts:
            # print(f"Looking for {val}")
            res = re.search(val, input)
            if res != None:
                return input.find(res.group(0))
        return -1



    def find_condition(self, input, pos, delimiter):
        res = delimiter.search(input[pos:])
        if res is None:
            return self.find_condition_simple(input, pos)
        else:
            return self.find_condition_delimiter(input, pos, delimiter)

    def find_condition_delimiter(self, input, pos, delimiter):
        res = delimiter.search(input[pos:])
        end_cond = input.find(res.group(0), pos)
        self.condition = clean_str(input[pos:end_cond])
        return end_cond+1

    def find_condition_simple(self, input, pos):
        go = True
        cond = ""
        new_line = input.find("\n", pos)
        is_anchor = self.is_anchor(input[pos:new_line])
        if is_anchor != -1:
            next = input[pos+1:pos+is_anchor]
            self.condition = clean_str(next)
            #print(f"COND: {self.condition} for {input[pos-10:pos+15]}")
            return pos + len(next)
        else:
            next_line = input[pos+1:new_line]
        first = True
        temp_pos = pos
        while go:
            #print(f"Current cond is: {cond}")
            #print(f"Looking at next line: {next_line}")
            if not first:
                if self.is_anchor(next_line) != -1:
                    #print("saw anchor")
                    go = False
                elif re.search(r'^(\s)*[^\s-]+(\s)*$',next_line):  # Special case of just one thing to finish the line
                    #print("saw signe element")
                    if any(x in next_line for x in self.statements_starts):
                        # print("saw move")
                        go = False
                    else:
                        # print("condition kept going")
                        cond += next_line.lstrip()
                        temp_pos = new_line + 1
                elif any(x in next_line for x in [">", "<", " IS ", " NOT ", " OR ", " AND ", " NUMERIC "]):
                    #print("Saw signe")
                    cond += next_line.strip() + " "
                    temp_pos = new_line + 1
                else:
                    #print("Saw nothing of interest, stop")
                    go = False
            else:
                cond += next_line.strip() + " "
                temp_pos = new_line + 1
            first = False
            new_line = input.find("\n", temp_pos)
            next_line = input[temp_pos:new_line]
        self.condition = clean_str(cond)
        #print(self.condition)
        return pos + len(cond.strip())

    def set_condition(self, cond):
        self.condition = cond

    def get_condition(self):
        return self.condition
