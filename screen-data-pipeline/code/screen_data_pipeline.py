"""
Screen data pipeline (masked version)

Downloads zipped impression and audience (demographics) files from a shared
folder, unzips them, summarises each file by hour, and appends the result to
two SQL Server tables. Files that were already processed are skipped, and the
whole run repeats on a schedule.

All secrets and names are read from environment variables (see .env.example).
"""
import os
import sqlite3
import time
import zipfile

import pandas as pd
import requests
import schedule
from sqlalchemy import create_engine

FOLDER_ID = os.environ["DRIVE_FOLDER_ID"]
API_KEY = os.environ["DRIVE_API_KEY"]
DB_URL = (
    f"mssql+pyodbc://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
    f"@{os.environ['DB_SERVER']}/{os.environ['DB_NAME']}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)
KINDS = ("impressions", "demographics")      # one folder set per file type
LOG_FILES = "processed_files.csv"            # every csv already loaded
LOG_ZIPS = "downloaded_zips.csv"             # every zip already downloaded

IMPRESSIONS_SQL = """
SELECT strftime('%Y-%m-%d %H:00:00', createdDateLocal) AS Created_Date_hr,
       COUNT(*) AS Rows_Count,
       CAST(REPLACE(duration, '.0', '') AS INT)    AS duration,
       isConnected, tenantId, adType,
       CAST(REPLACE(creativeId, '.0', '') AS INT)  AS creativeId, creative_name,
       CAST(REPLACE(screen_id, '.0', '') AS INT)   AS screen_id, screen_name,
       CAST(REPLACE(site_id, '.0', '') AS INT)     AS site_id, site_name,
       CAST(REPLACE(adgroup_id, '.0', '') AS INT)  AS adgroup_id,
       CAST(REPLACE(adgroup_name, '.0', '') AS CHAR) AS adgroup_name,
       CAST(REPLACE(campaign_id, '.0', '') AS INT) AS campaign_id, campaign_name,
       CAST(REPLACE(adId, '.0', '') AS INT)        AS ad_id,
       :source AS Excel_Source
FROM df
GROUP BY 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17
"""

DEMOGRAPHICS_SQL = """
SELECT timestamp AS Timestamp_Hr, COUNT(*) AS Rows_Count,
       siteName, screenDeviceId, gender, ageGroup, :source AS Excel_Source
FROM df
GROUP BY 1, 3, 4, 5, 6
"""


def _log(path, column):
    return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame(columns=[column])


def download_new_zips():
    """List the shared folder and download zip files not seen before."""
    url = f"https://www.googleapis.com/drive/v3/files?q='{FOLDER_ID}'+in+parents&key={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Could not list files: {response.status_code}")
        return
    seen = _log(LOG_ZIPS, "Names")
    for f in response.json().get("files", []):
        name = f["name"]
        kind = next((k for k in KINDS if k in name), None)
        if not kind or not name.endswith(".zip") or name in seen["Names"].values:
            continue
        data = requests.get(
            f"https://www.googleapis.com/drive/v3/files/{f['id']}?alt=media&key={API_KEY}",
            stream=True,
        )
        os.makedirs(f"{kind}_zip", exist_ok=True)
        with open(f"{kind}_zip/{name}", "wb") as out:
            for chunk in data.iter_content(chunk_size=1024):
                if chunk:
                    out.write(chunk)
        seen = pd.concat([seen, pd.DataFrame({"Names": [name]})], ignore_index=True)
        seen.to_csv(LOG_ZIPS, index=False)


def extract_zips():
    """Unzip every downloaded archive into <kind>_csv and delete the zip."""
    for kind in KINDS:
        src = f"{kind}_zip"
        if not os.path.isdir(src):
            continue
        for name in os.listdir(src):
            path = os.path.join(src, name)
            try:
                with zipfile.ZipFile(path) as z:
                    z.extractall(f"{kind}_csv")
                os.remove(path)
            except zipfile.BadZipFile:
                print(f"Not a valid zip file: {name}")


def summarise_and_load(kind, name, path, engine):
    """Aggregate one csv by hour in memory, then append it to SQL Server."""
    conn = sqlite3.connect(":memory:")
    df = pd.read_csv(path, low_memory=False)
    if kind == "impressions":
        df = df.dropna(subset=["createdDateLocal"])
        sql = IMPRESSIONS_SQL
        time_col = "Created_Date_hr"
    else:
        df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%d %H:00:00.000")
        df = df.dropna(subset=["timestamp"])
        sql = DEMOGRAPHICS_SQL
        time_col = "Timestamp_Hr"
    df.to_sql("df", conn, index=False)
    result = pd.read_sql(sql, conn, params={"source": name}).dropna(subset=[time_col])
    result.to_sql(kind, con=engine, if_exists="append", index=False, chunksize=1000)
    conn.close()


def load_new_files():
    """Load every csv that is not in the processed-files log yet."""
    engine = create_engine(DB_URL)
    done = _log(LOG_FILES, "File_Name")
    for kind in KINDS:
        for root, _, files in os.walk(f"{kind}_csv"):
            for name in files:
                if name in done["File_Name"].values:
                    continue
                try:
                    summarise_and_load(kind, name, os.path.join(root, name), engine)
                except Exception as exc:       # empty or malformed file
                    print(f"Skipped {name}: {exc}")
                done = pd.concat(
                    [done, pd.DataFrame({"File_Name": [name], "File_Location": [root]})],
                    ignore_index=True,
                )
                done.to_csv(LOG_FILES, index=False)


def run_all():
    download_new_zips()
    extract_zips()
    load_new_files()


if __name__ == "__main__":
    run_all()
    schedule.every(1).days.do(run_all)
    while True:
        schedule.run_pending()
        time.sleep(1)
