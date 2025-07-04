# Databricks notebook source
import dlt
from pyspark.sql.functions import col, lit
from pyspark.sql.types import StructType, StructField, StringType

schema_csv = StructType([
  StructField("Description", StringType(), nullable=True),
  StructField("Name", StringType(), nullable=True),
  StructField("value", StringType(), nullable=True)
])

cloud_file_options = {
  "cloudFiles.format": "csv"
}

@dlt.table(
  name="bronze_readstream_load"
)
def bronze_load():
    df = spark.readStream.format("cloudFiles").options(**cloud_file_options).schema(schema_csv).load("/Volumes/dlt/deltalivetables/delta/")
    return df

@dlt.table(
  name="dataQuality_table_1"
)
@dlt.expect_or_drop("validate Description column for null values", "Description is Not Null")
def dataQuality_table_1():
  df = dlt.read_stream("bronze_readstream_load")
  return df

@dlt.table(
  name="dataQuality_table_2"
)
@dlt.expect_or_drop("validate Name column for null values", "Name is Not Null")
def dataQuality_table_2():
  df = dlt.read_stream("bronze_readstream_load")
  return df

checks={}
checks["validate Name column for null values"]="(Name is Not Null)"
checks["validate Description column for null values"]="(Description is Not Null)"
checks["validate value column for null values"]="(value is Not Null)"

@dlt.view
@dlt.expect_all_or_drop(checks)
def dataQuality_table_2():
  df = dlt.read_stream("bronze_readstream_load")
  return df

@dlt.table(
  name="all_checks"
)
def dataQuality_table_2():
  df = dlt.read_stream("dataQuality_table_2")
  return df


