import argparse
from pathlib import Path

import pandas as pd


def read_csv_fallback(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="gbk")


def dedup_df(df: pd.DataFrame, seq_col: str = "序号") -> pd.DataFrame:
    if seq_col in df.columns:
        data_cols = [c for c in df.columns if c != seq_col]
    else:
        data_cols = list(df.columns)

    deduped = df.drop_duplicates(subset=data_cols, keep="first").copy()

    if seq_col in deduped.columns:
        deduped[seq_col] = range(1, len(deduped) + 1)
        return deduped

    deduped.insert(0, seq_col, range(1, len(deduped) + 1))
    return deduped


def process_csv(csv_path: Path, out_path: Path) -> None:
    df = read_csv_fallback(csv_path)
    deduped = dedup_df(df)
    deduped.to_csv(out_path, index=False, encoding="utf-8-sig")


def process_xlsx(xlsx_path: Path, out_path: Path) -> None:
    try:
        sheets = pd.read_excel(xlsx_path, sheet_name=None)
    except ImportError as exc:
        raise SystemExit(
            "openpyxl 版本过低或未安装，请先运行: pip install -U openpyxl"
        ) from exc

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        for name, df in sheets.items():
            deduped = dedup_df(df)
            deduped.to_excel(writer, sheet_name=name, index=False)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="去重 CrimeTrace-500.csv 和 CrimeTrace-500.xlsx，并重新标注序号。"
    )
    parser.add_argument("--csv", default="CrimeTrace-500.csv", help="CSV 文件路径")
    parser.add_argument("--xlsx", default="CrimeTrace-500.xlsx", help="XLSX 文件路径")
    parser.add_argument(
        "--suffix",
        default="",
        help="输出文件名后缀（默认: 为空，覆盖原文件）",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv)
    xlsx_path = Path(args.xlsx)

    if csv_path.exists():
        out_csv = csv_path.with_name(f"{csv_path.stem}{args.suffix}{csv_path.suffix}")
        process_csv(csv_path, out_csv)
        print(f"CSV 已输出: {out_csv}")
    else:
        print(f"CSV 未找到: {csv_path}")

    if xlsx_path.exists():
        out_xlsx = xlsx_path.with_name(
            f"{xlsx_path.stem}{args.suffix}{xlsx_path.suffix}"
        )
        process_xlsx(xlsx_path, out_xlsx)
        print(f"XLSX 已输出: {out_xlsx}")
    else:
        print(f"XLSX 未找到: {xlsx_path}")


if __name__ == "__main__":
    main()
