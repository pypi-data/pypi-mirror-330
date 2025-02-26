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

- **Replicate Crossover Design Analysis**:
  - Support for both partial (3-way) and full (4-way) replicate designs
  - Within-subject variability assessment for reference formulation
  - Reference-scaled average bioequivalence (RSABE) for highly variable drugs
  - Expanded bioequivalence limits based on reference variability

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

### Replicate Crossover Example

```python
import polars as pl
from bioeq import ReplicateCrossover

# Load data for a partial replicate (3-way) design
data = pl.read_csv("replicate_data.csv")

# Initialize analyzer for a partial replicate design
analyzer = ReplicateCrossover(
    data=data,
    design_type="partial",  # Use "full" for 4-way replicate design
    subject_col="SubjectID",
    seq_col="Sequence",
    period_col="Period",
    time_col="Time",
    conc_col="Concentration",
    form_col="Formulation"
)

# Calculate within-subject CV for the reference product
cv_results = analyzer.calculate_within_subject_cv("log_AUC")
print(f"Within-subject CV for reference: {cv_results['cv_percent']:.2f}%")

# If drug is highly variable (CV ≥ 30%), run reference-scaled approach
if cv_results['cv_percent'] >= 30:
    rsabe_results = analyzer.run_rsabe("log_AUC")
    print(f"RSABE criterion met: {rsabe_results['rsabe_criterion_met']}")
    print(f"Expanded BE limits: {rsabe_results['lower_scaled_limit']:.2f}% - {rsabe_results['upper_scaled_limit']:.2f}%")
else:
    # Use standard bioequivalence approach
    print("Standard bioequivalence assessment recommended (CV < 30%)")
```

## Documentation

Comprehensive documentation is available in the [docs](./docs) directory:

- **Regulatory Documentation**:
  - [Validation Strategy](./docs/validation/validation_strategy.md)
  - [Functional Requirements](./docs/requirements/functional_requirements.md)
  - [Traceability Matrix](./docs/validation/traceability_matrix.md)
  - [Algorithmic Specifications](./docs/specifications/algorithmic_specifications.md)
  - [Regulatory References](./docs/references/regulatory_references.md)

- **Developer Documentation**:
  - [Development Workflows](./docs/development/DOCUMENTATION.md)
  - [Notebook Integration](./docs/development/WORKFLOW_DOCUMENTATION.md)

- **Bioequivalence Notes**:
  - [Detailed Notes](./docs/notes/BE_NOTES.md)
  - [Concise Summary](./docs/notes/concise_BE_NOTES.md)

For a complete overview of the documentation, see the [docs README](./docs/README.md).

## Validation and Regulatory Compliance

BioEq is designed with regulatory requirements in mind. The package includes:

- **Validation Module**: Built-in functionality to validate calculations against known values
- **Traceability**: Documentation mapping requirements to implementation
- **Algorithm Documentation**: Detailed descriptions of implemented methods with scientific references
- **Regulatory References**: Documentation linking to relevant FDA guidance documents

### Running Validation Tests

To validate the package calculations:

```bash
# Run the built-in validation suite
bioeq validate --output validation_report.json
```

## Requirements

- Python ≥ 3.10
- Polars ≥ 1.18.0
- NumPy ≥ 2.2.1
- SciPy ≥ 1.15.0
- Statsmodels ≥ 0.14.4
- PyArrow ≥ 19.0.0

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
