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

import base64
import json
import pickle
import time
from datetime import datetime
from typing import Tuple, TypeVar, Type, Optional, Union

import requests
from chronulus_core.types.response import QueuePredictionResponse, PredictionGetByIdResponse, EstimatorGetResponse
from chronulus_core.types.requests import EstimatorCreationRequest
from chronulus_core.types.inputs import InputModelInfo, create_model_from_schema

from ..environment import BaseEnv, Env
from ..prediction import NormalizedForecast
from ..session import Session
from .base import Estimator, BaseModelSubclass


class NormalizedForecaster(Estimator):
    """
   A forecasting estimator that normalizes input data for time series predictions.

   This estimator handles the creation, queuing, and retrieval of normalized time series
   forecasts through the API. It supports various time horizons and can generate both
   numerical predictions and explanatory notes.

   Parameters
   ----------
   session : Session
       Active session instance for API communication.
   input_type : Type[BaseModelSubclass]
       Pydantic model class that defines the expected input data structure.

   Attributes
   ----------
   estimator_name : str
       Name identifier for the estimator. Set to "NormalizedForecaster".
   estimator_version : str
       Version string for the estimator. Set to "1".
   prediction_version : str
       Version string for the prediction. Set to "1".
   estimator_id : str or None
       Unique identifier assigned by the API after creation.

   """

    estimator_name = "NormalizedForecaster"
    estimator_version = "1"
    prediction_version = "1"

    def __init__(self, session: Session, input_type: Type[BaseModelSubclass], estimator_id: Optional[str] = None, verbose: bool = True):
        super().__init__(session, input_type)
        self.verbose = verbose
        self.estimator_id = estimator_id
        if self.estimator_id is None:
            self.create()

    def create(self):
        """
        Initialize the forecaster instance with the API.

        Creates a new forecaster instance on the API side with the specified input schema.
        The schema is serialized and base64 encoded before transmission.

        Raises
        ------
        ValueError
            If the API fails to create the estimator or returns an invalid response.
        """

        request_data = EstimatorCreationRequest(
            estimator_name=self.estimator_name,
            session_id=self.session.session_id,
            input_model_info=InputModelInfo(
                validation_schema=self.input_type.model_json_schema(mode="validation"),
                serialization_schema=self.input_type.model_json_schema(mode="serialization"),
            )
        )

        resp = requests.post(
            url=f"{self.session.env.API_URI}/estimators/{self.get_route_prefix()}/create",
            headers=self.session.headers,
            json=request_data.model_dump()
        )
        if resp.status_code == 200:
            response_json = resp.json()
            if 'estimator_id' in response_json:
                self.estimator_id = response_json['estimator_id']
                if self.verbose:
                    print(f"Estimator created with estimator_id: {response_json['estimator_id']}")
            else:
                if self.verbose:
                    print(resp.status_code)
                    print(resp.text)
                raise ValueError("There was an error creating the estimator. Please try again.")
        else:
            raise ConnectionError(f"There was an error creating the estimator. Status code: {resp.status_code}. Response: {resp.text}")

    def queue(
            self,
            item: BaseModelSubclass,
            start_dt: datetime,
            weeks: int = None,
            days: int = None,
            hours: int = None,
            note_length: Tuple[int, int] = (3, 5),
    ):
        """
        Queue a prediction request for processing.

        Parameters
        ----------
        item : BaseModelSubclass
            The input data conforming to the specified input_type schema.
        start_dt : datetime
            The starting datetime for the forecast.
        weeks : int, optional
            Number of weeks to forecast.
        days : int, optional
            Number of days to forecast.
        hours : int, optional
            Number of hours to forecast.
        note_length : tuple[int, int], optional
            Desired length range (number of sentences) for explanatory notes (min, max), by default (3, 5).

        Returns
        -------
        QueuePredictionResponse
            Response object containing the request status and ID.

        Raises
        ------
        TypeError
            If the provided item doesn't match the expected input_type.
        """

        if not isinstance(item, self.input_type):
            try:
                assert item.model_json_schema(mode='validation') == self.input_type.model_json_schema(mode='validation')
                assert item.model_json_schema(mode='serialization') == self.input_type.model_json_schema(mode='serialization')

            except Exception as e:
                raise TypeError(f"Expect item to be an instance of {self.input_type}, but item has type {type(item)}")

        data = dict(
            estimator_id=self.estimator_id,
            item_data=item.model_dump(),
            start_dt=start_dt.timestamp(),
            weeks=weeks,
            days=days,
            hours=hours,
            note_length=note_length,
        )
        resp = requests.post(
            url=f"{self.session.env.API_URI}/estimators/{self.get_route_prefix()}/queue-predict",
            headers=self.session.headers,
            json=data,
        )

        if resp.status_code == 200:
            return QueuePredictionResponse(**resp.json())
        else:
            return QueuePredictionResponse(
                success=False,
                request_id='',
                message=f'Queuing failed with status code {resp.status_code}: {resp.text}',
            )

    def get_predictions(self, request_id: str, try_every: int = 3, max_tries: int = 20):
        """
        Retrieve predictions for a queued request.

        Parameters
        ----------
        request_id : str
            The ID of the queued prediction request.
        try_every : int, optional
            Seconds to wait between retry attempts, by default 3.
        max_tries : int, optional
            Maximum number of retry attempts, by default 20.

        Returns
        -------
        list[NormalizedForecast] or dict
            List of NormalizedForecast objects if successful, or error dictionary if failed.

        Raises
        ------
        Exception
            If the maximum retry limit is exceeded or if an API error occurs.
        """

        retries = 0

        while retries < max_tries:

            resp = requests.post(
                url=f"{self.session.env.API_URI}/predictions/{self.prediction_version}/check-by-request-id",
                headers=self.session.headers,
                json=dict(request_id=request_id),
            )

            if resp.status_code != 200:
                if self.verbose:
                    print(resp)
                raise Exception(f"An error occurred. Status code: {resp.status_code}. Response: {resp.text}")

            else:
                response_json = resp.json()

                if response_json['status'] == 'ERROR':
                    return response_json

                if response_json['status'] == 'SUCCESS':
                    if self.verbose:
                        print(f'{response_json["status"]}. {response_json["message"]}. Fetching predictions.')
                    prediction_ids = response_json.get('prediction_ids', [])
                    return [self.get_prediction(prediction_id) for prediction_id in prediction_ids]

                if response_json['status'] in ['PENDING', 'NOT_FOUND']:
                    if self.verbose:
                        print(f'{response_json["status"]}. {response_json["message"]}. Trying again in {try_every} seconds...')
                    time.sleep(try_every)

                retries += 1

        if retries >= max_tries:
            raise Exception(f"Retry limit exceeded max_tries of {max_tries}")

    def get_prediction(self, prediction_id: str) -> Optional[NormalizedForecast]:

        """
        Retrieve a single prediction by its ID.

        Parameters
        ----------
        prediction_id : str
            Unique identifier for the prediction.

        Returns
        -------
        Forecast or None
            Forecast object containing the forecast results and notes if successful,
            None if the prediction couldn't be retrieved.
        """

        return self.get_prediction_static(prediction_id, env=self.session.env.model_dump(), verbose=self.verbose)

    @staticmethod
    def get_prediction_static(prediction_id: str, env: Optional[dict] = None, verbose: bool = True) -> Optional[NormalizedForecast]:
        """
        Static method to retrieve a single prediction with a prediction_id and session_id or session.

        Parameters
        ----------
        prediction_id : str
            Unique identifier for the prediction.
        env : dict, optional
            Environment configuration dictionary. If None, default environment will be used.
        verbose : bool, optional
            Print feedback to stdout if True. Default: True

        Returns
        -------
        NormalizedForecast or None
            NormalizedForecast object containing the forecast results and notes if successful,
            None if the prediction couldn't be retrieved.
        """

        prediction_version = NormalizedForecaster.prediction_version
        if isinstance(env, Env):
            base = BaseEnv(**env.model_dump())
        else:
            env = env if env and isinstance(env, dict) else {}
            base = BaseEnv(**env)

        resp = requests.post(
            url=f"{base.env.API_URI}/predictions/{prediction_version}/get-by-prediction-id",
            headers=base.headers,
            json=dict(prediction_id=prediction_id),
        )

        if resp.status_code == 200:
            response_json = resp.json()
            pred_response = PredictionGetByIdResponse(**response_json)
            if pred_response.success:
                estimator_response = pred_response.response
                prediction = NormalizedForecast(
                    _id=prediction_id,
                    text=estimator_response['notes'],
                    data=estimator_response['json_split_format_dict'],
                )
                return prediction
            else:
                if verbose:
                    print(f"The prediction could not be retrieved for prediction_id '{prediction_id}'")
                    print(pred_response.message)

        else:
            if verbose:
                print(f"The prediction could not be retrieved for prediction_id '{prediction_id}'")
                print(resp.status_code)
                print(resp.text)

    def predict(
            self,
            item: BaseModelSubclass,
            start_dt: datetime = None,
            weeks: int = None,
            days: int = None,
            hours: int = None,
            note_length: Tuple[int, int] = (3, 5),
       ) -> NormalizedForecast:
        """
        Convenience method to queue and retrieve predictions in a single call.

        This method combines the queue and get_predictions steps into a single operation,
        waiting for the prediction to complete before returning.

        Parameters
        ----------
        item : BaseModelSubclass
            The input data conforming to the specified input_type schema.
        start_dt : datetime, optional
            The starting datetime for the forecast.
        weeks : int, optional
            Number of weeks to forecast.
        days : int, optional
            Number of days to forecast.
        hours : int, optional
            Number of hours to forecast.
        note_length : tuple[int, int], optional
            Desired length range for explanatory notes (min, max), by default (3, 5).

        Returns
        -------
        NormalizedForecast or None
            The completed prediction if successful, None otherwise.
        """
        req = self.queue(item, start_dt, weeks, days, hours, note_length)
        predictions = self.get_predictions(req['request_id'])
        return predictions[0] if predictions else None

    @staticmethod
    def load_from_saved_estimator(estimator_id: str, env: Optional[dict] = None, verbose: bool = True):

        # get estimator from estimator id
        env = env if env and isinstance(env, dict) else {}
        base = BaseEnv(**env)

        resp = requests.post(
            url=f"{base.env.API_URI}/estimators/{NormalizedForecaster.estimator_version}/from-estimator-id",
            headers=base.headers,
            json=dict(estimator_id=estimator_id)
        )

        if resp.status_code != 200:
            raise ValueError(f"Failed to load estimator with status code: {resp.status_code}, {resp.text}")

        try:
            estimator_response = EstimatorGetResponse(**resp.json())
            if estimator_response.success:
                session = Session(**estimator_response.session.model_dump(), env=base.env.model_dump(), verbose=verbose)
                input_type = create_model_from_schema(estimator_response.input_model_info.validation_schema)
                estimator = NormalizedForecaster(
                    session=session,
                    input_type=input_type,
                    estimator_id=estimator_response.estimator_id,
                    verbose=verbose
                )

                if verbose:
                    print(f"Estimator retrieved with estimator_id: {estimator_response.estimator_id}")

                return estimator

            else:
                raise ValueError(estimator_response.message)

        except Exception as e:
            raise ValueError(f"Failed to parse estimator response: {resp.text}")

