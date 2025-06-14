import csv
from models.yacht.models.base_yacht.base_yacht import BaseYacht

# Path to your CSV file
CSV_PATH = 'data/seldenBoatList.csv'

# Example function to read CSV and create BaseYacht objects
def import_base_yachts_from_csv(csv_path=CSV_PATH):
    yachts = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert all keys to match BaseYacht __init__ args (if needed)
            # You may need to map/rename keys here if CSV headers differ from BaseYacht fields
            yacht = BaseYacht(**row)
            yachts.append(yacht)
    return yachts

if __name__ == '__main__':
    yachts = import_base_yachts_from_csv()
    print(f'Imported {len(yachts)} yachts.')
    # Optionally, print the first yacht for inspection
    if yachts:
        print(vars(yachts[0]))
