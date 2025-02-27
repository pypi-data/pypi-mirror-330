from math import log, pi
import numpy as np
import inspect

def FF_to_conc(ff, volume, concentration):
    return_list = []
    for i in ff:
        if 0 < i < 1:  # Ensure that 1 - i is positive
            result = -np.log(1 - i) / (volume * concentration)  # Use np.log for logarithm
            return_list.append(result)
        else:
            return_list.append(float('nan'))  # Append NaN for invalid values
    return return_list

def FF_to_volume(ff, diameter, volume, concentration):
    return_list = []
    for i in ff:
        if 0 < i < 1:  # Ensure that 1 - i is positive
            return_list.append(-log(1 - i) / (volume * concentration * (4/3) * pi * ((diameter/2) ** 3)))
        else:
            return_list.append(float('nan'))  # Append NaN for invalid values
    return return_list

def FF_to_surface(ff, diameter, volume, concentration):
    return_list = []
    for i in ff:
        if 0 < i < 1:  # Ensure that 1 - i is positive
            return_list.append(-log(1 - i) / (volume * concentration * 4 * pi * ((diameter / 2) ** 2)))
        else:
            return_list.append(float('nan'))  # Append NaN for invalid values
    return return_list

def FF_to_mass(ff, volume, mass_concentration):
    return_list = []
    for i in ff:
        if 0 < i < 1:  # Ensure that 1 - i is positive
            return_list.append(-log(1 - i) / (volume * mass_concentration))
        else:
            return_list.append(float('nan'))  # Append NaN for invalid values
    return return_list


def calculateDifferentialSpectra(temperatures, V, delta_T):
    """
    Calculate k(T) values for binned temperature data from -40 to 0.

    Parameters:
    V (float): Volume of droplets (constant).
    temperatures (list of float): List of temperature values.
    delta_T (float): Size of the interval.

    Returns:
    temp_bins (list of float): List of bin midpoints for the chart.
    Diff_Nuclei_Conc (list of float): Calculated k(T) values corresponding to the bin midpoints.
    """
    # Define bin edges from -40 to 5 with the specified delta_T
    bin_edges = np.arange(-40, 6, delta_T)

    # Create bins for the temperatures
    counts, _ = np.histogram(temperatures, bins=bin_edges)

    temp_bins = []
    Diff_Nuclei_Conc = []

    # Calculate k(T) for each bin
    for i in range(len(counts)):
        delta_N = counts[i]  # Number of frozen droplets in this bin

        # Calculate N(T) as the number of unfrozen droplets (count in bins of lower value than this)
        N_T = np.sum(counts[:i])  # Sum counts of all lower temperature bins

        # Ensure N(T) is not zero to avoid division by zero
        if N_T == 0:
            continue  # Skip the calculation for this bin if N(T) is zero

        # Calculate bin midpoint for plotting
        bin_midpoint = (bin_edges[i] + bin_edges[i + 1]) / 2

        if delta_N > 0:  # Only calculate k(T) for bins with data
            # Check to avoid log(0) or log of negative number
            fraction = delta_N / N_T
            if fraction >= 1:
                continue  # Skip calculation if delta_N is greater than or equal to N(T)

            k_T = - (1 / (V * delta_T)) * np.log(1 - fraction)
            temp_bins.append(bin_midpoint)
            Diff_Nuclei_Conc.append(k_T)

    return temp_bins, Diff_Nuclei_Conc


# Helper function: Bin and average (UPDATED to reverse rows)
def bin_and_average(data, rounding=0.5, temp_col='T', value_col='f',
                    temp_range=(-40, 0), min_points=1):
    """
    Bin temperatures and calculate the mean value for each bin.
    Replace NaNs before the first valid value with 0,
    and forward-fill NaN values after the first valid value with the most recent value.
    """
    # Create bins from high to low temperatures
    bins = np.arange(temp_range[1], temp_range[0] - rounding, -rounding)

    # Use digitize with reversed bins
    data['bin'] = np.digitize(data[temp_col], bins, right=True)

    # Group by bins and calculate counts and mean
    binned_group = data.groupby('bin').agg(
        Mean_value=(value_col, 'mean'),
        Count=(value_col, 'count')
    ).reset_index()

    # Filter out bins with fewer than min_points
    binned_group = binned_group[binned_group['Count'] >= min_points]

    # Map bin indices back to bin midpoints (now from high to low)
    binned_group['T_round'] = bins[binned_group['bin'] - 1] - rounding / 2

    # Include all bins (even empty ones) in the final DataFrame
    all_bins_df = pd.DataFrame({'T_round': bins[:-1] - rounding / 2})
    final_data = pd.merge(all_bins_df, binned_group[['T_round', 'Mean_value']],
                          on='T_round', how='left')

    # Sort from highest to lowest temperature
    final_data = final_data.sort_values('T_round',
                                        ascending=False).reset_index(drop=True)

    # Handle NaN values:
    # 1. Replace NaNs at the very beginning with 0
    first_valid_idx = final_data['Mean_value'].first_valid_index()
    if first_valid_idx is not None:
        final_data.loc[:first_valid_idx, 'Mean_value'] = final_data[
                                                             'Mean_value'].loc[
                                                         :first_valid_idx].fillna(
            0)

    # 2. Forward-fill only after the first valid value
    final_data['Mean_value'] = final_data['Mean_value'].ffill()

    return final_data


