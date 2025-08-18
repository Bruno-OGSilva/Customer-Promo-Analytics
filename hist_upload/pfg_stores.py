import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account


def load_store_dimension(directory: str) -> pd.DataFrame:
    """Loads all CSV files from the directory and concatenates them into a DataFrame."""
    all_files = [
        os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".csv")
    ]

    if not all_files:
        raise ValueError("No CSV files found in the specified directory.")

    df_list = []
    for file in all_files:
        try:
            print(f"Processing file: {file}")

            df = pd.read_csv(
                file, skiprows=0, dtype=str, encoding="utf-8"
            )  # Read all columns as string

            # Add current timestamp
            df["timestamp"] = pd.to_datetime("now")
            # Add the retail group
            df["retail_group"] = "Pattison Food Group"
            # Drop the header row if it is repeated as a data row
            expected_header = [
                "Store Number",
                "Store Name",
                "Address",
                "City Name",
                "Postal Code",
                "Banner Name",
                "Store Status",
            ]
            # Standardize column names by stripping whitespace
            df.columns = df.columns.str.strip()
            # Check if first row is the header and remove it if it matches
            if len(df.columns) == len(expected_header) and all(
                df.iloc[0].str.strip() == expected_header
            ):
                df = df.iloc[1:]
            df_list.append(df)
        except PermissionError:
            print(f"Permission denied: {file}. Skipping this file.")
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    if not df_list:
        raise ValueError("No valid CSV files were processed.")

    unified_df = pd.concat(df_list, ignore_index=True)
    return unified_df


def create_table_if_not_exists(
    client, dataset_id: str, table_id: str, df: pd.DataFrame
):
    """Creates a BigQuery table if it does not exist using DataFrame's columns."""
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    schema = [bigquery.SchemaField(col, "STRING") for col in df.columns]

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

    create_table_if_not_exists(
        client, dataset_id, table_id, df
    )  # Ensure table exists before uploading

    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # Wait for the job to complete

    print(f"Successfully uploaded {len(df)} records to {table_ref}")


if __name__ == "__main__":
    FILE_PATH = (
        "C:/Customer-Promo-Analytics/data/pfg_stores"  # Change to your file path
    )
    CREDENTIALS_PATH = (
        "C:/.keys/keyfilepromo.json"  # Update with your credentials file path
    )
    PROJECT_ID = "customer-promo"
    DATASET_ID = "raw"
    TABLE_ID = "raw_pfg_stores"

    try:
        df = load_store_dimension(FILE_PATH)
        upload_to_bigquery(df, CREDENTIALS_PATH, PROJECT_ID, DATASET_ID, TABLE_ID)
    except Exception as e:
        print(f"Error: {e}")
