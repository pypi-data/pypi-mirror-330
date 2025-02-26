# my_sample_package/db_operations.py

from pyspark.sql import SparkSession

def select_all_from_table(table_name: str, spark: SparkSession):
    """
    Simple function to run SELECT * on a given table using Spark SQL.
    
    :param table_name: Name of the table to query (e.g., "my_db.my_table")
    :param spark:      The Spark session
    :return:           A Spark DataFrame with the results
    """
    # Build the query
    query = f"SELECT * FROM {table_name}"
    
    # Run the query
    df = spark.sql(query)
    
    return df