def INP_Uncertainty(*datasets, rounding=0.5, temp_col='T', value_col='f',
                    temp_range=(-40, 0), confidence=0.83, min_points=1):
    # Helper function to clean datasets
    def clean_dataset(data):
        """
        Clean the dataset by:
        1. Converting columns to numeric
        2. Replacing infinity with NaN
        3. Dropping NaN values
        """
        cleaned_data = data.copy()
        cleaned_data[temp_col] = pd.to_numeric(cleaned_data[temp_col],
                                               errors='coerce')
        cleaned_data[value_col] = pd.to_numeric(cleaned_data[value_col],
                                                errors='coerce')
        cleaned_data.replace([np.inf, -np.inf], np.nan, inplace=True)
        cleaned_data.dropna(subset=[temp_col, value_col], inplace=True)
        return cleaned_data

    # Helper function: Combine datasets
    def combine_datasets(*datasets, rounding=0.5, temp_col='T', value_col='f',
                         temp_range=(-40, 0), confidence=0.83, min_points=1):
        cleaned_datasets = [clean_dataset(dataset) for dataset in datasets]
        caller_frame = inspect.currentframe().f_back
        variable_names = {id(v): k for k, v in caller_frame.f_locals.items()}
        dataset_names = [variable_names.get(id(dataset), f"Run_{i + 1}") for
                         i, dataset in enumerate(datasets)]

        first_dataset_binned = bin_and_average(cleaned_datasets[0], rounding,
                                               temp_col, value_col, temp_range,
                                               min_points)
        midpoints = first_dataset_binned['T_round']
        all_results = []

        for dataset in cleaned_datasets:
            binned_data = bin_and_average(dataset, rounding, temp_col,
                                          value_col, temp_range, min_points)
            merged_data = pd.merge(pd.DataFrame({'T_round': midpoints}),
                                   binned_data, on='T_round', how='left')
            all_results.append(merged_data['Mean_value'].values)

        combined_df = pd.DataFrame(all_results).transpose()
        combined_df.columns = dataset_names
        combined_df.insert(0, 'T_round', midpoints)
        combined_df = combined_df.dropna(how='all', subset=dataset_names)

        # Drop rows where all data columns are zero
        combined_df = combined_df[
            (combined_df[dataset_names].sum(axis=1) != 0)]

        # Update the trimming logic to work with reversed order
        while len(combined_df) > 1:
            last_row = combined_df.iloc[-1, 1:].values
            second_last_row = combined_df.iloc[-2, 1:].values
            if np.array_equal(last_row, second_last_row):
                combined_df = combined_df.iloc[:-1]
            else:
                break

        stats_df = combined_df.iloc[:, 1:]
        combined_df['Mean_value'] = stats_df.mean(axis=1, skipna=True)
        combined_df['std_dev'] = stats_df.std(axis=1, skipna=True)

        alpha = 1 - confidence
        t_values = stats_df.notna().sum(axis=1).apply(
            lambda n: t.ppf(1 - alpha / 2, n - 1) if n > 1 else np.nan
        )
        combined_df[f'CI_{int(confidence * 100)}'] = t_values * (
                    combined_df['std_dev'] / np.sqrt(
                stats_df.notna().sum(axis=1)))

        return combined_df[
            ['T_round'] + dataset_names + ['Mean_value', 'std_dev',
                                           f'CI_{int(confidence * 100)}']]

    return combine_datasets(*datasets, rounding=rounding, temp_col=temp_col,
                            value_col=value_col, temp_range=temp_range,
                            confidence=confidence, min_points=min_points)
