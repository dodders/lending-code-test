import dao
import engine


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
dao.save_unfunded(engine.unfunded)

print(f'finished with {len(engine.unfunded)} unfunded loans.')



