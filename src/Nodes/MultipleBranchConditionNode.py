from .ConditionNode import ConditionNode
from Utils.config import *
from Utils.utils import *

class MultipleBranchConditionNode(ConditionNode):

    def __init__(self, depth, type, regex):
        super().__init__(depth, type, regex)
        if self.type != NODE_COND_START or NODE_COND_BRANCH:
            self.condition = ""
        self.regex = regex
        self.current_child = None
        self.branch_childs = {} #Holding the conditions
        self.closed = False

    def __str__(self):
        #if self.type == NODE_COND_START:
        #    return self.depth*"\t"+f"Node EVALUATE {self.condition}"
        #else:
        #    return super().__str__()
        return self.get_str_code()

    def get_branches(self):
        result = []
        for e in self.branch_childs:
            result.append((e, self.branch_childs[e]))
        return result

    def find_condition_double(self, input, pos):
        self.condition = ""
        first = True
        go = True
        tot_end = input[pos:].find("END-EVALUATE")
        init_str = input[pos:pos+50]
        while go:
            go = False
            when = input[pos:].find("WHEN")
            next_end = input[pos:].find("\n")
            real_end = (input[pos+next_end+1:].find("\n"))+next_end+1
            if (when < tot_end and when < real_end) or first:
                if first:
                    first = False
                new_pos = pos+when
                end = input[new_pos:].find("\n")
                str = input[new_pos+4:new_pos+end]
                new_pos += len(str)
                pos = new_pos
                if len(self.condition) > 0:
                    self.condition += " OR "+ str.strip()
                else:
                    self.condition = str.strip()
                go = True
        return pos

    def get_str_code(self):
        if self.type == NODE_COND_START:
            return f"EVALUATE {self.condition}"
        elif self.type == NODE_COND_BRANCH:
            return f"WHEN {self.condition}"
        else:
            return super().get_str_code()

    def close_branch(self, end=False): #Closing branches
        self.current_child = None

    def get_branch_last_childs(self, index): #Get the last child from one specific branch
        condition = self.get_condition_from_index(index)
        if condition != None:
            start_child = self.get_branch_child(condition)
            if start_child != None:
                return start_child.get_last_childs()
        return None

    def get_condition_from_index(self, index):
        if index < len(self.branch_childs):
            idx_condition = ""
            for ix, condition in enumerate(self.branch_childs.get_keys()):
                if index == ix:
                    idx_condition = condition
            return idx_condition
        return None


    def get_branch_childs(self):
        return self.branch_childs

    def get_branch_child(self, condition):
        return self.branch_childs[condition]

    def get_child_condition(self, child):
        for e in self.branch_childs:
            if self.branch_childs[e] == child:
                return e
        return None

    def has_first_condition(self):
        return len(self.branch_childs) > 1

    def add_branch_condition(self, node, child):
        self.branch_childs[node.get_condition()] = child

    def add_branch_condition(self, condition):
        self.branch_childs[condition] = None
        # self.current_child = condition

    def add_branch_condition(self, node, child):
        self.branch_childs[node.get_condition()] = child
 
    def add_child_branch(self, node):
        to_add = self.current_child
        if to_add == None: #No previous child, create it
            # print("In if")
            # print(self.branch_childs)
            super().add_child(node)
            self.current_child = node
            for c in self.branch_childs:
                if self.branch_childs[c] == None:
                    self.branch_childs[c] = node 
            # print(self.branch_childs)
            return
        if not isinstance(to_add, list):
            to_add = [to_add]
        for child in to_add:
            child.add_child(node)


    #Fuction to add a child. If boolean true is set, ignore the closed branches and just change the child
    def add_child(self, node, end=False, branch=None):
        # print(f">>> Adding child to IF node ! Child:{node}, branch state: {self.branch_open}, current childs: {self.get_childs()}")
        if node == self: #Don't add yourself as a child ! #Dirtyfix
            print(">>> Trying to add myself as child (MultipleBranchConditionNode)")
            return
        
        #Force add the child
        if end:
            self.add_single_child_branch(branch, node)
            return

        if self.closed:
            # print(f"Adding child {node} to closed MultipleBranchConditionNode on condition(s) {self.current_child}")
            for child in self.current_child:
                self.branch_childs[child] = node
            self.current_child = []
            super().add_child(node)
            return
        
        # Normal processing
        self.add_child_branch(node)
        # print(f"Current state of children: {self.get_childs()}")
            
    
    def remove_child(self, node):
        # print(f"Removed child {node} from MultipleBranchConditionNode")
        if node in self.get_childs():
            super().remove_child(node)
        for condition in self.branch_childs.keys():
            # print(f"Looking at condition {condition}")
            if self.branch_childs[condition] == node:
                self.branch_childs[condition] = None
                if self.closed:
                    self.current_child.append(condition)

    def close(self, control_node): #Function to close an IF node
        for child in self.get_childs():
            test = flatten(child.get_last_childs())
            for sub_child in test:
                sub_child.add_child(control_node)
        self.closed = True
        self.current_child = []
