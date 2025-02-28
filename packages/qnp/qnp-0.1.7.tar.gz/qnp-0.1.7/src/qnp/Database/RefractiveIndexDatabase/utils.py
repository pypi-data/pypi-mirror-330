import os
import yaml
import pandas as pd


def get_yaml_catalog(PATH):
    fileName = os.path.join(PATH, "catalog-nk.yml")
    with open(fileName, "rt", encoding="utf-8") as f:
        try:
            return yaml.load(f, Loader=yaml.BaseLoader)
        except Exception:
            raise "database could not found."


def get_yaml_db(PATH):
    fileName = os.path.join(PATH)
    with open(fileName, "rt", encoding="utf-8") as f:
        try:
            return yaml.load(f, Loader=yaml.BaseLoader)
        except Exception:
            raise "database could not found."


def get_df_catalog(PATH):
    sql_catalog = []
    for shelf in get_yaml_catalog(PATH):
        # shelf_name = shelf.get("SHELF")
        # shelf_description = shelf.get("name")

        for book in shelf.get("content"):
            book_name = book.get("name")

            # do nothing for just a divider
            if book_name:
                for page in book.get("content"):
                    divider = page.get("DIVIDER", "")
                    page_name = page.get("name")
                    page_data = page.get("data")

                    # do not make a row for just a divider
                    if page_name:
                        sql_catalog.append([book_name, page_name, page_data, divider])

    df_catalog = pd.DataFrame(sql_catalog)
    df_catalog.columns = ["material", "article", "database_path", "note"]

    return df_catalog
