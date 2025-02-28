# GAbits

`gabits` is a Python package that implements a genetic algorithm based on
binary representation, along with utility functions for data manipulation and
transformation. The code is based on the original implementation by Roberto T.
Raittz and adapted to Python by Diogo de J. S. Machado.

## Features

### Genetic Algorithm
- **gago**: Genetic algorithm for optimization, based on binary representation.

### Utility Functions
- **mat2vec**: Converts a matrix to a 1D array.
- **vec2mat**: Creates a matrix from a 1D array.
- **bytes2bits**: Converts a list of numbers or a single number to a bit array.
- **bits2bytes**: Converts a bit array to bytes.

## Installation

To install the package, use `pip`:

```sh
pip install gabits
```

## Usage

### Genetic Algorithm

Here's a basic example of using the `gago` function for optimization:

```python
from gabits import gago, bits2bytes

# Options for the genetic algorithm
gaoptions = {
    "PopulationSize": 200,    # Population size
    "Generations": 50,        # Number of generations
    "InitialPopulation": [],  # Initial population (empty in this case)
    "MutationFcn": 0.15,      # Mutation rate
    "EliteCount": 2,          # Number of elite individuals to keep
}

# Fitness function for Genetic Algorithm
def fit_func(bits):
    """
    Fitness function for Genetic Algorithm.

    Objective
    --------
    Set integer values so that the following equation holds true:

    .. math:: x_1 + x_2 = |x_3 - x_4|

    Input
    -----
    64 bits (8 bytes). Each 16 bits (2 bytes) form an integer value.

    Output
    ------
    Absolute error from the expected result.
    """
    # Convert bit string to 16-bit integers
    X = bits2bytes(bits, 'int16').astype(int)
    # Calculate error based on integers
    error = abs((X[0] + X[1]) - abs(X[2] - X[3]))
    return error

# Run the genetic algorithm with the fitness function, 64 bits per individual
# and the defined options
result = gago(fit_func, 64, gaoptions)

# Extract bits from the best individual found by the genetic algorithm
bits = result[0]

# Convert the extracted bits into 16-bit integers
X = bits2bytes(bits, 'int16').astype(int)

# Print the result (the integer values found)
print('Result =', list(X))

# Calculate and print the error for the best individual found
print('Error =', fit_func(bits))

# Print the sum of the first two integer values found
print('x1 + x2 =', X[0] + X[1])

# Print the absolute value of the difference between the last two integer
# values found
print('|x3 - x4| =', abs(X[2] - X[3]))
```

### Utility Functions

Here are examples demonstrating the utility functions:

#### mat2vec

```python
import numpy as np
from gabits import mat2vec

mat = np.array([[1, 2, 3], [4, 5, 6]])
vec = mat2vec(mat)
print("Matrix converted to vector:", vec)
```

#### vec2mat

```python
from gabits import vec2mat

vec = [1, 2, 3, 4, 5]
larg = 3
mat = vec2mat(vec, larg)
print("Vector converted to matrix:")
print(mat)
```

#### bytes2bits

```python
from gabits import bytes2bits

num = 5
bits = bytes2bits(num)
print("Number converted to bits:", bits)
```

#### bits2bytes

```python
from gabits import bits2bytes

bits = [1, 0, 1, 0, 0, 0, 0, 0]
bytes_ = bits2bytes(bits)
print("Bits converted to bytes:", bytes_)
```

## Authors

- **Original Implementation**: Roberto T. Raittz
- **Python Adaptation**: Diogo de J. S. Machado
