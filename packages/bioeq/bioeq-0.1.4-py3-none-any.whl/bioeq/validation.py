"""
Validation module for BioEq package.

This module provides functions to validate the calculation methods in BioEq
against known reference values, providing traceability and verification
of numerical accuracy.
"""

import polars as pl
import numpy as np
from typing import Dict, List, Tuple, Any, Union
import json
import os
from datetime import datetime
from pathlib import Path

from .crossover2x2 import Crossover2x2
from .parallel import ParallelDesign


class ValidationReport:
    """
    Class to generate and maintain validation reports for BioEq calculations.
    
    This class enables comparison of calculated values against reference values
    and documents the validation results with timestamps, versions, and
    detailed metrics on calculation accuracy.
    """
    
    def __init__(self, report_name: str, version: str) -> None:
        """
        Initialize a validation report.
        
        Parameters
        ----------
        report_name : str
            Name of the validation report
        version : str
            Version of the BioEq package being validated
        """
        self.report_name = report_name
        self.version = version
        self.timestamp = datetime.now().isoformat()
        self.validation_results = []
        self.summary = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "pass_rate": 0.0
        }
    
    def add_result(self, 
                  test_name: str, 
                  expected: Any, 
                  actual: Any, 
                  tolerance: float = 1e-6,
                  passed: bool = None) -> None:
        """
        Add a validation test result to the report.
        
        Parameters
        ----------
        test_name : str
            Name of the test being performed
        expected : Any
            Expected reference value
        actual : Any
            Actual calculated value
        tolerance : float, optional
            Relative tolerance for numerical comparison, by default 1e-6
        passed : bool, optional
            Override automatic pass/fail determination, by default None
        """
        if passed is None:
            if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
                # For numeric values, compare within tolerance
                if expected == 0:
                    # Avoid division by zero
                    passed = abs(actual) < tolerance
                else:
                    rel_diff = abs((actual - expected) / expected)
                    passed = rel_diff < tolerance
            else:
                # For non-numeric values, use exact comparison
                passed = expected == actual
        
        result = {
            "test_name": test_name,
            "expected": str(expected),
            "actual": str(actual),
            "tolerance": tolerance,
            "passed": passed,
            "timestamp": datetime.now().isoformat()
        }
        
        self.validation_results.append(result)
        self.summary["total_tests"] += 1
        if passed:
            self.summary["passed_tests"] += 1
        else:
            self.summary["failed_tests"] += 1
        
        self.summary["pass_rate"] = (self.summary["passed_tests"] / 
                                     self.summary["total_tests"]) * 100
    
    def save_report(self, output_dir: str = "validation_reports") -> str:
        """
        Save the validation report to a JSON file.
        
        Parameters
        ----------
        output_dir : str, optional
            Directory to store reports, by default "validation_reports"
        
        Returns
        -------
        str
            Path to the saved report file
        """
        # Ensure the output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Create the report filename with timestamp
        filename = f"{self.report_name}_{self.version}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(output_dir, filename)
        
        # Compile the full report
        report = {
            "report_name": self.report_name,
            "version": self.version,
            "timestamp": self.timestamp,
            "summary": self.summary,
            "validation_results": self.validation_results
        }
        
        # Write the report to a JSON file
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filepath
    
    def print_summary(self) -> None:
        """
        Print a summary of the validation results.
        """
        print(f"Validation Report: {self.report_name}")
        print(f"BioEq Version: {self.version}")
        print(f"Timestamp: {self.timestamp}")
        print("-" * 50)
        print(f"Total Tests: {self.summary['total_tests']}")
        print(f"Passed: {self.summary['passed_tests']}")
        print(f"Failed: {self.summary['failed_tests']}")
        print(f"Pass Rate: {self.summary['pass_rate']:.2f}%")
        print("-" * 50)
        
        if self.summary['failed_tests'] > 0:
            print("Failed Tests:")
            for result in self.validation_results:
                if not result['passed']:
                    print(f"  - {result['test_name']}")
                    print(f"    Expected: {result['expected']}")
                    print(f"    Actual: {result['actual']}")
                    print()


