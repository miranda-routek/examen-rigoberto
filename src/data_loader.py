from __future__ import annotations

import pandas as pd
import os

from .config import EXAM_DATA_CSV, PROJECTS_CSV, PERCENT_NOT_COMPLETED_CSV


def _read_csv_safely(path):
    """Lee CSV tolerando encodings comunes."""
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin1"):
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            continue
    # último intento sin encoding (puede fallar con UnicodeDecodeError)
    return pd.read_csv(path)


def _drop_unnamed(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[:, ~df.columns.astype(str).str.match(r"^Unnamed")].copy()


def load_exam_data() -> pd.DataFrame:
    """Carga los datos de exam_data.csv."""
    df = _read_csv_safely(EXAM_DATA_CSV)
    df = _drop_unnamed(df)
    
    # Convertir tipos de datos
    if "PercentComplete" in df.columns:
        df["PercentComplete"] = pd.to_numeric(df["PercentComplete"], errors="coerce")
    
    if "BudgetThousands" in df.columns:
        df["BudgetThousands"] = pd.to_numeric(df["BudgetThousands"], errors="coerce")
    
    if "StartDate" in df.columns:
        df["StartDate"] = pd.to_datetime(df["StartDate"], errors="coerce")
    
    if "CriticalFlag" in df.columns:
        df["CriticalFlag"] = df["CriticalFlag"].astype(bool)
    
    # Normalizar strings
    for col in ["ProjectName", "Manager", "Category", "Country", "State"]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()
    
    return df


def load_projects() -> pd.DataFrame:
    df = _read_csv_safely(PROJECTS_CSV)
    df = _drop_unnamed(df)

    # Tipos / limpieza básica
    if "Percent complete" in df.columns:
        df["Percent complete"] = (
            df["Percent complete"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .str.strip()
        )
        df["Percent complete"] = pd.to_numeric(df["Percent complete"], errors="coerce")

    # Fechas (si existen)
    date_cols = [
        "Planned Go Live date",
        "Actual Go Live date",
        "Actual end date",
        "Planned start date",
        "Actual start date",
        "Last WAR",
    ]
    for c in date_cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")

    # Normaliza strings clave
    for c in ["State", "Domain", "Project manager", "Geographical scope", "Project Health"]:
        if c in df.columns:
            df[c] = df[c].astype("string").str.strip()

    return df


def load_percentage_not_completed() -> pd.DataFrame:
    df = _read_csv_safely(PERCENT_NOT_COMPLETED_CSV)
    df = _drop_unnamed(df)

    # Normalización CW (e.g. CW03 -> 3)
    if "CW" in df.columns:
        df["cw_num"] = (
            df["CW"].astype(str).str.extract(r"(\d+)")[0].astype(float)
        )
        df["cw_num"] = df["cw_num"].astype("Int64")

    # valor viene como fracción (0-1) en tu archivo
    if "valor" in df.columns:
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
        df["pct_not_completed"] = df["valor"] * 100.0

    for c in ["Region", "Group"]:
        if c in df.columns:
            df[c] = df[c].astype("string").str.strip()

    return df


def load_all_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    return load_projects(), load_percentage_not_completed()
