import boto3
import csv
import os
from datetime import datetime
from io import StringIO
import tempfile

class ExpenseExporter:
    """
    A class to export expense data from DynamoDB based on date range.
    
    This library queries DynamoDB for expense records within a specified date range
    and exports them to a CSV file for download.
    """
    
    def __init__(self, table_name, region_name='us-east-1'):
        """
        Initialize the ExpenseExporter.
        
        Args:
            table_name (str): The name of the DynamoDB table containing expense data
            region_name (str, optional): AWS region name. Defaults to 'us-east-1'.
        """
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.table = self.dynamodb.Table(table_name)
    
    def get_expenses_by_date_range(self, user_id, start_date, end_date):
        """
        Retrieve expense records from DynamoDB for a specific user within a date range.
        
        Args:
            user_id (str): The user identifier (used in PK)
            start_date (str): Start date in ISO format (YYYY-MM-DD)
            end_date (str): End date in ISO format (YYYY-MM-DD)
            
        Returns:
            list: List of expense items matching the query
        """
        # Validate date formats
        try:
            datetime.fromisoformat(start_date)
            datetime.fromisoformat(end_date)
        except ValueError:
            raise ValueError("Dates must be in ISO format (YYYY-MM-DD)")
            
        # Using the user-date-index GSI to query by date range
        response = self.table.query(
            IndexName='user-date-index',
            KeyConditionExpression='PK = :pk AND #date BETWEEN :start_date AND :end_date',
            ExpressionAttributeNames={
                '#date': 'date'
            },
            ExpressionAttributeValues={
                ':pk': f"USER-{user_id}",
                ':start_date': start_date,
                ':end_date': end_date
            }
        )
        
        return response.get('Items', [])
    
    def export_to_csv(self, expenses):
        """
        Convert expense items to CSV format.
        
        Args:
            expenses (list): List of expense items from DynamoDB
            
        Returns:
            StringIO: CSV data as StringIO object
        """
        if not expenses:
            raise ValueError("No expenses found to export")
            
        # Get all unique keys from all expenses to use as CSV headers
        fieldnames = set()
        for expense in expenses:
            fieldnames.update(expense.keys())
        
        # Sort fieldnames to ensure consistent column order
        fieldnames = sorted(list(fieldnames))
        
        # Create CSV in memory
        csv_output = StringIO()
        writer = csv.DictWriter(csv_output, fieldnames=fieldnames)
        writer.writeheader()
        
        for expense in expenses:
            writer.writerow(expense)
            
        csv_output.seek(0)
        return csv_output
    
    def save_to_file(self, csv_data, filename=None):
        """
        Save CSV data to a temporary file.
        
        Args:
            csv_data (StringIO): CSV data as StringIO object
            filename (str, optional): Filename for the CSV. Defaults to generated filename.
            
        Returns:
            str: Path to the saved temporary file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"expenses_{timestamp}.csv"
            
        # Create a temporary file that will be automatically cleaned up
        temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.csv')
        temp_file.write(csv_data.getvalue())
        temp_file.close()
        
        return temp_file.name
    
    def generate_expense_report(self, user_id, start_date, end_date, filename=None):
        """
        Generate an expense report for a user within a specified date range.
        
        Args:
            user_id (str): The user identifier
            start_date (str): Start date in ISO format (YYYY-MM-DD)
            end_date (str): End date in ISO format (YYYY-MM-DD)
            filename (str, optional): Custom filename for the CSV export
            
        Returns:
            dict: Report information including file path and summary statistics
        """
        # Get expense data
        expenses = self.get_expenses_by_date_range(user_id, start_date, end_date)
        
        if not expenses:
            return {
                'success': False,
                'message': f"No expenses found between {start_date} and {end_date}",
                'count': 0
            }
        
        # Export to CSV
        csv_data = self.export_to_csv(expenses)
        
        # Save to file
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"expenses_{user_id}_{timestamp}.csv"
            
        file_path = self.save_to_file(csv_data, filename)
        
        # Calculate some basic stats
        total_expenses = len(expenses)
        
        # You could add more stats here if needed, like total amount, categories, etc.
        # depending on what fields are in your expense records
        
        return {
            'success': True,
            'file_path': file_path,
            'filename': os.path.basename(file_path),
            'count': total_expenses,
            'start_date': start_date,
            'end_date': end_date
        }