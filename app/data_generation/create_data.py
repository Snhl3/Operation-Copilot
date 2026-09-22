"""
Industrial AI Operations Copilot
Synthetic Dataset Generation

Source:
    data/raw/ai4i2020.csv

Generated:
    data/processed/equipment.csv
    data/processed/production.csv
    data/processed/maintenance.csv
    data/processed/quality.csv
    data/processed/energy.csv

IMPORTANT:
    AI4I 2020 is the original source dataset.
    The other datasets are synthetic datasets generated for this
    portfolio project using AI4I variables and documented assumptions.
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

# Project root:
# Operation_copilot/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

SOURCE_FILE = RAW_DIR / "ai4i2020.csv"

# Create processed directory if it does not exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. CONFIGURATION
# ============================================================

RANDOM_SEED = 42
NUM_EQUIPMENT = 50

np.random.seed(RANDOM_SEED)
rng = np.random.default_rng(RANDOM_SEED)


# ============================================================
# 3. LOAD AI4I DATASET
# ============================================================

print("=" * 70)
print("LOADING AI4I DATASET")
print("=" * 70)

if not SOURCE_FILE.exists():
    raise FileNotFoundError(
        f"AI4I dataset not found at:\n{SOURCE_FILE}\n\n"
        "Please make sure ai4i2020.csv is inside data/raw/"
    )

df = pd.read_csv(SOURCE_FILE)

# Clean column names
df.columns = df.columns.str.strip()

print(f"Source file: {SOURCE_FILE}")
print(f"Rows       : {len(df):,}")
print(f"Columns    : {len(df.columns)}")


# ============================================================
# 4. VALIDATE REQUIRED AI4I COLUMNS
# ============================================================

required_columns = [
    "UDI",
    "Product ID",
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
    "Machine failure",
    "TWF",
    "HDF",
    "PWF",
    "OSF",
    "RNF",
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        "The following required columns are missing from AI4I:\n"
        + "\n".join(missing_columns)
    )

print("AI4I column validation: PASSED")


# ============================================================
# 5. BASIC SOURCE DATA VALIDATION
# ============================================================

print("\nSource missing values:")
print(df[required_columns].isnull().sum())

duplicate_count = df.duplicated().sum()

print(f"\nDuplicate rows: {duplicate_count}")

if duplicate_count > 0:
    print(
        "WARNING: Duplicate rows exist in the source dataset. "
        "They will not automatically be removed because the original "
        "AI4I dataset should remain unchanged."
    )


# ============================================================
# 6. CREATE SYNTHETIC EQUIPMENT IDs
# ============================================================

"""
AI4I does not contain a physical machine/equipment identifier.

Therefore, we introduce a synthetic equipment_id.

Assumption:
    10,000 AI4I observations are distributed across 50 synthetic
    CNC production machines.

The mapping is deterministic so that every generated dataset
can consistently refer to the same machine.
"""

equipment_ids = [
    f"CNC-{i:02d}"
    for i in range(1, NUM_EQUIPMENT + 1)
]

df["equipment_id"] = [
    equipment_ids[i % NUM_EQUIPMENT]
    for i in range(len(df))
]


# ============================================================
# 7. CREATE SYNTHETIC TIMESTAMP
# ============================================================

"""
AI4I does not contain timestamps.

For this project we create a synthetic operational timeline.

One observation represents one production batch/event.

