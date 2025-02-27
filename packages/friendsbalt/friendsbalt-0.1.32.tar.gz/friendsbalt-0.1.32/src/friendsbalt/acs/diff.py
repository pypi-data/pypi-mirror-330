import difflib
import json

class StringDiff:
    """
    A class to compute and apply differences between two strings.

    Attributes:
        original (str): The original string.
        modified (str): The modified string.
        additions (list): A list of additions with line numbers.
        deletions (list): A list of deletions with line numbers.

    Methods:
        __init__(original, modified): Initializes the StringDiff object.
        raw_diff(original, modified): Computes the raw diff between two strings.
        apply_diff(original, diff_obj): Applies the diff to the original string to produce the modified string.
        serialize(): Serializes the additions and deletions into a string representation.
        deserialize(serialized_str): Deserializes the string representation into a StringDiff object.
    """

    def __init__(self, original, modified):
        """
        Computes the difference between the original and modified files and parses it into additions and deletions.
        """
        self.additions = []
        self.deletions = []

        self._compute_diff(original, modified)

    def _compute_diff(self, original, modified):
        """
        Computes the difference between the original and modified files and parses it into additions and deletions.
        """
        original_lines = original.splitlines()
        modified_lines = modified.splitlines()

        diff = difflib.unified_diff(original_lines, modified_lines, lineterm='')

        original_line_num = 0
        modified_line_num = 0

        for line in diff:
            if line.startswith('---') or line.startswith('+++'):
                # Skip the file metadata lines
                continue
            if line.startswith('@@'):
                # Extract the line numbers from the hunk header
                parts = line.split()
                original_line_num = int(parts[1].split(',')[0][1:])
                modified_line_num = int(parts[2].split(',')[0][1:])
            elif line.startswith('+'):
                self.additions.append((modified_line_num, line[1:]))
                modified_line_num += 1
            elif line.startswith('-'):
                self.deletions.append((original_line_num, line[1:]))
                original_line_num += 1
            else:
                original_line_num += 1
                modified_line_num += 1

    @staticmethod
    def raw_diff(original, modified):
        """
        Computes the raw diff between two strings.

        Args:
            original (str): The original string.
            modified (str): The modified string.

        Returns:
            str: The raw diff as a string.
        """
        diff = difflib.unified_diff(original.splitlines(), modified.splitlines(), lineterm='')
        return '\n'.join(diff)

    @staticmethod
    def apply_diff(original, diff_obj):
        """
        Applies the diff to the original string to produce the modified string.

        Args:
            original (str): The original string.
            diff_obj (StringDiff): The StringDiff object containing additions and deletions.

        Returns:
            str: The modified string after applying the diff.
        """
        original_lines = original.splitlines()
        result_lines = original_lines[:]

        # Apply deletions in reverse order to avoid index shifting issues
        for line_num, _ in sorted(diff_obj.deletions, reverse=True):
            result_lines.pop(line_num - 1)

        # Apply additions
        for line_num, line in sorted(diff_obj.additions):
            result_lines.insert(line_num - 1, line)

        return '\n'.join(result_lines)

    def serialize(self):
        """
        Serializes the additions and deletions into a string representation.

        Returns:
            str: The serialized string representation of the additions and deletions.
        """
        return json.dumps({
            'additions': self.additions,
            'deletions': self.deletions
        })

    @staticmethod
    def deserialize(serialized_str):
        """
        Deserializes the string representation into a StringDiff object.

        Args:
            serialized_str (str): The serialized string representation of the additions and deletions.

        Returns:
            StringDiff: The deserialized StringDiff object.
        """
        data = json.loads(serialized_str)
        diff_obj = StringDiff('', '')  # Create an empty StringDiff object
        diff_obj.additions = data['additions']
        diff_obj.deletions = data['deletions']
        return diff_obj
