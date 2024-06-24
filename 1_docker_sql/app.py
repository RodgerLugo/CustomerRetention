import os
import pandas as pd
from google.cloud import bigquery
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
import joblib
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, this is your customer retention application."



# Set the Google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/credentials.json"

def load_data():
    # Load data from the local files in the data directory
    accounts_path = os.path.join('data', 'accounts.csv')
    products_path = os.path.join('data', 'products.csv')
    sales_pipeline_path = os.path.join('data', 'sales_pipeline.csv')
    sales_teams_path = os.path.join('data', 'sales_teams.csv')

    accounts = pd.read_csv(accounts_path, dtype={'AccountID': str})
    products = pd.read_csv(products_path, dtype={'ProductID': str})
    sales_pipeline = pd.read_csv(sales_pipeline_path, dtype={'OpportunityID': str}) 
    sales_teams = pd.read_csv(sales_teams_path, dtype={'AgentID': str})

    # Renaming columns to match schema
    accounts.rename(columns={
        'account': 'AccountID',
        'sector': 'Sector',
        'year_established': 'YearEstablished',
        'revenue': 'Revenue',
        'employees': 'Employees',
        'office_location': 'OfficeLocation',
        'subsidiary_of': 'SubsidiaryOf'
    }, inplace=True)

    products.rename(columns={
        'product': 'ProductID',
        'series': 'SeriesName',
        'sales_price': 'SalesPrice'
    }, inplace=True)

    sales_pipeline.rename(columns={
        'opportunity_id': 'OportunityID',
        'sales_agent': 'AgentName',
        'product': 'ProductName',
        'account': 'AccountName',
        'deal_stage': 'DealStage',
        'engage_date': 'EngageDate',
        'close_date': 'CloseDate',
        'close_value': 'CloseValue'
    }, inplace=True)

    sales_teams.rename(columns={
        'sales_agent': 'AgentID',
        'manager': 'Manager',
        'regional_office': 'RegionalOffice'
    }, inplace=True)

    return accounts, products, sales_pipeline, sales_teams


def preprocess_data(accounts, products, sales_pipeline, sales_teams):
    # Data preprocessing
    accounts.fillna(0, inplace=True)
    accounts['YearEstablished'] = accounts['YearEstablished'].astype(int)
    accounts['Revenue'] = accounts['Revenue'].astype(float)
    accounts['Employees'] = accounts['Employees'].astype(int)

    
    #  feature engineering
    accounts['Age'] = 2024 - accounts['YearEstablished']
    
    # Print the distribution of revenue
    print(accounts['Revenue'].describe())
    
    return accounts

def train_model(data):
    # Prepare data for modeling
    features = ['Revenue', 'Employees', 'Age']
    X = data[features].drop_duplicates()
    y = data['Revenue'] > 1000    # Lower threshold to ensure both classes are present

    # Check distribution of target variable
    print(y.value_counts())

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Check distribution in train and test sets
    print(y_train.value_counts())
    print(y_test.value_counts())

    # Train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy:.2f}')

    # Check shape of predicted probabilities
    y_pred_proba = model.predict_proba(X_test)
    print(y_pred_proba.shape)

    # Ensure two classes are present for roc_auc_score
    if y_pred_proba.shape[1] > 1:
        roc_auc = roc_auc_score(y_test, y_pred_proba[:, 1])
        print(f'ROC-AUC: {roc_auc:.2f}')
    else:
        print("ROC-AUC cannot be calculated because only one class is present.")

    print(classification_report(y_test, y_pred, zero_division=0))

    # Save the model
    joblib.dump(model, 'customer_churn_model.pkl')

if __name__ == "__main__":
    accounts, products, sales_pipeline, sales_teams = load_data()
    data = preprocess_data(accounts, products, sales_pipeline, sales_teams)
    train_model(data)
    app.run(host='0.0.0.0', port=8080)

