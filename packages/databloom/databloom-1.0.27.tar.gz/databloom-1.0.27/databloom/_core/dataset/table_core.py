import pyspark
import os

class TableBase:
    """
    This database is a palantir database
    """
    table_name = "" # khi một table object được khởi tạo sẽ overwrite lại biến này là tên table thật, giờ a hard code nha
    db_name = ""
    trino_credential = {
        "host": "trino.ird.vng.vn",
        "port": 443,
        "user": "trino",
        "password": os.environ.get("TRINO_PASSWORD"),
        "catalog_name": "unity",
        "schema_name": "public", # db name 
    } # credential to connect to source

    def __init__(self, db_name: str) -> None:
        self.set_db_name(db_name)
        pass

    def set_db_name(self, db_name: str):
        self.db_name = db_name
        self.trino_credential["schema_name"] = db_name

    def write_df(self, df: pyspark.sql.DataFrame):
        """
        Write a DataFrame to a dataset
        """
        trino_jdbc_url = (
            f"jdbc:trino://"
            f"{self.trino_credential['host']}:"
            f"{self.trino_credential['port']}/"
            f"{self.trino_credential['catalog_name']}/"
            f"{self.trino_credential['schema_name']}"
            f"?user={self.trino_credential['username']}"
            f"&password={self.trino_credential['password']}"
        )
        df.write \
            .format("jdbc") \
            .option("url", trino_jdbc_url) \
            .option("driver", "io.trino.jdbc.TrinoDriver") \
            .option("dbtable", self.table_name) \
            .option("isolationLevel", "NONE") \
            .mode("overwrite") \
            .save()

        print("Done write to trino")