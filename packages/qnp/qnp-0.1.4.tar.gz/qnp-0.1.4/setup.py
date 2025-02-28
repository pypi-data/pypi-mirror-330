import os
import urllib.request
import zipfile


class RefractiveIndexDatabase:
    _DATABASE_SHA = "451b9136b4b3566f6259b703990add5440ca125f"
    DB_URL = f"https://github.com/polyanskiy/refractiveindex.info-database/archive/{_DATABASE_SHA}.zip"

    BASE_PATH = os.path.join(
        os.path.expanduser("~"), ".QNP", "Databases", "RefractiveIndex"
    )
    ZIP_PATH = os.path.join(BASE_PATH, "RefractiveIndex.zip")

    def download_db(self):
        # Create the directories if they don't exist
        os.makedirs(self.BASE_PATH, exist_ok=True)

        # Download the ZIP file if necessary
        if not os.listdir(self.BASE_PATH):
            print(f"Downloading database from {self.DB_URL}...")
            urllib.request.urlretrieve(self.DB_URL, self.ZIP_PATH)
            print(f"Database downloaded to: {self.ZIP_PATH}")

            # Unzip and move contents
            self.unzip_db()
        else:
            print("Database already exists. Skipping download.")

    def unzip_db(self):
        print(f"Unzipping database contents to: {self.BASE_PATH}...")
        try:
            with zipfile.ZipFile(self.ZIP_PATH, "r") as zip_ref:
                # Extract only the "database/" folder
                for member in zip_ref.namelist():
                    if member.startswith(
                        f"refractiveindex.info-database-{self._DATABASE_SHA}/database/"
                    ):
                        # Remove the ZIP folder structure to place files directly
                        relative_path = member.split("database/")[1]
                        target_path = os.path.join(self.BASE_PATH, relative_path)

                        if member.endswith("/"):
                            # If it's a folder, create it
                            os.makedirs(target_path, exist_ok=True)
                        else:
                            # If it's a file, extract it
                            os.makedirs(os.path.dirname(target_path), exist_ok=True)
                            with (
                                zip_ref.open(member) as source,
                                open(target_path, "wb") as target,
                            ):
                                target.write(source.read())

            print(f"Database contents extracted to: {self.BASE_PATH}")

            # Remove the ZIP file after extraction
            os.remove(self.ZIP_PATH)
            print(f"Deleted ZIP file: {self.ZIP_PATH}")

        except zipfile.BadZipFile:
            raise BaseException(
                "Failed to unzip the database. The file may be corrupted."
            )


if __name__ == "__main__":
    RefractiveIndexDatabase().download_db()
