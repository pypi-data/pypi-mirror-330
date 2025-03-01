import pandas as pd
import numpy as np
from scipy.stats import ks_2samp, chi2_contingency
from typing import Dict, Any


class DriftDetector:
    """
    Advanced drift detector with configurable thresholds and comprehensive per-feature analysis.
    """

    def __init__(
        self,
        ks_alpha: float = 0.05,
        tvd_threshold: float = 0.1,
        mean_diff_threshold: float = 0.1,
        std_diff_threshold: float = 0.1,
        chi2_alpha: float = 0.05,
    ):
        """
        Initialize the detector with thresholds.
        :param ks_alpha: Significance level for the KS test.
        :param tvd_threshold: Threshold for total variation distance (categorical drift).
        :param mean_diff_threshold: Threshold for mean difference (numerical drift).
        :param std_diff_threshold: Threshold for standard deviation difference (numerical drift).
        :param chi2_alpha: Significance level for the chi-squared test.
        """
        self.ks_alpha = ks_alpha
        self.tvd_threshold = tvd_threshold
        self.mean_diff_threshold = mean_diff_threshold
        self.std_diff_threshold = std_diff_threshold
        self.chi2_alpha = chi2_alpha

    def detect_drift(
        self, current_data: pd.DataFrame, reference_data: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Perform drift detection over numerical and categorical features.
        Returns a detailed report including per-feature drift indicators and an overall drift flag.
        """
        drift_report = {}
        drift_flags = []
        # Analyze numerical features
        numerical_features = current_data.select_dtypes(include=[np.number]).columns
        drift_report["numerical"] = {}
        for feature in numerical_features:
            current = current_data[feature].dropna()
            reference = reference_data[feature].dropna()
            if len(current) == 0 or len(reference) == 0:
                drift_report["numerical"][feature] = {
                    "error": "Insufficient data for drift detection"
                }
                continue
            ks_stat, ks_p = ks_2samp(reference, current)
            mean_diff = abs(current.mean() - reference.mean())
            std_diff = abs(current.std() - reference.std())
            numeric_flags = {
                "ks_drift": ks_p < self.ks_alpha,
                "mean_drift": mean_diff > self.mean_diff_threshold,
                "std_drift": std_diff > self.std_diff_threshold,
            }
            overall_numeric_flag = any(numeric_flags.values())
            drift_report["numerical"][feature] = {
                "ks_statistic": ks_stat,
                "ks_p_value": ks_p,
                "mean_difference": mean_diff,
                "std_difference": std_diff,
                "drift_flag": overall_numeric_flag,
                "detailed_flags": numeric_flags,
            }
            drift_flags.append(overall_numeric_flag)
        # Analyze categorical features
        categorical_features = current_data.select_dtypes(
            include=["category", "object"]
        ).columns
        drift_report["categorical"] = {}
        for feature in categorical_features:
            current_dist = current_data[feature].value_counts(normalize=True)
            reference_dist = reference_data[feature].value_counts(normalize=True)
            all_categories = set(current_dist.index).union(set(reference_dist.index))
            current_dist = current_dist.reindex(
                all_categories, fill_value=0
            ).sort_index()
            reference_dist = reference_dist.reindex(
                all_categories, fill_value=0
            ).sort_index()
            tvd = 0.5 * np.sum(np.abs(current_dist - reference_dist))
            chi2_p = self._chi2_test(current_data, reference_data, feature)
            categorical_flags = {
                "tvd_drift": tvd > self.tvd_threshold,
                "chi2_drift": chi2_p < self.chi2_alpha,
            }
            overall_categorical_flag = any(categorical_flags.values())
            drift_report["categorical"][feature] = {
                "tvd": tvd,
                "chi2_p_value": chi2_p,
                "drift_flag": overall_categorical_flag,
                "detailed_flags": categorical_flags,
            }
            drift_flags.append(overall_categorical_flag)
        # Overall drift determination
        drift_report["overall_drift"] = any(drift_flags)
        drift_report["drift_summary"] = {
            "total_features": len(numerical_features) + len(categorical_features),
            "features_with_drift": sum(drift_flags),
        }
        return drift_report

    def _chi2_test(
        self, current: pd.DataFrame, reference: pd.DataFrame, feature: str
    ) -> float:
        """
        Conduct a chi-squared test for a categorical feature.
        Returns the p-value.
        """
        current_counts = current[feature].value_counts()
        reference_counts = reference[feature].value_counts()
        all_categories = set(current_counts.index).union(set(reference_counts.index))
        current_counts = current_counts.reindex(all_categories, fill_value=0)
        reference_counts = reference_counts.reindex(all_categories, fill_value=0)
        contingency_table = (
            pd.DataFrame({"current": current_counts, "reference": reference_counts})
            .transpose()
            .values
        )
        _, p_value, _, _ = chi2_contingency(contingency_table)
        return p_value
