import os
import re

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account


# Detect "Time:Promo Week Ending 111324" inside the file
TIME_RE = re.compile(r"Time:Promo Week Ending (\d{6})")


def _parse_one_csv(file: str) -> pd.DataFrame:
    """
    Read a Sobeys CSV that contains multiple weekly blocks and return a tidy DataFrame
    where each data row has the correct Time value. All numbers remain strings.
    """
    # Read as a raw grid; no header; keep everything as strings
    raw = pd.read_csv(
        file,
        header=None,
        sep=None,
        engine="python",
        dtype=str,
        keep_default_na=False,
        na_values=[],
    )

    # Find rows like "Time:Promo Week Ending 111324", convert to YYYY-MM-DD, and forward-fill
    time_hits = raw[0].astype(str).str.extract(TIME_RE, expand=True)[0]

    raw["Time"] = (
        pd.to_datetime(time_hits, format="%m%d%y", errors="coerce")
        .dt.strftime("%Y-%m-%d")
        .ffill()
    )

    # Drop non-data lines
    drop_prefix = (
        raw[0].str.startswith("Product & Geography Sales Metrics")
        | raw[0].str.startswith("Sobeys Brand")
        | raw[0].str.startswith("Sobeys Sales Organizations")
        | raw[0].str.startswith("Vendor")
        | raw[0].str.startswith("Time:Promo Week Ending")
    )

    # Keep only the actual table rows (under the "Geography ... Unit ..." header)
    mask = (
        (raw[0] != "Geography")  # not the table header row
        & raw[0].ne("")
        & raw[1].ne("")
        & raw[2].ne("")  # has first 3 columns
        & ~drop_prefix.fillna(False)
    )

    df = raw.loc[mask, [0, 1, 2, 3, 4, "Time"]].copy()
    df.columns = [
        "Geography",
        "Product",
        "UPC No",
        "Dollar Sales All Sales",
        "Unit Sales All Sales",
        "Time",
    ]

    # Enrichments kept from your original code
    df["store_id"] = df["Geography"].str.extract(r"Store (\d+)", expand=False)
    df["unique_id"] = "sobeys|" + df["UPC No"] + "|" + df["store_id"] + "|" + df["Time"]
    df["timestamp"] = pd.to_datetime("now")
    df["retail_group"] = "Sobeys"

    # Extra safety: remove any stray header text that might slip in
    df = df[df["Geography"] != "Geography"]
    df = df[df["Geography"] != "Unit Sales All Sales"]

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
        bigquery.SchemaField("UPC No", "STRING"),
        bigquery.SchemaField("Dollar Sales All Sales", "STRING"),
        bigquery.SchemaField("Unit Sales All Sales", "STRING"),
        bigquery.SchemaField("Time", "STRING"),
        bigquery.SchemaField("store_id", "STRING"),
        bigquery.SchemaField("unique_id", "STRING"),
        bigquery.SchemaField("timestamp", "TIMESTAMP"),
        bigquery.SchemaField("retail_group", "STRING"),
    ]

    try:
        client.get_table(table_ref)
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

    create_table_if_not_exists(client, dataset_id, table_id)

    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND
    )

    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()

    print(f"Successfully uploaded {len(df)} records to {table_ref}")


if __name__ == "__main__":
    DIRECTORY = "C:/Customer-Promo-Analytics/data/sobeys"
    CREDENTIALS_PATH = "C:/.keys/keyfilepromo.json"
    PROJECT_ID = "customer-promo"
    DATASET_ID = "raw"
    TABLE_ID = "raw_sobeys_sales"

    try:
        df = load_csv_files(DIRECTORY)
        upload_to_bigquery(df, CREDENTIALS_PATH, PROJECT_ID, DATASET_ID, TABLE_ID)
    except Exception as e:
        print(f"Error: {e}")
