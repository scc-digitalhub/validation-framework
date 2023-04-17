"""
DataReader registry.
"""
# Base imports
from datajudge.data_reader.base_reader.base_file_reader import FileReader
from datajudge.data_reader.base_reader.base_native_reader import NativeReader
from datajudge.data_reader.base_reader.base_buffer_reader import BufferReader
from datajudge.utils.commons import (
    BASE_FILE_READER,
    BASE_NATIVE_READER,
    BASE_BUFFER_READER,
)


# Registry of data readers
REGISTRY = {
    BASE_FILE_READER: FileReader,
    BASE_NATIVE_READER: NativeReader,
    BASE_BUFFER_READER: BufferReader,
}

try:
    from datajudge.data_reader.pandas_dataframe_duckdb_reader import (
        PandasDataFrameDuckDBReader,
    )
    from datajudge.utils.commons import PANDAS_DATAFRAME_DUCKDB_READER

    REGISTRY[PANDAS_DATAFRAME_DUCKDB_READER] = PandasDataFrameDuckDBReader
except ImportError:
    ...

try:
    from datajudge.data_reader.pandas_dataframe_file_reader import (
        PandasDataFrameFileReader,
    )
    from datajudge.utils.commons import PANDAS_DATAFRAME_FILE_READER

    REGISTRY[PANDAS_DATAFRAME_FILE_READER] = PandasDataFrameFileReader
except ImportError:
    ...

try:
    from datajudge.data_reader.pandas_dataframe_sql_reader import (
        PandasDataFrameSQLReader,
    )
    from datajudge.utils.commons import PANDAS_DATAFRAME_SQL_READER

    REGISTRY[PANDAS_DATAFRAME_SQL_READER] = PandasDataFrameSQLReader
except ImportError:
    ...

try:
    from datajudge.data_reader.polars_dataframe_duckdb_reader import (
        PolarsDataFrameDuckDBReader,
    )
    from datajudge.utils.commons import POLARS_DATAFRAME_DUCKDB_READER

    REGISTRY[POLARS_DATAFRAME_DUCKDB_READER] = PolarsDataFrameDuckDBReader
except ImportError:
    ...

try:
    from datajudge.data_reader.polars_dataframe_file_reader import (
        PolarsDataFrameFileReader,
    )
    from datajudge.utils.commons import POLARS_DATAFRAME_FILE_READER

    REGISTRY[POLARS_DATAFRAME_FILE_READER] = PolarsDataFrameFileReader
except ImportError:
    ...

try:
    from datajudge.data_reader.polars_dataframe_sql_reader import (
        PolarsDataFrameSQLReader,
    )
    from datajudge.utils.commons import POLARS_DATAFRAME_SQL_READER

    REGISTRY[POLARS_DATAFRAME_SQL_READER] = PolarsDataFrameSQLReader
except ImportError:
    ...
