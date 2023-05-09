from typing import Any


class TreeNode:
    
    def __init__(self, key: int, value: Any, right: 'TreeNode' = None, 
                 left: 'TreeNode' = None, parent: 'TreeNode' = None):
        """Initialize TreeNode.

        Args:
            key (int): Key used for sorting the node into a BST.
            value (Any): Whatever data the node shall carry.
            right (TreeNode, optional): Node to the right, with a larger key. Defaults to None.
            left (TreeNode, optional): Node to the left, with a lesser key. Defaults to None.
            parent (TreeNode, optional): Parent node. Defaults to None.
        """
        self.key = key
        self.value = value
        self.right = right
        self.left = left
        self.parent = parent

    def __repr__(self) -> str:
        return f"TreeNode({self.key}, {self.value})"

    @property
    def depth(self) -> int:
        """Return depth of the node, i.e. the number of parents/grandparents etc.

        Returns:
            int: Depth of node
        """
        if self.parent is None:
            return 0
        return self.parent.depth + 1

    @property
    def is_external(self) -> bool:
        """Return if node is an external node (= leaf)."""
        return self.left is None and self.right is None
   
    @property
    def is_internal(self) -> bool: 
        """Return if node is an internal node."""
        return not self.is_external