def validate_auc_calculation(report: ValidationReport) -> None:
    """
    Validate AUC calculation against known values.
    
    Parameters
    ----------
    report : ValidationReport
        Validation report to add results to
    """
    # Simple test case with known solution
    times = np.array([0, 1, 2, 4, 8, 12, 24])
    concentrations = np.array([0, 10, 8, 6, 3, 1.5, 0.5])
    
    # Calculate expected AUC using numpy's trapezoid function for reference
    expected_auc = np.trapezoid(concentrations, times)
    
    # Create dataset in the format required by BioEq
    data = []
    for i, (t, c) in enumerate(zip(times, concentrations)):
        data.append({
            "SubjectID": 1,
            "Period": 1,
            "Sequence": "RT",
            "Formulation": "Test",
            "Time (hr)": t,
            "Concentration (ng/mL)": c
        })
    
    df = pl.DataFrame(data)
    
    # Initialize Crossover2x2 analyzer
    analyzer = Crossover2x2(
        data=df,
        subject_col="SubjectID",
        seq_col="Sequence",
        period_col="Period",
        time_col="Time (hr)",
        conc_col="Concentration (ng/mL)",
        form_col="Formulation"
    )
    
    # Get calculated AUC
    params_df = analyzer.get_params_df()
    actual_auc = params_df.filter(
        (pl.col("SubjectID") == 1) & 
        (pl.col("Period") == 1) &
        (pl.col("Formulation") == "Test")
    )["AUC"].to_numpy()[0]
    
    # Add result to validation report
    report.add_result(
        test_name="AUC Calculation",
        expected=expected_auc,
        actual=actual_auc,
        tolerance=1e-10
    )


def validate_cmax_calculation(report: ValidationReport) -> None:
    """
    Validate Cmax calculation against known values.
    
    Parameters
    ----------
    report : ValidationReport
        Validation report to add results to
    """
    # Simple test case with known solution
    times = np.array([0, 1, 2, 4, 8, 12, 24])
    concentrations = np.array([0, 10, 8, 6, 3, 1.5, 0.5])
    
    # Expected Cmax is the maximum concentration
    expected_cmax = np.max(concentrations)
    
    # Create dataset in the format required by BioEq
    data = []
    for i, (t, c) in enumerate(zip(times, concentrations)):
        data.append({
            "SubjectID": 1,
            "Period": 1,
            "Sequence": "RT",
            "Formulation": "Test",
            "Time (hr)": t,
            "Concentration (ng/mL)": c
        })
    
    df = pl.DataFrame(data)
    
    # Initialize Crossover2x2 analyzer
    analyzer = Crossover2x2(
        data=df,
        subject_col="SubjectID",
        seq_col="Sequence",
        period_col="Period",
        time_col="Time (hr)",
        conc_col="Concentration (ng/mL)",
        form_col="Formulation"
    )
    
    # Get calculated Cmax
    params_df = analyzer.get_params_df()
    actual_cmax = params_df.filter(
        (pl.col("SubjectID") == 1) & 
        (pl.col("Period") == 1) &
        (pl.col("Formulation") == "Test")
    )["Cmax"].to_numpy()[0]
    
    # Add result to validation report
    report.add_result(
        test_name="Cmax Calculation",
        expected=expected_cmax,
        actual=actual_cmax,
        tolerance=1e-10
    )


def validate_half_life_calculation(report: ValidationReport) -> None:
    """
    Validate half-life calculation against known values.
    
    Parameters
    ----------
    report : ValidationReport
        Validation report to add results to
    """
    # Simple test case with exponential decay and known half-life
    # C(t) = C0 * exp(-kt) where k = ln(2)/t_half
    t_half = 4.0  # hours
    k = np.log(2) / t_half
    C0 = 10.0
    
    times = np.array([0, 1, 2, 4, 8, 12, 24])
    concentrations = C0 * np.exp(-k * times)
    
    # Create dataset in the format required by BioEq
    data = []
    for i, (t, c) in enumerate(zip(times, concentrations)):
        data.append({
            "SubjectID": 1,
            "Period": 1,
            "Sequence": "RT",
            "Formulation": "Test",
            "Time (hr)": t,
            "Concentration (ng/mL)": c
        })
    
    df = pl.DataFrame(data)
    
    # Initialize Crossover2x2 analyzer
    analyzer = Crossover2x2(
        data=df,
        subject_col="SubjectID",
        seq_col="Sequence",
        period_col="Period",
        time_col="Time (hr)",
        conc_col="Concentration (ng/mL)",
        form_col="Formulation"
    )
    
    # Get calculated half-life
    params_df = analyzer.get_params_df()
    actual_half_life = params_df.filter(
        (pl.col("SubjectID") == 1) & 
        (pl.col("Period") == 1) &
        (pl.col("Formulation") == "Test")
    )["t_half"].to_numpy()[0]
    
    # Add result to validation report
    report.add_result(
        test_name="Half-life Calculation",
        expected=t_half,
        actual=actual_half_life,
        tolerance=0.05  # 5% tolerance for half-life due to regression estimation
    )


