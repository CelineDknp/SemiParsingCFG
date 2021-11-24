from Nodes.Node import Node
import re

class ConditionNode(Node):

    def __init__(self, depth, type):
        super().__init__(depth, type)
        if self.type != "IF":
            self.condition = ""

    def __str__(self):
        if self.type == 'IF':
            return self.depth*"\t"+f"Node IF {self.condition}"
        else:
            return self.depth*"\t"+f"Node {self.type}"

    def is_anchor(self, input, anchors):
        for val in anchors:
            res = re.search(val, input)
            if res != None:
                return True
        return False

    def find_condition(self, input, pos):
        go = True
        cond = ""
        new_line = input.find("\n", pos)
        next_line = input[pos:new_line]
        while go:
            if self.is_anchor(next_line, ["\sIF(\s)+", "ELSE", "END-IF","EXEC SQL", "\*"]):
                go = False
            elif re.search('^(\s)+(\S)+(\s)*$', next_line): #Special case of just one thing to finish the line
                if any(x in next_line for x in ["MOVE", "DISPLAY"]):
                    go = False
                else:
                    cond += next_line.lstrip()
                    pos = new_line+1
            elif any(x in next_line for x in [">", "<", "=", "NOT", "OR", "AND", "NUMERIC"]):
                cond += next_line.strip()+" "
                pos = new_line+1
            else:
                go = False
            new_line = input.find("\n", pos)
            next_line = input[pos:new_line]
        self.condition = cond
        return pos
