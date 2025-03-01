"""Pyfunc model abstraction for T2T grounding."""

import json
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List

import pandas as pd
from mlflow.pyfunc import PythonModel

from databricks.kie.eval_utils import guideline_adherence_with_evaluation_criteria
from databricks.kie.t2t_models.base_t2t_model import BaseT2TModel
from databricks.kie.t2t_models.t2t_model_registrations import get_t2t_default_model
from databricks.kie.t2t_schema import T2TSystemParams

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class T2TGroundingModel(PythonModel):
    """MLflow model for T2T grounding."""
    MAX_WORKERS = 3

    def load_context(self, context) -> None:
        """Load the model artifacts from the context."""
        # pylint: disable=import-outside-toplevel
        import mlflow
        mlflow.set_tracking_uri("databricks")
        mlflow.set_registry_uri("databricks-uc")

    def evaluate(self, df: pd.DataFrame, system_params: T2TSystemParams) -> pd.DataFrame:
        """Generate evaluation results."""
        evaluation_criteria = system_params.evaluation_criteria

        def process_row(row) -> Dict[str, Any]:
            """Process a single row ensuring all inputs remain as strings."""
            request = str(row['request'])
            response_str = row['generated_response']
            if not response_str:
                return {}

            result = {}
            for criterion in evaluation_criteria:
                metric_name = re.sub(r'[^a-zA-Z0-9]', '_', criterion)
                assessment = guideline_adherence_with_evaluation_criteria(request, response_str, criterion)

                result[f"metric/t2t/{metric_name}/value"] = assessment.value
                result[f"metric/t2t/{metric_name}/rationale"] = assessment.rationale

            return result

        df_results = pd.DataFrame(df.apply(process_row, axis=1))
        logger.info(f'Finished generating evaluation results for {len(df_results)} rows')

        return df_results

    def _generate_responses(self, requests: List[str], model: BaseT2TModel) -> List[str]:
        """Generate responses for requests without expected responses.

        Args:
            requests: List of request strings to generate responses for
            model: T2T model to use for generating responses
        Returns:
            List of generated responses.
        """
        results = [None] * len(requests)
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Map each future to its original index for ordering.
            future_to_index = {executor.submit(model, n): idx for idx, n in enumerate(requests)}

        # In order to prevent program crash when a single request fails,
        # we use `submit()` and instead catch all exceptions.
        # If request fails, we set the result to None and this will be skipped
        # during the grounding loop.
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                results[idx] = future.result()
            except RuntimeError as e:
                logger.warning(f"LLMProxyError: Error generating response for request {requests[idx]}: {e}")
                results[idx] = None

        return results

    def predict(self, context, model_input: pd.DataFrame, params: Dict[str, Any] = None):
        """Label T2T grounding samples and return evaluation results.

        Args:
            context: MLflow context
            model_input: DataFrame with `request` and optionally `expected_response` columns.
            params: Dictionary with `system_parameter` key

        Returns:
            DataFrame with generated_response and eval_results columns
        """
        del context

        if params is None or 'system_parameter' not in params:
            raise ValueError(
                "Expected params to be a dict containing the 'system_parameter' for grounding but found None.")

        system_params_str = params['system_parameter']
        try:
            system_params_json = json.loads(system_params_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse 'system_parameter': {e}") from e

        system_params = T2TSystemParams(**system_params_json)
        model = get_t2t_default_model(system_params)
        df = model_input.copy()
        requests: List[str] = df['request'].tolist()
        df['generated_response'] = self._generate_responses(requests, model)
        df['eval_results'] = self.evaluate(df, system_params)

        return df
