from .avl import AVLTree

class OrderedMap:
    """
    OrderedMap is a dictionary-like data structure that maintains the order of keys.
    It uses an AVL tree for efficient insertion, deletion, and lookup operations.

    Methods:
    --------
        __init__(): Initializes an empty OrderedMap.
        __getitem__(key): Retrieves the value associated with the given key.
        __setitem__(key, value): Associates the given value with the given key.
        __delitem__(key): Deletes the key-value pair associated with the given key.
        __contains__(key): Checks if the given key is in the OrderedMap.
        __len__(): Returns the number of key-value pairs in the OrderedMap.
        __iter__(): Returns an iterator over the keys in the OrderedMap.
        __repr__(): Returns a string representation of the OrderedMap.
    """

    def __init__(self):
        """
        Initializes an empty OrderedMap.
        """
        self.tree = AVLTree()

    def __getitem__(self, key):
        """
        Retrieves the value associated with the given key.
        If the key is a slice, returns a list of values within the range specified by the slice.

        Args:
            key: The key to look up, or a slice object specifying a range of keys.

        Returns:
            The value associated with the key, or a list of values if a slice is provided.
        """
        if isinstance(key, slice):
            start = key.start
            stop = key.stop

            if key.start is None:
                start = self.tree.get_min()
            if key.stop is None:
                stop = self.tree.get_max()
            return self.tree.range_select(start, stop)
        return self.tree.get(key)

    def __setitem__(self, key, value):
        """
        Associates the given value with the given key.

        Args:
            key: The key to associate with the value.
            value: The value to associate with the key.
        """
        self.tree.put(key, value)

    def __delitem__(self, key):
        """
        Deletes the key-value pair associated with the given key.

        Args:
            key: The key to delete.
        """
        self.tree.delete(key)

    def __contains__(self, key):
        """
        Checks if the given key is in the OrderedMap.

        Args:
            key: The key to check for.

        Returns:
            True if the key is in the OrderedMap, False otherwise.
        """
        return self.tree.get(key) is not None

    def __len__(self):
        """
        Returns the number of key-value pairs in the OrderedMap.

        Returns:
            The number of key-value pairs.
        """
        return self.tree.size()

    def __iter__(self):
        """
        Returns an iterator over the keys in the OrderedMap.

        Returns:
            An iterator over the keys.
        """
        return iter(self.tree.items())

    def __repr__(self):
        """
        Returns a string representation of the OrderedMap.

        Returns:
            A string representation of the OrderedMap.
        """
        return f"OrderedMap({self.tree.items()})"