


provider "google" {
  project = "customerretention-de"
  region  = "us-central1"
}

#create a Google Cloud Storage bucket
resource "google_storage_bucket" "datalake" {
  name     = "customerretention-datalake-bucket" 
  location = "US"
}

#create a BigQuery dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = "customerretention_dataset" 
  location   = "US"

}


resource "google_bigquery_table" "accounts_table" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "accounts"
  schema     = file("accounts_schema.json")
}

resource "google_bigquery_table" "products_table" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "products"
  schema     = file("products_schema.json")
}

resource "google_bigquery_table" "sales_pipeline_table" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "sales_pipeline"
  schema     = file("sales_pipeline_schema.json")
}

resource "google_bigquery_table" "sales_teams_table" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "sales_teams"
  schema     = file("sales_teams_schema.json")
}
