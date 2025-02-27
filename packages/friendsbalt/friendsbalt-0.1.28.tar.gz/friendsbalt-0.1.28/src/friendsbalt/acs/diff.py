import difflib

class StringDiff:
    """
    A class to compute and apply differences between two strings.

    Attributes:
        original (str): The original string.
        modified (str): The modified string.
        additions (list): A list of additions with line numbers.
        deletions (list): A list of deletions with line numbers.
    """

    def __init__(self, original, modified):
        """
        Initializes the Diff class with the original and modified strings.

        Args:
            original (str): The original string.
            modified (str): The modified string.
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
    def apply_diff(original, diff_obj):
        """
        Applies the diff to the original string to produce the modified string.

        Args:
            original (str): The original string.
            diff_obj (Diff): The Diff object containing additions and deletions.

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

# Test the class

original = "Hello\nWorld\n"
modified = "Yay\nHello\nPython\nYay"
diff = StringDiff(original, modified)

# Apply the diff to transform the original string into the modified string
result = StringDiff.apply_diff(original, diff)
print("Result:")
print(result)