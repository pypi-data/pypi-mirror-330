import pytest
import pandas as pd
import numpy as np
import os
import sys
from modelscout.engine import load_models, scout_models, interactive_args

@pytest.fixture
def sample_df():
    """Provides a sample DataFrame for testing."""
    return pd.DataFrame(
        {
            "license": [1, 0, 1],
            "Performance": [9.0, 7.5, 8.2],
            "Cost per Million Tokens": [0.002, 0.005, 0.003],
            "Context Length": [2048, 4096, 1024],
            "Support": [8.5, 6.0, 9.0],
        }
    )


def test_load_models(tmp_path):
    """Tests that load_models correctly loads a CSV file."""
    csv_file = tmp_path / "test_models.csv"
    df = pd.DataFrame(
        {
            "license": [1, 0],
            "Performance": [9.0, 7.5],
            "Cost per Million Tokens": [0.002, 0.005],
            "Context Length": [2048, 4096],
            "Support": [8.5, 6.0],
        }
    )
    df.to_csv(csv_file, index=False)

    loaded_df = load_models(str(csv_file))
    pd.testing.assert_frame_equal(loaded_df, df)


def test_load_models_missing_file():
    """Tests that load_models exits on a missing file."""
    with pytest.raises(SystemExit):
        load_models("non_existent_file.csv")


def test_scout_models(sample_df):
    """Tests the model selection algorithm."""
    result_df = scout_models(
        sample_df,
        top=2,
        license=1,
        performance=8.0,
        cost=0.003,
        context_length=2048,
        support=8.5,
    )
    assert "license" in result_df
    assert "Performance" in result_df
    assert "Cost per Million Tokens" in result_df
    assert "Context Length" in result_df
    assert "Support" in result_df
    assert len(result_df.split("\n")) == 3


def test_interactive_args(monkeypatch, sample_df):
    """Tests interactive argument parsing with mocked user input."""
    inputs = iter(["3", "1", "9.0", "0.002", "2048", "8.5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    args = interactive_args(sample_df)
    assert args[1] == 3  # top
    assert args[2] == 1  # license
    assert args[3] == 9.0  # performance
    assert args[4] == 0.002  # cost
    assert args[5] == 2048  # context length
    assert args[6] == 8.5  # support
