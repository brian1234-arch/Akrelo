import pandas as pd
from filelock import FileLock
from pathlib import Path

EXCEL_PATH = Path(__file__).resolve().parent.parent / 'data' / 'AKELO_FAMILY_ASSOCIATION_2024.xlsx'
LOCK_PATH = EXCEL_PATH.with_suffix('.lock')
lock = FileLock(str(LOCK_PATH), timeout=10)

DEFAULT_COLS = ['id','name','phone','contributions','notes']

def read_excel():
    if not EXCEL_PATH.exists():
        df = pd.DataFrame(columns=DEFAULT_COLS)
        df.to_excel(EXCEL_PATH, index=False)
        return df
    df = pd.read_excel(EXCEL_PATH)
    for c in DEFAULT_COLS:
        if c not in df.columns:
            df[c] = None
    return df[DEFAULT_COLS]

def write_excel(df):
    df.to_excel(EXCEL_PATH, index=False)
