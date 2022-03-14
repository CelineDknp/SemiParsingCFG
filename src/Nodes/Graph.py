from Nodes.Node import Node
from Nodes.FusedNode import FusedNode
from Nodes.SimpleBranchConditionNode import SimpleBranchConditionNode
from Nodes.MultipleBranchConditionNode import MultipleBranchConditionNode
from Nodes.ControlLoopNode import ControlLoopNode
from Utils.config import *
from Utils.utils import clean_regex
import graphviz


class Graph:

    def __init__(self, start_node):
        self.start_node = start_node
        self.last_node = start_node
        self.open_ifs = []
        self.open_loops = []
        self.all_nodes = [start_node]

    def match_if(self, branch_node):
        res = None
        # print(f"Searching corr node for: {branch_node}")
        for cond_node in self.open_ifs:
            # print(f"Looking at {cond_node} at depth {cond_node.get_depth()}")
            # print(f"{cond_node.get_regex()} VS {branch_node.get_regex()}")
            if cond_node.get_depth() == branch_node.get_depth() and (
                    cond_node.get_regex() == branch_node.get_regex() or branch_node.get_type() == NODE_COND_END_ANY):
                # print("match !")
                res = cond_node
        return res

    def match_open_loops(self, node):
        to_remove = []

        # print(f"Added label node {node}")
        for n in self.open_loops:
            # print(f"searching match for {n} with label {n.get_label()}")
            if not isinstance(n, ControlLoopNode) and n.get_label() == node.get_label():
                # print("match found !")
                n.add_child(node)
                to_remove.append(n)
        for n in to_remove:
            self.open_loops.remove(n)

    def match_control_node(self, control_node, child):
        to_remove = []
        for n in self.open_loops:
            if isinstance(n, ControlLoopNode) and control_node.get_type() == n.get_control():
                n.add_child(child)
                to_remove.append(n)
        for n in to_remove:
            self.open_loops.remove(n)

    def match_label_node(self, loop_node):
        if isinstance(loop_node, ControlLoopNode):
            return True
        for n in self.all_nodes:
            if n.get_type() == NODE_LABEL and n.get_label() == loop_node.get_label():
                loop_node.add_child(n)
                return False
        return True

    def add_single_node(self, node):
        if self.last_node is not None:
            self.last_node.add_child(node)
        self.last_node = node
        self.all_nodes.append(node)

    def add_node(self, node):
        # print(f"Adding node {node}")
        if node.get_type() == NODE_COND_START:
            # print(">>> In IF")
            self.add_single_node(node)
            self.open_ifs.append(node)
        elif node.get_type() == NODE_SQL:
            self.add_single_node(node)
        elif node.get_type() == NODE_LABEL:
            # print(">>> In EXEC")
            self.add_single_node(node)
            self.match_open_loops(node)
        elif node.get_type() == NODE_LOOP:
            self.add_single_node(node)
            self.last_node = None
            if self.match_label_node(node):
                self.open_loops.append(node)
        elif node.get_type() == NODE_COND_BRANCH:
            # print(">>> In ELSE")
            corr_if = self.match_if(node)
            if corr_if is None:
                print(f"Was looking for node to match {node} in array {self.open_ifs}, but found none")
                raise Exception('Missmatched condition branch')
            temp = Node(corr_if.get_depth(), NODE_CONTROL)
            if isinstance(node, MultipleBranchConditionNode):  # We have a multiple condition, grab the condition
                corr_if.add_branch_condition(node, temp)
            corr_if.close_branch()  # If we found an else, we should close the previous branch
            corr_if.add_child(temp)
            self.all_nodes.append(temp)
            self.last_node = temp
        elif node.get_type() == NODE_COND_END or node.get_type() == NODE_COND_END_ANY:
            # print(">>> In END-IF")
            corr_if = self.match_if(node)
            if corr_if is None:
                print(f"Was looking for node to match {node} in array {self.open_ifs}, but found none")
                raise Exception('Missmatched condition end')
            # print(f"Found matching if: {corr_if}", flush=True)
            temp = Node(corr_if.get_depth(), NODE_CONTROL)
            corr_if.close(temp)
            if node.get_type() == NODE_COND_END_ANY:
                self.match_control_node(node, temp)
            self.open_ifs.remove(corr_if)
            self.last_node = temp
            self.all_nodes.append(temp)
        elif node.get_type() == "END":  # Adding the end_node
            self.add_single_node(node)
        # print("Added the last_node")
        else:
            print(f"Issue during adding node {node}")

    def get_start_node(self):
        return self.start_node

    def get_size(self):
        return len(self.all_nodes)

    def get_all_nodes(self):
        return self.all_nodes

    def replace_child(self, target, old_child, new_child):
        if isinstance(target, SimpleBranchConditionNode):
            if target.true_child == old_child:
                target.remove_child(old_child)
                target.add_child(new_child, end=True, branch=True)
            if target.false_child == old_child:
                target.remove_child(old_child)
                target.add_child(new_child, end=True, branch=False)
        else:
            target.remove_child(old_child)
            target.add_child(new_child)
        for grand_child in old_child.get_childs():
            grand_child.remove_parent(old_child)
            grand_child.add_parent(target)
        if old_child in self.all_nodes:
            self.all_nodes.remove(old_child)

    def cleanup_triangle(self, current_node, new_child):
        self.replace_child(current_node.get_parent()[0], current_node, new_child)

    def one_parent(self, node):
        if len(node.get_parent()) == 0:
            return False
        if len(node.get_parent()) == 1:  # Easy case, only one parent
            return True
        first = node.get_parent()[0]
        for elem in node.get_parent():
            if elem != node:  # Dirty
                if elem != first:
                    return False
        return True

    def cleanup(self):
        cleaned = True
        while cleaned == True:
            visited = []
            cleaned = False
            start_node = self.all_nodes.copy()
            while len(start_node) != 0:
                current_node = start_node[0]
                visited.append(current_node)
                if current_node.get_type() == NODE_CONTROL:
                    children = current_node.get_childs()
                    # print(f">>> Found control node ! len children: {len(children)} len grand_children: {len(children[0].get_childs())}")
                    if len(children) == 2:
                        if children[0] == children[1]:  # Two links pointing the same direction
                            current_node.remove_child(children[0])
                            cleaned = True
                        # We are dealing with a triangle (V1)
                        elif children[1] == children[0].get_childs()[0]:
                            self.cleanup_triangle(current_node, children[1])
                            cleaned = True
                        # We are dealing with a triangle (V2)
                        elif children[0] == children[1].get_childs()[0]:
                            self.cleanup_triangle(current_node, children[0])
                            cleaned = True
                    elif len(children) == 1:
                        # We are in a control node having a single child of a control node
                        parent_node = current_node.get_parent().copy()
                        for p in parent_node:
                            self.replace_child(p, current_node, children[0])
                        cleaned = True
                elif current_node.get_type() == NODE_LABEL:
                    parents = current_node.get_parent()
                    if len(parents) == 1 and parents[0].get_type() != NODE_LOOP:  # A single parent that is not a GOTO
                        child_node = current_node.get_childs().copy()
                        for c in child_node:
                            self.replace_child(parents[0], current_node, c)
                        cleaned = True

                for child in current_node.get_childs().copy():  # Look at a node's childrens
                    if child.get_type() == NODE_CONTROL:  # When we find a control node
                        if len(child.get_childs()) == 1 and self.one_parent(child):  # Only one parent and one child
                            self.replace_child(current_node, child, child.get_childs()[0])
                            cleaned = True

                start_node.remove(current_node)

    def fuse(self, node_up, node_down):
        if node_down.get_type() == NODE_FUSED:
            node_down.fuse_node(node_up, up=True)
            self.all_nodes.remove(node_up)
            return node_down
        elif node_up.get_type() == NODE_FUSED:
            node_up.fuse_node(node_down, down=True)
            self.all_nodes.remove(node_down)
        else:
            node = FusedNode(node_up.get_depth(), NODE_FUSED)
            self.all_nodes.append(node)
            node.fuse_node(node_up, up=True)
            self.all_nodes.remove(node_up)
            node.fuse_node(node_down, down=True)
            self.all_nodes.remove(node_down)
            return node

    def squish(self):
        squished = True
        while squished:
            squished = False
            start_node = self.all_nodes.copy()
            all_nodes = []
            while len(start_node) != 0:
                current_node = start_node[0]
                all_nodes.append(current_node)
                if (
                        current_node.get_type() == NODE_COND_START or current_node.get_type() == NODE_FUSED) and current_node.point_to_one():
                    # We are in a if node that points to a single node
                    # print(f"Found a node that points to one: {current_node} with childs: {current_node.get_childs()}")
                    child = current_node.get_childs()[0]
                    if child.get_type() != "END" and child.get_type() != NODE_SQL:
                        merge = True
                        for c in child.get_childs():
                            if c.get_type() == NODE_SQL:
                                merge = False
                        if merge:
                            # print("Decided to merge !")
                            res = self.fuse(current_node, child)
                            squished = True
                            break
                elif current_node.get_type() == NODE_FUSED and any(
                        child.get_type() == NODE_FUSED for child in current_node.get_childs()):
                    # print("Found a fused node having fused child")
                    # We found a fused node having a FUSED child
                    to_fuse = None
                    for child in current_node.get_childs():
                        if child.get_type() == NODE_FUSED:
                            to_fuse = child
                    if to_fuse != None:
                        # print("Decided to fuse the fuse")
                        res = self.fuse(current_node, to_fuse)
                        squished = True
                start_node.remove(current_node)

    def save_as_file(self, filename, output_dir='doctest-output'):
        dot = graphviz.Digraph(filename)
        for current_node in self.all_nodes:
            if current_node.get_type() == NODE_COND_START:
                dot.attr('node', shape='ellipse')
                dot.node(str(current_node.id), clean_regex(current_node) + " " + current_node.condition)
            elif current_node.get_type() == NODE_LOOP:
                dot.attr('node', shape='ellipse')
                if isinstance(current_node, ControlLoopNode):
                    dot.node(str(current_node.id), "NEXT SENTENCE")
                else:
                    dot.node(str(current_node.id), "GOTO " + current_node.get_label())
            elif current_node.get_type() == NODE_SQL:
                dot.attr('node', shape='box')
                dot.node(str(current_node.id), current_node.parsable)
            elif current_node.get_type() == NODE_LABEL:
                dot.attr('node', shape='note')
                dot.node(str(current_node.id), current_node.label)
            elif current_node.get_type() == NODE_CONTROL:
                dot.node(str(current_node.id), str(current_node.id))
            elif current_node.get_type() == "START":
                dot.attr('node', shape='diamond')
                dot.node(str(current_node.id), 'START')
            elif current_node.get_type() == "END":
                dot.attr('node', shape='diamond')
                dot.node(str(current_node.id), 'END')
            elif current_node.get_type() == NODE_FUSED:
                dot.attr('node', shape='circle')
                dot.node(str(current_node.id), str(current_node.amount_contained()))
        for n in self.all_nodes:
            if n.get_type() == NODE_COND_START and isinstance(n, SimpleBranchConditionNode):
                dot.edge(str(n.id), str(n.true_child.id), label='True')
                dot.edge(str(n.id), str(n.false_child.id), label='False')
            elif n.get_type() == NODE_COND_START and isinstance(n, MultipleBranchConditionNode):
                for condition in n.get_branch_childs().keys():
                    # print(condition)
                    dot.edge(str(n.id), str(n.get_branch_child(condition).id), label=condition)
            else:
                for link in n.get_childs():
                    dot.edge(str(n.id), str(link.id))
        dot.render(directory=output_dir, view=False)

    def add_node_to_list(self, node):
        self.all_nodes.append(node)

    def __str__(self):
        result = "Nodes in graph:\n"
        for n in self.all_nodes:
            # print(n.id)
            result += n.__repr__() + "\n"
        return result
