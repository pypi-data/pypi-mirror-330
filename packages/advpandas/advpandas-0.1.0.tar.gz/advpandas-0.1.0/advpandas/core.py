import pandas as pd

def advanced_head(df, n=5):
    """
    An advanced version of pandas' head() method.
    Adds additional metadata about the DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        n (int): Number of rows to display.

    Returns:
        pd.DataFrame: A DataFrame with metadata.
    """
    print(f"DataFrame Shape: {df.shape}")
    print(f"Number of Columns: {len(df.columns)}")
    print("Column Names:", list(df.columns))
    return df.head(n)