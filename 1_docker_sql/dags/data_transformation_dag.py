from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

with DAG(
    'data_lake_to_warehouse',
    default_args=default_args,
    description='A simple data lake to warehouse DAG',
    schedule_interval='@daily',
    start_date=days_ago(1),
    tags=['example'],
) as dag:

    load_accounts_to_bigquery = GCSToBigQueryOperator(
        task_id='load_accounts_to_bigquery',
        bucket='customerretention-datalake-bucket',  
        source_objects=['data/accounts.csv'], 
        destination_project_dataset_table='customerretention_dataset.accounts',
        source_format='CSV',
        skip_leading_rows=1,
        write_disposition='WRITE_TRUNCATE',
    )

    load_products_to_bigquery = GCSToBigQueryOperator(
        task_id='load_products_to_bigquery',
        bucket='customerretention-datalake-bucket',
        source_objects=['data/products.csv'],
        destination_project_dataset_table='customerretention_dataset.products',
        source_format='CSV',
        skip_leading_rows=1,
        write_disposition='WRITE_TRUNCATE',
    )

    load_sales_pipeline_to_bigquery = GCSToBigQueryOperator(
        task_id='load_sales_pipeline_to_bigquery',
        bucket='customerretention-datalake-bucket',
        source_objects=['data/sales_pipeline.csv'],
        destination_project_dataset_table='customerretention_dataset.sales_pipeline',
        source_format='CSV',
        skip_leading_rows=1,
        write_disposition='WRITE_TRUNCATE',
    )

    load_sales_teams_to_bigquery = GCSToBigQueryOperator(
        task_id='load_sales_teams_to_bigquery',
        bucket='customerretention-datalake-bucket',
        source_objects=['data/sales_teams.csv'],
        destination_project_dataset_table='customerretention_dataset.sales_teams',
        source_format='CSV',
        skip_leading_rows=1,
        write_disposition='WRITE_TRUNCATE',
    )


    transform_data = BigQueryInsertJobOperator(
        task_id='transform_data',
        configuration={
            "query": {
                "query": """
                CREATE OR REPLACE TABLE customerretention_dataset.transformed_data AS
                SELECT
                  a.account AS AccountID,
                  a.sector AS Sector,
                  a.year_established AS YearEstablished,
                  a.revenue AS Revenue,
                  a.employees AS Employees,
                  a.office_location AS OfficeLocation,
                  a.subsidiary_of AS SubsidiaryOf,
                  2024 - a.year_established AS Age,
                  CASE
                    WHEN a.revenue > 1000 THEN 0  -- Assumed non-churned if revenue is greater than 1000
                    ELSE 1                      -- Assumed churned otherwise
                  END AS Churn
                FROM
                  customerretention_dataset.accounts a;
                """,
                "useLegacySql": False,
            }
        }
    )

    [load_accounts_to_bigquery, load_products_to_bigquery, load_sales_pipeline_to_bigquery, load_sales_teams_to_bigquery] >> transform_data
