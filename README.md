# Loose Internal documentation of the timetable generation logic

- backtrack.py is the main file that runs the generate algorithm

## Models

- primary_subs : Dict[Standard:List[Subject]]
- timetable is a 3d array where the odd outer indices are section A and even are section B (gimmick)
- primary classes from 1 to 5
- secondary classes from 6 to 10

## Constraints

- The constraints model has the ConstraintGroup which can be subclassed
- Any function that is a subclass of ConstraintGroup and has the "constraint" decorator becomes a constraint that runs when "validate" is called
- All valid constraints are "stateless"

## Tests

- unitttests are contained in tests/
- tests can be run by running `python -m unittest discover` on the top directory
- Profiling is done using cpython
- can be visualized using snakeviz

## TODOs

- Ditch backtracking, takes a lot of time on bad random seeds
- Implement restricted teachers
- Use backtracking's advantage of traversing back multiple classes for cross-class constraints
