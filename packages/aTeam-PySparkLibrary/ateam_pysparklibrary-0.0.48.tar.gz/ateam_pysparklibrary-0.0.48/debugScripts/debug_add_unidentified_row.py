from pyspark.sql import SparkSession
from delta import *
from pyspark.sql.types import *
from delta.tables import *
from pyspark.sql.functions import *

import sys
sys.path.insert(0, './src/')
from aTeam_PySparkLibrary.add_unidentified_row import add_unidentified_row


directoryLevel = 'silver'
folderPath = "Dimensions/PropertyManagementGroup/"
businessKeyColumn  = "asset_id"
dimensionKeyColumn = "pk_dim_property_management_group_key"
storageAccName = "pedataplatformdev"

fullPath = f"data/silver/{folderPath}"




builder = SparkSession.builder.appName("debugSession").config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")


add_unidentified_row(fullPath, businessKeyColumn, dimensionKeyColumn, spark)
spark.stop()