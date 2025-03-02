from __future__ import annotations

import polars as pl

__all__ = ("append_slash",)


def append_slash(files: pl.LazyFrame) -> pl.LazyFrame:
    return files.with_columns(
        pl.when(pl.col("is_dir"))
        .then(pl.col("name") + "/")
        .otherwise(pl.col("name"))
        .alias("name")
    )
