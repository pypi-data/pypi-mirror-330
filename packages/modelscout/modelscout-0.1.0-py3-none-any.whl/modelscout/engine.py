import os
import pandas as pd
import numpy as np


def get_default_csv_path():
    """Get the path to the bundled models.csv file."""
    return os.path.join(os.path.dirname(__file__), "models.csv")


def load_models(file):
    if file is None:
        file = get_default_csv_path()
    if not os.path.exists(file):
        print(f"Error: File '{file}' not found.")
        exit(1)
    return pd.read_csv(file)


def interactive_args(df):
    """
    Interactive mode for selecting args
    """
    print("\nWelcome to ModelScout Interactive Mode!")
    try:
        # get and typecast user input
        top = int(input("How many models do you want to see (ret for 5): ") or 5)

        license = int(
            input(
                "Enter preferred license (1 for open source, 0 for no preference, ret to skip): "
            )
            or 0
        )

        performance = (
            input("Enter ideal performance rating (1.0-10.0, ret to skip): ") or None
        )
        performance = float(performance) if performance is not None else None

        cost = input("Enter ideal cost per million tokens (ret to skip): ") or None
        cost = float(cost) if cost is not None else None

        context_length = input("Enter ideal context length (ret to skip): ") or None
        context_length = int(context_length) if context_length is not None else None

        support = input("Enter ideal support rating (1.0-10.0, ret to skip): ") or None
        support = float(support) if support is not None else None

    except:
        print(
            "Not a valid input. Please try again with floats and ints as appropriate."
        )
        exit(1)

    return (df, top, license, performance, cost, context_length, support)


def scout_models(
    df, top=5, license=0, performance=None, cost=None, context_length=None, support=None
):
    """
    Scouts models based on user preferences utilizing a euclidean distance based algorithm
    """
    # compute scalefactor for each feature to normalize the values between 0 and 1
    scale_license = 1
    scale_performance = 0.1111
    scale_cost = 0.0066
    scale_context_length = 0.00005120
    scale_support = 0.111

    # compute euclidean distance dentoted by rho
    df["rho"] = np.sqrt(
        (scale_license if license else 0)
        * ((df["license"] - license)) ** 2  # weigh preference for open source only
        + scale_performance
        * ((df["Performance"] - (performance if performance else df["Performance"])))
        ** 2  # asuming arg of 0 means do not consider
        + scale_cost
        * (
            (
                df["Cost per Million Tokens"]
                - (cost if cost is not None else df["Cost per Million Tokens"])
            )
        )
        ** 2  # asuming arg of 0 means minimize
        + scale_context_length
        * (
            df["Context Length"]
            - (context_length if context_length else df["Context Length"])
        )
        ** 2
        + scale_support * (df["Support"] - (support if support else df["Support"])) ** 2
    )
    return df.nsmallest(top, "rho").drop(columns=["rho"]).to_string(index=False)
