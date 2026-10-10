import pandas as pd

# =====================================================
# LOAD FILES
# =====================================================

wq1 = pd.read_csv(
    "River water quality monitoring data(1).csv",
    low_memory=False
)

wq2 = pd.read_csv(
    "River water quality monitoring data(2).csv",
    low_memory=False
)

stations = pd.read_csv(
    "Basic information on river water quality monitoring sites (including geographic information).csv",
    low_memory=False
)

# =====================================================
# COMBINE DATA
# =====================================================

wq = pd.concat([wq1, wq2], ignore_index=True)

print("Total rows:", len(wq))

# =====================================================
# FILTER DAHAN RIVER
# =====================================================

dahan = wq[
    wq["river"]
    .astype(str)
    .str.contains("大漢溪", na=False)
].copy()

print("Rows in Dahan River:", len(dahan))

# =====================================================
# KEEP PARAMETERS NEEDED
# =====================================================

wanted_parameters = [
    "酸鹼值",         # pH
    "導電度",         # Conductivity
    "溶氧(電極法)",    # Dissolved Oxygen
    "氨氮",           # NH3
    "濁度"            # Turbidity
]

dahan = dahan[
    dahan["itemname"].isin(wanted_parameters)
].copy()

print("Rows after parameter filter:", len(dahan))

print("\nParameters found:")
print(dahan["itemname"].value_counts())

# =====================================================
# DATE PROCESSING
# =====================================================

dahan["sampledate"] = pd.to_datetime(
    dahan["sampledate"],
    errors="coerce"
)

latest_date = dahan["sampledate"].max()

print("\nLatest Date:", latest_date)

# =====================================================
# USE LATEST RECORD FOR EACH STATION + PARAMETER
# =====================================================

dahan = dahan.sort_values(
    by="sampledate",
    ascending=False
)

dahan = dahan.drop_duplicates(
    subset=["sitename", "itemname"],
    keep="first"
)

# =====================================================
# PIVOT TABLE
# =====================================================

sensor = dahan.pivot_table(
    index="sitename",
    columns="itemname",
    values="itemvalue",
    aggfunc="first"
)

sensor.reset_index(inplace=True)

# =====================================================
# RENAME COLUMNS
# =====================================================

sensor = sensor.rename(
    columns={
        "sitename": "name",
        "溶氧(電極法)": "DO_mgL",
        "導電度": "Cond_uScm",
        "氨氮": "NH3_mgL",
        "濁度": "Turb_NTU",
        "酸鹼值": "pH"
    }
)

# =====================================================
# COORDINATES
# =====================================================

coords = stations[
    [
        "sitename",
        "twd97lon",
        "twd97lat"
    ]
].copy()

coords = coords.rename(
    columns={
        "sitename": "name",
        "twd97lon": "lon",
        "twd97lat": "lat"
    }
)

# =====================================================
# MERGE
# =====================================================

final_sensor = pd.merge(
    sensor,
    coords,
    on="name",
    how="left"
)

# =====================================================
# KEEP ONLY REQUIRED COLUMNS
# =====================================================

final_sensor = final_sensor[
    [
        "name",
        "lon",
        "lat",
        "DO_mgL",
        "Cond_uScm",
        "NH3_mgL",
        "Turb_NTU",
        "pH"
    ]
]

# =====================================================
# REMOVE ROWS WITH NO COORDINATES
# =====================================================

final_sensor = final_sensor.dropna(
    subset=["lon", "lat"]
)

# =====================================================
# SAVE
# =====================================================

final_sensor.to_csv(
    "sensors.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n==============================")
print("SUCCESS")
print("==============================")
print("Rows:", len(final_sensor))
print("\nPreview:")
print(final_sensor.head())

print("\nSaved as sensors.csv")