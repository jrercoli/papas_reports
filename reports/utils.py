import csv


def string_to_csv(input_string, output_file):
    # Split the input string by newline character to get individual rows
    rows = input_string.strip().split('\n')
    # Write the rows to a CSV file using csv.writer
    with open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in rows:
            # Split each row by comma to get individual cells
            cells = row.split(',')
            # Write the cells as a row in the CSV file
            csv_writer.writerow(cells)
    return csv_file
