def get_lakehouse_path(lakehouse_name: str, fabric) -> str:
    """
    Get the Azure Blob File System (ABFS) path of the lakehouse.
 
    :param lakehouse_name: Name of the lakehouse.
    :param fabric: Fabric object.
    :returns: ABFS path of the lakehouse.
    """
    workspace_id = fabric.get_workspace_id()
    workspace_name = fabric.resolve_workspace_name(workspace_id)
 
    lakehouse_name = lakehouse_name.lower()
 
    client = fabric.FabricRestClient()
    response = client.get(f"/v1/workspaces/{workspace_id}/lakehouses")
    json_response = response.json()
 
    lakehouse_id = ''
 
    for value in json_response['value']:
        lh_name = value['displayName'].lower()
        lh_id = value['id']
        #print(lakehouse_name, ' ', lakehouse_id)
        if lh_name == lakehouse_name:
            lakehouse_id = lh_id
 
    return f'abfss://{workspace_id}@onelake.dfs.fabric.microsoft.com/{lakehouse_id}'
 
 
# lh_silver_ab_base_path = get_lakehouse_path("lh_silver") + "/Tables/";
# lh_gold_ab_base_path = get_lakehouse_path("lh_gold") + "/Tables/";
# sample_df = spark.read.format("delta").load(lh_silver_ab_base_path + "sample")
# sample_sample_df.write.format("delta").mode("overwrite").option("overwriteSchema", "True").save(lh_gold_ab_base_path + 'sample')
# df = spark.read.format("json").load(get_lakehouse_path("lh_bronze") + "/Files/Sample/sample.json")