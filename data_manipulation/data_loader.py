import ftplib
import os
from io import BytesIO


def load_file_from_ftp(
    server, port, file_path, username=None, password=None, encoding="utf-8"
):
    """
    Loads a file from an FTP server into memory. Authentication is optional.

    :param server: Address of the FTP server.
    :param port: Port of the FTP server.
    :param file_path: Path of the file on the FTP server.
    :param username: Username for FTP authentication (optional).
    :param password: Password for FTP authentication (optional).
    :param encoding: Encoding used to decode the bytes into a string (default is 'utf-8').
    :return: A BytesIO object containing the file data.
    """
    # Create an FTP connection
    with ftplib.FTP() as ftp:
        ftp.connect(server, port)

        # Perform authentication if a username and password are provided
        if username and password:
            ftp.login(username, password)
        else:
            # Otherwise, use the anonymous user
            ftp.login()

        # Create a BytesIO object to store the file data
        memory = BytesIO()

        # Load the file from the FTP server into the BytesIO object
        ftp.retrbinary(f"RETR {file_path}", memory.write)

        # Convert the binary data in BytesIO to a string using the specified encoding
        file_contents = memory.getvalue().decode(encoding)

        return file_contents


def list_files_without_extensions(directory_path):
    """
    List all files in the specified directory without their extensions.

    Parameters:
    - directory_path (str): The path to the directory from which to list files.

    Returns:
    - list[str]: A list of file names without their extensions.
    """
    # List all entries in the directory
    entries = os.listdir(directory_path)

    # Filter out directories, keep only files, and remove their extensions
    files_without_extensions = [
        os.path.splitext(entry)[0]
        for entry in entries
        if os.path.isfile(os.path.join(directory_path, entry))
    ]

    return files_without_extensions