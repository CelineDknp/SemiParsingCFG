from Nodes.Node import Node
from Utils.utils import *
import re

class ConditionNode(Node):

    def __init__(self, depth, type):
        super().__init__(depth, type)
        if self.type != "IF":
            self.condition = ""
        self.branch_open = [True, False] #When creating an if, the true branch is always open and the false is not
        self.true_child = None
        self.false_child = None

    def __str__(self):
        if self.type == 'IF':
            return self.depth*"\t"+f"Node IF {self.condition}"
        else:
            return super().__str__()

    def true_branch_open(self): #Return true if the node's "true" branch is closed
        return self.branch_open[0]

    def false_branch_open(self):
        return self.branch_open[1]

    def close_branch(self): #Closing branches
        for index, val in enumerate(self.branch_open):
            if val:
                self.branch_open[index] = False
                if index+1 < len(self.branch_open): 
                    self.branch_open[index+1] = True  
                return

    def get_branch_last_childs(self, value): #Get the last child from one specific brancg
        start_child = None
        if value:
            start_child = self.get_branch_childs(True)
        else:
            start_child = self.get_branch_childs(False)
        if start_child != None:
            return start_child.get_last_childs()
        else:
            return None


    def get_branch_childs(self, value):
        if value:
            return self.true_child if self.true_child != None else None
        else:
            return self.false_child if self.false_child != None else None

    def add_single_child_branch(self, branch, node):
        if branch:
            self.true_child = node
            super().add_child(node)
        else:
            self.false_child = node
            super().add_child(node)

    def add_child_branch(self, branch, node):
        to_add = self.get_branch_childs(branch)
        if to_add == None: #No previous child, create it
            self.add_single_child_branch(branch, node)
            return
        # print(f">>> Got previous children ! {to_add}")
        for child in to_add:
            child.add_child(node)


    #Fuction to add a child. If boolean true is set, ignore the closed branches and just change the child
    def add_child(self, node, end=False, branch=None):
        # print(f">>> Adding child to IF node ! Child:{node}, branch state: {self.branch_open}, current childs: {self.get_childs()}")
        if node == self: #Don't add yourself as a child ! #Dirtyfix
            print(">>> Trying to add myself as child (ConditionNode)")
            return
        
        #Force add the child
        if end:
            self.add_single_child_branch(branch, node)
            return
        
        # Normal processing
        if self.true_branch_open():
            self.add_child_branch(True, node)
        elif self.false_branch_open():
            self.add_child_branch(False, node)
        else:
            print("Trying to add childs to closed IF node !")
            return
            
    def remove_child(self, node):
        if node == self.true_child:
            self.true_child = None
        elif node == self.false_child:
            self.false_child = None
        else:
            print("this should not happen !")
            return
        if node in self.get_childs():
            super().remove_child(node)


    def close(self, control_node): #Function to close an IF node
        # print("Closing !", flush=True)
        # print(f"True: {self.true_child} False: {self.false_child}", flush=True)
        if self.true_child == None: #If I don't have a child on my true branch, add the control node
            self.add_child(control_node, end=True, branch=True)
        else:
            # print("In else", flush=True)
            for child in flatten(self.true_child.get_last_childs()):
                child.add_child(control_node)
            # print("After for", flush=True)
        if self.true_branch_open():
            self.close_branch() #Close my True branch
        if self.false_child == None: #If I don't have a child on my false branch, add the control node
            self.add_child(control_node, end=True, branch=False)
        else:
            for child in flatten(self.false_child.get_last_childs()):
                child.add_child(control_node)
        if self.false_branch_open():
            self.close_branch()

    def point_to_one(self):
        return self.true_child == self.false_child

    def is_anchor(self, input, anchors):
        for val in anchors:
            res = re.search(val, input)
            if res != None:
                return True
        return False


    def find_condition(self, input, pos):
        go = True
        cond = ""
        new_line = input.upper().find("\n", pos)
        next_line = input[pos:new_line]
        while go:
            if self.is_anchor(next_line.upper(), [r"\sIF(\s)+", "ELSE", "END-IF","EXEC SQL", r"\*"]):
                go = False
            elif re.search(r'^(\s)*(\S)+(\s)*$', next_line.upper()): #Special case of just one thing to finish the line
                if any(x in next_line.upper() for x in ["MOVE", "DISPLAY"]):
                    go = False
                else:
                    cond += next_line.lstrip()
                    pos = new_line+1
            elif any(x in next_line.upper() for x in [">", "<", "=", "NOT", "OR", "AND", "NUMERIC"]):
                cond += next_line.strip()+" "
                pos = new_line+1
            else:
                go = False
            new_line = input.find("\n", pos)
            next_line = input[pos:new_line]
        self.condition = cond.strip()
        return pos

    def get_condition(self):
        return self.condition
