# BioEq

A Python package for performing bioequivalence calculations and analysis.

## Overview

BioEq is a comprehensive Python package for analyzing pharmacokinetic data in bioequivalence studies. It provides methods for processing and analyzing data from both crossover and parallel design bioequivalence studies.

## Features

- **Crossover 2x2 Design Analysis**:
  - Calculation of AUC, Cmax, Tmax, and other PK parameters
  - ANOVA and mixed effects model analysis
  - Point estimates and 90% confidence intervals for bioequivalence assessment

- **Parallel Design Analysis**:
  - Calculation of PK parameters for parallel group studies
  - ANOVA and t-test analysis
  - Point estimates and 90% confidence intervals

- **Additional Features**:
  - Estimation of elimination half-life
  - Extrapolation of AUC to infinity
  - Summary statistics for PK parameters
  - Data visualization tools
  - Flexible data input/output handling

## Installation

```bash
pip install bioeq
```

## Quick Start

```python
import polars as pl
from bioeq import Crossover2x2

# Load your data
data = pl.read_csv("your_data.csv")

# Initialize analyzer
analyzer = Crossover2x2(
    data=data,
    subject_col="SubjectID",
    seq_col="Sequence",
    period_col="Period",
    time_col="Time",
    conc_col="Concentration",
    form_col="Formulation"
)

# Calculate point estimate and confidence intervals
results = analyzer.calculate_point_estimate("log_AUC")
print(f"Point Estimate: {results['point_estimate']:.2f}%")
print(f"90% CI: {results['lower_90ci']:.2f}% - {results['upper_90ci']:.2f}%")
```

## Documentation

For comprehensive documentation and examples, please refer to the [notebooks](./notebooks) directory.

## Requirements

- Python ≥ 3.10
- Polars ≥ 1.18.0
- NumPy ≥ 2.2.1
- SciPy ≥ 1.15.0
- Statsmodels ≥ 0.14.4
- PyArrow ≥ 19.0.0

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
