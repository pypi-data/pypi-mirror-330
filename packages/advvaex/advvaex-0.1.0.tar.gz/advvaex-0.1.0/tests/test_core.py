try:
    import vaex
    from advvaex.core import advanced_aggregate
    print("Successfully imported vaex and advvaex")
except ImportError as e:
    print(f"ImportError: {e}")

def test_advanced_aggregate():
    # Create a simple Vaex DataFrame
    df = vaex.from_dict({"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]})

    # Perform aggregation
    result = advanced_aggregate(df, column="A", agg_func="mean", verbose=False)

    # Validate results
    assert result["result"] == 3, "Test failed: Incorrect aggregation result"
    print("Test passed!")

if __name__ == "__main__":
    test_advanced_aggregate()