"""Run all applicable V3.1 regressions without constructing a 37-class model."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests'))
EXCLUDED={'test_solver.SolverTests.test_unknown_is_not_infeasible','test_solver.SolverTests.test_morning_37_class_capacity_diagnosis','test_v3_1.V31Tests.test_unknown_no_conflict_claim'}
def flatten(s):
 for t in s:
  if isinstance(t,unittest.TestSuite):yield from flatten(t)
  else:yield t
suite=unittest.TestLoader().discover(str(ROOT/'tests'),pattern='test_*.py');alltests=list(flatten(suite));excluded=[t.id() for t in alltests if t.id() in EXCLUDED];selected=[t for t in alltests if t.id() not in EXCLUDED]
r=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(selected))
out=dict(tests=r.testsRun,success=r.wasSuccessful(),failures=[t.id() for t,_ in r.failures],errors=[t.id() for t,_ in r.errors],scope_exclusions=[dict(test=t,reason='Legacy whole-school solve is outside authorized grade-only scope; UNKNOWN covered by grade-only test') for t in excluded],runtime='Linux Python3.12; not Windows acceptance')
(ROOT/'reports/TIME_CONFLICT_REGRESSION.json').write_text(json.dumps(out,indent=2));sys.exit(0 if r.wasSuccessful() else 1)
