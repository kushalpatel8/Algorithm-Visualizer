class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key):
    if root is None:
        yield Node(key), [key]
        return Node(key)
    else:
        if root.val < key:
            if root.right is None:
                root.right = Node(key)
                yield root, [key]
            else:
                yield from insert(root.right, key)
        else:
            if root.left is None:
                root.left = Node(key)
                yield root, [key]
            else:
                yield from insert(root.left, key)
    yield root, [key]

def get_tree_structure(root, pos=None, x=0, y=0, layer=1):
    if pos is None:
        pos = {}
    if root:
        pos[root.val] = (x, -y)
        get_tree_structure(root.left, pos, x - 1/2**layer, y + 1, layer + 1)
        get_tree_structure(root.right, pos, x + 1/2**layer, y + 1, layer + 1)
    return pos

def inorder(root, visited=None):
    if visited is None: visited = []
    if root:
        yield from inorder(root.left, visited)
        visited.append(root.val)
        yield root.val, visited
        yield from inorder(root.right, visited)

def preorder(root, visited=None):
    if visited is None: visited = []
    if root:
        visited.append(root.val)
        yield root.val, visited
        yield from preorder(root.left, visited)
        yield from preorder(root.right, visited)

def postorder(root, visited=None):
    if visited is None: visited = []
    if root:
        yield from postorder(root.left, visited)
        yield from postorder(root.right, visited)
        visited.append(root.val)
        yield root.val, visited
