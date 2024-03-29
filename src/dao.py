import csv
import model

root = '../data/'
yields_hdr = ['facility_id', 'expected_yield']
assignments_hdr = ['loan_id', 'facility_id']
unfunded_hdr = ['loan_id']


def save_unfunded(loans):
    with open(root + 'unfunded.loans.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(unfunded_hdr)
        writer.writerows(loans)


def save_assignments(assignments):  # assignments is a list
    with open(root + 'assignments.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(yields_hdr)
        writer.writerows(assignments)


def save_yields(yields):  # yields is a dict
    with open(root + 'yields.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(assignments_hdr)
        for item in yields.items():
            row = [item[0], str(round(item[1]))]
            writer.writerow(row)


# load banks, facilities and covenants
def load_inputs():
    banks = []
    with open(root + 'banks.csv', 'r') as bank_csv:
        reader = csv.reader(bank_csv)
        next(reader)
        for row in reader:
            banks.append(model.Bank(row[0], row[1]))

    facilities = {}
    with open(root + 'facilities.csv', 'r') as facilities_csv:
        reader = csv.reader(facilities_csv)
        next(reader)
        for row in reader:
            facility = model.Facility(row[3], row[2], row[0], row[1])
            facilities[facility.id] = facility

    covenants = []
    with open(root + 'covenants.csv', 'r') as covenant_csv:
        reader = csv.reader(covenant_csv)
        next(reader)
        for row in reader:
            covenant = model.Covenant(row[2], row[0], row[1], row[3])
            covenants.append(covenant)

    print('loaded.')
    # print('banks', banks)
    # print('facilities', facilities)
    # print('covenants', covenants)
    return banks, facilities, covenants


def load_loans():
    loans = []
    with open(root + 'loans.csv', 'r') as loans_csv:
        reader = csv.reader(loans_csv)
        next(reader)  # skip header
        for row in reader:
            loan = model.Loan(row[2], row[1], row[0], row[3], row[4])
            loans.append(loan)
    return loans
