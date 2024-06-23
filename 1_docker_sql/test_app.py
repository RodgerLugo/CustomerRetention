import unittest
import pandas as pd
from app import preprocess_data, train_model

class TestApp(unittest.TestCase):

    def setUp(self):
        # setup for testing
        self.accounts = pd.DataFrame({
            'AccountID': ['A1', 'A2'],
            'Sector': ['Tech', 'Finance'],
            'YearEstablished': [2000, 1995],
            'Revenue': [1200.5, 850.3],
            'Employees': [50, 200],
            'OfficeLocation': ['NY', 'SF'],
            'SubsidiaryOf': [None, 'F1']
        })
        self.products = pd.DataFrame({
            'ProductID': ['P1', 'P2'],
            'SeriesName': ['SeriesA', 'SeriesB'],
            'SalesPrice': [100.0, 150.0]
        })
        self.sales_pipeline = pd.DataFrame({
            'OpportunityID': ['O1', 'O2'],
            'AgentName': ['AgentX', 'AgentY'],
            'ProductName': ['P1', 'P2'],
            'AccountName': ['A1', 'A2'],
            'DealStage': ['Stage1', 'Stage2'],
            'EngageDate': ['2023-01-01', '2023-02-01'],
            'CloseDate': ['2023-06-01', '2023-08-01'],
            'CloseValue': [500, 1000]
        })
        self.sales_teams = pd.DataFrame({
            'AgentID': ['AgentX', 'AgentY'],
            'Manager': ['Manager1', 'Manager2'],
            'RegionalOffice': ['East', 'West']
        })

    def test_preprocess_data(self):
        data = preprocess_data(self.accounts, self.products, self.sales_pipeline, self.sales_teams)
        # Check if the Age column is calculated correctly
        self.assertEqual(data['Age'].iloc[0], 24)
        self.assertEqual(data['Age'].iloc[1], 29)
        # Check if NaN values are filled with 0
        self.assertFalse(data.isnull().values.any())

    def test_train_model(self):
        data = preprocess_data(self.accounts, self.products, self.sales_pipeline, self.sales_teams)
        # The function doesnt have exceptions
        try:
            train_model(data)
        except Exception as e:
            self.fail(f"train_model raised {type(e).__name__} unexpectedly")

if __name__ == '__main__':
    unittest.main()
