import argparse
import time
from pathlib import Path
from search_offline_evaluation.sql.sql_queries import SEARCH_LOGS, ADS_SQL
from search_offline_evaluation.sql.general_queries import SQL_CATEGORIES
from search_offline_evaluation.utils.data_extraction import DataExtraction


def load_country_data(
    data_ext: DataExtraction, country_name, start_date, end_date, overwrite=False
):
    """
    Extract Search logs data and save it to a file. If file already exists get data from memory.

    :param data_ext: data extraction object
    :param country_name: country code name, it has to be consistent with database convention
    :param start_date:
    :param end_date:
    :param overwrite: boolean, set to True to extract from database and overwrite locally
    :return: pd.DataFrame with search logs with autocomplete info.
    """
    start = time.time()
    df = data_ext.load_data_per_day(
        sql_query=SEARCH_LOGS,
        country_name=country_name,
        start_date=start_date,
        end_date=end_date,
        overwrite=overwrite,
    )

    end = time.time()
    proc_time = round((end - start) / 60, 3)
    print(f"Extracting logs data took: {proc_time} minutes.")
    return df


def load_ads_data(
    data_ext: DataExtraction,
    filepath: str,
    country_name: str,
    start_date: str,
    end_date: str,
    overwrite=False,
):
    """
    Extracts and saves search logs data related to ads for a specified country and date range.

    :param data_ext: Object for data extraction with a `load_data` method.
    :param filepath: File path for saving the data. Loads data from this file if exists and `overwrite` is False.
    :param country_name: Country code, consistent with database conventions.
    :param start_date: Start date for data extraction ('YYYY-MM-DD').
    :param end_date: End date for data extraction ('YYYY-MM-DD').
    :param overwrite: If True, extracts and overwrites existing data; otherwise, loads existing data.
    :return: DataFrame containing ads search logs with autocomplete information.
    """

    # Estimate avg amount of sessions per day & country
    sql_query = ADS_SQL.format(COUNTRY_NAME=country_name, START_DATE=start_date, END_DATE=end_date)

    print(f"Extracting Ads data for {country_name} for [{start_date},{end_date}].")
    ads_df = data_ext.load_data(filepath=filepath, sql_query=sql_query, overwrite=overwrite)

    return ads_df


def get_categories_data(data_ext: DataExtraction, country_name, overwrite=False):
    start = time.time()
    # Estimate avg amount of sessions per day & country
    cat_sql = SQL_CATEGORIES.format(COUNTRY_NAME=country_name)

    print(f"Extracting categories data for {country_name}")
    filepath = Path("data", "categories_{country_name}.parquet")
    cat_df = data_ext.load_data(filepath=filepath, sql_query=cat_sql, overwrite=overwrite)

    end = time.time()
    proc_time = round((end - start) / 60, 3)
    print(f"Extracting categories data took: {proc_time} minutes.")
    return cat_df


def main(start_date="2024-04-01", end_date="2024-04-03", country_name="pt"):
    # Usage
    print(
        f"Main: Extracting search logs data for period [{start_date}, {end_date}] in {country_name}"
    )

    # Set up connection
    data_ext = DataExtraction(
        region="eu-west-1",
        profile_name="big-data-global-data-science-ireland",
        bucket="olxgroup-reservoir-ares",
    )

    search_logs = load_country_data(
        data_ext=data_ext,
        country_name=country_name,
        start_date=start_date,
        end_date=end_date,
        overwrite=False,
    )

    categories = get_categories_data(data_ext=data_ext, country_name=country_name)

    return search_logs, categories


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data Extraction Script")
    parser.add_argument(
        "-s",
        "--start_date",
        type=str,
        required=True,
        help="Start date for the data extraction period (YYYY-MM-DD)",
    )
    parser.add_argument(
        "-e",
        "--end_date",
        type=str,
        required=True,
        help="End date for the data extraction period (YYYY-MM-DD)",
    )
    parser.add_argument(
        "-c",
        "--country_name",
        type=str,
        required=True,
        help="Country code name, it has to be consistent with database convention",
    )

    args = parser.parse_args()
    print(args)

    logs_df, categories_df = main(
        start_date=args.start_date, end_date=args.end_date, country_name=args.country_name
    )

    print("Data extraction completed.")
