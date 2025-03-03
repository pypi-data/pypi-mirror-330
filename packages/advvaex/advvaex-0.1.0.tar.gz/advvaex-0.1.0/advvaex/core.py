import vaex

def advanced_aggregate(df, column, agg_func="mean", verbose=True):
    """
    An advanced version of Vaex's aggregation functions.
    Adds additional metadata about the aggregation process.

    Parameters:
        df (vaex.DataFrame): The input Vaex DataFrame.
        column (str): The column to aggregate.
        agg_func (str): Aggregation function ('mean', 'sum', 'count', etc.).
        verbose (bool): Whether to print metadata.

    Returns:
        dict: A dictionary containing the aggregation result and metadata.
    """
    if agg_func == "mean":
        result = df[column].mean()
    elif agg_func == "sum":
        result = df[column].sum()
    elif agg_func == "count":
        result = df[column].count()
    else:
        raise ValueError(f"Unsupported aggregation function: {agg_func}")

    if verbose:
        print(f"Aggregation Function: {agg_func}")
        print(f"Column: {column}")
        print(f"Result: {result}")

    return {
        "result": result,
        "metadata": {
            "function": agg_func,
            "column": column,
            "row_count": len(df)
        }
    }