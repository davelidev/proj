import os

# Mapping of iteration index (1-based) to current filename
mapping = {}
for i in range(1, 101):
    mapping[i] = f"it_{i}.py"

# Directory
base_dir = "gemini/algos/"

# Rename files (if they exist under old names)
# This is now a general check
for it, current_name in mapping.items():
    # If there are any stray old names, we could add logic here
    # but for now, the directory is clean.
    pass
