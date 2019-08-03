import dao
import engine
import csv
import model

print('starting...')
yields = []
assignments = []

# process loans
loans = dao.load_loans()
for loan in loans:
        engine.process(loan)

# save output
dao.save_yields(engine.yields)
dao.save_assignments(engine.assignments)


print('done.')
print('assignments:', engine.assignments)
print('yields:', engine.yields)



