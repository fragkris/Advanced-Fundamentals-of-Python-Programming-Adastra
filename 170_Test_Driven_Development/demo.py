import trace, sys
from unittest import TestCase




# all our test code




if __name__ == "__main__":
    t = trace.Trace(ignoredirs=[sys.prefix, sys.exec_prefix], count=1, trace=0)
    t.runfunc(unittest.main)
    r = t.results()
    r.write_results(show_missing=True)

"""The trace objects, traces the execution of our program and returns the tests coverage."""
