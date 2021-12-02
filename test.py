import sys
from antlr4 import *
from Parse.MySqlLexer import MySqlLexer
from Parse.MySqlParser import MySqlParser
import re
from Nodes.ConditionNode import ConditionNode
from Nodes.ParseNode import ParseNode
from Nodes.Node import Node
import graphviz


SQLL = MySqlLexer
SQLP = MySqlParser

class WriteTreeListener(ParseTreeListener):
    def visitTerminal(self, node:TerminalNode):
        print ("Visit Terminal: " + str(node) + " - " + repr(node))


class CaseChangingStream():
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

def def_anchors():
    #GOTO, PERFORM, IF, EVALUATE
    identifier = "(\S)+" #At least one character, no whitespace
    operators = "(NOT|=|NOT =|>|>=|<|<=)"
    logic_links = "AND|OR"
    anchors = ["\sIF(\s)+", "ELSE", "END-IF", "\.(\s)+","EXEC SQL","'", "\*"]
    return anchors

def next_anchor(input, pos, anchors):
    next_pos = []
    for val in anchors:
        res = re.search(val, input[pos:])
        if res != None:
            next_pos.append({val:input.find(res.group(0), pos)})
        else:
            next_pos.append({val:-1})
    min_val = len(input)+1
    min_key = ""
    for index in range(len(next_pos)):
        for key in next_pos[index]:
            val = next_pos[index][key]
            if val < min_val and val != -1:
                min_val = val 
                min_key = key
    return [min_val, min_key]



def fuzzy_parse(input, anchors):
    pos = 0
    lot = []
    if_depth = 0
    [next_val, n_anchor] = next_anchor(input, pos, anchors)
    while next_val != len(input)+1:
        if n_anchor == anchors[-1]: #Found a comment, skip the whole line !
            # print(">>> FOUND Comment")
            if input.find("\n", next_val) != -1:
                pos = input.find("\n", next_val) +1
            else:
                pos = next_val+len(n_anchor)
        elif n_anchor == anchors[5]:
            # print(">>> Found string")
            if input.find("'", next_val+1) != -1:
                pos = input.find("'", next_val+1) +1
            else:
                pos = next_val+len(n_anchor)
        elif n_anchor == anchors[0]: #Found a if, take note
            # print('>>> FOUND IF')
            pos = next_val+len(re.search(n_anchor, input[pos:]).group(0))
            node = ConditionNode(if_depth, "IF")
            pos = node.find_condition(input, pos)
            if_depth += 1
            # print(node)
            lot.append(node)
            # print(f">>>>>> COND:{cond}")
        elif n_anchor == anchors[1]:
            # print('>>> FOUND ELSE')
            node = ConditionNode(if_depth-1, "ELSE")
            lot.append(node)

            pos = next_val+len(n_anchor)
        elif n_anchor == anchors[2]: #Found a end-if, take note
            # print('>>> FOUND END-IF')
            if_depth -= 1
            node = ConditionNode(if_depth, "END-IF")
            lot.append(node)
            pos = next_val+len(n_anchor)
        elif n_anchor == anchors[3]:
            while if_depth != 0:
                node = ConditionNode(if_depth, "END-IF")
                lot.append(node)
                if_depth -= 1
            pos = next_val+len(n_anchor)

        elif n_anchor == anchors[4]:
            # lot.append("EXEC NODE")
            node = ParseNode(if_depth, "EXEC")
            lot.append(node)
            pos = node.find_parse_text(input, pos)
            # lot.append(parse(input[next_val+8:], SQLL, SQLP))
            # pos = input.find("END-EXEC", pos)+8
            # print('>>> FOUND EXEC')
        else:
            pos += 1
        [next_val, n_anchor] = next_anchor(input, pos, anchors)
    return lot

def parse(input, lexer_base, parser_base):    
    input_stream = InputStream(input)
    lexer = lexer_base(input_stream)
    stream = CommonTokenStream(CaseChangingStream(lexer, True))
    parser = parser_base(stream)
    tree = parser.root()
    return tree

def match_if(open_ifs, else_node):
    for n in open_ifs:
        res = None
        if n.get_depth() == else_node.get_depth():
            res = n
    return n


def construct_graph(node_array):
    last_n = Node(0, "START") 
    graph = last_n
    open_ifs = []
    for node in node_array:
        print(f">>> Last node is: {last_n} with childs: {last_n.get_childs()} parents: {last_n.get_parent()}")
        if node.get_type() == "IF":
            print(">>> In IF")
            last_n.add_child(node)
            last_n = node
            open_ifs.append(node)
        elif node.get_type() == "EXEC":
            print(">>> In EXEC")
            last_n.add_child(node)
            last_n = node
        elif node.get_type() == "ELSE":
            print(">>> In ELSE")
            corr_if = match_if(open_ifs, node)
            print(f">>> In ELSE ! Current if branches:{corr_if.branch_open} and childs: {corr_if.get_childs()}")
            corr_if.close_branch() #If we found an else, we should close the previous branch
            print(f">>> In ELSE ! Closed one branch: {corr_if.branch_open} and childs: {corr_if.get_childs()}")
            temp = Node(corr_if.get_depth(), "CONTROL")
            corr_if.add_child(temp)
            print(f">>> In ELSE ! childs post adding: {corr_if.get_childs()}")
            last_n = temp
        elif node.get_type() == "END-IF":
            print(">>> In END-IF")
            corr_if = match_if(open_ifs, node)
            temp = Node(corr_if.get_depth(), "CONTROL")
            corr_if.close(temp)
            open_ifs.remove(corr_if)
            last_n = temp
    end = Node(0, "END")
    last_n.add_child(end)
    return graph

