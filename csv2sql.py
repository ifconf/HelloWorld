import csv
from datetime import datetime

def convert_csv_to_sql(csv_file_path, table_name, date_columns=[]):
    insert_statements = []

    # Open the CSV file
    with open(csv_file_path, mode='r', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        column_names = reader.fieldnames
        
        for row in reader:
            columns = []
            values = []
            for column in column_names:
                columns.append(column)
                value = row[column]
                
                # Handle date columns
                if column in date_columns:
                    # Assume date format is YYYY-MM-DD, adjust if necessary
                    value = datetime.strptime(value, '%Y-%m-%d').strftime('%Y-%m-%d')
                    values.append(f"'{value}'")
                else:
                    # Handle string values
                    if isinstance(value, str):
                        value = value.replace("'", "''")  # Escape single quotes
                        values.append(f"'{value}'")
                    else:
                        values.append(value)
            
            insert_statement = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});"
            insert_statements.append(insert_statement)
    
    return insert_statements

def write_sql_to_file(sql_statements, output_file_path):
    with open(output_file_path, mode='w', newline='') as file:
        for statement in sql_statements:
            file.write(statement + '\n')

# Example usage
csv_file_path = 'data.csv'
table_name = 'my_table'
date_columns = ['birthdate', 'signup_date']  # List of columns containing date values

sql_statements = convert_csv_to_sql(csv_file_path, table_name, date_columns)
output_file_path = 'output.sql'
write_sql_to_file(sql_statements, output_file_path)

print("SQL insert statements have been written to output.sql")
