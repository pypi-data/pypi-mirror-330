from typing import Dict, Iterator, Union

import polars as pl
from bioframe import SCHEMAS
from datafusion import DataFrame
from polars.io.plugins import register_io_source
from tqdm.auto import tqdm

from polars_bio.polars_bio import (
    InputFormat,
    ReadOptions,
    VcfReadOptions,
    py_register_table,
    py_scan_table,
    py_stream_scan_table,
)

from .context import ctx
from .range_op_helpers import stream_wrapper


def read_bam(path: str) -> pl.LazyFrame:
    """
    Read a BAM file into a LazyFrame.

    Parameters:
        path: The path to the BAM file.
    """
    return file_lazy_scan(path, InputFormat.Bam, None)


# TODO handling reference
# def read_cram(path: str) -> pl.LazyFrame:
#     """
#     Read a CRAM file into a LazyFrame.
#
#     Parameters:
#         path: The path to the CRAM file.
#     """
#     return file_lazy_scan(path, InputFormat.Cram)


# TODO passing of bam_region_filter
# def read_indexed_bam(path: str) -> pl.LazyFrame:
#     """
#     Read an indexed BAM file into a LazyFrame.
#
#     Parameters:
#         path: The path to the BAM file.
#
#     !!! warning
#         Predicate pushdown is not supported yet. So no real benefit from using an indexed BAM file.
#     """
#     return file_lazy_scan(path, InputFormat.IndexedBam)


def read_vcf(
    path: str,
    info_fields: Union[list[str], None] = None,
    thread_num: int = 1,
    streaming: bool = False,
) -> Union[pl.LazyFrame, pl.DataFrame]:
    """
    Read a VCF file into a LazyFrame.

    Parameters:
        path: The path to the VCF file.
        info_fields: The fields to read from the INFO column.
        thread_num: The number of threads to use for reading the VCF file.
        streaming: Whether to read the VCF file in streaming mode.
    """
    vcf_read_options = VcfReadOptions(info_fields=info_fields, thread_num=thread_num)
    read_options = ReadOptions(vcf_read_options=vcf_read_options)
    if streaming:
        return read_file(path, InputFormat.Vcf, read_options, streaming)
    else:
        return file_lazy_scan(path, InputFormat.Vcf, read_options)


def read_fasta(path: str) -> pl.LazyFrame:
    """
    Read a FASTA file into a LazyFrame.

    Parameters:
        path: The path to the FASTA file.
    """
    return file_lazy_scan(path, InputFormat.Fasta, None)


def read_fastq(path: str) -> pl.LazyFrame:
    """
    Read a FASTQ file into a LazyFrame.

    Parameters:
        path: The path to the FASTQ file.
    """
    return file_lazy_scan(path, InputFormat.Fastq, None)


# def read_indexed_vcf(path: str) -> pl.LazyFrame:
#     """
#     Read an indexed VCF file into a LazyFrame.
#
#     Parameters:
#         Parameters:
#         path: The path to the VCF file.
#
#     !!! warning
#         Predicate pushdown is not supported yet. So no real benefit from using an indexed VCF file.
#     """
#     return file_lazy_scan(path, InputFormat.Vcf)


def file_lazy_scan(
    path: str, input_format: InputFormat, read_options: ReadOptions
) -> pl.LazyFrame:
    df_lazy: DataFrame = read_file(path, input_format, read_options)
    arrow_schema = df_lazy.schema()

    def _overlap_source(
        with_columns: Union[pl.Expr, None],
        predicate: Union[pl.Expr, None],
        n_rows: Union[int, None],
        _batch_size: Union[int, None],
    ) -> Iterator[pl.DataFrame]:
        if n_rows and n_rows < 8192:  # 8192 is the default batch size in datafusion
            df = df_lazy.execute_stream().next().to_pyarrow()
            df = pl.DataFrame(df).limit(n_rows)
            if predicate is not None:
                df = df.filter(predicate)
            # TODO: We can push columns down to the DataFusion plan in the future,
            #  but for now we'll do it here.
            if with_columns is not None:
                df = df.select(with_columns)
            yield df
            return
        df_stream = df_lazy.execute_stream()
        progress_bar = tqdm(unit="rows")
        for r in df_stream:
            py_df = r.to_pyarrow()
            df = pl.DataFrame(py_df)
            if predicate is not None:
                df = df.filter(predicate)
            # TODO: We can push columns down to the DataFusion plan in the future,
            #  but for now we'll do it here.
            if with_columns is not None:
                df = df.select(with_columns)
            progress_bar.update(len(df))
            yield df

    return register_io_source(_overlap_source, schema=arrow_schema)


def read_file(
    path: str,
    input_format: InputFormat,
    read_options: ReadOptions,
    streaming: bool = False,
) -> Union[pl.LazyFrame, pl.DataFrame]:
    """
    Read a file into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the file.
    input_format : InputFormat
        The input format of the file.
    read_options : ReadOptions, e.g. VcfReadOptions
    streaming: Whether to read the file in streaming mode.

    Returns
    -------
    pl.DataFrame
        The DataFrame.
    """
    table = py_register_table(ctx, path, input_format, read_options)
    if streaming:
        return stream_wrapper(py_stream_scan_table(ctx, table.name))
    else:
        return py_scan_table(ctx, table.name)


def read_table(path: str, schema: Dict = None, **kwargs) -> pl.LazyFrame:
    """
     Read a tab-delimited (i.e. BED) file into a Polars LazyFrame.
     Tries to be compatible with Bioframe's [read_table](https://bioframe.readthedocs.io/en/latest/guide-io.html)
     but faster and lazy. Schema should follow the Bioframe's schema [format](https://github.com/open2c/bioframe/blob/2b685eebef393c2c9e6220dcf550b3630d87518e/bioframe/io/schemas.py#L174).

    Parameters:
        path: The path to the file.
        schema: Schema should follow the Bioframe's schema [format](https://github.com/open2c/bioframe/blob/2b685eebef393c2c9e6220dcf550b3630d87518e/bioframe/io/schemas.py#L174).


    """
    df = pl.scan_csv(path, separator="\t", has_header=False, **kwargs)
    if schema is not None:
        columns = SCHEMAS[schema]
        if len(columns) != len(df.collect_schema()):
            raise ValueError(
                f"Schema incompatible with the input. Expected {len(columns)} columns in a schema, got {len(df.collect_schema())} in the input data file. Please provide a valid schema."
            )
        for i, c in enumerate(columns):
            df = df.rename({f"column_{i+1}": c})
    return df
