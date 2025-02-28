import os
import pandas as pd
from io import StringIO
from qnp.Database.RefractiveIndexDatabase.utils import get_df_catalog, get_yaml_db


class RefractiveIndexDatabase:
    PATH = os.path.join(os.path.expanduser("~"), ".QNP", "Databases", "RefractiveIndex")

    def __init__(self):
        self.catalog = get_df_catalog(self.PATH)

    def search(self, material: str = None, article: str = None):
        if material and article:
            query = self.catalog.material.str.contains(
                material
            ) & self.catalog.article.str.contains(article)

        elif material:
            query = self.catalog.material.str.contains(material)

        elif article:
            query = self.catalog.article.str.contains(article)

        else:
            raise BaseException(
                "you have to search with atleast one field: material or(and) article"
            )

        return self.catalog[query]

    def get_data(self, id: int, logs: bool = True):
        material = self.catalog.iloc[id]
        database_path = os.path.join(self.PATH, "data-nk", material.database_path)
        db = get_yaml_db(database_path)

        article = db.get("REFERENCES")
        comments = db.get("COMMENTS", "")

        if len(db.get("DATA")[0]) == 1:
            print("warning... losing some data")
        raw_data = db.get("DATA")[0].get("data")
        df = pd.read_csv(StringIO(raw_data), sep=" ", names=["wavelength", "n", "k"])
        df["epsilon"] = (df.n + df.k * 1j) ** 2

        if logs:
            print(material.material)
            print(article)
            print(comments)

        return df
