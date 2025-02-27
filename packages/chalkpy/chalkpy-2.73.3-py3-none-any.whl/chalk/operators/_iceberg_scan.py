from __future__ import annotations

from typing import Literal, Mapping

from typing_extensions import final

from chalk import StaticOperator


@final
class IcebergScanOperator(StaticOperator):
    _chalk__operator_name = StaticOperator._chalk__operator_prefix + "iceberg_scan"

    def __init__(
        self,
        target: str | None,
        catalog_options: Mapping[str, str | int | None],
        column_names: tuple[str, ...],
        custom_partitions: dict[str, tuple[Literal["date_trunc(day)"], str]],
    ) -> None:
        catalog_options = dict(catalog_options)
        super().__init__(
            target=target,
            catalog_options=catalog_options,
            column_names=column_names,
            parent=None,
            custom_partitions=custom_partitions,
        )
        self._target = target
        self._catalog_options = catalog_options
        self.column_names = column_names
        self.custom_partitions = custom_partitions
