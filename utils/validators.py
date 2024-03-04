class Validators:
    @staticmethod
    def validate_node_dict(node_dict: dict) -> bool:
        """
        Validates a node dictionary ensuring presence and type of 'x' and 'y' keys.

        Args:
            node_dict (dict): The dictionary representing a node.

        Returns:
            bool: True if the dictionary is valid, False otherwise.
        """

        if not all(key in node_dict for key in ['x', 'y']):
            return False

        for key, value in node_dict.items():
            try:
                float(value)
            except ValueError:
                return False
        return True
