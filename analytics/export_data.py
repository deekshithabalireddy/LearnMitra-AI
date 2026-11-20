
import os
import sys
import json
import pandas as pd

# Get project root directory
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(BASE_DIR)

# Import MongoDB collection
from backend.database import history_collection


# Fetch learning activities
records = list(
    history_collection.find(
        {},
        {"_id": 0}
    ).sort("created_at", -1)
)


if records:

    # Convert MongoDB records into a DataFrame
    df = pd.DataFrame(records)

    # Convert complex quiz results into readable JSON text
    if "result" in df.columns:
        df["result"] = df["result"].apply(
            lambda value: json.dumps(value, ensure_ascii=False)
            if isinstance(value, (dict, list))
            else value
        )

    # Format date
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(
            df["created_at"],
            errors="coerce"
        ).dt.strftime("%Y-%m-%d %H:%M:%S")

    # Create data folder if it does not exist
    DATA_DIR = os.path.join(BASE_DIR, "data")
    os.makedirs(DATA_DIR, exist_ok=True)

    # Export CSV
    OUTPUT_FILE = os.path.join(
        DATA_DIR,
        "learnmitra_activity.csv"
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print("Learning activities exported successfully!")
    print("Total records:", len(df))
    print("CSV file location:", OUTPUT_FILE)

else:
    print("No learning activities found in MongoDB.")
