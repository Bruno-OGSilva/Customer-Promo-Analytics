import os
import re

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account


# Detect "Time:Week Ending mm-dd-yy" inside the file
TIME_RE = re.compile(r"Time:Week Ending (\d{2}-\d{2}-\d{2})")


def _parse_one_csv(file: str) -> pd.DataFrame:
    """
    Read a PFG CSV that contains multiple weekly blocks and return a tidy DataFrame
    where each data row has the correct Time value. All numbers remain strings.
    """
    # Read as a raw grid; no header; keep everything as strings
    raw = pd.read_csv(
        file,
        header=None,
        sep=None,
        engine="python",  # auto-detect delimiter
        dtype=str,
        keep_default_na=False,
        na_values=[],
    )

    # Find rows like "Time:Week Ending 11-06-24", convert to YYYY-MM-DD, and forward-fill
    time_hits = raw[0].astype(str).str.extract(TIME_RE, expand=True)[0]
    raw["Time"] = (
        pd.to_datetime(time_hits, format="%m-%d-%y", errors="coerce")
        .dt.strftime("%Y-%m-%d")
        .ffill()
    )

    # Drop non-data/label rows
    drop_prefix = (
        raw[0].str.startswith("Product & Geography Sales Metrics")
        | raw[0].str.startswith("Brand")
        | raw[0].str.startswith("Sales Organizations")
        | raw[0].str.startswith("Vendor")
        | raw[0].str.startswith("Time:Week Ending")
    )

    # Keep only actual table rows under the "Geography ... Unit ..." header
    mask = (
        (raw[0] != "Geography")  # not the header line
        & raw[0].ne("")
        & raw[1].ne("")
        & raw[2].ne("")  # has first 3 columns
        & ~drop_prefix.fillna(False)
    )

    df = raw.loc[mask, [0, 1, 2, 3, 4, "Time"]].copy()
    df.columns = [
        "Geography",
        "Product",
        "UPC ID",
        "Dollar Sales",
        "Unit Sales",
        "Time",
    ]

    # Keep numbers as strings
    # unique_id same pattern you used
    df["unique_id"] = "pfg|" + df["UPC ID"] + "|" + df["Geography"] + "|" + df["Time"]

    # Metadata
    df["timestamp"] = pd.to_datetime("now")
    df["retail_group"] = "Pattison Food Group"

    # Extra safety: remove any stray header text
    df = df[df["Geography"] != "Geography"]

    # Drop rows where both Dollar Sales and Unit Sales are "0"
    df = df[~((df["Dollar Sales"] == "0") & (df["Unit Sales"] == "0"))]

    return df


def load_csv_files(directory: str) -> pd.DataFrame:
    """Loads all CSV files from a directory and concatenates them."""
    all_files = [
        os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".csv")
    ]
    if not all_files:
        raise ValueError("No CSV files found in the specified directory.")
    frames = [_parse_one_csv(f) for f in all_files]
    return pd.concat(frames, ignore_index=True)


def create_table_if_not_exists(client, dataset_id: str, table_id: str):
    """Creates a BigQuery table if it does not exist."""
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    schema = [
        bigquery.SchemaField("Geography", "STRING"),
        bigquery.SchemaField("Product", "STRING"),
        bigquery.SchemaField("UPC ID", "STRING"),
        bigquery.SchemaField("Dollar Sales", "STRING"),
        bigquery.SchemaField("Unit Sales", "STRING"),
        bigquery.SchemaField("Time", "STRING"),
        bigquery.SchemaField("unique_id", "STRING"),
        bigquery.SchemaField("timestamp", "TIMESTAMP"),
        bigquery.SchemaField("retail_group", "STRING"),
    ]

    try:
        client.get_table(table_ref)  # Check if the table exists
        print(f"Table {table_id} already exists.")
    except Exception:
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        print(f"Created table {table_id}.")


def upload_to_bigquery(
    df: pd.DataFrame,
    credentials_path: str,
    project_id: str,
    dataset_id: str,
    table_id: str,
):
    """Uploads a DataFrame to a BigQuery table using service account credentials."""
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path
    )
    client = bigquery.Client(credentials=credentials, project=project_id)

    create_table_if_not_exists(client, dataset_id, table_id)  # Ensure table exists

    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND
    )

    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # Wait for the job to complete

    print(f"Successfully uploaded {len(df)} records to {table_ref}")


if __name__ == "__main__":
    DIRECTORY = "C:/Customer-Promo-Analytics/data/pfg"
    CREDENTIALS_PATH = "C:/.keys/keyfilepromo.json"
    PROJECT_ID = "customer-promo"
    DATASET_ID = "raw"
    TABLE_ID = "raw_pfg_sales"

    try:
        df = load_csv_files(DIRECTORY)
        upload_to_bigquery(df, CREDENTIALS_PATH, PROJECT_ID, DATASET_ID, TABLE_ID)
    except Exception as e:
        print(f"Error: {e}")
