### author: Martin Nenseth / Ludvig Løite / Magnus Erdvik


from .helpFunctions.exists_and_has_files import exists_and_has_files

from pyspark.sql import functions as F
from pyspark.sql.functions import coalesce, row_number
from pyspark.sql.window import Window
from pyspark.sql.functions import lit, when, col



def perform_delta_load(full_bronze_path, full_silver_path, file_extension, dataset_type, dataset_name, business_key_column_name, spark):
    """
    This function performs a delta load from bronze to silver and primary key generation
    Parameters:
        full_bronze_path: str
            The full path to the bronze dataset
            Example: abfss://bronze@example.dfs.core.windows.net/folder/Dataset/DatasetName.parquet
        full_silver_path: str
            The full path to the silver dataset
            Example: abfss://silver@example.dfs.core.windows.net/folder/Dimensions/DatasetName/
        file_extension: str
            The file extension of the bronze dataset
            Example: 'csv', 'parquet'
        dataset_type: str
            The type of the dataset
            Example: 'dim', 'fact'
        dataset_name: str
            The name of the dataset
            Example: 'date', 'sales'
        business_key_column_name: str
            The name of the business key column
            Example: 'date_id', 'sales_id' 
        spark: SparkSession
            The SparkSession used in the notebook, can be passed on to the function as "spark" withouth any additional code
    Returns:
        None
    """
    print("Performing delta load for dataset ",dataset_type,'_', dataset_name,", using ", business_key_column_name, " as business key")
    print("full bronze path: ",full_bronze_path)
    print("checking if delta load exist here:" ,f"{full_silver_path}_delta_log")

    bronze_df = get_bronze_df(file_extension, full_bronze_path, spark)
    dataset_key_name = 'silver_pk_' + dataset_type + '_' + dataset_name + '_key'
    
    if(exists_and_has_files(full_silver_path, spark)):
        print("Dataset already exists, executing delta load")

        #read silver dataset
        silver_dataset_df = spark.read.format('delta').load(full_silver_path)
        #if new columns from bronze add them to silver dataset
        silver_dataset_df = add_new_columns_from_bronze_to_silver_dataset_df(silver_dataset_df, bronze_df)

        # join bronze and silver
        bronze_df_alias_prefix = bronze_df.select([F.col(c).alias("bronze_"+c) for c in bronze_df.columns])
        silver_df_alias_prefix = silver_dataset_df.select([F.col(c).alias("silver_"+c) for c in silver_dataset_df.columns])
        joined = bronze_df_alias_prefix.join(silver_df_alias_prefix, bronze_df_alias_prefix['bronze_' + business_key_column_name] == silver_df_alias_prefix['silver_' + business_key_column_name], how='full_outer')
        select_expression = create_select_expression(dataset_key_name, bronze_df)
        merged = joined.select(select_expression)

        #generate unique ids for new rows
        max_key = merged.selectExpr(f"max({dataset_key_name}) as key").collect()[0].key
        #filter out rows without key
        new_rows_without_key = merged.filter(merged[dataset_key_name].isNull())
        new_rows_array = []
        #generate new keys
        for row in new_rows_without_key.collect():
            max_key = max_key + 1
            row_dict = row.asDict()
            row_dict[dataset_key_name] = max_key
            new_rows_array.append(tuple(row_dict.values()))
        new_rows_with_generated_key = spark.createDataFrame(new_rows_array, merged.schema)

        #combine new rows with existing
        upserted_rows = merged.filter(merged[dataset_key_name].isNotNull()).union(new_rows_with_generated_key)
        # remove prefix from column names
        upserted_rows_without_prefix_column_names = upserted_rows.withColumnRenamed(dataset_key_name, dataset_key_name.replace('silver_', ''))

        upserted_rows_without_prefix_column_names = upserted_rows_without_prefix_column_names.withColumn('business_key_deleted_in_source', lit(False))

        fixedSchema = spark.createDataFrame(upserted_rows_without_prefix_column_names.collect(), schema=upserted_rows_without_prefix_column_names.schema)
        #add flag indicating business_key/row has been removed in source
        business_keys_in_silver_not_in_bronze = fixedSchema.join(bronze_df, on=[business_key_column_name], 
            how='left_anti').select(business_key_column_name).rdd.flatMap(lambda x: x).collect()

        fixedSchema = fixedSchema.withColumn('business_key_deleted_in_source', lit(False))
        fixedSchema = fixedSchema.withColumn("business_key_deleted_in_source", 
            when(col(business_key_column_name).isin(business_keys_in_silver_not_in_bronze), True).otherwise(fixedSchema["business_key_deleted_in_source"]))
        
        fixedSchema.write.option("mergeSchema", "true").format('delta').mode("overwrite").save(full_silver_path)
        
        
        # upserted_rows_without_prefix_column_names.write.option("mergeSchema", "true") .format('delta').mode("overwrite").save(full_silver_path) // old code that worked before adding the business_key_deleted_in_source column
        #TODO: Validate unique business and dataset keys

        print("Delta load executed. Silver path: ", full_silver_path)
        #maybe do som validation
    else:
        print("Dataset does not exists in silver, create it for the first time")
        #create unique ids for all rows in bronze_df
        window_spec = Window.orderBy(business_key_column_name)
        df_with_consecutive_id = bronze_df.withColumn(dataset_key_name.replace('silver_', ''), row_number().over(window_spec) - 1)

        df_with_consecutive_id = df_with_consecutive_id.withColumn('business_key_deleted_in_source', lit(False))

        #write to silver
        df_with_consecutive_id.write.format('delta').mode("append").option("mergeSchema", "true").save(full_silver_path)
        print("Dataset created for the first time. Silver path: ", full_silver_path)
        

def create_select_expression(dataset_key_name, bronze_df):
    column_names = []
    for col in bronze_df.dtypes:
        column_names.append(col[0])

    select_exprs = []
    for column in column_names:
        select_exprs.append(coalesce(f"bronze_{column}", f"silver_{column}").alias(column))

    select_exprs.append(dataset_key_name)
    return select_exprs

def get_bronze_df(file_extension, full_bronze_path, spark):
    if file_extension == 'csv':
        bronze_df = spark.read.option("header", "true").csv(full_bronze_path)
        #remove whitespace in column names
        bronze_df = bronze_df.toDF(*[col.replace(" ", "") for col in bronze_df.columns])
    elif file_extension == 'parquet':
        bronze_df = spark.read.parquet(full_bronze_path)
    elif file_extension == 'table':
        bronze_df = spark.read.table(full_bronze_path)
    else:
        print("File extension not supported")
        raise Exception(f'File extension not supported.')
    return bronze_df
    
# Iterate over columns in bronze_df
def add_new_columns_from_bronze_to_silver_dataset_df(silver_dataset_df, bronze_df):
    for column in bronze_df.columns:
        # Check if column exists in silver_dataset_df
        if column not in silver_dataset_df.columns:
            # Add the column to silver_dataset_df
            silver_dataset_df = silver_dataset_df.withColumn(column, lit(None).cast(bronze_df.schema[column].dataType))
    return silver_dataset_df