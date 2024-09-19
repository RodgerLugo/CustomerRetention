# Customer Retention Prediction Project

## Overview

This project centers on developing a data-driven solution to predict customer churn. The primary focus is on using advanced data engineering techniques to automate data processing pipelines, optimize storage, and enhance accessibility, while also leveraging machine learning models to deliver predictive insights that inform customer retention strategies.

## Objectives

- **Data Engineering**: Design and implement robust, scalable ETL pipelines that extract data from various sources, transform it for analysis, and load it into a data warehouse for further processing.
- **Machine Learning**: Develop a Random Forest classifier to predict customer churn based on historical customer data, providing actionable insights that can guide business decisions.
- **Cloud Infrastructure**: Leverage Google Cloud Platform services (BigQuery, Google Cloud Storage) for storage and querying of large datasets.
- **CI/CD and Automation**: Ensure seamless deployment of data pipelines and machine learning models using CI/CD practices through GitHub Actions and Makefile automation.

## Key Features

- **Automated ETL Pipelines**: Using Apache Airflow, data is automatically ingested from Google Cloud Storage, transformed, and loaded into BigQuery. The pipelines are scheduled and monitored to ensure reliability.
- **Data Transformation & Aggregation**: Feature engineering is performed using BigQuery SQL queries to prepare the data for model training. This includes creating new features such as customer age, revenue segmentation, and churn labels.
- **Machine Learning Integration**: A Random Forest classifier is used to predict customer churn. The model is trained on processed data from BigQuery and evaluated for accuracy using metrics like ROC-AUC and F1-score.
- **Visualization**: Google Data Studio is used to create dynamic dashboards that visualize key metrics, such as customer churn rate, sales trends, and customer demographics, offering real-time insights for stakeholders.

## Technologies Used

* **Python**: For data preprocessing and machine learning model development.
* **Apache Airflow**: Orchestrates ETL workflows.
* **BigQuery**: Stores and queries the transformed data.
* **Google Cloud Storage**: Data lake for storing raw CSV files.
* **Docker & Docker Compose**: Ensures consistent environments for development and deployment.
* **Terraform**: Automates infrastructure provisioning.
* **GitHub Actions**: CI/CD pipeline for automated testing and deployment.
* **Google Data Studio**: Visualizes key metrics and model results.

## Data Pipeline Overview

1. **Data Extraction**: Raw customer data from multiple CSV files is stored in Google Cloud Storage.
2. **Data Transformation**: Data is processed using BigQuery SQL scripts to clean and enrich features (e.g., customer age, revenue).
3. **Model Training**: A Random Forest Classifier is used to predict customer churn based on the processed features.
4. **ETL Orchestration**: Apache Airflow manages the entire process, automating tasks on a daily schedule.
5. **Visualization**: Key metrics and model predictions are visualized in a Google Data Studio dashboard, providing insights to stakeholders.

## Key Results

- Successfully built an end-to-end data pipeline that automates the ingestion, transformation, and storage of customer data.
- Achieved a predictive accuracy of 94% using the Random Forest model, offering valuable insights for business decisions.
- Real-time dashboards provide stakeholders with a comprehensive view of customer churn trends and key metrics.


 **Access the Customer Retention Project**:
    - The dashboard link can be found [here](https://sites.google.com/view/rodgerlc-customer-retention/customer-retention-dashboard).
