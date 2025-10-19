from .excel_util import read_excel, write_excel, lock
import pandas as pd

def read_members():
    df = read_excel()
    # ensure id is int where possible
    if 'id' in df.columns:
        df['id'] = df['id'].fillna(0).astype(int)
    return df.to_dict(orient='records')

def _next_id(df):
    if df.empty:
        return 1
    try:
        return int(df['id'].max()) + 1
    except:
        return len(df)+1

def add_member(payload):
    with lock:
        df = read_excel()
        payload['id'] = _next_id(df)
        df = pd.concat([df, pd.DataFrame([payload])], ignore_index=True)
        write_excel(df)
        return payload

def update_member(member_id, payload):
    with lock:
        df = read_excel()
        mask = df['id'] == int(member_id)
        if not mask.any():
            return None
        for k,v in payload.items():
            if k!='id':
                df.loc[mask, k] = v
        write_excel(df)
        return df[mask].iloc[0].to_dict()

def delete_member(member_id):
    with lock:
        df = read_excel()
        member_id = int(member_id)
        if member_id not in df['id'].values:
            return False
        df = df[df['id'] != member_id]
        write_excel(df)
        return True