def replace_child(target, old_child, new_child):
    if target.get_type() == "IF":
        if target.true_child == old_child:
            target.remove_child(old_child)
            target.add_child(new_child, end=True, branch=True)
        if target.false_child == old_child:
            target.remove_child(old_child)
            target.add_child(new_child, end=True, branch=False)
    else:
        target.remove_child(old_child)
        target.add_child(new_child)

def cleanup_triangle (current_node, new_child):
    replace_child(current_node.get_parent()[0], current_node, new_child)

def one_parent(node):
    # print(f">>> Looking at parent of {node}")
    if len(node.get_parent()) == 0:
        return False
    if len(node.get_parent()) == 1: #Easy case, only one parent
        return True
    first = node.get_parent()[0]
    for elem in node.get_parent():
        if elem != node: #Dirty
            if elem != first:
                # print(f">>> Diff parent: {elem} and {first}")
                return False
    return True

def cleanup_graph(graph):
    cleaned = True
    while cleaned == True:
        cleaned = False
        start_node = []
        start_node.append(graph)
        while len(start_node) != 0:
            current_node = start_node[0]
            print(f">>> Looking into {current_node} with childs {current_node.get_childs()}")
            if current_node.get_type() == "CONTROL":
                children = current_node.get_childs()
                print(f">>> Found control node ! len children: {len(children)} len grand_children: {len(children[0].get_childs())}")
                if len(children[0].get_childs()) == 1:
                    print(f">>> type: {children[0].get_type()}")
                if len(children) == 2:
                    print(f">>> It has two children !")
                    if children[0] == children[1]: #Two links pointing the same direction
                        current_node.remove_child(children[0])
                        cleaned = True
                    #We are dealing with a triangle (V1)
                    elif children[1] == children[0].get_childs()[0]:
                        cleanup_triangle(current_node, children[1])
                        cleaned = True
                    #We are dealing with a triangle (V2)
                    elif children[0] == children[1].get_childs()[0]:
                        cleanup_triangle(current_node, children[0])
                        cleaned = True
                    print(f"Cleaned: {cleaned}")
                elif len(children) == 1 and len(children[0].get_childs()) == 1 and children[0].get_type() == "CONTROL":
                    print(f">>> It has one child !") 
                    #We are in a control node having a single child of a control node 
                    parent_node = current_node.get_parent()
                    for p in parent_node:
                        replace_child(p, current_node, children[0])
                    cleaned = True
                    print(f"Cleaned: {cleaned}")
            
            for child in current_node.get_childs(): #Look at a node's childrens
                # print(f">>> Looking at a node's childrens {current_node}, {current_node.get_childs()}")
                if child.get_type() == "CONTROL": #When we find a control node
                    # print(f">>> Child is indeed control ! {child.get_childs()}, {child.get_parent()}")
                    # print(f">>> Tests: {len(child.get_childs()) == 1}, {one_parent(current_node)}")
                    
                    if len(child.get_childs()) == 1 and one_parent(child): #Only one parent and one child
                        replace_child(current_node, child, child.get_childs()[0])
                        # print(f">>> Trying to fuse !")
                        # print(f"Cleaned up: {current_node} new_childs: {current_node.get_childs()}")
                        cleaned = True

            for child in current_node.get_childs():
                if child not in start_node:
                    start_node.append(child)
            start_node.remove(current_node)



def print_graph(graph):
    next = graph
    while next.get_childs() != []:
        print(next)
        next_next = None
        # print(f">>> {next.get_childs()}")
        for index, e in enumerate(next.get_childs()):
            # print(f">>> {e}")
            if next.get_type() == "IF":
                if len(next.get_childs()) == 1:
                    print(f"->Link True and False to {e}")
                else:
                    if index == 0:
                        print(f"->Link True to {e}")
                    elif index == 1:
                        print(f"->Link False to {e}")
                    else:
                        print("Probable error")
            else:
                print(f"->Link to {e}")
            # print(f"Test {e.get_childs()}")
            next_next = e
        next = next_next
    print(next)





def main(argv):
    with open(argv[1], "r") as f:
        lot = fuzzy_parse(f.read(), def_anchors())
        # print(lot)
        for node in lot:
            print(str(node))
        g = construct_graph(lot)
        
        print("_________________________")
        # print_graph(g)
        cleanup_graph(g)
        print("__________________________")
        # for node in lot:
            # print(str(node))
            # print(node.get_childs())


        dot = graphviz.Digraph('control-flow')
        start_node = []
        start_node.append(g)
        all_nodes = []
        while len(start_node) != 0:
            current_node = start_node[0]
            all_nodes.append(current_node)
            start_node.remove(current_node)
            if current_node.get_type() == "IF":
                dot.node(str(current_node.id), "IF "+current_node.condition) 
            elif current_node.get_type() == "EXEC":
                dot.node(str(current_node.id), current_node.parsable)
            elif current_node.get_type() == "CONTROL":
                dot.node(str(current_node.id), str(current_node.id))
            elif current_node.get_type() == "START":
                dot.node(str(current_node.id), 'START')
            elif current_node.get_type() == "END":
                dot.node(str(current_node.id), 'END')
            for c in current_node.get_childs():
                # print(f">>> Adding child of {current_node}, state of all nodes {all_nodes}")
                # print(f"{c in all_nodes}")
                if c not in all_nodes and c not in start_node:
                    # print(f">>> Added {c}")
                    start_node.append(c)
        # print(all_nodes)
        for n in all_nodes:
            if n.get_type() == "IF":
                dot.edge(str(n.id), str(n.true_child.id), label='True')
                dot.edge(str(n.id), str(n.false_child.id), label='False')
            else:
                for link in n.get_childs():
                    dot.edge(str(n.id), str(link.id))
        dot.render(directory='doctest-output', view=False) 





if __name__ == '__main__':
    print("Running")
    main(sys.argv)