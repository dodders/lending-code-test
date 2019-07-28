import loader
import model
from operator import itemgetter

# banks is a dict of bank
# facilities is a dict of facility
# covenants is a list of covenant
banks, facilities, covenants = loader.load()
assignments = []  # list of tuples (loan.id, facility.id)
yields = []


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
# yields is a list of tuples (facility.id, facility.rate, expected_yield)
def allocate(loan, yields):
    print(f'allocating loan {loan.id}...')
    # yields.sort(key=itemgetter(1))  # sort by yield.
    # facility_id = yields[0][0]
    # facility = facilities[facility_id]  # facility.id
    # facility.amount -= loan.amount
    # facilities[facility_id] = facility
    # print(f'loan {loan.id} allocated to facility {facility.id} and facility amount reduced to {facility.amount}')
    # assignments.append((loan.id, facility_id))


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
                yields.append((facility.id, facility.rate, expected_yield))
    print(f'yields for loan {loan.id}', yields)
    allocate(loan, yields)
