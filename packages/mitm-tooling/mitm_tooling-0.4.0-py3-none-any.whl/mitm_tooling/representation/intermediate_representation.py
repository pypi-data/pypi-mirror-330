from __future__ import annotations

import itertools
import logging
from collections import defaultdict
from collections.abc import Iterator, Iterable, Sequence, Mapping
from typing import Self

import pandas as pd
import pydantic
from pydantic import ConfigDict

from mitm_tooling.data_types.data_types import MITMDataType
from mitm_tooling.definition import get_mitm_def
from mitm_tooling.definition.definition_representation import ConceptName, MITM
from mitm_tooling.utilities.python_utils import take_first
from .common import mk_header_file_columns, ColumnName

logger = logging.getLogger('api')


class HeaderEntry(pydantic.BaseModel):
    concept: ConceptName
    kind: str
    type_name: str
    attributes: list[ColumnName]
    attribute_dtypes: list[MITMDataType]

    @pydantic.model_validator(mode='after')
    def attr_check(self):
        if not len(self.attributes) == len(self.attribute_dtypes):
            raise ValueError('Length of specified attributes and their data types differs.')
        return self

    @classmethod
    def from_row(cls, row: Sequence[str], mitm: MITM) -> Self | None:
        kind, type_name = row[0], row[1]
        concept = get_mitm_def(mitm).inverse_concept_key_map.get(kind)
        if not concept:
            logger.error(f'Encountered unknown concept key: "{kind}".')
            return None

        attrs, attr_dts = [], []
        for a, a_dt in zip(row[slice(2, None, 2)], row[slice(3, None, 2)]):
            if pd.notna(a) and pd.notna(a_dt):
                attrs.append(a)
                try:
                    mitm_dt = MITMDataType(a_dt.lower()) if a_dt else MITMDataType.Unknown
                    attr_dts.append(mitm_dt)
                except ValueError:
                    logger.error(f'Encountered unrecognized data type during header import: {a_dt}.')
                    return None
        return HeaderEntry(concept=concept, kind=kind, type_name=type_name, attributes=attrs, attribute_dtypes=attr_dts)

    def get_k(self) -> int:
        return len(self.attributes)

    def to_row(self) -> list[str | None]:
        return [self.kind, self.type_name] + list(
            itertools.chain(*zip(self.attributes, map(str, self.attribute_dtypes))))


class Header(pydantic.BaseModel):
    mitm: MITM
    header_entries: list[HeaderEntry] = pydantic.Field(default_factory=list)

    @classmethod
    def from_df(cls, df: pd.DataFrame, mitm: MITM) -> Self:
        header_entries = [HeaderEntry.from_row(row, mitm) for row in df.itertuples(index=False)]
        return Header(mitm=mitm, header_entries=header_entries)

    def generate_header_df(self) -> pd.DataFrame:
        k = max(map(lambda he: he.get_k(), self.header_entries), default=0)
        deduplicated = {}
        for he in self.header_entries:
            deduplicated[(he.kind, he.type_name)] = he
        lol = [he.to_row() for he in deduplicated.values()]
        return pd.DataFrame(data=lol, columns=mk_header_file_columns(k))

    def get(self, concept: ConceptName, type_name: str) -> HeaderEntry | None:
        return self._map.get(concept, {}).get(type_name)

    @property
    def _map(self) -> Mapping[ConceptName, Mapping[str, HeaderEntry]]:
        res = defaultdict(dict)
        for he in self.header_entries:
            res[he.concept][he.type_name] = he
        return dict(res)


class MITMData(Iterable[tuple[ConceptName, pd.DataFrame]], pydantic.BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    header: Header
    concept_dfs: dict[ConceptName, pd.DataFrame] = pydantic.Field(default_factory=dict)

    def __iter__(self):
        return iter(self.concept_dfs.items())

    def as_generalized(self) -> Self:
        mitm_def = get_mitm_def(self.header.mitm)
        dfs = defaultdict(list)
        for c, df in self.concept_dfs.items():
            c = mitm_def.get_parent(c)
            dfs[c].append(df)
        dfs = {c: pd.concat(dfs_, axis='rows', ignore_index=True) for c, dfs_ in dfs.items()}
        return MITMData(header=self.header, concept_dfs=dfs)

    def as_specialized(self) -> Self:
        mitm_def = get_mitm_def(self.header.mitm)
        dfs = {}
        for c, df in self:
            if mitm_def.get_properties(c).is_abstract:
                leaf_concepts = mitm_def.get_leafs(c)

                for sub_c_key, idx in df.groupby('kind').groups.items():
                    sub_c = mitm_def.inverse_concept_key_map[str(sub_c_key)]
                    dfs[sub_c] = df.loc[idx]
            else:
                dfs[c] = df
        return MITMData(header=self.header, concept_dfs=dfs)


class StreamingConceptData(pydantic.BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    structure_df: pd.DataFrame
    chunk_iterators: list[Iterator[tuple[pd.DataFrame, list[HeaderEntry]]]] = pydantic.Field(default_factory=list)


class StreamingMITMData(Iterable[tuple[ConceptName, StreamingConceptData]], pydantic.BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    mitm: MITM
    data_sources: dict[ConceptName, StreamingConceptData] = pydantic.Field(default_factory=dict)

    def __iter__(self):
        return iter(self.data_sources.items())

    def as_generalized(self) -> Self:
        mitm_def = get_mitm_def(self.mitm)
        combined_data_sources = defaultdict(list)
        for c, ds in self:
            combined_data_sources[mitm_def.get_parent(c)].append(ds)
        data_sources = {}
        for c, ds_list in combined_data_sources.items():
            structure_dfs = [ds.structure_df for ds in ds_list]
            assert all(
                a.equals(b) for a, b in
                zip(structure_dfs[:-1],
                    structure_dfs[1:])), f'concept {c} not generalizable in {self} (structure_dfs differ)'
            data_sources[c] = StreamingConceptData(structure_df=take_first(structure_dfs),
                                                   chunk_iterators=[it for ds in ds_list for it in ds.chunk_iterators])
        return StreamingMITMData(mitm=self.mitm, data_sources=data_sources)
