from pathlib import Path

import pandas as pd
from psycopg2.extras import execute_values

from app.database.connection import get_connection


# Project root:
# D:\Operation_copilot
PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def load_dataframe(
    cursor,
    df: pd.DataFrame,
    table_name: str,
    columns: list[str],
):
    """
    Insert a DataFrame into a PostgreSQL table.
    """

    # Keep only the columns required by the database table.
    df = df[columns].copy()

    # Convert pandas NaN values to Python None.
    # PostgreSQL understands None as SQL NULL.
    df = df.where(pd.notnull(df), None)

    values = [tuple(row) for row in df.itertuples(index=False, name=None)]

    column_names = ", ".join(columns)

    query = f"""
        INSERT INTO {table_name} ({column_names})
        VALUES %s
    """

    execute_values(
        cursor,
        query,
        values,
        page_size=1000,
    )

    print(f"{table_name:<15} {len(df):>6} rows loaded.")


def load_all_data():
    """
    Load all processed CSV datasets into PostgreSQL.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # ---------------------------------------------------------
        # 1. EQUIPMENT
        # ---------------------------------------------------------

        equipment_file = PROCESSED_DATA_DIR / "equipment.csv"

        equipment_df = pd.read_csv(equipment_file)

        equipment_columns = [
            "equipment_id",
            "equipment_name",
            "equipment_type",
            "primary_product_type",
            "installation_year",
            "location",
            "criticality",
            "rated_speed_rpm",
            "rated_torque_nm",
            "maintenance_interval_hours",
        ]

        load_dataframe(
            cursor,
            equipment_df,
            "equipment",
            equipment_columns,
        )

        # ---------------------------------------------------------
        # 2. PRODUCTION
        # ---------------------------------------------------------

        production_file = PROCESSED_DATA_DIR / "production.csv"

        production_df = pd.read_csv(
            production_file,
            parse_dates=["timestamp"],
        )

        production_columns = [
            "batch_id",
            "timestamp",
            "equipment_id",
            "udi",
            "product_id",
            "product_type",
            "shift",
            "air_temperature_k",
            "process_temperature_k",
            "rotational_speed_rpm",
            "torque_nm",
            "tool_wear_min",
            "machine_failure",
            "operating_duration_min",
            "downtime_min",
            "production_qty",
            "cycle_time_sec",
            "operating_status",
        ]

        load_dataframe(
            cursor,
            production_df,
            "production",
            production_columns,
        )

        # ---------------------------------------------------------
        # 3. MAINTENANCE
        # ---------------------------------------------------------

        maintenance_file = PROCESSED_DATA_DIR / "maintenance.csv"

        maintenance_df = pd.read_csv(
            maintenance_file,
            parse_dates=["timestamp"],
        )

        maintenance_columns = [
            "maintenance_id",
            "timestamp",
            "equipment_id",
            "maintenance_type",
            "failure_mode",
            "severity",
            "tool_wear_min",
            "downtime_min",
            "technician_team",
            "parts_replaced",
            "maintenance_status",
        ]

        load_dataframe(
            cursor,
            maintenance_df,
            "maintenance",
            maintenance_columns,
        )

        # ---------------------------------------------------------
        # 4. QUALITY
        # ---------------------------------------------------------

        quality_file = PROCESSED_DATA_DIR / "quality.csv"

        quality_df = pd.read_csv(
            quality_file,
            parse_dates=["timestamp"],
        )

        quality_columns = [
            "inspection_id",
            "timestamp",
            "equipment_id",
            "batch_id",
            "product_id",
            "defect_score",
            "dimension_error_mm",
            "surface_quality_index",
            "quality_status",
        ]

        load_dataframe(
            cursor,
            quality_df,
            "quality",
            quality_columns,
        )

        # ---------------------------------------------------------
        # 5. ENERGY
        # ---------------------------------------------------------

        energy_file = PROCESSED_DATA_DIR / "energy.csv"

        energy_df = pd.read_csv(
            energy_file,
            parse_dates=["timestamp"],
        )

        energy_columns = [
            "energy_id",
            "timestamp",
            "equipment_id",
            "batch_id",
            "power_kw",
            "operating_duration_min",
            "energy_kwh",
            "production_qty",
            "specific_energy_kwh_per_unit",
            "energy_status",
        ]

        load_dataframe(
            cursor,
            energy_df,
            "energy",
            energy_columns,
        )

        # Commit only after all five datasets are loaded successfully.
        conn.commit()

        print()
        print("All datasets loaded successfully.")

    except Exception as e:

        # If any dataset fails, undo the entire transaction.
        conn.rollback()

        print()
        print("Data loading failed.")
        print(f"Error: {e}")

        raise

    finally:

        cursor.close()
        conn.close()


if __name__ == "__main__":
    load_all_data()