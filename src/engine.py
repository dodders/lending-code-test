import dao
from decimal import Decimal
from operator import itemgetter

# banks is a dict of bank
# facilities is a dict of facility
# covenants is a list of covenant
banks, facilities, covenants = dao.load_inputs()
assignments = []  # (loan.id, facility.id)
yields = {}  # key=facility.id, value=sum of all loan yields
unfunded = []  # list of unfunded loan ids


def get_yield(loan, facility):
    expected_yield = (1 - loan.default_likelihood) * loan.rate * loan.amount \
            - (loan.default_likelihood * loan.amount) \
            - (facility.rate * loan.amount)
    return expected_yield


def is_eligible(loan, facility):
    eligible = True
    print(f'processing eligibility for loan {loan.id} and facility {facility.id}')
    if loan.amount > facility.amount:
        print(f'loan {loan.id} ineligible for facility {facility.id} because loan amount {loan.amount} '
              f'too large for remaining facility amount {facility.amount}')
        return False
    bank_covenants = [c for c in covenants if c.bank_id == facility.bank_id]
    for covenant in bank_covenants:
        # this covenant applies to either a specific facility or all facilities
        if covenant.facility_id == facility.id or covenant.facility_id is None:
            # print('applying covenant ', covenant)
            if covenant.banned_state == loan.state:
                eligible = False
                print(f'ineligible due to state {loan.state}')
                break
            if covenant.max_default_likelihood is not None:
                if loan.default_likelihood > covenant.max_default_likelihood:
                    eligible = False
                    print('ineligible due to default rate ', loan.default_likelihood)
                    break
    return eligible


# assign loan to the cheapest eligible facility id
# update expected yield for that facility too.
# loan_yields is a list of tuples (facility.id, facility.rate, expected_yield)
def allocate(loan, loan_yields):
    # allocate loan and reduce facility amount
    # print(f'allocating loan {loan.id}...')
    loan_yields.sort(key=itemgetter(1))  # sort by yield.
    facility_id = loan_yields[0][0]
    facility = facilities[facility_id]  # facility.id
    facility.amount -= Decimal(loan.amount)
    facilities[facility_id] = facility
    print(f'loan {loan.id} allocated to facility {facility.id} and facility amount reduced to {facility.amount}')
    assignments.append((loan.id, facility_id))

    # update yield for selected facility
    old_yield = yields.get(facility_id, 0)  # default to zero yield if no yield present for this facility
    yields[facility_id] = old_yield + Decimal(loan_yields[0][2])


def process(loan):
    print('processing loan:', loan.id)
    loan_yields = []
    for facility in facilities.values():
        eligible = is_eligible(loan, facility)
        if eligible:
            print(f'loan {loan.id} eligible for facility {facility.id}')
            expected_yield = get_yield(loan, facility)
            if expected_yield < 0:
                print(f'expected yield {expected_yield} for loan {loan.id} from facility {facility.id} is negative. skipping...')
            else:
                loan_yields.append((facility.id, facility.rate, expected_yield))
    if len(loan_yields) > 0:
        # print(f'yields for loan {loan.id}', loan_yields)
        allocate(loan, loan_yields)
    else:
        print(f'oh dear. no eligible facilities for loan {loan.id}')
        unfunded.append(loan.id)
    return yields, assignments
