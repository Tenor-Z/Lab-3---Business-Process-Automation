import sys
import os
import pandas
from datetime import date
import re

def main():
    sales_csv = get_sales_csv()
    orders_dir = create_orders_dir(sales_csv)
    process_sales_data(sales_csv, orders_dir)

# Get path of sales data CSV file from the command line
def get_sales_csv():
    # Check whether command line parameter provided
    num_params = len(sys.argv) - 1
    if num_params >= 1:
        csv_path = sys.argv[1]
        # Check whether provide parameter is valid path of file
        if os.path.isfile(csv_path):
            return csv_path
        else:
            print("Error: CSV file does not exist.")
            sys.exit(1)
    else:
        print("Error: Missing CSV file path parameter.")
        sys.exit(1)

    return

# Create the directory to hold the individual order Excel sheets
def create_orders_dir(sales_csv):
    # Get directory in which sales data CSV file resides
    sales_dir = os.path.dirname(sales_csv)
    # Determine the name and path of the directory to hold the order data files
    todays_date = date.today().isoformat()
    orders_directory_name = f'Orders{todays_date}'
    orders_path = os.path.join(sales_dir, orders_directory_name)
    # Create the order directory if it does not already exist
    if not os.path.isdir(orders_path):
        os.makedirs(orders_path)
    return orders_path

# Split the sales data into individual orders and save to Excel sheets
def process_sales_data(sales_csv, orders_dir):
    sales_df = pandas.read_csv(sales_csv)
    sales_df.insert(7, 'TOTAL PRICE', sales_df['ITEM QUANTITY'] * sales_df['ITEM PRICE'])
    # Import the sales data from the CSV file into a DataFrame
    # Insert a new "TOTAL PRICE" column into the DataFrame
    # Remove columns from the DataFrame that are not needed
    sales_df.drop(columns=['ADDRESS','CITY','STATE','POSTAL CODE','COUNTRY'], inplace=True)
    # Group the rows in the DataFrame by order ID
    for order_id, order_df in sales_df.groupby('ORDER ID'):

    # For each order ID:
        # Remove the "ORDER ID" column
        order_df.drop(columns=['ORDER ID'], inplace=True)
        # Sort the items by item number
        order_df.sort_values(by='ITEM NUMBER', inplace=True)
        # Append a "GRAND TOTAL" row
        the_total = order_df['TOTAL PRICE'].sum()
        grand_total = pandas.DataFrame({'ITEM PRICE': ['GRAND TOTAL:'], 'TOTAL PRICE': [the_total]})
        order_df = pandas.concat([order_df, grand_total])
        # Determine the file name and full path of the Excel sheet
        customer_name = order_df['CUSTOMER NAME'].values[0]
        customer_name = re.sub(r'\W','',customer_name)
        order_file_name = f'Order{order_id}_{customer_name}.xlsx'
        order_path = os.path.join(orders_dir, order_file_name)
        # Export the data to an Excel sheet
        sheetname = f'ORDER {order_id}'
        order_df.to_excel(order_path, index=False, sheet_name=sheetname)
        # TODO: Format the Excel sheet
        #print(order_df)

if __name__ == '__main__':
    main()