# -*- coding: utf-8 -*-

import dataclasses
import json
import os

from collections import OrderedDict
from collections import defaultdict
from typing import Mapping

# 3-rd party modules

from icecream import ic
import numpy as np
import pandas as pd

# local

from .. constants import (
    STAGING_FIELD,
)

from .. config import (
    AssignIdConfig,
    Config,
)

from . search_column_value import search_column_value
from . set_nested_field_value import set_nested_field_value
from . set_row_value import set_row_staging_value

from .. types import (
    AssignIdConfig,
    IdContextMap,
    Row,
)

def assign_id(
    id_context_map: IdContextMap,
    row: Row,
    config: Config,
):
    context_columns = []
    context_values = []
    if config.context:
        for context_column in config.context:
            value, found = search_column_value(row.nested, context_column)
            if not found:
                raise KeyError(f'Column not found: {context_column}, existing columns: {row.flat.keys()}')
            context_columns.append(context_column)
            context_values.append(value)
    primary_columns = []
    primary_values = []
    for primary_column in config.primary:
        value, found = search_column_value(row.nested, primary_column)
        if not found:
            raise KeyError(f'Column not found: {primary_column}, existing columns: {row.flat.keys()}')
        primary_columns.append(primary_column)
        primary_values.append(value)
    context_key = (
        tuple(context_columns),
        tuple(context_values),
        tuple(primary_columns),
    )
    primary_value = tuple(primary_values)
    id_map = id_context_map[context_key]
    if primary_value not in id_map.dict_value_to_id:
        field_id = id_map.max_id + 1
        id_map.max_id = field_id
        id_map.dict_value_to_id[primary_value] = field_id
        id_map.dict_id_to_value[field_id] = primary_value
    else:
        field_id = id_map.dict_value_to_id[primary_value]
    set_row_staging_value(row, config.target, field_id)
    return row
