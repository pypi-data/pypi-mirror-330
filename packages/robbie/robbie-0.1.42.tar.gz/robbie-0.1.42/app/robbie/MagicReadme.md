# Prototype: Run a magic function

What it does

- Dumps the Jupyter context via `dill` with some special filtering logic.
- Saves cell contents in a `.py` file using `executable_wrapper.py` as a base.
- Runs `robbie run` with custom commands to:
  - Install requirements
  - Loads the context with `dill` with some specially filtering logic.
  - Run the `.py`
  - Dumps the new context with `dill`
- Robbie downloads the results
- Loads the new context via `dill`

Test in `test/magic/magics.ipynb`

## Production Ready?

No.

Bugs

- The current logic to `dill.detect.baditems` does not handle array of arrays. Ex. a simple `numpy` matrix multiply will not work.
- `IOPub data rate exceeded.` Since we're piping all logs to stdout it seems like Jupyter doesn't like that. Occurs intermittently.

Consider

- Implement a new `job_type` that is a magic function so that we do not need to muck around with subprocesses.
  - May also be able to call `position_cli.cli.run` directly, however this exposed some other issues.
  - Pickled files like `localpickle.pkl` are in the current dir, should move them to `.robbie` or get rid of them (serialize in mem and upload to cloud storage)
- Refactor helper methods
