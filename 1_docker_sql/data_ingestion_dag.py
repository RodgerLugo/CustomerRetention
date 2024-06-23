from airflow import DAG
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import logging

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

def create_bucket_if_not_exists(bucket_name):
    gcs_hook = GCSHook()
    client = gcs_hook.get_conn()
    try:
        bucket = client.lookup_bucket(bucket_name)
        if bucket:
            logging.info(f'Bucket {bucket_name} already exists.')
        else:
            client.create_bucket(bucket_name)
            logging.info(f'Bucket {bucket_name} created.')
    except Exception as e:
        logging.error(f'Error creating bucket {bucket_name}: {e}')
        raise

with DAG(
    'data_ingestion',
    default_args=default_args,
    description='A simple data ingestion DAG',
    schedule_interval='@daily',
    start_date=days_ago(1),
    tags=['example'],
) as dag:

    create_bucket = PythonOperator(
        task_id='create_bucket',
        python_callable=create_bucket_if_not_exists,
        op_kwargs={'bucket_name': 'customerretention-datalake-bucket'}, 
    )

    upload_accounts_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_accounts_to_gcs',
        src='C:/Users/elroy/Documents/CustomerRetention/1_docker_sql/data/accounts.csv',  
        dst='data/accounts.csv',  
        bucket='customerretention-datalake-bucket',  
        google_cloud_storage_conn_id='google_cloud_default',
    )

    upload_products_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_products_to_gcs',
        src='C:/Users/elroy/Documents/CustomerRetention/1_docker_sql/data/products.csv', 
        dst='data/products.csv',  
        bucket='customerretention-datalake-bucket',  
        google_cloud_storage_conn_id='google_cloud_default',
    )

    upload_sales_pipeline_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_sales_pipeline_to_gcs',
        src='C:/Users/elroy/Documents/CustomerRetention/1_docker_sql/data/sales_pipeline.csv',  
        dst='data/sales_pipeline.csv',  
        bucket='customerretention-datalake-bucket',  
        google_cloud_storage_conn_id='google_cloud_default',
    )

    upload_sales_teams_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_sales_teams_to_gcs',
        src='C:/Users/elroy/Documents/CustomerRetention/1_docker_sql/data/sales_teams.csv', 
        dst='data/sales_teams.csv',  
        bucket='customerretention-datalake-bucket',  
        google_cloud_storage_conn_id='google_cloud_default',
    )

    create_bucket >> [upload_accounts_to_gcs, upload_products_to_gcs, upload_sales_pipeline_to_gcs, upload_sales_teams_to_gcs]
