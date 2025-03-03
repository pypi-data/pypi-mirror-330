# AdvVaex

AdvVaex is an advanced extension of the popular Vaex library, providing enhanced functionality for large-scale data processing. It includes utility functions that extend the capabilities of Vaex, such as adding metadata insights during aggregation processes.

## Installation

```bash
pip install advvaex

USAGE:
import vaex
from advvaex import advanced_aggregate

# Create a Vaex DataFrame
df = vaex.from_dict({"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]})

# Perform advanced aggregation
result = advanced_aggregate(df, column="A", agg_func="mean")
print(result)
```
