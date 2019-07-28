import csv
import model


# load banks, facilities and covenants
def load():
    banks = []
    with open('../data/banks.csv', 'r') as bank_csv:
        reader = csv.reader(bank_csv)
        next(reader)
        for row in reader:
            banks.append(model.Bank(row[0], row[1]))

    facilities = {}
    with open('../data/facilities.csv', 'r') as facilities_csv:
        reader = csv.reader(facilities_csv)
        next(reader)
        for row in reader:
            facility = model.Facility(row[3], row[2], row[0], row[1])
            facilities[facility.id] = facility

    covenants = []
    with open('../data/covenants.csv', 'r') as covenant_csv:
        reader = csv.reader(covenant_csv)
        next(reader)
        for row in reader:
            covenant = model.Covenant(row[2], row[0], row[1], row[3])
            covenants.append(covenant)

    print('loaded.')
    print('banks', banks)
    print('facilities', facilities)
    print('covenants', covenants)
    return banks, facilities, covenants