The timestamp is synthetic and must NOT be interpreted as
real historical AI4I timing information.
"""

start_timestamp = pd.Timestamp("2025-01-01 06:00:00")

df["timestamp"] = (
    start_timestamp
    + pd.to_timedelta(
        np.arange(len(df)) * 2,
        unit="h"
    )
)


# ============================================================
# 8. EQUIPMENT MASTER DATASET
# ============================================================

print("\n" + "=" * 70)
print("CREATING EQUIPMENT DATASET")
print("=" * 70)

equipment_rows = []

for equipment_id in equipment_ids:

    machine_data = df[
        df["equipment_id"] == equipment_id
    ]

    # Product type most frequently processed by this machine
    dominant_product_type = (
        machine_data["Type"]
        .mode()
        .iloc[0]
    )

    avg_speed = machine_data[
        "Rotational speed [rpm]"
    ].mean()

    avg_torque = machine_data[
        "Torque [Nm]"
    ].mean()

    equipment_rows.append({

        "equipment_id": equipment_id,

        "equipment_name":
            f"CNC Production Machine {equipment_id.split('-')[1]}",

        "equipment_type":
            "CNC Production Machine",

        "primary_product_type":
            dominant_product_type,

        "installation_year":
            int(
                rng.choice(
                    [2019, 2020, 2021, 2022, 2023]
                )
            ),

        "location":
            rng.choice(
                [
                    "Production-Line-A",
                    "Production-Line-B",
                    "Production-Line-C"
                ]
            ),

        "criticality":
            rng.choice(
                ["High", "Medium", "Low"],
                p=[0.30, 0.50, 0.20]
            ),

        # These are synthetic baseline/rated values
        # based on observed AI4I operating values.
        "rated_speed_rpm":
            round(avg_speed, 0),

        "rated_torque_nm":
            round(avg_torque, 2),

        "maintenance_interval_hours":
            int(
                rng.choice(
                    [400, 500, 600, 750]
                )
            )
    })


df_equipment = pd.DataFrame(equipment_rows)

equipment_file = PROCESSED_DIR / "equipment.csv"

df_equipment.to_csv(
    equipment_file,
    index=False
)

print(f"Created: {equipment_file}")
print(f"Rows   : {len(df_equipment)}")


# ============================================================
# 9. PRODUCTION DATASET
# ============================================================

print("\n" + "=" * 70)
print("CREATING PRODUCTION DATASET")
print("=" * 70)

df_production = pd.DataFrame()

df_production["batch_id"] = [
    f"BAT-{10000 + i}"
    for i in range(len(df))
]

df_production["timestamp"] = df["timestamp"]

df_production["equipment_id"] = df["equipment_id"]

df_production["udi"] = df["UDI"]

df_production["product_id"] = df["Product ID"]

df_production["product_type"] = df["Type"]


# ------------------------------------------------------------
# Shift
# ------------------------------------------------------------

hour = df["timestamp"].dt.hour

df_production["shift"] = np.select(
    [
        hour < 14,
        hour < 22
    ],
    [
        "Morning",
        "Evening"
    ],
    default="Night"
)


# ------------------------------------------------------------
# AI4I operating parameters
# ------------------------------------------------------------

df_production["air_temperature_k"] = (
    df["Air temperature [K]"]
)

df_production["process_temperature_k"] = (
    df["Process temperature [K]"]
)

df_production["rotational_speed_rpm"] = (
    df["Rotational speed [rpm]"]
)

df_production["torque_nm"] = (
    df["Torque [Nm]"]
)

df_production["tool_wear_min"] = (
    df["Tool wear [min]"]
)

df_production["machine_failure"] = (
    df["Machine failure"]
)


# ------------------------------------------------------------
# Synthetic operating duration
# ------------------------------------------------------------

"""
Each production observation is assigned a synthetic operating
duration.

This is intentionally independent of tool wear.

