import dao
import engine
import csv
import model

print('starting...')
yields = []
assignments = []

# process loans
with open('../data/loans.csv', 'r') as loans_csv:
    reader = csv.reader(loans_csv)
    next(reader)  # skip header
    for row in reader:
        loan = model.Loan(row[2], row[1], row[0], row[3], row[4])
        engine.process(loan)

# save output
dao.save_yields(engine.yields)
dao.save_assignments(engine.assignments)


print('done.')
print('assignments:', engine.assignments)
print('yields:', engine.yields)



