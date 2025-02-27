# MIT License
#
# Copyright (c) 2024 Chronulus AI Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
from io import StringIO
from datetime import datetime
from copy import deepcopy

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    import warnings


class Prediction:
    """
    A class representing the output of a prediction request

    Parameters
    ----------
    _id : str
        Unique identifier for the prediction.

    Attributes
    ----------
    _id : str
        Unique identifier for the prediction.

    """

    def __init__(self, _id: str):
        self._id = _id

    @property
    def id(self) -> str:
        """Get the unique identifier for the prediction"""
        return self._id


class Forecast(Prediction):
    """
    A class representing the output of a prediction request, containing both numerical results and explanatory text.

    This class encapsulates the prediction results returned from the chronulus API,
    including a unique identifier, descriptive text, and the numerical predictions in
    a pandas DataFrame format.

    Parameters
    ----------
    _id : str
        Unique identifier for the prediction.
    text : str
        Descriptive text or notes explaining the prediction results.
    data : dict
        JSON-Split formatted dictionary containing the prediction results.

    Attributes
    ----------
    _id : str
        Unique identifier for the prediction.
    _text : str
        Explanatory text describing the prediction results.
    _data : dict
        JSON-Split formatted dictionary containing the prediction results.

    """

    def __init__(self, _id: str, text: str, data: dict):
        super().__init__(_id)
        self._text = text
        self._data = data

    @property
    def data(self) -> dict:
        """Get the forecast data after the transformation defined by this forecast"""
        return self._transform_data(self._data)

    @property
    def text(self) -> str:
        """Get the forecast explanation after the transformation defined by this forecast"""
        return self._transform_text(self._text)

    def _transform_data(self, data: dict) -> dict:
        """Hook for transforming the forecast data"""
        return data

    def _transform_text(self, text: str) -> str:
        """Hook for transforming the forecast text"""
        return text

    def to_json(self, orient='columns'):
        """
        Convert the forecast data to JSON format with specified orientation.

        Parameters
        ----------
        orient : str, optional
            Data orientation for the JSON output. Options are:

            - 'split': Original JSON-split format
            - 'rows': List of dictionaries, each representing a row
            - 'columns': Dictionary of lists, each representing a column
            Default is 'columns'.

        Returns
        -------
        dict or list
            Forecast data in the specified JSON format:

            - For 'split': Original JSON-split dictionary
            - For 'rows': List of row dictionaries
            - For 'columns': Dictionary of column arrays

        Examples
        --------
        >>> # Get data in columns format
        >>> json_cols = forecast.to_json(orient='columns')
        >>> # Get data in rows format
        >>> json_rows = forecast.to_json(orient='rows')
        """

        if orient == 'split':
            return self.data

        elif orient == 'rows':
            columns = self.data.get('columns')
            rows = list()
            for row in self.data.get('data'):
                _row = {columns[j]: val for j, val in enumerate(row)}
                rows.append(_row)
            return rows

        else:
            col_names = self.data.get('columns')
            columns = {k: list() for k in col_names}

            for row in self.data.get('data'):
                for j, val in enumerate(row):
                    columns[col_names[j]].append(val)

            return columns

    def to_pandas(self):
        """
        Convert the forecast data to a pandas DataFrame.

        The first column is automatically set as the index of the resulting DataFrame.
        Typically, this is a timestamp or date column.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing the forecast data with the first column as index.

        Raises
        ------
        UserWarning
            If pandas is not installed in the environment.

        Examples
        --------
        >>> df = forecast.to_pandas()
        >>> print(df.head())
                   y_hat
        date
        2025-01-01   .12345
        2025-01-02   .67890
        """
        if not PANDAS_AVAILABLE:
            warnings.warn(
                "pandas is not installed but his method requires pandas."
                "Please install pandas using `pip install pandas` and then try again.",
                UserWarning
            )
        else:
            json_str = json.dumps(self.data)
            df = pd.read_json(StringIO(json_str), orient='split')
            return df.set_index(self.data.get('columns')[0], drop=True)


class NormalizedForecast(Forecast):
    """
    A class representing the output of a NormalizedForecast prediction request, containing both numerical results and explanatory text.

    This class provides methods for operating on normalized forecast data.

    Parameters
    ----------
    _id : str
        Unique identifier for the prediction.
    text : str
        Descriptive text or notes explaining the prediction results.
    data : dict
        JSON-Split formatted dictionary containing the prediction results.
    y_min : float
        The minimum value of the source scale.
    y_max : float
        The maximum value of the source scale
    """

    def __init__(self, _id: str, text: str, data: dict, y_min: float = 0.0, y_max: float = 1.0):
        super().__init__(_id, text, data)
        self.y_min = y_min
        self.y_max = y_max

    def to_rescaled_forecast(self, y_min: float = 0.0, y_max: float = 1.0, invert_scale: bool = False):
        """
        Create a RescaledForecast instance from  NormalizedForecast object.

        This static method allows conversion from a generic Forecast to a RescaledForecast,
        applying the specified scaling parameters.

        Parameters
        ----------
        y_min : float, default 0.0
            The minimum value of the target scale.
        y_max : float, default 1.0
            The maximum value of the target scale.
        invert_scale : bool, default False
            Whether to invert the scale before rescaling.

        Returns
        -------
        RescaledForecast
            A new RescaledForecast instance containing the rescaled data.
        """
        return RescaledForecast(
            _id=self.id,
            data=self.data,
            text=self.text,
            y_min=y_min,
            y_max=y_max,
            invert_scale=invert_scale
        )


class RescaledForecast(Forecast):
    """
    A class representing a RescaledForecast prediction

    This class provides methods for rescaling (denormalizing) a Forecast.

    Parameters
    ----------
    _id : str
        Unique identifier for the prediction.
    text : str
        Descriptive text or notes explaining the prediction results.
    data : dict
        JSON-Split formatted dictionary containing the prediction results.
    y_min : float
        The minimum value of the source scale.
    y_max : float
        The maximum value of the source scale
    invert_scale : bool
        Should we invert the scale before rescaling?
    """

    def __init__(self, _id: str, text: str, data: dict, y_min: float = 0.0, y_max: float = 1.0, invert_scale: bool = False):
        super().__init__(_id, text, data)
        self.y_min = y_min
        self.y_max = y_max
        self.invert_scale = invert_scale

    def _transform_data(self, data: dict) -> dict:

        # data should be in split format
        # we should create types for this instead of assuming
        new_data = deepcopy(data)
        json_data = new_data.get("data")
        for i, (ds, y_hat) in enumerate(json_data):
            yhat = 1 - y_hat if self.invert_scale else y_hat
            yhat = yhat * (self.y_max - self.y_min) + self.y_min
            json_data[i][1] = yhat

        new_data['data'] = json_data

        return new_data

    @staticmethod
    def from_forecast(forecast: Forecast, y_min: float = 0.0, y_max: float = 1.0, invert_scale: bool = False):
        """
        Convert the normalized forecast to a rescaled forecast with specified scale parameters.

        This method creates a new RescaledForecast instance using the current forecast's data,
        allowing you to specify the target range and whether to invert the scale.

        Parameters
        ----------
        y_min : float, default 0.0
            The minimum value of the target scale.
        y_max : float, default 1.0
            The maximum value of the target scale.
        invert_scale : bool, default False
            Whether to invert the scale before rescaling.

        Returns
        -------
        RescaledForecast
            A new forecast instance with values rescaled to the specified range.
        """

        return RescaledForecast(
            _id=forecast.id,
            data=forecast.data,
            text=forecast.text,
            y_min=y_min,
            y_max=y_max,
            invert_scale=invert_scale
        )





