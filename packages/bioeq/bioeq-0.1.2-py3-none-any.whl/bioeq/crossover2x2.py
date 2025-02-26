import polars as pl
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from typing import Dict, List, Optional, Tuple, Union


class Crossover2x2:
    """
    Analyze a 2x2 crossover study to compute bioequivalence (BE) metrics and statistical analyses.
    
    This class implements the standard methods for analyzing data from a 2x2 crossover 
    bioequivalence study, including computation of:
    - Area under the curve (AUC)
    - Maximum concentration (Cmax)
    - Time to maximum concentration (Tmax)
    - Log-transformed PK parameters
    - Statistical analyses (ANOVA, mixed effects models)
    - Point estimates and 90% confidence intervals for BE assessment
    
    Parameters
    ----------
    data : pl.DataFrame
        Input dataset containing concentration-time profiles
    subject_col : str
        Column name for subject identifiers
    seq_col : str
        Column name for sequence information (e.g., "RT", "TR")
    period_col : str
        Column name for period information (e.g., 1, 2)
    time_col : str
        Column name for time points
    conc_col : str
        Column name for concentration measurements
    form_col : str
        Column name for formulation information (Test vs Reference)
    
    Attributes
    ----------
    params_df : pl.DataFrame
        DataFrame containing calculated PK parameters for each subject/period/formulation
    """

    def __init__(
        self,
        data: pl.DataFrame,
        subject_col: str,
        seq_col: str,
        period_col: str,
        time_col: str,
        conc_col: str,
        form_col: str,
    ) -> None:
        """Initialize the Crossover2x2 analyzer with study data and column specifications."""

        self._data = data
        self._subject_col = subject_col
        self._seq_col = seq_col
        self._period_col = period_col
        self._time_col = time_col
        self._conc_col = conc_col
        self._form_col = form_col

        self._validate_data()
        self._validate_colvals()

        # Calculate all PK parameters
        self._df_params = self._calculate_auc()
        self._df_params = self._calculate_cmax()
        self._df_params = self._calculate_tmax()
        self._df_params = self._calculate_log_transform()
        self._df_params = self._calculate_half_life()
        self._df_params = self._calculate_auc_extrapolated()

        # Sort the dataframe for better readability
        self.params_df = self._df_params.sort(
            [self._subject_col, self._form_col, self._period_col]
        )

    def _validate_data(self) -> None:
        """Check that data is a Polars DataFrame."""
        if not isinstance(self._data, pl.DataFrame):
            raise TypeError("Data must be a Polars DataFrame")

    def _validate_colvals(self) -> None:
        """Ensure all required columns exist in the dataset."""
        required = [
            self._subject_col,
            self._seq_col,
            self._period_col,
            self._time_col,
            self._conc_col,
            self._form_col,
        ]
        missing = [col for col in required if col not in self._data.columns]
        if missing:
            raise ValueError(
                f"Required column(s) not found in dataset: {', '.join(missing)}"
            )

    def _calculate_auc(self) -> pl.DataFrame:
        """
        Compute AUC (Area Under the Curve) using the trapezoidal rule.
        
        Returns
        -------
        pl.DataFrame
            DataFrame with AUC values added
        """
        grouped_df = self._data.group_by(
            [self._subject_col, self._period_col, self._seq_col, self._form_col]
        ).agg([pl.col(self._time_col), pl.col(self._conc_col)])
        auc_vals = [
            np.trapezoid(row[self._conc_col], row[self._time_col])
            for row in grouped_df.to_dicts()
        ]
        return grouped_df.with_columns(pl.Series("AUC", auc_vals))

    def _calculate_cmax(self) -> pl.DataFrame:
        """
        Compute Cmax (maximum concentration).
        
        Returns
        -------
        pl.DataFrame
            DataFrame with Cmax values added
        """
        cmax_df = self._data.group_by(
            [self._subject_col, self._period_col, self._form_col]
        ).agg(pl.col(self._conc_col).max().alias("Cmax"))
        return self._df_params.join(
            cmax_df, on=[self._subject_col, self._period_col, self._form_col]
        )

    def _calculate_tmax(self) -> pl.DataFrame:
        """
        Compute Tmax (time when Cmax occurs).
        
        Returns
        -------
        pl.DataFrame
            DataFrame with Tmax values added
        """
        tmax_df = (
            self._data.filter(
                pl.col(self._conc_col)
                == pl.col(self._conc_col)
                .max()
                .over([self._subject_col, self._period_col, self._form_col])
            )
            .group_by([self._subject_col, self._period_col, self._form_col])
            .agg(pl.col(self._time_col).min().alias("Tmax"))
        )
        return self._df_params.join(
            tmax_df, on=[self._subject_col, self._period_col, self._form_col]
        )

    def _calculate_log_transform(self) -> pl.DataFrame:
        """
        Compute log-transformed AUC and Cmax.
        
        Returns
        -------
        pl.DataFrame
            DataFrame with log-transformed values added
        """
        return self._df_params.with_columns(
            [
                pl.col("AUC").log().alias("log_AUC"),
                pl.col("Cmax").log().alias("log_Cmax"),
            ]
        )

    def _calculate_half_life(self) -> pl.DataFrame:
        """
        Estimate elimination half-life using log-linear regression on terminal phase.
        
        This is a simplified estimation using the last 3 time points.
        
        Returns
        -------
        pl.DataFrame
            DataFrame with half-life estimates added
        """
        half_lives = []
        for row in self._df_params.to_dicts():
            subject = row[self._subject_col]
            period = row[self._period_col]
            formulation = row[self._form_col]
            
            # Get concentration-time data for this subject/period/formulation
            subject_data = self._data.filter(
                (pl.col(self._subject_col) == subject) &
                (pl.col(self._period_col) == period) &
                (pl.col(self._form_col) == formulation)
            ).sort(self._time_col)
            
            times = subject_data[self._time_col].to_numpy()
            concs = subject_data[self._conc_col].to_numpy()
            
            # Use last 3 time points if available, otherwise use all time points except t=0
            if len(times) >= 4:  # At least 4 points (including t=0)
                terminal_times = times[-3:]
                terminal_concs = concs[-3:]
            else:
                terminal_times = times[1:] if len(times) > 1 else times
                terminal_concs = concs[1:] if len(concs) > 1 else concs
            
            # Skip if all concentrations are zero or less than 3 points
            if np.all(terminal_concs <= 0) or len(terminal_times) < 2:
                half_lives.append(None)
                continue
                
            # Remove any zero concentrations
            valid_indices = terminal_concs > 0
            if np.sum(valid_indices) < 2:
                half_lives.append(None)
                continue
                
            valid_times = terminal_times[valid_indices]
            valid_concs = terminal_concs[valid_indices]
            
            # Linear regression on log-transformed concentrations
            log_concs = np.log(valid_concs)
            X = sm.add_constant(valid_times)
            model = sm.OLS(log_concs, X).fit()
            
            # Calculate half-life (t1/2 = ln(2)/ke, where ke is the slope)
            slope = model.params[1]
            if slope >= 0:  # Invalid slope (should be negative)
                half_lives.append(None)
            else:
                half_life = np.log(2) / (-slope)
                half_lives.append(half_life)
                
        return self._df_params.with_columns(
            pl.Series("t_half", half_lives).alias("t_half")
        )

    def _calculate_auc_extrapolated(self) -> pl.DataFrame:
        """
        Calculate AUC extrapolated to infinity using the terminal elimination rate constant.
        
        AUC_inf = AUC_last + C_last/ke, where ke is obtained from half-life estimation.
        
        Returns
        -------
        pl.DataFrame
            DataFrame with AUC_inf values added
        """
        auc_inf_values = []
        
        for row in self._df_params.to_dicts():
            subject = row[self._subject_col]
            period = row[self._period_col]
            formulation = row[self._form_col]
            t_half = row.get("t_half")
            
            if t_half is None or t_half <= 0:
                auc_inf_values.append(None)
                continue
            
            # Get concentration-time data for this subject/period/formulation
            subject_data = self._data.filter(
                (pl.col(self._subject_col) == subject) &
                (pl.col(self._period_col) == period) &
                (pl.col(self._form_col) == formulation)
            ).sort(self._time_col)
            
            # Get the last concentration
            if len(subject_data) > 0:
                last_time = subject_data[self._time_col][-1]
                last_conc = subject_data[self._conc_col][-1]
                
                # Calculate terminal elimination rate constant
                ke = np.log(2) / t_half
                
                # Calculate extrapolated AUC
                auc_extrapolated = last_conc / ke if ke > 0 else 0
                auc_inf = row["AUC"] + auc_extrapolated
                auc_inf_values.append(auc_inf)
            else:
                auc_inf_values.append(None)
        
        return self._df_params.with_columns(
            pl.Series("AUC_inf", auc_inf_values).alias("AUC_inf")
        )

    def run_anova(self, metric: str) -> Dict[str, any]:
        """
        Perform ANOVA for the specified metric.
        
        Parameters
        ----------
        metric : str
            The PK parameter to analyze (e.g., "AUC", "Cmax", "log_AUC", "log_Cmax")
            
        Returns
        -------
        Dict
            Dictionary with ANOVA results
            
        Notes
        -----
        The function displays unique levels for formulation, period, and sequence before 
        printing ANOVA results, and performs validation checks.
        """
        df = self._df_params.to_pandas()
        unique_form = df[self._form_col].unique()
        unique_period = df[self._period_col].unique()
        unique_seq = df[self._seq_col].unique()

        print("Formulation levels:", unique_form)
        print("Period levels:", unique_period)
        print("Sequence levels:", unique_seq)

        if len(unique_form) < 2:
            error_msg = "Error: Formulation is constant. Provide data with ≥2 formulation levels."
            print(error_msg)
            return {"error": error_msg}
            
        if len(unique_period) < 2:
            error_msg = "Error: Period is constant. Provide data with ≥2 period levels."
            print(error_msg)
            return {"error": error_msg}
            
        if len(unique_seq) < 2:
            error_msg = "Error: Sequence is confounded. Provide data with ≥2 sequence levels."
            print(error_msg)
            return {"error": error_msg}

        formula = f"{metric} ~ C({self._form_col}) + C({self._period_col}) + C({self._seq_col})"
        model = smf.ols(formula, data=df).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        print("ANOVA Results for", metric)
        print(anova_table)
        
        return {
            "anova_table": anova_table,
            "model": model,
            "formula": formula
        }

    def run_nlme(self, metric: str) -> Dict[str, any]:
        """
        Perform a mixed effects model analysis for the specified metric.
        
        Parameters
        ----------
        metric : str
            The PK parameter to analyze (e.g., "AUC", "Cmax", "log_AUC", "log_Cmax")
            
        Returns
        -------
        Dict
            Dictionary with mixed effects model results
            
        Notes
        -----
        The function displays unique levels for formulation, period, and sequence before 
        printing model summary, and performs validation checks.
        """
        df = self._df_params.to_pandas()
        unique_form = df[self._form_col].unique()
        unique_period = df[self._period_col].unique()
        unique_seq = df[self._seq_col].unique()

        print("Formulation levels:", unique_form)
        print("Period levels:", unique_period)
        print("Sequence levels:", unique_seq)

        if len(unique_form) < 2:
            error_msg = "Error: Formulation is constant. Provide data with ≥2 formulation levels."
            print(error_msg)
            return {"error": error_msg}
            
        if len(unique_period) < 2:
            error_msg = "Error: Period is constant. Provide data with ≥2 period levels."
            print(error_msg)
            return {"error": error_msg}
            
        if len(unique_seq) < 2:
            error_msg = "Error: Sequence is confounded. Provide data with ≥2 sequence levels."
            print(error_msg)
            return {"error": error_msg}

        formula = f"{metric} ~ C({self._form_col}) + C({self._period_col}) + C({self._seq_col})"
        model = smf.mixedlm(formula, data=df, groups=df[self._subject_col])
        mdf = model.fit()
        print("Mixed Effects Model Results for", metric)
        print(mdf.summary())
        
        return {
            "model_summary": mdf.summary(),
            "model": mdf,
            "formula": formula
        }
        
    def calculate_point_estimate(self, metric: str = "log_AUC") -> Dict[str, float]:
        """
        Calculate point estimate for Test/Reference ratio.
        
        Parameters
        ----------
        metric : str
            The log-transformed PK parameter to analyze (default: "log_AUC")
            
        Returns
        -------
        Dict
            Dictionary with point estimate and confidence intervals
        """
        if not metric.startswith("log_"):
            print(f"Warning: {metric} may not be log-transformed. Point estimates are valid for log-transformed metrics.")
        
        df = self._df_params.to_pandas()
        
        # Filter out rows with missing values
        df_valid = df.dropna(subset=[metric])
        
        # Fit mixed effects model
        formula = f"{metric} ~ C({self._form_col}) + C({self._period_col}) + C({self._seq_col})"
        model = smf.mixedlm(formula, data=df_valid, groups=df_valid[self._subject_col])
        result = model.fit()
        
        # Extract coefficient for Test formulation
        coef_index = result.params.index[result.params.index.str.contains(self._form_col)]
        if len(coef_index) == 0:
            return {"error": f"Could not find coefficient for {self._form_col}"}
            
        test_ref_diff = result.params[coef_index[0]]
        
        # Calculate confidence intervals
        conf_int = result.conf_int(alpha=0.1)  # 90% CI for bioequivalence
        lower_ci = conf_int.loc[coef_index[0], 0]
        upper_ci = conf_int.loc[coef_index[0], 1]
        
        # Convert from log scale to ratio
        point_estimate = np.exp(test_ref_diff) * 100  # as percentage
        lower_ci_ratio = np.exp(lower_ci) * 100       # as percentage
        upper_ci_ratio = np.exp(upper_ci) * 100       # as percentage
        
        # Check if bioequivalence criteria are met (80-125% rule)
        be_criteria_met = 80 <= lower_ci_ratio and upper_ci_ratio <= 125
        
        results = {
            "point_estimate": point_estimate,
            "lower_90ci": lower_ci_ratio,
            "upper_90ci": upper_ci_ratio,
            "be_criteria_met": be_criteria_met
        }
        
        print(f"Point Estimate (Test/Reference): {point_estimate:.2f}%")
        print(f"90% Confidence Interval: {lower_ci_ratio:.2f}% - {upper_ci_ratio:.2f}%")
        if be_criteria_met:
            print("Bioequivalence criteria MET (80-125% rule)")
        else:
            print("Bioequivalence criteria NOT MET (80-125% rule)")
            
        return results
        
    def summarize_pk_parameters(self) -> pl.DataFrame:
        """
        Calculate summary statistics for PK parameters by formulation.
        
        Returns
        -------
        pl.DataFrame
            DataFrame with summary statistics
        """
        # Define the parameters to summarize
        pk_params = ["AUC", "Cmax", "Tmax", "t_half", "AUC_inf"]
        
        # Create an empty list to hold the result rows
        summary_rows = []
        
        for param in pk_params:
            if param not in self._df_params.columns:
                continue
                
            # Group by formulation and calculate statistics
            summary = (
                self._df_params
                .group_by(self._form_col)
                .agg([
                    pl.col(param).mean().alias("Mean"),
                    pl.col(param).std().alias("SD"),
                    pl.col(param).median().alias("Median"),
                    pl.col(param).min().alias("Min"),
                    pl.col(param).max().alias("Max"),
                    pl.col(param).count().alias("N")
                ])
            )
            
            # Convert to rows for each parameter
            for row in summary.to_dicts():
                summary_row = {
                    "Parameter": param,
                    "Formulation": row[self._form_col],
                    "N": row["N"],
                    "Mean": row["Mean"],
                    "SD": row["SD"],
                    "Median": row["Median"],
                    "Min": row["Min"],
                    "Max": row["Max"],
                    "CV%": (row["SD"] / row["Mean"] * 100) if row["Mean"] != 0 else None
                }
                summary_rows.append(summary_row)
        
        # Create DataFrame from the rows
        return pl.DataFrame(summary_rows)
        
    def export_results(self, file_path: str) -> None:
        """
        Export PK parameters and derived results to a CSV file.
        
        Parameters
        ----------
        file_path : str
            Path where the CSV file will be saved
        """
        # Ensure we have the most updated parameter data
        self._df_params.write_csv(file_path)
        print(f"Results exported to {file_path}")

    def get_params_df(self) -> pl.DataFrame:
        """
        Get the DataFrame containing all calculated PK parameters.
        
        Returns
        -------
        pl.DataFrame
            DataFrame with PK parameters
        """
        return self._df_params