Tool wear represents accumulated tool usage in AI4I.
It is NOT used as operating duration.
"""

operating_duration_min = rng.uniform(
    30,
    90,
    len(df)
)

# Failed machines tend to have less productive operating time
operating_duration_min = np.where(
    df["Machine failure"].values == 1,
    operating_duration_min * rng.uniform(
        0.50,
        0.80,
        len(df)
    ),
    operating_duration_min
)

operating_duration_min = np.round(
    operating_duration_min,
    2
)

df_production["operating_duration_min"] = (
    operating_duration_min
)


# ------------------------------------------------------------
# Synthetic downtime
# ------------------------------------------------------------

normal_downtime = rng.uniform(
    0,
    5,
    len(df)
)

failure_downtime = rng.uniform(
    30,
    180,
    len(df)
)

df_production["downtime_min"] = np.where(
    df["Machine failure"].values == 1,
    failure_downtime,
    normal_downtime
)

df_production["downtime_min"] = (
    df_production["downtime_min"].round(2)
)


# ------------------------------------------------------------
# Synthetic production quantity
# ------------------------------------------------------------

"""
Production quantity is influenced by:

    - rotational speed
    - torque
    - downtime
    - machine failure

This creates useful relationships for later SQL/Python analysis.
"""

speed_effect = (
    df["Rotational speed [rpm]"] / 1500
)

torque_effect = (
    1
    - 0.003
    * np.abs(df["Torque [Nm]"] - 40)
)

availability = (
    1
    - df_production["downtime_min"]
    / 240
)

failure_penalty = np.where(
    df["Machine failure"] == 1,
    0.70,
    1.0
)

base_rate = 1.65

production_quantity = (
    base_rate
    * operating_duration_min
    * speed_effect
    * torque_effect
    * availability
    * failure_penalty
)

# Add realistic process variation
production_quantity += rng.normal(
    0,
    3,
    len(df)
)

production_quantity = np.maximum(
    production_quantity,
    0
)

df_production["production_qty"] = (
    np.round(production_quantity, 1)
)


# ------------------------------------------------------------
# Cycle time
# ------------------------------------------------------------

df_production["cycle_time_sec"] = np.round(
    (
        operating_duration_min * 60
        / np.maximum(
            production_quantity,
            1
        )
    ),
    2
)

# ------------------------------------------------------------
# Operating status
# ------------------------------------------------------------

df_production["operating_status"] = np.where(
    df["Machine failure"] == 1,
    "Failure",
    "Running"
)


production_file = (
    PROCESSED_DIR / "production.csv"
)

df_production.to_csv(
    production_file,
    index=False
)

print(f"Created: {production_file}")
print(f"Rows   : {len(df_production):,}")


# ============================================================
# 10. MAINTENANCE DATASET
# ============================================================

print("\n" + "=" * 70)
print("CREATING MAINTENANCE DATASET")
print("=" * 70)

maintenance_records = []

maintenance_counter = 1


# ------------------------------------------------------------
# Corrective maintenance
# ------------------------------------------------------------

failure_rows = df[
    df["Machine failure"] == 1
]

failure_columns = [
    "TWF",
    "HDF",
    "PWF",
    "OSF",
    "RNF"
]

for index, row in failure_rows.iterrows():

    active_modes = [
        mode
        for mode in failure_columns
        if row[mode] == 1
    ]

    if active_modes:
        failure_mode = active_modes[0]
    else:
        failure_mode = "GENERAL_FAILURE"

    severity_map = {
        "TWF": "Medium",
        "HDF": "High",
        "PWF": "High",
        "OSF": "High",
        "RNF": "Medium",
        "GENERAL_FAILURE": "High"
    }

    maintenance_records.append({

        "maintenance_id":
            f"MNT-{maintenance_counter:05d}",

        "timestamp":
            row["timestamp"]
            + pd.Timedelta(
                minutes=int(
                    rng.integers(5, 120)
                )
            ),

        "equipment_id":
            row["equipment_id"],

        "maintenance_type":
            "Corrective",

        "failure_mode":
            failure_mode,

        "severity":
            severity_map[failure_mode],

        "tool_wear_min":
            row["Tool wear [min]"],

        "downtime_min":
            round(
                rng.uniform(45, 180),
                2
            ),

        "technician_team":
            rng.choice(
                [
                    "Maintenance-Team-A",
                    "Maintenance-Team-B",
                    "Maintenance-Team-C"
                ]
            ),

        "parts_replaced":
            rng.choice(
                [
                    "Cutting Tool",
                    "Bearing",
                    "Motor Component",
                    "Cooling Component",
                    "Electrical Component"
                ]
            ),

        "maintenance_status":
            "Completed"
    })

    maintenance_counter += 1


# ------------------------------------------------------------
# Preventive maintenance
# ------------------------------------------------------------

"""
Preventive maintenance is generated for high tool-wear
observations.

