import csv
import model

banks = {}  # key=id
facilities = {}
covenants = []


# load banks, facilities and covenants
def load():
    with open('../data/banks.csv', 'r') as bank_csv:
        reader = csv.reader(bank_csv)
        next(reader)
        for row in reader:
            banks[row[0]] = model.Bank(row[0], row[1])

    with open('../data/facilities.csv', 'r') as facilities_csv:
        reader = csv.reader(facilities_csv)
        next(reader)
        for row in reader:
            facility = model.Facility(row[3], row[2], row[0], row[1])
            facilities[facility.id] = facility

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


def get_yield(loan, facility):
    expected_yield = (1 - float(loan.default_likelihood)) * float(loan.rate) * float(loan.amount) \
            - (float(loan.default_likelihood) * float(loan.amount)) \
            - (float(facility.rate) * float(loan.amount))
    return expected_yield


def is_eligible(loan, facility):
    eligible = True
    print(f'processing eligibility for loan {loan.id} and facility {facility.id}')
    if float(loan.amount) > float(facility.amount):
        print(f'loan {loan.id} ineligible for facility {facility.id} because loan amount {loan.amount} too large for remaining facility amount {facility.amount}')
        return False
    bank_covenants = [c for c in covenants if c.bank_id == facility.bank_id]
    for covenant in bank_covenants:
        # this covenant applies to either a specific facility or all facilities
        if covenant.facility_id == facility.id or covenant.facility_id == '':
            print('applying covenant ', covenant)
            if covenant.banned_state == loan.state:
                eligible = False
                print('ineligible due to state ', loan.state)
                break
            if covenant.max_default_likelihood != '':
                if float(loan.default_likelihood) > float(covenant.max_default_likelihood):
                    eligible = False
                    print('ineligible due to default rate ', loan.default_likelihood)
                    break
    return eligible


# find the cheapest facility id that has the highest yield for this loan
def allocate(loan, yields):
    print(f'allocating loan {loan.id}')
    for ayield in yields:  # yield is a tuple of facility_id and expected_yield


def process(loan):
    print('processing loan:', loan.id)
    yields = []
    for facility in facilities.values():  # facilities is a dict, so only iterate over the values here
        eligible = is_eligible(loan, facility)
        if eligible:
            print(f'loan {loan.id} eligible for facility {facility.id}')
            expected_yield = get_yield(loan, facility)
            if expected_yield < 0:
                print(f'expected yield {expected_yield} for loan {loan.id} from facility {facility.id} is negative. skipping...')
            else:
                yields.append((facility.id, expected_yield))
    print(f'yields for loan {loan.id}', yields)
    allocate(loan, yields)
