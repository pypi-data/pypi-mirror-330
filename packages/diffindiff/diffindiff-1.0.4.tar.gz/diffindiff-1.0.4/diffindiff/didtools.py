# -------------------------------------------------------------------------------
# Name:        didtools (diffindiff)
# Purpose:     Creating data for Difference-in-Differences Analysis
# Author:      Thomas Wieland (geowieland@googlemail.com)
# Version:     1.0.3
# Last update: 2025-02-26 18:22
# Copyright (c) 2025 Thomas Wieland
#-------------------------------------------------------------------------------

import pandas as pd
import numpy as np


def is_balanced (
    data,
    unit_col,
    time_col,
    outcome_col,
    other_cols = None
    ):

    unit_freq = data[unit_col].nunique()
    time_freq = data[time_col].nunique()
    unitxtime = unit_freq*time_freq

    if other_cols is None:
        cols_relevant = [unit_col, time_col, outcome_col]
    else:
        cols_relevant = [unit_col, time_col, outcome_col] + other_cols

    data_relevant = data[cols_relevant]

    if unitxtime != len(data_relevant.notna()):
        return False
    else:
        return True

def is_missing(
    data,
    drop_missing: bool = True,
    missing_replace_by_zero: bool = False
    ):

    missing_outcome = data.isnull().any()
    missing_outcome_var = any(missing_outcome == True)

    if missing_outcome_var:
        missing_true_vars = [name for name, value in missing_outcome.items() if value]
    else:
        missing_true_vars = []

    if drop_missing:
        if missing_replace_by_zero:
            missing_replace_by_zero = False
        data = data.dropna(subset = missing_true_vars)
        
    if missing_replace_by_zero:
        data[missing_true_vars] = data[missing_true_vars].fillna(0)

    return [missing_outcome_var, missing_true_vars, data]

def is_simultaneous(
    data,
    unit_col,
    time_col,
    treatment_col
    ):

    data_isnotreatment = is_notreatment(data, unit_col, treatment_col)
    treatment_group = data_isnotreatment[1]
    data_TG = data[data[unit_col].isin(treatment_group)]

    data_TG_pivot = data_TG.pivot_table (index = time_col, columns = unit_col, values = treatment_col)

    col_identical = (data_TG_pivot.nunique(axis=1) == 1).all()

    return col_identical

def is_notreatment(
    data,
    unit_col,
    treatment_col
    ):

    data_relevant = data[[unit_col, treatment_col]]

    treatment_timepoints = data_relevant.groupby(unit_col).sum(treatment_col)
    treatment_timepoints = treatment_timepoints.reset_index()

    no_treatment = (treatment_timepoints[treatment_col] == 0).any()

    treatment_group = treatment_timepoints.loc[treatment_timepoints[treatment_col] > 0, unit_col]
    control_group = treatment_timepoints.loc[treatment_timepoints[treatment_col] == 0, unit_col]

    return [no_treatment, treatment_group, control_group]

def date_counter(df, date_col, new_col = "date_counter"):
    
    dates = df[date_col].unique()

    date_counter = pd.DataFrame({
       'date': dates,
        new_col: range(1, len(dates) + 1)
        })

    df = df.merge(
        date_counter,
        left_on = date_col,
        right_on = "date")
    
    return df