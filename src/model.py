class Bank:
    def __init__(self, bank_id, name):
        self.id = bank_id
        self.name = name

    def __str__(self):
        return 'id:' + self.id + ' name:' + self.name

    def __repr__(self):
        return 'id:' + self.id + ' name:' + self.name


class Facility:
    def __init__(self, bank_id, facility_id, amount, rate):
        self.bank_id = bank_id
        self.id = facility_id
        self.amount = float(amount)
        self.rate = float(rate)

    def __repr__(self):
        return f'bank id: {self.bank_id} facility id: {self.id} \
               amount: {self.amount} rate: {self.rate}'


class Covenant:
    def __init__(self, bank_id, facility_id, max_default_likelihood, banned_state):
        self.bank_id = bank_id
        self.facility_id = facility_id
        if max_default_likelihood == '':
            self.max_default_likelihood = None
        else:
            self.max_default_likelihood = float(max_default_likelihood)
        self.banned_state = banned_state

    def __repr__(self):
        return f'bank id: {self.bank_id} facility id: {self.facility_id} \
               max default: {self.max_default_likelihood} banned state: {self.banned_state}'


class Loan:
    def __init__(self, loan_id, amount, rate, default_likelihood, state):
        self.id = loan_id
        self.amount = float(amount)
        self.rate = float(rate)
        self.default_likelihood = float(default_likelihood)
        self.state = state

    def __repr__(self):
        return f'id: {self.id} amount: {self.amount} rate: {self.rate} \
            default likelihood: {self.default_likelihood} state: {self.state}'
