import pytest

from great_expectations.compatibility.pydantic import ValidationError
from great_expectations.core.types import Comparable
from great_expectations.metrics.domain import AbstractClassInstantiationError, ColumnValues, Domain
from great_expectations.metrics.metric import Metric, MixinTypeError
from great_expectations.validator.metric_configuration import (
    MetricConfiguration,
    MetricConfigurationID,
)

BATCH_ID = "my_data_source-my_data_asset-year_2025"
COLUMN = "my_column"

FULLY_QUALIFIED_METRIC_NAME = "column_values.above"


class MockDomain(Domain):
    galaxy: str


class NotADomain: ...


class TestMetric:
    @pytest.mark.unit
    def test_metric_instantiation_raises(self):
        with pytest.raises(AbstractClassInstantiationError):
            Metric(batch_id=BATCH_ID, column=COLUMN)


class TestMetricDefinition:
    @pytest.mark.unit
    def test_success(self):
        class ColumnValuesAbove(Metric, ColumnValues):
            name = FULLY_QUALIFIED_METRIC_NAME

            min_value: Comparable
            strict_min: bool = False

    @pytest.mark.unit
    def test_missing_domain_mixin_raises(self):
        with pytest.raises(MixinTypeError):

            class ColumnValuesAbove(Metric):
                name = FULLY_QUALIFIED_METRIC_NAME

                min_value: Comparable
                strict_min: bool = False

    @pytest.mark.unit
    def test_more_than_one_domain_mixin_raises(self):
        with pytest.raises(MixinTypeError):

            class ColumnValuesAbove(Metric, ColumnValues, MockDomain):
                name = FULLY_QUALIFIED_METRIC_NAME

                min_value: Comparable
                strict_min: bool = False

    @pytest.mark.unit
    def test_non_domain_mixin_raises(self):
        with pytest.raises(MixinTypeError):

            class ColumnValuesAbove(Metric, NotADomain):
                name = FULLY_QUALIFIED_METRIC_NAME

                min_value: Comparable
                strict_min: bool = False


class TestMetricInstantiation:
    class ColumnValuesAbove(Metric, ColumnValues):
        name = FULLY_QUALIFIED_METRIC_NAME

        min_value: Comparable
        strict_min: bool = False

    @pytest.mark.unit
    def test_instantiation_success(self):
        self.ColumnValuesAbove(
            batch_id=BATCH_ID,
            column=COLUMN,
            min_value=42,
        )

    @pytest.mark.unit
    def test_instantiation_missing_domain_parameters_raises(self):
        with pytest.raises(ValidationError):
            self.ColumnValuesAbove(min_value=42)


class TestMetricConfig:
    class ColumnValuesAbove(Metric, ColumnValues):
        name = FULLY_QUALIFIED_METRIC_NAME

        min_value: Comparable
        strict_min: bool = False

    @pytest.mark.unit
    def test_success(self):
        expected_config = MetricConfiguration(
            metric_name=FULLY_QUALIFIED_METRIC_NAME,
            metric_domain_kwargs={
                "batch_id": BATCH_ID,
                "row_condition": None,
                "column": COLUMN,
            },
            metric_value_kwargs={
                "min_value": 42,
                "strict_min": False,
            },
        )

        actual_config = self.ColumnValuesAbove(
            batch_id=BATCH_ID,
            column=COLUMN,
            min_value=42,
        ).config

        assert actual_config.metric_name == expected_config.metric_name
        assert actual_config.metric_domain_kwargs == expected_config.metric_domain_kwargs
        assert actual_config.metric_value_kwargs == expected_config.metric_value_kwargs
        assert isinstance(actual_config.id, MetricConfigurationID)


class TestMetricImmutability:
    class ColumnValuesAbove(Metric, ColumnValues):
        name = FULLY_QUALIFIED_METRIC_NAME

        min_value: Comparable
        strict_min: bool = False

    @pytest.mark.unit
    def test_domain_kwarg_immutability_success(self):
        column_values_above = self.ColumnValuesAbove(
            batch_id=BATCH_ID,
            column=COLUMN,
            min_value=42,
        )

        with pytest.raises(TypeError):
            column_values_above.column = "updated_column"

    @pytest.mark.unit
    def test_value_kwarg_immutability_success(self):
        column_values_above = self.ColumnValuesAbove(
            batch_id=BATCH_ID,
            column=COLUMN,
            min_value=42,
        )

        with pytest.raises(TypeError):
            column_values_above.min_value = 42
