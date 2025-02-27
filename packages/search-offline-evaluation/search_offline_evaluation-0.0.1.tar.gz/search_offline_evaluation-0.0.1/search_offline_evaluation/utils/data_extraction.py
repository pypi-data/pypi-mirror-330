"""
Define Athena SQL connection
"""

import time
import pandas as pd
from pathlib import Path
from pandas import Timestamp
from pyathena import connect
from pyathena.pandas.util import as_pandas


def get_date_range(start_date, end_date):
    adjusted_end_date = Timestamp(end_date) + pd.Timedelta(days=1)

    dates = [
        str(date.to_period("D")) for date in pd.date_range(start=start_date, end=adjusted_end_date)
    ]
    return dates


class DataExtraction:

    def __init__(self, region, profile_name, bucket):
        self.region = region
        self.profile_name = profile_name
        self.bucket = bucket
        self.conn = self._set_connection()

    def _set_connection(self):
        """Establishes a connection to the database using class attributes.
        This method configures and returns a database connection using parameters such as region name,
        profile name, S3 staging directory, and schema name, all derived from the instance's attributes.

        Returns:
            A database connection object.
        """
        params = dict(
            region_name=self.region,
            profile_name=self.profile_name,
            s3_staging_dir=f"s3://{self.bucket}/tmp/",
            schema_name=self.bucket,
        )
        return connect(**params)

    def read_sql(self, sql_query: str):
        """Executes a SQL query and returns the result as a pandas DataFrame.
        Args:
            sql_query (str): The SQL query to be executed.

        Returns:
            pd.DataFrame: The result of the SQL query as a pandas DataFrame.
        """
        cursor = self.conn.cursor()
        cursor.execute(sql_query)
        return as_pandas(cursor)

    def get_sql_data(self, sql_query: str) -> pd.DataFrame:
        """Wrapper method to execute a SQL query and return the result as a pandas DataFrame.
        This method is a straightforward wrapper around `read_sql`, directly passing the SQL query
        and returning its result.

        Args:
            sql_query (str): The SQL query to be executed.

        Returns:
            pd.DataFrame: The result of the SQL query as a pandas DataFrame.
        """
        return self.read_sql(sql_query)

    def load_data(self, filepath: str, sql_query=None, overwrite=False) -> pd.DataFrame:
        """
        Load or extract data to/from a parquet file based on existence and overwrite conditions.

        Args:
            filepath (str): Path to the parquet file for loading/saving data.
            sql_query (str, optional): SQL query for data extraction if needed. Defaults to None.
            overwrite (bool, optional): Whether to overwrite existing file. Defaults to False.

        Returns:
            pd.DataFrame: Data loaded from file or extracted from DB.

        If the data is loaded from the parquet file, it prints "Loading data from memory". If the data is
        extracted from the database, it prints "Extracting data from DB" and the duration of the extraction
        step in minutes. If neither condition is met, it prints an error message suggesting to review the

        """
        if Path(filepath).exists() and not overwrite:
            print("Loading data from memory")
            return pd.read_parquet(filepath)
        elif sql_query:
            print("Extracting data from DB")
            st = time.time()
            extracted_data = self.get_sql_data(sql_query)
            et = time.time()
            final_res = round((et - st) / 60, 3)
            print(f"Data Extraction step took {final_res} min.")

            # save to memory
            extracted_data.to_parquet(filepath, engine="pyarrow")
            return extracted_data
        else:
            print(
                "Something went wrong. Please review filepath or provide a sql query to extract data from DB."
            )
