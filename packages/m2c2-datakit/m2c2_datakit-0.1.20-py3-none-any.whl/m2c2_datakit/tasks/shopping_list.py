import pandas as pd


def score(row):
    """
    Score a single trial by determining if the response is correct.
    The correctness logic is based on 'response_correct'.
    """
    try:
        return row["response_correct"]
    except Exception as e:
        print(f"Error processing row: {e}")
        return None


def summarize(df, trials_expected=10, rt_outlier_low=100, rt_outlier_high=10000):
    """
    Summarizes Shopping List task performance for both phases separately.

    Args:
        df (pd.DataFrame): Trial-level scored dataset.
        trials_expected (int): Expected number of trials per phase.
        rt_outlier_low (int): Lower bound for valid response times.
        rt_outlier_high (int): Upper bound for valid response times.

    Returns:
        pd.Series: Summary statistics for each phase.
    """
    summary = {}

    for phase in df["phase"].unique():
        phase_df = df[df["phase"] == phase]

        # Number of trials in this phase
        summary[f"phase_{phase}_number_of_trials"] = phase_df["trial_index"].nunique()

        # Check if trials match expectations
        summary[f"phase_{phase}_flag_trials_match_expected"] = (
            summary[f"phase_{phase}_number_of_trials"] == trials_expected
        )
        summary[f"phase_{phase}_flag_trials_lt_expected"] = (
            summary[f"phase_{phase}_number_of_trials"] < trials_expected
        )
        summary[f"phase_{phase}_flag_trials_gt_expected"] = (
            summary[f"phase_{phase}_number_of_trials"] > trials_expected
        )

        # Correct/incorrect responses
        summary[f"phase_{phase}_n_trials_correct"] = phase_df["response_correct"].sum()
        summary[f"phase_{phase}_n_trials_incorrect"] = (
            phase_df.shape[0] - summary[f"phase_{phase}_n_trials_correct"]
        )

        # Filter response times to remove outliers
        rt_filtered = phase_df.loc[
            (phase_df["response_time_ms"] >= rt_outlier_low)
            & (phase_df["response_time_ms"] <= rt_outlier_high),
            "response_time_ms",
        ]
        summary[f"phase_{phase}_median_response_time_filtered"] = rt_filtered.median()

        # Overall response time stats
        summary[f"phase_{phase}_median_response_time_overall"] = phase_df[
            "response_time_ms"
        ].median()
        summary[f"phase_{phase}_median_response_time_correct"] = phase_df.loc[
            phase_df["response_correct"] == True, "response_time_ms"
        ].median()
        summary[f"phase_{phase}_median_response_time_incorrect"] = phase_df.loc[
            phase_df["response_correct"] == False, "response_time_ms"
        ].median()

    return pd.Series(summary)
