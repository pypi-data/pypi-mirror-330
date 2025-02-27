import pyarrow as pa  # type: ignore[import-untyped]
import unicodedata


def _return_df(table: pa.Table, info: str = "") -> str:
    # just copy metadata
    df = table.to_pandas().copy(deep=False)

    # Remove non ascii characters from the columns. Those hang claude desktop - server
    # at least on Windows
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].apply(
            lambda x: unicodedata.normalize("NFKD", str(x))
            .encode("ascii", "ignore")
            .decode("ascii")
            .replace("\n", " ")
            .replace("\r", " ")
        )
    if info:
        info += "csv delimited with | containing header starts in next line:\n"
    return str(info + df.to_csv(index=False, sep="|"))
