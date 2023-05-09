from typing import Any, Generator, Tuple

from tree_node import TreeNode


class BinarySearchTree:
    """Binary-Search-Tree implemented for didactic reasons."""

    def __init__(self, root: TreeNode = None):
        """Initialize BinarySearchTree.

        Args:
            root (TreeNode, optional): Root of the BST. Defaults to None.
        
        Raises:
            ValueError: root is neither a TreeNode nor None.
        """
        self._root = root
        self._size = 0 if root is None else 1
        self._num_of_comparisons = 0

    def insert(self, key: int, value: Any) -> None:
        """Insert a new node into BST.

        Args:
            key (int): Key which is used for placing the value into the tree.
            value (Any): Value to insert.

        Raises:
            ValueError: If key is not an integer.
            KeyError: If key is already present in the tree.
        """
        if not isinstance(key, int):
            raise ValueError

        if self._root is None:
            self._root = TreeNode(key, value)
            self._size += 1
        else:
            try:
                self._insert_recursive(self._root, key, value)
            except KeyError:
                raise KeyError

    def find(self, key: int) -> TreeNode:
        """Return node with given key.

        Args:
            key (int): Key of node.

        Raises:
            ValueError: If key is not an integer.
            KeyError: If key is not present in the tree.

        Returns:
            TreeNode: Node
        """
        if not isinstance(key, int):
            raise ValueError
        node = self._find_recursive(self._root, key)
        if node is None:
            raise KeyError
        return node

    @property
    def size(self) -> int:
        """Return number of nodes contained in the tree."""
        return self._size

    # If users instead call `len(tree)`, this makes it return the same as `tree.size`
    __len__ = size

    def __getitem__(self, key: int) -> Any:
        """Return value of node with given key.

        Args:
            key (int): Key to look for.

        Raises:
            ValueError: If key is not an integer.
            KeyError: If key is not present in the tree.

        Returns:
            Any: [description]
        """
        return self.find(key).value

    def remove(self, key: int) -> None:
        """Remove node with given key, maintaining BST-properties.

        Args:
            key (int): Key of node which should be deleted.

        Raises:
            ValueError: If key is not an integer.
            KeyError: If key is not present in the tree.
        """

        def remove_recursive(node):
            if node is None:
                return node, False

            if key < node.key:
                node.left, removed = remove_recursive(node.left)
            elif key > node.key:
                node.right, removed = remove_recursive(node.right)
            else:
                removed = True
                if node.left and node.right:
                    successor = node.right
                    while successor.left:
                        successor = successor.left
                    node.key, node.value = successor.key, successor.value
                    node.right, _ = remove_recursive(node.right)
                elif node.left:
                    node = node.left
                else:
                    node = node.right

            return node, removed

        if not isinstance(key, int):
            raise ValueError

        self._root, deleted = remove_recursive(self._root)
        if not deleted:
            raise KeyError
        self._size -= 1

    def inorder(self, node: TreeNode = None) -> Generator[TreeNode, None, None]:
        """Yield nodes in inorder."""
        node = node or self._root
        # This is needed in the case that there are no nodes.
        if not node:
            return iter(())
        yield from self._inorder(node)

    def preorder(self, node: TreeNode = None) -> Generator[TreeNode, None, None]:
        """Yield nodes in preorder."""
        node = node or self._root
        if not node:
            return iter(())
        yield from self._preorder(node)

    def postorder(self, node: TreeNode = None) -> Generator[TreeNode, None, None]:
        """Yield nodes in postorder."""
        node = node or self._root
        if not node:
            return iter(())
        yield from self._postorder(node)

    # this allows for e.g. `for node in tree`, or `list(tree)`.
    def __iter__(self) -> Generator[TreeNode, None, None]:
        yield from self._preorder(self._root)

    @property
    def is_valid(self) -> bool:
        """Return if the tree fulfills BST-criteria."""

        def is_valid_recursive(node: TreeNode, lower: float, upper: float) -> bool:
            if node is None:
                return True

            if not lower < node.key < upper:
                return False

            return (is_valid_recursive(node.left, lower, node.key) and
                    is_valid_recursive(node.right, node.key, upper))

    def return_min_key(self) -> TreeNode:
        """Return the node with the smallest key (None if tree is empty)."""
        node = self._root
        while node and node.left:
            node = node.left
        return node

    # def find_comparison(self, key: int) -> Tuple[int, int]:
    #     """Create an inbuilt python list of BST values in preorder and compute the number of comparisons needed for
    #        finding the key both in the list and in the BST.
    #        Return the numbers of comparisons for both, the list and the BST
    #     """
    #     python_list = list(node.key for node in self._preorder())
    #     # TODO

    def __repr__(self) -> str:
        return f"BinarySearchTree({list(self._inorder(self._root))})"

    ####################################################
    # Helper Functions
    ####################################################

    def get_root(self):
        return self._root

    def _inorder(self, current_node):
        if current_node is None:
            return []

        result = []
        result.extend(self._inorder(current_node.left))
        result.append(current_node)
        result.extend(self._inorder(current_node.right))
        return result

    def _preorder(self, current_node):
        if current_node is None:
            return []

        result = [current_node]
        result.extend(self._preorder(current_node.left))
        result.extend(self._preorder(current_node.right))
        return result

    def _postorder(self, current_node):
        if current_node is None:
            return []

        result = []
        result.extend(self._postorder(current_node.left))
        result.extend(self._postorder(current_node.right))
        result.append(current_node)
        return result

    def _find_recursive(self, node: TreeNode, key: int) -> TreeNode:
        if node is None:
            return None

        if key == node.key:
            return node
        elif key < node.key:
            return self._find_recursive(node.left, key)
        else:
            return self._find_recursive(node.right, key)

    def _insert_recursive(self, node: TreeNode, key: int, value: Any) -> None:
        if key == node.key:
            raise KeyError

        if key < node.key:
            if node.left is None:
                node.left = TreeNode(key, value)
                self._size += 1
            else:
                self._insert_recursive(node.left, key, value)
        else:
            if node.right is None:
                node.right = TreeNode(key, value)
                self._size += 1
            else:
                self._insert_recursive(node.right, key, value)
