class TreeNode(object):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.child = {}

    def __len__(self):
        return self.child.__len__()

    # 添加孩子节点
    def add_child(self, name, child=None):
        if child and not isinstance(TreeNode):
            raise ValueError("TreeNode 请添加 TreeNode子节点")
        if child is None:
            child = TreeNode(name)
        child.parent = self
        self.child[name] = child
        return child

    # 移除孩子节点
    def remove_child(self, name):
        if name in self.child:
            del self.child[name]
        else:
            raise ValueError("%s无%sname节点！" % (self.name, name))

    # 获取孩子节点
    def get_child(self, name):
        if name in self.child:
            return self.child[name]
        else:
            raise ValueError("%s无%sname节点！" % (self.name, name))
