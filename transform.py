import pandas as pd
import ingest 
from io import BytesIO

def transform():

    data, content_type = ingest.extract()

    raw_df = pd.read_excel( BytesIO(data), header =None, engine="openpyxl")

    header_row = None

    for index, row in raw_df.iterrows():
        if "Reporting unit" in row.astype(str).values:
            header_row = index
            break

    df = pd.read_excel(BytesIO(data),skiprows=header_row, header=0, engine="openpyxl")

    df = df[['Reporting unit', 'Reporting unit type', 'State','Year', 'Triage category', 'Number of presentations']]

    df["Year"] = df["Year"].str.split("–").str[0].astype(int)

    df['Number of presentations'] = df['Number of presentations'].replace("<5",None)

    df["Number of presentations"] = pd.to_numeric(df["Number of presentations"], errors="coerce")
    df["Number of presentations"] = df["Number of presentations"].astype("Int64")

    df = df.rename(columns={'Reporting unit':'reporting_unit', 'Reporting unit type':'reporting_unit_type', 'State': 'state','Year':'year', 'Triage category': 'triage_cat', 'Number of presentations': 'presentation'})


    return df, content_type

if __name__ == "__main__":
    df, content_type = transform()
    print(df.head(5))
    print(content_type)
    print(len(df))
    print(df.columns.tolist())
    print(df["year"].unique())
