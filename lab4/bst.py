import pickle


class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = TreeNode(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if key < node.val:
            if node.left is None:
                node.left = TreeNode(key)
            else:
                self._insert_recursive(node.left, key)
        elif key > node.val:
            if node.right is None:
                node.right = TreeNode(key)
            else:
                self._insert_recursive(node.right, key)

    def find(self, key):
        return self._find_recursive(self.root, key)

    def _find_recursive(self, node, key):
        if node is None or node.val == key:
            return node
        if key < node.val:
            return self._find_recursive(node.left, key)
        return self._find_recursive(node.right, key)

    def delete(self, key):
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node, key):
        if node is None:
            return node
        if key < node.val:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.val:
            node.right = self._delete_recursive(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._min_value_node(node.right)
            node.val = temp.val
            node.right = self._delete_recursive(node.right, temp.val)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def print_tree(self):
        self._print_inorder(self.root)

    def _print_inorder(self, node):
        if node:
            self._print_inorder(node.left)
            print(node.val, end=' ')
            self._print_inorder(node.right)

    def clear(self):
        self.root = None

    def serialize(self):
        return self._serialize_recursive(self.root)

    def _serialize_recursive(self, node):
        if node is None:
            return None
        return {'val': node.val, 'left': self._serialize_recursive(node.left), 'right': self._serialize_recursive(node.right)}

    def deserialize(self, data):
        if data is None:
            return None
        node = TreeNode(data['val'])
        node.left = self.deserialize(data['left'])
        node.right = self.deserialize(data['right'])
        return node


BACKUP_FILE = 'bst_backup.pickle'
