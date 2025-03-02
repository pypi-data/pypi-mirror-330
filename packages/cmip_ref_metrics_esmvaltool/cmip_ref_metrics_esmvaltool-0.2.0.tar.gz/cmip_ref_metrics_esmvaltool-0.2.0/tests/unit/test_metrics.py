import cmip_ref_metrics_esmvaltool
import pytest
from cmip_ref_metrics_esmvaltool.metrics import GlobalMeanTimeseries

from cmip_ref_core.datasets import DatasetCollection, MetricDataset, SourceDatasetType


@pytest.fixture
def metric_dataset(cmip6_data_catalog) -> MetricDataset:
    selected_dataset = cmip6_data_catalog[
        cmip6_data_catalog["instance_id"] == cmip6_data_catalog.instance_id.iloc[0]
    ]
    return MetricDataset(
        {
            SourceDatasetType.CMIP6: DatasetCollection(
                selected_dataset,
                "instance_id",
            )
        }
    )


def test_example_metric(mocker, metric_dataset, cmip6_data_catalog, definition_factory):
    metric = GlobalMeanTimeseries()
    ds = cmip6_data_catalog.groupby("instance_id", as_index=False).first()

    definition = definition_factory(cmip6=DatasetCollection(ds, "instance_id"))
    definition.output_directory.mkdir(parents=True)

    result_dir = definition.output_directory / "results" / "recipe_test_a"
    result = result_dir / "work" / "timeseries" / "script1" / "result.nc"

    def mock_check_call(cmd, *args, **kwargs):
        result.parent.mkdir(parents=True)
        result.touch()

    mocker.patch.object(
        cmip_ref_metrics_esmvaltool.recipe.subprocess,
        "check_call",
        autospec=True,
        spec_set=True,
        side_effect=mock_check_call,
    )
    open_dataset = mocker.patch.object(
        cmip_ref_metrics_esmvaltool.metrics.example.xarray,
        "open_dataset",
        autospec=True,
        spec_set=True,
    )
    open_dataset.return_value.attrs.__getitem__.return_value = "ABC"

    result = metric.run(definition)

    output_bundle_path = definition.output_directory / result.output_bundle_filename
    metric_bundle_path = definition.output_directory / result.metric_bundle_filename

    assert result.successful
    assert output_bundle_path.exists()
    assert output_bundle_path.is_file()
    assert result.output_bundle_filename.name == "output.json"

    assert metric_bundle_path.exists()
    assert metric_bundle_path.is_file()
    assert result.metric_bundle_filename.name == "metric.json"
