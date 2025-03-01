# Parallel Execution

Simple parallel execution of functions.

## Installation

```bash
git clone https://github.com/QuintessenceLabs/parallel_execution.git; cd parallel_execution
pip install -e .
```

## Usage

```python
import parallel_execution

# define the function to execute
def function(a, b):
    return a + b

input_values = [
    {'a': 1, 'b': 2},
    {'a': 3, 'b': 4},
    {'a': 5, 'b': 6},
]

parallel_input = {en: kwargs for en, kwargs in enumerate(input_values)}

# initialize the executor
executor = parallel_execution.ParallelExecutor(max_threads=8)
executor(function, parallel_input)
```

You could also use the `parallel_execution` function to call the executor:

```python
parallel_execution.parallel_execution(function, parallel_input)
```

