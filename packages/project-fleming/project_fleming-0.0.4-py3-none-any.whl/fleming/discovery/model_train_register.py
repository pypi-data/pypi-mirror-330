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

import warnings
import mlflow
import numpy as np
import pandas as pd
import torch
from mlflow.pyfunc import PythonModel
from pyspark.sql import SparkSession
from sentence_transformers import SentenceTransformer, util


class SemanticSearchModel(PythonModel):
    """
    A class representing a semantic search model.

    This class is used to perform semantic search over a corpus of sentences using a pre-trained model.

    Attributes:
        model: The pre-trained model used for encoding sentences.
        corpus: The corpus of sentences used for semantic search.
        corpus_embeddings: The embeddings of the sentences in the corpus.

    Methods:
        load_context: Load the model context for inference, including the corpus from a file.
        predict: Perform semantic search over the corpus and return the most relevant results.
    """

    def load_context(self, context):
        """
        Load the model context for inference, including the corpus from a file.
        """
        try:
            self.model = SentenceTransformer.load(context.artifacts["model_path"])

            # Load the corpus from the specified file
            corpus_file = context.artifacts["corpus_file"]
            with open(corpus_file) as file:
                self.corpus = file.read().splitlines()

            self.corpus_embeddings = torch.load(
                context.artifacts["corpus_embedding_file"]
            )

        except Exception as e:
            raise ValueError(f"Error loading model and corpus: {e}")

    def predict(self, context, model_input, params=None):
        """
        Predict method to perform semantic search over the corpus.

        Args:
            context: The context object containing the model artifacts.
            model_input: The input data for performing semantic search.
            params: Optional parameters for controlling the search behavior.

        Returns:
            A list of tuples containing the most relevant sentences from the corpus and their similarity scores.
        """

        if isinstance(model_input, pd.DataFrame):
            if model_input.shape[1] != 1:
                raise ValueError("DataFrame input must have exactly one column.")
            model_input = model_input.iloc[0, 0]
        elif isinstance(model_input, dict):
            model_input = model_input.get("sentence")
            if model_input is None:
                raise ValueError(
                    "The input dictionary must have a key named 'sentence'."
                )
        else:
            raise TypeError(
                f"Unexpected type for model_input: {type(model_input)}. Must be either a Dict or a DataFrame."
            )

        # Encode the query
        query_embedding = self.model.encode(model_input, convert_to_tensor=True)

        # Compute cosine similarity scores
        cos_scores = util.cos_sim(query_embedding, self.corpus_embeddings).cpu()[0]

        # Determine the number of top results to return
        top_k = params.get("top_k", 3) if params else 3  # Default to 3 if not specified

        _ = (
            params.get("minimum_relevancy", 0.4) if params else 0.4
        )  # Default to 0.4 if not specified

        # Get the top_k most similar sentences from the corpus
        top_results = np.argsort(cos_scores, axis=0)[-top_k:]

        # Prepare the initial results list
        initial_results = [
            (self.corpus[idx], cos_scores[idx].item()) for idx in reversed(top_results)
        ]

        # Filter the results based on the minimum relevancy threshold
        filtered_results = [result for result in initial_results if result[1] >= 0]

        # If all results are below the threshold, issue a warning and return the top result
        if not filtered_results:
            warnings.warn(
                "All top results are below the minimum relevancy threshold. "
                "Returning the highest match instead.",
                RuntimeWarning,
            )
            return [initial_results[0]]
        else:
            return filtered_results


class ModelTrainRegister:
    """
    A class to train and register a semantic search model.

    Example:
    --------
    ```python

    from fleming.discovery.model_train_register import ModelTrainRegister, SemanticSearchModel
    from pyspark.sql import SparkSession

    # Not required if using Databricks
    spark = SparkSession.builder.appName("model_serving").getOrCreate()

    model_directory = "/tmp/BERT_Semantic_Search_model"
    corpus_file = "/tmp/search_corpus.txt"
    corpus_embedding_file = '/tmp/corpus_embedding.pt'

    model_developer = ModelTrainRegister(spark, model_directory, corpus_file, corpus_embedding_file)

    # Register the model
    semantic_search_model = "multi-qa-mpnet-base-dot-v1"
    model_developer.register_model(semantic_search_model)

    # Embed the corpus
    model_developer.embed_corpus()

    # Define parameters and artifacts
    parameters = {"top_k": 50, "relevancy_score": 0.45}
    input_example = ["Innersource best practices"]
    test_output = ["match 1", "match 2"]
    signature = infer_signature(input_example, test_output, params=parameters)
    artifacts = {
        "model_path": model_directory,
        "corpus_file": corpus_file,
        "corpus_embedding_file": corpus_embedding_file
    }
    unique_model_name = "semantic_search_model"

    # Create and serve the model
    experiment_location = "/path/to/experiment"
    model_developer.create_registered_model(unique_model_name, input_example, signature, artifacts, experiment_location)
    ```

    Parameters:
    -----------
    model_directory (str): The directory to save the trained model.
    corpus_file (str): The file containing the corpus of sentences.
    corpus_embedding_file (str): The file to save the embeddings of the corpus.
    semantic_search_model (str): The pre-trained model to use for semantic search.
    """

    spark: SparkSession
    model_directory: str
    corpus_file: str
    corpus_embedding_file: str
    semantic_search_model: str

    def __init__(
        self,
        spark: SparkSession,
        model_directory: str,
        corpus_file: str,
        corpus_embedding_file: str,
        semantic_search_model: str,
    ) -> None:
        """
        Initialize the ModelDeveloper class.

        Parameters:
        -----------
        spark : SparkSession
        model_directory : str
            The directory to save the trained model.
        corpus_file : str
            The file containing the corpus of sentences.
        corpus_embedding_file : str
            The file to save the embeddings of the corpus.
        semantic_search_model : str
            The pre-trained model to use for semantic search.
        """
        self.model_directory = model_directory
        self.corpus_file = corpus_file
        self.corpus_embedding_file = corpus_embedding_file
        self.semantic_search_model = semantic_search_model

    def register_model(self) -> None:
        """
        Register the pre-trained model.

        """
        model = SentenceTransformer(self.semantic_search_model)
        model.save(self.model_directory)

    def embed_corpus(self) -> None:
        """
        Embed the corpus of sentences using the pre-trained model.
        """
        model = SentenceTransformer.load(self.model_directory)

        with open(self.corpus_file) as file:
            corpus = file.read().splitlines()

        corpus_embeddings = model.encode(corpus, convert_to_tensor=True)
        torch.save(corpus_embeddings, self.corpus_embedding_file)

    def create_registered_model(
        self,
        unique_model_name: str,
        input_example: list,
        signature: object,
        artifacts: str,
        experiment_location: str,
    ) -> None:
        """
        Create and serve the semantic search model.

        Parameters:
        -----------
        unique_model_name : str
            The unique name for the model.
        input_example : list
            An example input for the model.
        signature : object
            The signature object for the model.
        artifacts : dict
            The artifacts required for the model.
        experiment_location : str
            The location to store the experiment.
        """
        mlflow.set_experiment(experiment_location)

        with mlflow.start_run() as run:
            model_info = mlflow.pyfunc.log_model(
                unique_model_name,
                python_model=SemanticSearchModel(),
                input_example=input_example,
                signature=signature,
                artifacts=artifacts,
                pip_requirements=["sentence_transformers", "numpy"],
            )
            _ = run.info.run_id

            model_uri = model_info.model_uri

            mlflow.register_model(model_uri=model_uri, name=unique_model_name)
