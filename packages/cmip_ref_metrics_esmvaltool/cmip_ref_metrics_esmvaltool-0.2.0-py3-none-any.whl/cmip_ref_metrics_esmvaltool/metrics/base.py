from abc import abstractmethod
from pathlib import Path
from typing import ClassVar

import pandas

from cmip_ref_core.datasets import SourceDatasetType
from cmip_ref_core.metrics import Metric, MetricExecutionDefinition, MetricResult
from cmip_ref_core.pycmec.metric import CMECMetric
from cmip_ref_core.pycmec.output import CMECOutput
from cmip_ref_metrics_esmvaltool.recipe import load_recipe, run_recipe
from cmip_ref_metrics_esmvaltool.types import OutputBundle, Recipe


class ESMValToolMetric(Metric):
    """ESMValTool Metric base class."""

    base_recipe: ClassVar[str]

    @staticmethod
    @abstractmethod
    def update_recipe(recipe: Recipe, input_files: pandas.DataFrame) -> None:
        """
        Update the base recipe for the run.

        Parameters
        ----------
        recipe:
            The base recipe to update.
        input_files:
            The dataframe describing the input files.

        """

    @staticmethod
    @abstractmethod
    def format_result(result_dir: Path) -> OutputBundle:
        """
        Create a CMEC output bundle for the results.

        Parameters
        ----------
        result_dir
            Directory containing results from an ESMValTool run.

        Returns
        -------
            A CMEC output bundle.
        """

    def run(self, definition: MetricExecutionDefinition) -> MetricResult:
        """
        Run a metric

        Parameters
        ----------
        definition
            A description of the information needed for this execution of the metric

        Returns
        -------
        :
            The result of running the metric.
        """
        input_files = definition.metric_dataset[SourceDatasetType.CMIP6].datasets
        recipe = load_recipe(self.base_recipe)
        self.update_recipe(recipe, input_files)
        result_dir = run_recipe(recipe, definition)
        metric_bundle = self.format_result(result_dir)
        # validate the metric bundle
        CMECMetric.model_validate(metric_bundle)
        # create a empty output bundle
        output_bundle = CMECOutput.create_template()
        CMECOutput.model_validate(output_bundle)
        # cmec_output_bundle and metric_output_bundle are required keyword
        return MetricResult.build_from_output_bundle(
            definition, cmec_output_bundle=output_bundle, cmec_metric_bundle=metric_bundle
        )