def validate_point_estimate_calculation(report: ValidationReport) -> None:
    """
    Validate point estimate calculation for bioequivalence assessment.
    
    Parameters
    ----------
    report : ValidationReport
        Validation report to add results to
    """
    # Create a dataset with known Test/Reference ratio
    true_ratio = 0.95  # Test is 95% of Reference
    
    test_conc_scale = true_ratio
    ref_conc_scale = 1.0
    
    # Base concentration-time profile
    times = np.array([0, 1, 2, 4, 8, 12, 24])
    base_conc = np.array([0, 10, 8, 6, 3, 1.5, 0.5])
    
    # Create dataset for both Test and Reference
    data = []
    # First subject: Sequence RT (Reference in period 1, Test in period 2)
    for period in [1, 2]:
        formulation = "Reference" if period == 1 else "Test"
        scale = ref_conc_scale if formulation == "Reference" else test_conc_scale
        
        for t, c in zip(times, base_conc):
            data.append({
                "SubjectID": 1,
                "Period": period,
                "Sequence": "RT",
                "Formulation": formulation,
                "Time (hr)": t,
                "Concentration (ng/mL)": c * scale
            })
    
    # Second subject: Sequence TR (Test in period 1, Reference in period 2)
    for period in [1, 2]:
        formulation = "Test" if period == 1 else "Reference"
        scale = ref_conc_scale if formulation == "Reference" else test_conc_scale
        
        for t, c in zip(times, base_conc):
            data.append({
                "SubjectID": 2,
                "Period": period,
                "Sequence": "TR",
                "Formulation": formulation,
                "Time (hr)": t,
                "Concentration (ng/mL)": c * scale
            })
    
    df = pl.DataFrame(data)
    
    # Initialize Crossover2x2 analyzer
    analyzer = Crossover2x2(
        data=df,
        subject_col="SubjectID",
        seq_col="Sequence",
        period_col="Period",
        time_col="Time (hr)",
        conc_col="Concentration (ng/mL)",
        form_col="Formulation"
    )
    
    # Calculate point estimate
    result = analyzer.calculate_point_estimate("log_AUC")
    
    # Expected point estimate (as percentage)
    expected_point_estimate = true_ratio * 100
    
    # Add result to validation report
    report.add_result(
        test_name="Point Estimate Calculation",
        expected=expected_point_estimate,
        actual=result["point_estimate"],
        tolerance=0.05  # 5% tolerance due to regression estimation
    )


def run_validation(version: str = "current") -> ValidationReport:
    """
    Run all validation tests and generate a comprehensive report.
    
    Parameters
    ----------
    version : str, optional
        Version of the BioEq package being validated, by default "current"
    
    Returns
    -------
    ValidationReport
        Completed validation report
    """
    # Initialize validation report
    report = ValidationReport("BioEq_Comprehensive_Validation", version)
    
    # Run individual validation tests
    validate_auc_calculation(report)
    validate_cmax_calculation(report)
    validate_half_life_calculation(report)
    validate_point_estimate_calculation(report)
    
    # Print summary and save report
    report.print_summary()
    report_path = report.save_report()
    print(f"Validation report saved to: {report_path}")
    
    return report


if __name__ == "__main__":
    # If run as a script, perform validation
    try:
        from importlib import metadata
        version = metadata.version("bioeq")
    except:
        version = "unknown"
    
    run_validation(version) 