We sample a subset so that we don't create an event for
every high-wear observation.
"""

preventive_candidates = df[
    (df["Tool wear [min]"] >= 180)
    & (df["Machine failure"] == 0)
]

# Approximately 35% of eligible high-wear observations
for index, row in preventive_candidates.iterrows():

    if rng.random() > 0.35:
        continue

    maintenance_records.append({

        "maintenance_id":
            f"MNT-{maintenance_counter:05d}",

        "timestamp":
            row["timestamp"]
            + pd.Timedelta(
                minutes=int(
                    rng.integers(10, 90)
                )
            ),

        "equipment_id":
            row["equipment_id"],

        "maintenance_type":
            "Preventive",

        "failure_mode":
            "TOOL_WEAR_RISK",

        "severity":
            "Medium",

        "tool_wear_min":
            row["Tool wear [min]"],

        "downtime_min":
            round(
                rng.uniform(15, 60),
                2
            ),

        "technician_team":
            rng.choice(
                [
                    "Maintenance-Team-A",
                    "Maintenance-Team-B",
                    "Maintenance-Team-C"
                ]
            ),

        "parts_replaced":
            "Cutting Tool",

        "maintenance_status":
            "Completed"
    })

    maintenance_counter += 1


df_maintenance = pd.DataFrame(
    maintenance_records
)

if not df_maintenance.empty:
    df_maintenance = (
        df_maintenance
        .sort_values("timestamp")
        .reset_index(drop=True)
    )


maintenance_file = (
    PROCESSED_DIR / "maintenance.csv"
)

df_maintenance.to_csv(
    maintenance_file,
    index=False
)

print(f"Created: {maintenance_file}")
print(f"Rows   : {len(df_maintenance):,}")


# ============================================================
# 11. QUALITY DATASET
# ============================================================

print("\n" + "=" * 70)
print("CREATING QUALITY DATASET")
print("=" * 70)

"""
Quality is synthetic.

It is influenced by:

    - temperature deviation
    - rotational speed deviation
    - torque deviation
    - tool wear
    - machine failure

