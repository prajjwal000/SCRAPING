import sqlite3
import csv
import os

def export_tables_to_csv(db_file, output_dir):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get the list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table_name in tables:
        table_name = table_name[0]  # Extract the table name from the tuple
        print(f'Exporting table: {table_name}')

        # Query all data from the table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]

        # Write to CSV file
        csv_file_path = os.path.join(output_dir, f"{table_name}.csv")
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_names)  # Write header
            writer.writerows(rows)          # Write data

    # Close the database connection
    conn.close()
    print("Export completed.")

# Usage
db_file = 'imdb.db'  # Replace with your SQLite database file
output_dir = 'output_csv'         # Replace with your desired output directory
export_tables_to_csv(db_file, output_dir)

