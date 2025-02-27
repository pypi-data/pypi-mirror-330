# Optimation Framework

Optimation is a flexible framework for iterative variable weighting, balancing trade-offs, and adaptive decision-making.

## Installation

```
pip install optimation
```

## Usage
```python
from optimation.core import optimate

result = optimate(A=10, B=20, weight_A=70)
print(result)  # Outputs optimized result
```

## Features
- **Variable Weighting**
- **Iterative Trade-Offs**
- **Half-Adding & Exponential Adjustments**
