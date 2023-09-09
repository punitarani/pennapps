"""mlbot.store.py"""


from mlbot import supabase
import tempfile


class StorageBucket:
    """Storage Bucket"""

    def __init__(self, name: str):
        """Initialize Storage Bucket."""
        self.name = name
        self.bucket = supabase.storage.get_bucket(name)

    def file_exists(self, folder: str, filename: str) -> bool:
        """
        Check if file exists in bucket.
        :param folder: Folder path excluding the bucket name
        :param filename: File name including the extension in the folder
        """
        return any(
            file.get("name") == filename
            for file in supabase.storage.from_(self.name).list(folder)
        )

    def upload(self, source: str, destination: str):
        """Upload file to bucket"""
        with open(source, "rb+") as file:
            file_bytes = file.read()
            supabase.storage.from_(self.name).upload(destination, file_bytes)

    def download(self, source: str) -> tempfile.NamedTemporaryFile:
        """Download file from bucket to a temporary file and return it."""
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False)

        # Download the file from the Supabase bucket
        res = supabase.storage.from_(self.name).download(source)
        temp_file.write(res)

        # Reset the file pointer to the beginning of the file
        temp_file.seek(0)

        return temp_file