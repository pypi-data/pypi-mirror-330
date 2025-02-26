"""
ReplicateCrossover Module

This module implements the ReplicateCrossover class for analyzing replicate crossover designs in bioequivalence studies.
It supports both partial replicate (3-way) and full replicate (4-way) designs, which are particularly useful for
highly variable drugs where reference-scaled average bioequivalence (RSABE) assessment may be required.

Partial replicate designs typically use three periods with sequences like TRR, RTR, RRT, while full replicate designs
use four periods with sequences like TRTR or RTRT, where T is Test and R is Reference formulation.

This implementation provides methods for calculating pharmacokinetic parameters and performing statistical analyses
specific to replicate designs, including within-subject variability assessment and reference-scaled average
bioequivalence calculations.
"""

import polars as pl
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from typing import Dict, List, Optional, Tuple, Union
from scipy import stats


class ReplicateCrossover:
    """
    A class for analyzing replicate crossover bioequivalence studies.
    
    This class is specifically designed for analyzing replicate crossover studies,
    including partial (3-way) and full (4-way) replicate designs. These designs
    are particularly useful for assessing bioequivalence of highly variable drugs,
    as they allow for the estimation of within-subject variability for the reference
    product, which can be used in reference-scaled average bioequivalence (RSABE) assessments.
    
    The class provides methods for calculating pharmacokinetic parameters (PK),
    such as AUC, Cmax, and Tmax, as well as specialized statistical analyses
    relevant to replicate designs.
    
    Partial replicate designs have three periods with sequences like TRR, RTR, RRT.
    Full replicate designs have four periods with sequences like TRTR, RTRT.
    
    Parameters
    ----------
    data : pl.DataFrame
        DataFrame containing the concentration-time data with columns for subject ID,
        sequence, period, time, concentration, and formulation.
    design_type : str
        Type of replicate design: "partial" for 3-way or "full" for 4-way.
    subject_col : str
        Name of the column containing subject identifiers.
    seq_col : str
        Name of the column containing sequence information.
    period_col : str
        Name of the column containing period information.
    time_col : str
        Name of the column containing time points.
    conc_col : str
        Name of the column containing concentration measurements.
    form_col : str
        Name of the column containing formulation information.
    
    Attributes
    ----------
    data : pl.DataFrame
        The input data.
    design_type : str
        The type of replicate design ("partial" or "full").
    subject_col : str
        Column name for subject identifiers.
    seq_col : str
        Column name for sequence information.
    period_col : str
        Column name for period information.
    time_col : str
        Column name for time points.
    conc_col : str
        Column name for concentration measurements.
    form_col : str
        Column name for formulation information.
    half_life_df : pl.DataFrame or None
        DataFrame containing calculated half-life values.
    params_df : pl.DataFrame
        DataFrame containing calculated PK parameters.
    
    Examples
    --------
    >>> import polars as pl
    >>> from bioeq import ReplicateCrossover
    >>> # Load data
    >>> data = pl.read_csv("replicate_data.csv")
    >>> # Initialize analyzer for a partial replicate design
    >>> analyzer = ReplicateCrossover(
    ...     data=data,
    ...     design_type="partial",
    ...     subject_col="SubjectID",
    ...     seq_col="Sequence",
    ...     period_col="Period",
    ...     time_col="Time (hr)",
    ...     conc_col="Concentration (ng/mL)",
    ...     form_col="Formulation"
    ... )
    >>> # Calculate within-subject CV for the reference product
    >>> cv_results = analyzer.calculate_within_subject_cv("log_AUC")
    >>> print(f"Within-subject CV for AUC: {cv_results['cv_percent']:.2f}%")
    >>> # Run reference-scaled average bioequivalence assessment
    >>> rsabe_results = analyzer.run_rsabe("log_AUC")
    >>> print(f"RSABE criterion met: {rsabe_results['rsabe_criterion_met']}")
    """

    def __init__(
        self,
        data: pl.DataFrame,
        design_type: str,
        subject_col: str,
        seq_col: str,
        period_col: str,
        time_col: str,
        conc_col: str,
        form_col: str,
    ) -> None:
        """
        Initialize ReplicateCrossover class.
        
        Parameters
        ----------
        data : pl.DataFrame
            Concentration-time data
        design_type : str
            Type of replicate design: "partial" (3-way) or "full" (4-way)
        subject_col : str
            Name of column containing subject identifiers
        seq_col : str
            Name of column containing sequence information
        period_col : str
            Name of column containing period information
        time_col : str
            Name of column containing time points
        conc_col : str
            Name of column containing concentration measurements
        form_col : str
            Name of column containing formulation information
        """
        self.data = data
        self.design_type = design_type
        self.subject_col = subject_col
        self.seq_col = seq_col
        self.period_col = period_col
        self.time_col = time_col
        self.conc_col = conc_col
        self.form_col = form_col
        
        # Validate inputs
        self._validate_data()
        self._validate_colvals()
        
        # Calculate half-life first (needed for AUC_inf)
        self.half_life_df = self._calculate_half_life()
        
        # Calculate all PK parameters
        self.params_df = self._calculate_pk_parameters()
        
    def _validate_data(self) -> None:
        """Validate that the input data has the required columns."""
        required_cols = [
            self.subject_col, self.seq_col, self.period_col, 
            self.time_col, self.conc_col, self.form_col
        ]
        
        for col in required_cols:
            if col not in self.data.columns:
                raise ValueError(f"Required column '{col}' not found in the input data")
    
    def _validate_colvals(self) -> None:
        """Validate column values in the data."""
        # Check that design_type is valid
        if self.design_type.lower() not in ["partial", "full"]:
            raise ValueError("design_type must be either 'partial' (3-way) or 'full' (4-way)")
        
        # Standardize design_type
        self.design_type = self.design_type.lower()
        
        # Check formulation values
        unique_forms = self.data[self.form_col].unique().to_list()
        if len(unique_forms) != 2 or "Test" not in unique_forms or "Reference" not in unique_forms:
            raise ValueError("data must contain exactly two formulations: 'Test' and 'Reference'")
            
        # Check sequence values according to design type
        unique_seqs = self.data[self.seq_col].unique().to_list()
        if self.design_type == "partial":
            valid_seqs = ["TRR", "RTR", "RRT"]
            if not all(seq in valid_seqs for seq in unique_seqs):
                raise ValueError("Partial replicate design sequences must be TRR, RTR, or RRT")
        elif self.design_type == "full":
            valid_seqs = ["TRTR", "RTRT"]
            if not all(seq in valid_seqs for seq in unique_seqs):
                raise ValueError("Full replicate design sequences must be TRTR or RTRT")
                
        # Check periods according to design type
        unique_periods = self.data[self.period_col].unique().to_list()
        if self.design_type == "partial" and max(unique_periods) > 3:
            raise ValueError("Partial replicate design should have at most 3 periods")
        elif self.design_type == "full" and max(unique_periods) > 4:
            raise ValueError("Full replicate design should have at most 4 periods")
        
    def _calculate_pk_parameters(self) -> pl.DataFrame:
        """Calculate all PK parameters and return a dataframe with results."""
        # Calculate individual PK parameters
        auc_df = self._calculate_auc()
        cmax_df = self._calculate_cmax()
        tmax_df = self._calculate_tmax()
        half_life_df = self._calculate_half_life()
        auc_inf_df = self._calculate_auc_extrapolated()
        
        # Combine basic parameters for log transformation
        base_df = auc_df.join(
            cmax_df, 
            on=[self.subject_col, self.period_col, self.seq_col, self.form_col],
            how="inner"
        )
        
        # Calculate log-transformed parameters
        log_df = self._calculate_log_transform(base_df)
        
        # Combine all parameters into one dataframe
        result_dfs = [auc_df, cmax_df, tmax_df, log_df]
        
        # Add half-life and AUC_inf if available
        if half_life_df is not None:
            result_dfs.append(half_life_df)
            
        if auc_inf_df is not None:
            result_dfs.append(auc_inf_df)
        
        # Join all dataframes
        result = auc_df
        for df in result_dfs[1:]:
            result = result.join(
                df,
                on=[self.subject_col, self.period_col, self.seq_col, self.form_col],
                how="left"
            )
            
        return result
        
    def _calculate_auc(self) -> pl.DataFrame:
        """
        Calculate AUC for each subject/period using the trapezoidal rule.
        
        Returns
        -------
        pl.DataFrame
            DataFrame containing AUC values for each subject/period/formulation
        """
        # Get unique subjects and periods
        unique_subjects = self.data[self.subject_col].unique().to_list()
        
        result = []
        
        for subject in unique_subjects:
            # Get data for this subject
            subject_data = self.data.filter(pl.col(self.subject_col) == subject)
            
            # Get unique periods for this subject
            periods = subject_data[self.period_col].unique().sort().to_list()
            
            for period in periods:
                # Get data for this period
                period_data = subject_data.filter(pl.col(self.period_col) == period)
                
                # Sort by time
                period_data = period_data.sort(self.time_col)
                
                # Calculate AUC using trapezoidal rule
                times = period_data[self.time_col].to_numpy()
                concs = period_data[self.conc_col].to_numpy()
                auc = np.trapezoid(concs, times)
                
                # Get sequence and formulation
                sequence = period_data[self.seq_col].unique()[0]
                formulation = period_data[self.form_col].unique()[0]
                
                # Add to results
                result.append({
                    self.subject_col: subject,
                    self.period_col: period,
                    self.seq_col: sequence,
                    self.form_col: formulation,
                    "AUC": auc
                })
        
        return pl.DataFrame(result)
        
    def _calculate_cmax(self) -> pl.DataFrame:
        """
        Calculate the maximum concentration (Cmax) for each subject/period/formulation.
        
        Returns
        -------
        pl.DataFrame
            DataFrame containing Cmax values for each subject/period/formulation
        """
        result = []
        
        for subject in self.data[self.subject_col].unique():
            for period in self.data[self.period_col].unique():
                # Filter data for the current subject and period
                subject_data = self.data.filter(
                    (pl.col(self.subject_col) == subject) & 
                    (pl.col(self.period_col) == period)
                )
                
                if len(subject_data) == 0:
                    continue
                    
                # Get the formulation and sequence for this subject/period
                formulation = subject_data[self.form_col].unique()[0]
                sequence = subject_data[self.seq_col].unique()[0]
                
                # Find maximum concentration
                cmax = subject_data[self.conc_col].max()
                
                result.append({
                    self.subject_col: subject,
                    self.period_col: period,
                    self.form_col: formulation,
                    self.seq_col: sequence,
                    "Cmax": cmax
                })
                
        return pl.DataFrame(result)
        
    def _calculate_tmax(self) -> pl.DataFrame:
        """
        Calculate the time to maximum concentration (Tmax) for each subject/period/formulation.
        
        Returns
        -------
        pl.DataFrame
            DataFrame containing Tmax values for each subject/period/formulation
        """
        result = []
        
        for subject in self.data[self.subject_col].unique():
            for period in self.data[self.period_col].unique():
                # Filter data for the current subject and period
                subject_data = self.data.filter(
                    (pl.col(self.subject_col) == subject) & 
                    (pl.col(self.period_col) == period)
                )
                
                if len(subject_data) == 0:
                    continue
                    
                # Get the formulation and sequence for this subject/period
                formulation = subject_data[self.form_col].unique()[0]
                sequence = subject_data[self.seq_col].unique()[0]
                
                # Find time of maximum concentration
                max_conc_idx = subject_data[self.conc_col].arg_max()
                tmax = subject_data[self.time_col][max_conc_idx]
                
                result.append({
                    self.subject_col: subject,
                    self.period_col: period,
                    self.form_col: formulation,
                    self.seq_col: sequence,
                    "Tmax": tmax
                })
                
        return pl.DataFrame(result)
        
    def _calculate_log_transform(self, base_df: pl.DataFrame) -> pl.DataFrame:
        """
        Calculate log-transformed PK parameters (log_AUC, log_Cmax).
        
        Parameters
        ----------
        base_df : pl.DataFrame
            DataFrame containing AUC and Cmax values
            
        Returns
        -------
        pl.DataFrame
            DataFrame containing log-transformed values for each subject/period/formulation
        """
        # Add log-transformed columns
        log_df = base_df.with_columns([
            pl.col("AUC").log().alias("log_AUC"),
            pl.col("Cmax").log().alias("log_Cmax")
        ]).select([
            self.subject_col, self.period_col, self.seq_col, self.form_col, "log_AUC", "log_Cmax"
        ])
        
        return log_df
        
    def _calculate_half_life(self) -> Optional[pl.DataFrame]:
        """
        Calculate the elimination half-life for each subject/period/formulation.
        
        Returns
        -------
        Optional[pl.DataFrame]
            DataFrame containing half-life values, or None if calculation is not possible
        """
        result = []
        
        for subject in self.data[self.subject_col].unique():
            for period in self.data[self.period_col].unique():
                # Filter data for the current subject and period
                subject_data = self.data.filter(
                    (pl.col(self.subject_col) == subject) & 
                    (pl.col(self.period_col) == period)
                )
                
                if len(subject_data) == 0:
                    continue
                    
                # Get the formulation and sequence for this subject/period
                formulation = subject_data[self.form_col].unique()[0]
                sequence = subject_data[self.seq_col].unique()[0]
                
                # Sort by time
                subject_data = subject_data.sort(self.time_col)
                times = subject_data[self.time_col].to_numpy()
                concs = subject_data[self.conc_col].to_numpy()
                
                # Need at least 3 non-zero points for terminal elimination rate
                if len(times) >= 3 and np.count_nonzero(concs) >= 3:
                    # Use the last 3 non-zero concentration points for half-life estimation
                    # (This is a simplified approach, a more sophisticated algorithm would be better)
                    non_zero_indices = np.nonzero(concs)[0]
                    
                    if len(non_zero_indices) >= 3:
                        terminal_indices = non_zero_indices[-3:]
                        terminal_times = times[terminal_indices]
                        terminal_concs = concs[terminal_indices]
                        
                        # Log-transform concentrations for linear regression
                        log_concs = np.log(terminal_concs)
                        
                        # Simple linear regression to get elimination rate constant
                        slope, intercept, r_value, p_value, std_err = stats.linregress(
                            terminal_times, log_concs
                        )
                        
                        # Negative slope gives elimination rate constant
                        ke = -slope
                        
                        # Calculate half-life
                        if ke > 0:
                            half_life = np.log(2) / ke
                            
                            result.append({
                                self.subject_col: subject,
                                self.period_col: period,
                                self.form_col: formulation,
                                self.seq_col: sequence,
                                "t_half": half_life
                            })
        
        if result:
            return pl.DataFrame(result)
        else:
            return None
            
    def _calculate_auc_extrapolated(self) -> Optional[pl.DataFrame]:
        """
        Calculate AUC extrapolated to infinity (AUC_inf) for each subject/period.
        
        Returns
        -------
        pl.DataFrame or None
            DataFrame containing AUC_inf values for each subject/period/formulation,
            or None if half-life calculation was not successful
        """
        if not hasattr(self, 'half_life_df') or self.half_life_df is None:
            return None
            
        # Get unique subjects and periods
        unique_subjects = self.data[self.subject_col].unique().to_list()
        
        result = []
        
        for subject in unique_subjects:
            # Get data for this subject
            subject_data = self.data.filter(pl.col(self.subject_col) == subject)
            
            # Get unique periods for this subject
            periods = subject_data[self.period_col].unique().sort().to_list()
            
            for period in periods:
                # Get period data
                period_data = subject_data.filter(pl.col(self.period_col) == period)
                
                if len(period_data) == 0:
                    continue
                
                # Get the formulation for this subject/period
                formulation = period_data[self.form_col].unique()[0]
                sequence = period_data[self.seq_col].unique()[0]
                
                # Sort by time and get last non-zero concentration
                period_data = period_data.sort(self.time_col)
                last_conc = period_data.filter(pl.col(self.conc_col) > 0).slice(-1)[self.conc_col].item()
                
                # Get half-life data for this subject/period
                lambda_z_entry = self.half_life_df.filter(
                    (pl.col(self.subject_col) == subject) & 
                    (pl.col(self.period_col) == period)
                )
                
                # Check if we have t_half for this subject/period
                if len(lambda_z_entry) == 0 or "t_half" not in lambda_z_entry.columns:
                    continue
                    
                # Check if t_half value is valid
                if lambda_z_entry["t_half"].is_null().any():
                    continue
                
                # Get elimination rate constant from half-life (ke = ln(2)/t_half)
                t_half = lambda_z_entry["t_half"].item()
                lambda_z = np.log(2) / t_half
                
                # Calculate AUC up to the last time point
                times = period_data[self.time_col].to_numpy()
                concs = period_data[self.conc_col].to_numpy()
                auc_last = np.trapezoid(concs, times)
                
                # Calculate extrapolated portion
                auc_extra = last_conc / lambda_z
                
                # Total AUC
                auc_inf = auc_last + auc_extra
                
                # Calculate percent extrapolated
                pct_extrap = (auc_extra / auc_inf) * 100
                
                result.append({
                    self.subject_col: subject,
                    self.period_col: period,
                    self.form_col: formulation,
                    self.seq_col: sequence,
                    "AUC_inf": auc_inf,
                    "AUC_last": auc_last,
                    "pct_extrap": pct_extrap
                })
        
        if result:
            return pl.DataFrame(result)
        else:
            return None
            
    def calculate_within_subject_cv(self, parameter: str = "log_AUC") -> Dict[str, float]:
        """
        Calculate the within-subject coefficient of variation (CV) for the reference product.
        
        This method calculates the within-subject variability for the reference product
        based on the replicate administrations in the study design. This is a key calculation
        for reference-scaled average bioequivalence (RSABE) approaches.
        
        For partial replicate designs, subjects receive the reference product twice.
        For full replicate designs, subjects receive both test and reference products twice.
        
        The CV is calculated using the formula:
            CV% = sqrt(exp(s²_WR) - 1) × 100
        
        where s²_WR is the within-subject variance for the reference product.
        
        Parameters
        ----------
        parameter : str, default="log_AUC"
            The log-transformed PK parameter to use for CV calculation.
            Typically "log_AUC" or "log_Cmax".
            
        Returns
        -------
        Dict[str, float]
            Dictionary containing:
            - 'within_subject_variance': The calculated within-subject variance
            - 'cv_percent': The calculated coefficient of variation as a percentage
            - 'within_subject_cv': The calculated coefficient of variation as a percentage (alias for backward compatibility)
            - 'parameter': The parameter used for calculation
            - 'n_subjects': Number of subjects included in the calculation
            - 'mse': The calculated within-subject variance (alias for backward compatibility)
            
        Notes
        -----
        The FDA considers a drug highly variable if the within-subject CV for the
        reference product is ≥ 30%. For highly variable drugs, reference-scaled
        approaches to bioequivalence may be appropriate.
        """
        # Ensure we have a valid parameter
        if parameter not in self.params_df.columns:
            raise ValueError(f"Parameter '{parameter}' not found in the parameter dataframe")
            
        # For replicate designs, we need repeated Reference measurements to calculate within-subject CV
        reference_data = self.params_df.filter(pl.col(self.form_col) == "Reference")
        
        # Group by subject and calculate variance
        subject_variances = reference_data.group_by(self.subject_col).agg(
            pl.col(parameter).var().alias("variance")
        )
        
        # Mean within-subject variance (MSE)
        mse = subject_variances["variance"].mean()
        
        # Calculate CV
        cv = np.sqrt(np.exp(mse) - 1) * 100
        
        return {
            "within_subject_variance": mse,
            "cv_percent": cv,
            "within_subject_cv": cv,
            "parameter": parameter,
            "n_subjects": len(subject_variances),
            "mse": mse
        }
        
    def run_rsabe(self, parameter: str = "log_AUC") -> Dict[str, any]:
        """
        Perform reference-scaled average bioequivalence (RSABE) analysis.
        
        This method implements the FDA's reference-scaled average bioequivalence approach
        for highly variable drugs. RSABE adjusts the bioequivalence limits based on the
        within-subject variability of the reference product.
        
        The method uses a mixed effects model to estimate the test-reference difference
        and constructs a linearized criterion for assessing bioequivalence:
        
            (μT - μR)² - θ·s²WR ≤ 0
        
        where:
        - μT and μR are the means for test and reference products
        - s²WR is the within-subject variance for the reference product
        - θ is a constant (0.893 for FDA approach, corresponding to the standard BE limits)
        
        Parameters
        ----------
        parameter : str, default="log_AUC"
            The log-transformed PK parameter to use for RSABE assessment.
            Typically "log_AUC" or "log_Cmax".
            
        Returns
        -------
        Dict[str, any]
            Dictionary containing:
            - 'model_summary': Summary of the mixed effects model
            - 'test_ref_diff': Estimated test-reference difference
            - 'within_subject_variance': Within-subject variance for reference product
            - 'within_subject_cv': Within-subject coefficient of variation for reference product
            - 'rsabe_criterion': Value of the linearized RSABE criterion
            - 'rsabe_criterion_met': Boolean indicating if bioequivalence is established
            - 'be_conclusion': Boolean indicating if bioequivalence is established (alias for backward compatibility)
            - 'expanded_limits': Expanded BE limits based on reference variability
            - 'point_estimate': Test/Reference ratio as a percentage
            - 'upper_scaled_limit': Upper expanded limit as a percentage
            - 'lower_scaled_limit': Lower expanded limit as a percentage
            
        Notes
        -----
        The FDA allows RSABE for highly variable drugs (within-subject CV ≥ 30%) 
        for Cmax, and in some cases for AUC. The method scales the BE limits based
        on the reference variability, but caps the expansion at 50-200%.
        
        References
        ----------
        FDA Guidance for Industry: Statistical Approaches to Establishing Bioequivalence, 2001.
        Davit, B. M., et al. (2012). Highly Variable Drugs: Observations from Bioequivalence
        Data Submitted to the FDA for New Generic Drug Applications. The AAPS Journal, 14(1), 148-158.
        """
        # Calculate within-subject CV
        cv_results = self.calculate_within_subject_cv(parameter)
        within_subject_variance = cv_results["within_subject_variance"]
        
        # Create model formula for mixed effects model
        formula = f"{parameter} ~ C({self.form_col}) + C({self.seq_col}) + C({self.period_col})"
        
        # Filter data to include only needed columns
        model_data = self.params_df.select([
            self.subject_col, self.seq_col, self.period_col, self.form_col, parameter
        ]).to_pandas()
        
        # Fit mixed effects model with subject as random effect
        model = smf.mixedlm(
            formula, 
            model_data,
            groups=model_data[self.subject_col]
        )
        
        model_fit = model.fit()
        
        # Get formulation effect (Test vs Reference)
        form_effect = None
        for term in model_fit.params.index:
            if self.form_col in term and "Test" in term:
                form_effect = model_fit.params[term]
                break
        
        if form_effect is None:
            raise ValueError("Could not extract formulation effect from model")
            
        # Calculate point estimate
        point_estimate = np.exp(form_effect) * 100
        
        # Calculate regulatory constant based on CV
        if cv_results["cv_percent"] <= 30:
            # Use standard BE limits for low-variability drugs
            lower_limit = 80
            upper_limit = 125
            regulatory_constant = 0
        else:
            # Scaling factor for highly variable drugs
            regulatory_constant = (cv_results["cv_percent"] / 100) ** 2
            
            # Scale the BE limits for high variability
            # Using FDA approach where the limits expand with increasing CV
            lower_limit = max(80 - (cv_results["cv_percent"] - 30), 75)
            upper_limit = min(125 + (cv_results["cv_percent"] - 30), 125)
        
        # Standard error
        se = np.sqrt(model_fit.cov_params().loc[term, term])
        
        # Calculate scaled criterion
        criterion = form_effect ** 2 - regulatory_constant * within_subject_variance
        
        # Calculate 95% upper confidence bound for criterion
        df = model_fit.df_resid
        t_crit = stats.t.ppf(0.95, df)
        ucb = criterion + t_crit * np.sqrt(4 * form_effect ** 2 * se ** 2 / model_fit.df_resid)
        
        # Bioequivalence is concluded if UCB <= 0
        be_conclusion = ucb <= 0
        
        # Return comprehensive results
        results = {
            "model_summary": str(model_fit.summary()),
            "test_ref_diff": form_effect,
            "within_subject_variance": within_subject_variance,
            "within_subject_cv": cv_results["within_subject_cv"],
            "rsabe_criterion": criterion,
            "rsabe_criterion_met": be_conclusion,
            "be_conclusion": be_conclusion,
            "expanded_limits": [lower_limit, upper_limit],
            "point_estimate": point_estimate,
            "upper_scaled_limit": upper_limit,
            "lower_scaled_limit": lower_limit,
            "reference_scaled_method": "RSABE",
            "formula": formula
        }
        
        return results
        
    def summarize_pk_parameters(self) -> pl.DataFrame:
        """
        Generate summary statistics for all PK parameters by formulation.
        
        This method calculates descriptive statistics for each pharmacokinetic parameter
        by formulation group. It provides a comprehensive statistical summary including
        sample size, mean, standard deviation, coefficient of variation, median, minimum,
        and maximum values.
        
        The summary statistics are useful for reporting in bioequivalence study reports
        and for comparing the general characteristics of test and reference formulations.
        
        Returns
        -------
        pl.DataFrame
            DataFrame containing summary statistics with the following columns:
            - Parameter: Name of the PK parameter (AUC, Cmax, etc.)
            - Formulation: Formulation group (Test or Reference)
            - N: Sample size
            - Mean: Arithmetic mean
            - SD: Standard deviation
            - CV%: Coefficient of variation as a percentage
            - Median: Median value
            - Min: Minimum value
            - Max: Maximum value
            
        Notes
        -----
        For replicate designs, this summary considers all observations for each formulation,
        meaning that if a subject received the same formulation multiple times, each administration
        contributes to the summary statistics.
        """
        summary_data = []
        
        # Parameters to summarize
        parameters = ["AUC", "Cmax", "Tmax"]
        if "t_half" in self.params_df.columns:
            parameters.append("t_half")
        if "AUC_inf" in self.params_df.columns:
            parameters.append("AUC_inf")
            
        for parameter in parameters:
            for formulation in self.params_df[self.form_col].unique():
                # Filter data for this formulation
                form_data = self.params_df.filter(pl.col(self.form_col) == formulation)
                
                # Skip if parameter not in dataframe
                if parameter not in form_data.columns:
                    continue
                    
                # Calculate statistics
                param_data = form_data[parameter].to_numpy()
                param_data = param_data[~np.isnan(param_data)]
                
                if len(param_data) == 0:
                    continue
                    
                n = len(param_data)
                mean = np.mean(param_data)
                sd = np.std(param_data, ddof=1)
                cv = (sd / mean) * 100 if mean != 0 else np.nan
                median = np.median(param_data)
                min_val = np.min(param_data)
                max_val = np.max(param_data)
                
                summary_data.append({
                    "Parameter": parameter,
                    "Formulation": formulation,
                    "N": n,
                    "Mean": mean,
                    "SD": sd,
                    "CV%": cv,
                    "Median": median,
                    "Min": min_val,
                    "Max": max_val
                })
                
        return pl.DataFrame(summary_data)
        
    def export_results(self, file_path: str) -> None:
        """
        Export analysis results to a CSV file.
        
        Parameters
        ----------
        file_path : str
            Path to save the results
        """
        # Export the PK parameters
        self.params_df.write_csv(file_path)
        
    def get_params_df(self) -> pl.DataFrame:
        """
        Get the calculated PK parameters dataframe.
        
        Returns
        -------
        pl.DataFrame
            DataFrame containing all calculated PK parameters
        """
        return self.params_df.clone() 