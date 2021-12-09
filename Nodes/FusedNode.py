from Nodes.Node import Node

class FusedNode(Node):

    def __init__(self, depth, type):
        super().__init__(depth, type)
        self.node_contained = []

    def replace_child(self, target, old_child, new_child):
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

    def fuse_node(self, node, up = False, down = False):
        print(f">>> Fusing node ! Up: {up} Down: {down}")
        if node.get_type() == "IF":
            self.node_contained.append(node)
        elif node.get_type() == "FUSED":
            self.node_contained.extend(node.get_contained_nodes())
        if node in self.get_childs():
                self.remove_child(node)
        if node in self.get_parent():
                self.remove_parent(node)
        print(f">>> In self child: {self.get_childs()} and parent: {self.get_parent()}")
        if up:
            all_p = node.get_parent().copy()
            for p in all_p:
                self.replace_child(p, node, self)
            if node in self.get_parent():
                self.remove_parent(node)

            print(f">>> In self child: {self.get_childs()} and parent: {self.get_parent()}")
        if down:
            all_p = node.get_parent().copy()
            for p in all_p:
                self.replace_child(p, node, self)
            for child in node.get_childs():
                if child != self:
                    self.add_child(child)
                    child.remove_parent(node)
            if node in self.get_childs():
                self.remove_child(node)

            print(f">>> In self child: {self.get_childs()} and parent: {self.get_parent()}")

    def get_contained_nodes(self):
        return self.node_contained

    def amount_contained(self):
        return len(self.node_contained)