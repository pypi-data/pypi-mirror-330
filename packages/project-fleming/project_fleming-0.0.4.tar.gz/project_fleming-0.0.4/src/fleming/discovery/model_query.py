# Copyright 2024 Fleming
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

import pandas as pd
import requests


class ModelQuery:
    """
    A class which allows for querying a model serving endpoint on databricks.

    This class is used to query a model serving endpoint on databricks with a dataset.

    Example:
    --------
    ```python

    url = "https://example.com/model_endpoint"
    token = "your_auth_token"

    # Create an instance of ModelQuery
    model_query = ModelQuery(url, token)

    # Example dataset
    dataset = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': [4, 5, 6]})

    try:
        # Score the model using the dataset
        response = model_query.score_model(dataset)
        print(response)
    except requests.exceptions.HTTPError as e:
        print(f"Error: {str(e)}")

    ```

    Parameters:
        url (str): The URL of the model serving endpoint.
        token (str): The authorization token for the model serving endpoint.
    """

    url: str
    token: str

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def create_tf_serving_json(self, data):
        """
        Creates a JSON object for TensorFlow serving.

        Parameters:
            data (Union[dict, pd.DataFrame, np.ndarray]): The input data.

        Returns:
            dict: The JSON object for TensorFlow serving.
        """
        return {
            "inputs": (
                {name: data[name].tolist() for name in data.keys()}
                if isinstance(data, dict)
                else data.tolist()
            )
        }

    def score_model(self, dataset):
        """
        Scores the model using the provided dataset.

        Parameters:
            dataset (Union[pd.DataFrame, np.ndarray]): The dataset to be scored.

        Returns:
            dict: The response JSON from the model serving endpoint.

        Raises:
            requests.exceptions.HTTPError: If the request to the model serving endpoint fails.
        """
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        ds_dict = (
            {"dataframe_split": dataset.to_dict(orient="split")}
            if isinstance(dataset, pd.DataFrame)
            else self.create_tf_serving_json(dataset)
        )
        data_json = json.dumps(ds_dict, allow_nan=True)
        response = requests.request(
            method="POST", headers=headers, url=self.url, data=data_json
        )
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(
                f"Request failed with status {response.status_code}, {response.text}"
            )
        return response.json()
