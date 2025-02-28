"""
Data Processor
"""

# pylint: disable=invalid-name, dangerous-default-value, too-many-arguments

from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
from sklearn.preprocessing import OneHotEncoder

from .transform_data import DataTransformer


class DataProcessor:
    """Class for processing data before training."""

    def __init__(self) -> None:
        self.scaler = None
        self.encoder = None
        self.sampler = None

    def encode_one_hot(self, df: pd.DataFrame, col_name: str) -> pd.DataFrame:
        """Function to encode category feature with one-hot-encoder. In result the encoded column is dropped.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe containing column to encode
        col_name : str
            Name of column to encode

        Returns
        -------
        pd.DataFrame
            Dataframe containing encoded columns
        """

        self.encoder = OneHotEncoder()

        encoded_data = self.encoder.fit_transform(df[[col_name]]).toarray()  # type: ignore
        encoded_columns = self.encoder.get_feature_names_out([col_name])  # type: ignore

        encoded_df = pd.DataFrame(encoded_data, columns=encoded_columns, index=df.index)

        df = pd.concat([df, encoded_df], axis=1)
        df = df.drop(col_name, axis=1)
        return df

    def __create_intervals(self, int_list: list[float]) -> list[str]:
        """Function to create intervals names from given list, so given elements are both ends of interval.

        For example, for given [18, 25, 35, 45, 55, 65] it creates
        ['18_25', '25_35', '35_45', '45_55', '55_65', '65']

        Parameters
        ----------
        int_list : list[float]
            List of elements to create intervals from

        Returns
        -------
        list[str]
            List of intervals names
        """
        labels = []
        for i in range(len(int_list) - 1):
            lower = int_list[i]
            upper = int_list[i + 1]  # Tworzymy otwarty przedział na końcu
            labels.append(f"{lower}_{upper}")
        labels.append(f"{int_list[-1]}")  # Dodajemy ostatni przedział bez ograniczenia
        return labels

    def convert_numerical_to_categorized(self, df: pd.DataFrame, bins: List[float], col_name: str) -> pd.DataFrame:
        """Function to convert numerical feature to categorized, basing on given bins - intervals.
        Every bin is interval left side closed and right side opened.
        For bins given: [18, 25, 35, 45, 55, 65] it maps values to categorized:
        ['18_25', '25_35', '35_45', '45_55', '55_65', '65'].

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe numerical containing column to convert
        bins : List[float]
            Numbers that represent elements of intervals to convert the numerical feature
        col_name : str
            Name of column to be converted

        Returns
        -------
        pd.DataFrame
            Dataframe containing converted feature
        """
        labels = self.__create_intervals(bins)
        df[col_name] = df[col_name].apply(lambda x: x if x < max(bins) else max(bins) + 1)
        bins.append(df[col_name].max() + 1)
        assert len(bins) - 1 == len(
            labels
        ), f"Numbers of bins and labels must be equal. bins: {len(bins) - 1}, labels: {len(labels)}"
        range_col_name = col_name + "_range"
        df[range_col_name] = pd.cut(df[col_name], bins=bins, labels=labels, right=False)
        df = df.drop(col_name, axis=1)
        return df

    def scale_train_test(
        self,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        scaler_object: Any,
        params: Dict[str, Any] | None = None,
        exclude_cols: List[str] | None = None,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Function to scale train and test inputs by given scaler.

        Parameters
        ----------
        X_train : pd.DataFrame
            Data with all columns to train model
        X_test : pd.DataFrame
            Data with all columns to test model
        scaler_object : Any
            Object of selected scaler to execute
        params : Dict[str, Any], optional
            Dictionary of params for selected scaler, by default None
        exclude_cols : List[str], optional
            List of columns to exclude from scaling, by default None

        Returns
        -------
        Tuple[pd.DataFrame, pd.DataFrame]
            - X_train_scaled : Scaled training data
            - X_test_scaled : Scaled testing data
        """

        if params is None:
            params = {}
        if exclude_cols is None:
            exclude_cols = []

        exclude_cols.append("id_client")

        numeric_cols = X_train.select_dtypes(include=["float64", "int64"]).columns.tolist()
        cols_to_scale = [col for col in numeric_cols if col not in exclude_cols]

        self.scaler = scaler_object(**params)

        X_train_scaled = X_train.copy()
        X_test_scaled = X_test.copy()

        X_train_scaled[cols_to_scale] = self.scaler.fit_transform(X_train[cols_to_scale])  # type: ignore
        X_test_scaled[cols_to_scale] = self.scaler.transform(X_test[cols_to_scale])  # type: ignore

        return X_train_scaled, X_test_scaled

    def resample_X_y(
        self, X_train: pd.DataFrame, y_train: pd.Series, sampler_object: Any, params: Dict[str, Any] | None = None
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """Function for resampling train data and target column.

        Parameters
        ----------
        X_train : pd.DataFrame
            Data with all columns to train model
        y_train : pd.Series
            Target column
        sampler_object : Any
            Object of selected sampler to execute
        params : Dict[str, Any], optional
            Dictionary of params for selected sampler, by default None

        Returns
        -------
        Tuple[pd.DataFrame, pd.Series]
            - X_resampled : Resampled training data
            - y_resampled : Resampled target column
        """
        if params is None:
            params = {}

        if "id_client" in X_train.columns:
            X_train = X_train.drop("id_client", axis=1)
        self.sampler = sampler_object(**params)
        X_resampled, y_resampled = self.sampler.fit_resample(X_train, y_train)  # type: ignore
        return X_resampled, y_resampled

    def get_transformed_data(
        self,
        data: pd.DataFrame,
        sqrt_col: Optional[List[str]] = None,
        log_default: Optional[List[str]] = None,
        ihs: Optional[List[str]] = None,
        extensive_log: Optional[List[str]] = None,
        neglog: Optional[List[str]] = None,
        boxcox_zero: Optional[List[str]] = None,
        log_x_divide_2: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """Use DataTransformer to transform input data.

        Parameters
        ----------
        data : pd.DataFrame
            Data to be transformed
        sqrt_col : Optional[List[str]], optional
            Columns to perform sqrt_col transformation, by default None
        log_default : Optional[List[str]], optional
            Columns to perform log_default transformation, by default None
        ihs : Optional[List[str]], optional
            Columns to perform ihs transformation, by default None
        extensive_log : Optional[List[str]], optional
            Columns to perform extensive_log transformation, by default None
        neglog : Optional[List[str]], optional
            Columns to perform neglog transformation, by default None
        boxcox_zero : Optional[List[str]], optional
            Columns to perform boxcox_zero transformation, by default None
        log_x_divide_2 : Optional[List[str]], optional
            Columns to perform log_x_divide_2 transformation, by default None

        Returns
        -------
        pd.DataFrame
            DataFrame with transformed columns
        """
        sqrt_col = sqrt_col or []
        log_default = log_default or []
        ihs = ihs or []
        extensive_log = extensive_log or []
        neglog = neglog or []
        boxcox_zero = boxcox_zero or []
        log_x_divide_2 = log_x_divide_2 or []

        dt = DataTransformer(data, sqrt_col, log_default, ihs, extensive_log, neglog, log_x_divide_2)
        return dt.func_transform_data()


def replace_outliers_with_percentile(
    df: pd.DataFrame, columns: List[str], first_percentile: float = 0.01, percentile: float = 0.99, first: bool = False
) -> pd.DataFrame:
    """Replace outliers with percentile values.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe to process
    columns : List[str]
        List of columns to process
    first_percentile : float, optional
        First (lower) percentile value for replacing lower outliers, by default 0.01
    percentile : float, optional
        Upper percentile value for replacing upper outliers, by default 0.99
    first : bool, optional
        If True, replace values below first_percentile as well, by default False

    Returns
    -------
    pd.DataFrame
        DataFrame with outliers replaced by percentile values
    """
    df_copy = df.copy()

    for column in columns:
        threshold = df_copy[column].quantile(percentile)
        print(f"For col {column} upper threshold is: {threshold}")

        df_copy[column] = df_copy[column].apply(lambda x, t=threshold: t if x > t else x)
        if first:
            first_threshold = df_copy[column].quantile(first_percentile)
            df_copy[column] = df_copy[column].apply(lambda x, t=first_threshold: t if x < t else x)
            print(f"For col {column} lower threshold is: {first_threshold}")

    return df_copy
