# etl.py
import requests
import sqlalchemy

API_KEY = "c84fcd1a-4d39-4b7c-948d-6d48367965bc"
BASE_URL = "https://api.harvardartmuseums.org"

# Fetch data from Harvard API

def fetch_objects(classification, count=2500):
    params = {"apikey": API_KEY, "classification": classification, "size": 100, "page": 1} # fetch 100 records per page
    all_data = []

    while len(all_data) < count:
        try:
            # Call API
            res = requests.get(f"{BASE_URL}/object", params=params, timeout=10)
            res.raise_for_status()
            data = res.json()

            # Stop if no records        
            if "records" not in data or not data["records"]:
                break
            # Add records
            all_data.extend(data["records"])
            # Go to next page if available
            if "info" in data and data["info"].get("next"):
                params["page"] += 1
            else:
                break
        except Exception as e:
            print("Error fetching:", e)
            break

    return all_data[:count]

# Transform raw API data
# into structured format for database insertion
# Returns three lists: metadata, media, colors

def transform_data(records):
    metadata, media, colors = [], [], []
    for item in records:
        if not item.get("id") or not item.get("title"):    # Skip records without ID or Title
            continue

        metadata.append((
            item.get("id"), item.get("title"), item.get("culture"), item.get("period"),
            item.get("century"), item.get("medium"), item.get("dimensions"),
            item.get("description"), item.get("department"), item.get("classification"),
            item.get("accessionyear"), item.get("accessionmethod")
        ))

        media.append((
            item.get("id"), item.get("imagecount", 0), item.get("mediacount", 0),
            item.get("colorcount", 0), item.get("rank", 0),
            item.get("datebegin", 0), item.get("dateend", 0)
        ))

        for color in item.get("colors", []):
            colors.append((
                item.get("id"), color.get("color"), color.get("spectrum"),
                color.get("hue"), color.get("percent"), color.get("css3")
            ))
    return metadata, media, colors

# Insert into TiDB tables
# Uses ON DUPLICATE KEY UPDATE to avoid duplicates.
def insert_records(engine, table, data):  #Uses ON DUPLICATE KEY UPDATE to avoid duplicates.
    if not data:
        return

    with engine.begin() as conn:
        if table == "artifact_metadata":
            columns = ['id', 'title', 'culture', 'period', 'century',
                       'medium', 'dimensions', 'description', 'department',
                       'classification', 'accessionyear', 'accessionmethod']
            upd = ','.join([f"{col}=VALUES({col})" for col in columns if col != 'id'])

        elif table == "artifact_media":
            columns = ['objectid', 'imagecount', 'mediacount', 'colorcount',
                       'rank_value', 'datebegin', 'dateend']
            upd = ','.join([f"{col}=VALUES({col})" for col in columns if col != 'objectid'])

        else:  # artifact_colors
            columns = ['objectid', 'color', 'spectrum', 'hue', 'percent', 'css3']
            upd = ','.join([f"{col}=VALUES({col})" for col in columns if col not in ['objectid','color']])

        # Build SQL
        keys = ','.join(columns)
        vals = ','.join([f":{col}" for col in columns])
        # Convert tuples into dictionaries (for SQLAlchemy)
        q = f"INSERT INTO {table} ({keys}) VALUES ({vals}) ON DUPLICATE KEY UPDATE {upd}"

        # Run insert query
        dict_data = [dict(zip(columns, row)) for row in data]
        conn.execute(sqlalchemy.text(q), dict_data)