The generated quality values are NOT measurements from AI4I.
"""

temperature_difference = (
    df["Process temperature [K]"]
    - df["Air temperature [K]"]
)

temperature_deviation = np.abs(
    temperature_difference - 10
)

speed_deviation = np.abs(
    df["Rotational speed [rpm]"] - 1500
)

torque_deviation = np.abs(
    df["Torque [Nm]"] - 40
)

tool_wear_effect = np.maximum(
    df["Tool wear [min]"] - 160,
    0
)


# ------------------------------------------------------------
# Defect score
# ------------------------------------------------------------

defect_score = (

    0.12 * temperature_deviation

    + 0.004 * speed_deviation

    + 0.012 * torque_deviation

    + 0.004 * tool_wear_effect

    + 0.85 * df["Machine failure"]

    + rng.normal(
        0,
        0.18,
        len(df)
    )
)

defect_score = np.maximum(
    defect_score,
    0
)


# ------------------------------------------------------------
# Dimension error
# ------------------------------------------------------------

dimension_error = (

    0.04

    + 0.004
    * torque_deviation

    + 0.0008
    * df["Tool wear [min]"]

    + 0.06
    * df["Machine failure"]

    + rng.normal(
        0,
        0.012,
        len(df)
)

)

dimension_error = np.clip(
    dimension_error,
    0.005,
    0.50
)


# ------------------------------------------------------------
# Surface quality
# ------------------------------------------------------------

surface_quality = (

    99

    - 3.5 * defect_score

    + rng.normal(
        0,
        0.7,
        len(df)
    )
)

surface_quality = np.clip(
    surface_quality,
    60,
    100
)


# ------------------------------------------------------------
# Quality status
# ------------------------------------------------------------

quality_status = np.select(

    [
        defect_score >= 1.8,
        defect_score >= 1.0
    ],

    [
        "Rejected",
        "Review"
    ],

    default="Accepted"
)


df_quality = pd.DataFrame({

    "inspection_id": [
        f"QC-{30000 + i}"
        for i in range(len(df))
    ],

    "timestamp":
        df["timestamp"]
        + pd.to_timedelta(
            rng.integers(
                1,
                10,
                len(df)
            ),
            unit="m"
        ),

    "equipment_id":
        df["equipment_id"],

    "batch_id":
        df_production["batch_id"],

    "product_id":
        df["Product ID"],

    "defect_score":
        np.round(
            defect_score,
            3
        ),

    "dimension_error_mm":
        np.round(
            dimension_error,
            3
        ),

    "surface_quality_index":
        np.round(
            surface_quality,
            2
        ),

    "quality_status":
        quality_status
})


quality_file = (
    PROCESSED_DIR / "quality.csv"
)

df_quality.to_csv(
    quality_file,
    index=False
)

print(f"Created: {quality_file}")
print(f"Rows   : {len(df_quality):,}")


# ============================================================
# 12. ENERGY DATASET
# ============================================================

print("\n" + "=" * 70)
print("CREATING ENERGY DATASET")
print("=" * 70)

"""
Mechanical power approximation:

Power(kW)
    =
Torque(Nm) × Rotational Speed(rpm)
---------------------------------
             9550

Energy:

Energy(kWh)
    =
Power(kW) × Operating Time(hours)

