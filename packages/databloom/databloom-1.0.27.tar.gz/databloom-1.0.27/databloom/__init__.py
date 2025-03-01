from databloom._dynamic import *
from databloom.v1 import Datasource, Dataset
from pyspark.sql import SparkSession

__version__ = "1.0.27"

__all__ = [
    "Datasource",
    "Dataset"
]

__SC__ = None  # Global SparkContext (Singleton-like pattern)

def get_or_create_spark_session():
    """
    Gets or creates a SparkSession.  This ensures we have a single
    SparkContext across the SDK.
    """
    global __SC__
    if __SC__ is None:
        __SC__ = SparkSession.builder\
            .config("spark.jars", "https://jdbc.postgresql.org/download/postgresql-42.7.3.jar,https://repo1.maven.org/maven2/io/trino/trino-jdbc/469/trino-jdbc-469.jar")\
            .appName("DatabloomSDK")\
            .getOrCreate()
    return __SC__