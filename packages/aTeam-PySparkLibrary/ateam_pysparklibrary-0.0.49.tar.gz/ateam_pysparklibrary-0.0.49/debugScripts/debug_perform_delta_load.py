from pyspark.sql import SparkSession
from delta import *
from pyspark.sql.types import *
from delta.tables import *
from pyspark.sql.functions import *

import sys
sys.path.insert(0, './src/')
from aTeam_PySparkLibrary.perform_delta_load import perform_delta_load


bronze_path = "manual/VarigPropertiesMappedToFazileProperties.csv"
file_extension = 'csv'
dataset_type = 'dim'
dataset_name = 'property_management_group'
business_key_column_name = 'asset_id'



full_bronze_path = f"data/bronze/{bronze_path}"
if dataset_type == "dim":
    full_silver_path = f"data/silver/Dimensions/Delta_executed/{dataset_name.capitalize()}/"
elif dataset_type == "fact":
    full_silver_path = f"data/silver/Facts/Delta_executed/{dataset_name.capitalize()}/"
else:
    print("Dataset type is wrong.")
    raise Exception(f'Dataset type is wrong.') 

builder = SparkSession.builder.appName("debugSession").config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

perform_delta_load(full_bronze_path, full_silver_path, file_extension, dataset_type, dataset_name, business_key_column_name, spark)

spark.stop()