We intentionally DO NOT use Tool Wear as operating duration.
"""


# ------------------------------------------------------------
# Mechanical power
# ------------------------------------------------------------

mechanical_power_kw = (

    df["Torque [Nm]"]
    * df["Rotational speed [rpm]"]

) / 9550


# ------------------------------------------------------------
# Synthetic electrical efficiency
# ------------------------------------------------------------

efficiency = rng.uniform(
    0.82,
    0.94,
    len(df)
)


# Electrical power slightly higher than mechanical power
electrical_power_kw = (
    mechanical_power_kw
    / efficiency
)


# ------------------------------------------------------------
# Energy consumption
# ------------------------------------------------------------

energy_kwh = (

    electrical_power_kw
    * df_production["operating_duration_min"]
    / 60

)


# Small measurement noise
energy_kwh *= (
    1
    + rng.normal(
        0,
        0.03,
        len(df)
    )
)

energy_kwh = np.maximum(
    energy_kwh,
    0
)


# ------------------------------------------------------------
# Specific energy
# ------------------------------------------------------------

production_qty = (
    df_production["production_qty"]
)

specific_energy = (
    energy_kwh
    / np.maximum(
        production_qty,
        1
    )
)


# ------------------------------------------------------------
# Energy status
# ------------------------------------------------------------

high_threshold = (
    specific_energy.quantile(0.90)
)

critical_threshold = (
    specific_energy.quantile(0.98)
)

energy_status = np.select(

    [
        specific_energy >= critical_threshold,
        specific_energy >= high_threshold
    ],

    [
        "Critical Consumption",
        "High Consumption"
    ],

    default="Normal"
)


df_energy = pd.DataFrame({

    "energy_id": [
        f"NRG-{40000 + i}"
        for i in range(len(df))
    ],

    "timestamp":
        df["timestamp"],

    "equipment_id":
        df["equipment_id"],

    "batch_id":
        df_production["batch_id"],

    "power_kw":
        np.round(
            electrical_power_kw,
            3
        ),

    "operating_duration_min":
        df_production[
            "operating_duration_min"
        ],

    "energy_kwh":
        np.round(
            energy_kwh,
            3
        ),

    "production_qty":
        production_qty,

    "specific_energy_kwh_per_unit":
        np.round(
            specific_energy,
            5
        ),

    "energy_status":
        energy_status
})


energy_file = (
    PROCESSED_DIR / "energy.csv"
)

df_energy.to_csv(
    energy_file,
    index=False
)

print(f"Created: {energy_file}")
print(f"Rows   : {len(df_energy):,}")


# ============================================================
# 13. DATASET RELATIONSHIP VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("VALIDATING DATA RELATIONSHIPS")
print("=" * 70)


# Equipment IDs
equipment_set = set(
    df_equipment["equipment_id"]
)

production_equipment_set = set(
    df_production["equipment_id"]
)

quality_equipment_set = set(
    df_quality["equipment_id"]
)

energy_equipment_set = set(
    df_energy["equipment_id"]
)

maintenance_equipment_set = set(
    df_maintenance["equipment_id"]
)


print(
    "Production equipment FK:",
    production_equipment_set.issubset(
        equipment_set
    )
)

print(
    "Quality equipment FK:",
    quality_equipment_set.issubset(
        equipment_set
    )
)

print(
    "Energy equipment FK:",
    energy_equipment_set.issubset(
        equipment_set
    )
)

print(
    "Maintenance equipment FK:",
    maintenance_equipment_set.issubset(
        equipment_set
    )
)


# Production -> Quality
production_batches = set(
    df_production["batch_id"]
)

quality_batches = set(
    df_quality["batch_id"]
)

print(
    "Quality -> Production FK:",
    quality_batches.issubset(
        production_batches
    )
)


# Production -> Energy
energy_batches = set(
    df_energy["batch_id"]
)

print(
    "Energy -> Production FK:",
    energy_batches.issubset(
        production_batches
    )
)


# ============================================================
# 14. DATASET SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("DATASET SUMMARY")
print("=" * 70)

summary = pd.DataFrame({

    "dataset": [
        "equipment",
        "production",
        "maintenance",
        "quality",
        "energy"
    ],

    "rows": [
        len(df_equipment),
        len(df_production),
        len(df_maintenance),
        len(df_quality),
        len(df_energy)
    ],

    "columns": [
        len(df_equipment.columns),
        len(df_production.columns),
        len(df_maintenance.columns),
        len(df_quality.columns),
        len(df_energy.columns)
    ]
})

print(
    summary.to_string(
        index=False
    )
)


# ============================================================
# 15. ADD DATA DICTIONARY
# ============================================================

data_dictionary = pd.DataFrame({

    "dataset": [

        "equipment.csv",
        "production.csv",
        "maintenance.csv",
        "quality.csv",
        "energy.csv"

    ],

    "description": [

        "Synthetic equipment master data.",

        "Synthetic production events derived from AI4I operating parameters.",

        "Synthetic preventive and corrective maintenance events.",

        "Synthetic quality inspection results.",

        "Synthetic energy consumption and specific energy metrics."

    ],

    "source": [

        "AI4I + synthetic assumptions",
        "AI4I + synthetic assumptions",
        "AI4I failure/wear signals + synthetic assumptions",
        "AI4I operating parameters + synthetic assumptions",
        "AI4I operating parameters + synthetic assumptions"

    ]
})

data_dictionary_file = (
    PROCESSED_DIR / "data_dictionary.csv"
)

data_dictionary.to_csv(
    data_dictionary_file,
    index=False
)


# ============================================================
# 16. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("DATA GENERATION COMPLETED")
print("=" * 70)

print(
    f"\nGenerated files are available in:\n"
    f"{PROCESSED_DIR}"
)

print("\nFiles:")

for file in PROCESSED_DIR.iterdir():

    if file.is_file():

        print(
            f"  - {file.name}"
        )

print("\nIMPORTANT:")
print(
    "ai4i2020.csv remains unchanged. "
    "All generated datasets are synthetic."
)