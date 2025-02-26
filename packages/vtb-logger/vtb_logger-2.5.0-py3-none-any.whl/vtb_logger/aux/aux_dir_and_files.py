import os


def ensure_file_exists(file_path):
    """
    Ensures that the directory for the given file exists, 
    and creates the file if it doesn't exist.
    """
    # Extract the directory path
    directory = os.path.dirname(file_path)

    # Ensure the directory exists
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    # Create the file if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("")  # Create an empty file


def write_to_file(log, file_path):
    """
    Writes an array of elements to a .log or .txt file.

    :param elements: List of elements to write to the file.
    :param file_path: Path to the file (.log or .txt).
    """
    # Validate file extension
    if not file_path.endswith(('.log', '.txt')):
        raise ValueError("Only .log and .txt file extensions are supported.")

    # Ensure the directory exists
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    # Write elements to file
    with open(file_path, "a") as file:
        file.write(f"{log}\n")
