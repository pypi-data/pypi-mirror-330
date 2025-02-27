from pyspark.sql import SparkSession
from delta import *
from pyspark.sql.types import *
from delta.tables import *
from pyspark.sql.functions import *

import sys
sys.path.insert(0, './src/')
from aTeam_PySparkLibrary.propagate_value_over_period import propagate_value_over_period


from datetime import timedelta
from dateutil.relativedelta import relativedelta

silver_path = "Facts/tmp/PropertyEnergyLabelNonMonthly"
new_silver_path = "Facts/PropertyEnergyLabel"

start_date_column_in_input_table = "issuedDate"
end_date_column_in_input_table = "expireDate"
business_key_in_input_table = "asset_id"

date_column_in_output_table = "first_date_in_month"

months_added_in_case_of_null_end_date = 12

time_periods = ["monthly", "quarterly", "yearly"]
time_period = time_periods[2]

read_path = f"data/silver/{silver_path}/"
write_path = f"data/silver/{new_silver_path}/"

builder = SparkSession.builder.appName("debugSession").config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")


propagate_value_over_period(read_path, write_path, start_date_column_in_input_table, end_date_column_in_input_table, date_column_in_output_table,months_added_in_case_of_null_end_date,time_period, spark)

spark.stop()