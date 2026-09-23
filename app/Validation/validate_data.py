from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


# ============================================================
# EXPECTED SCHEMAS
# ============================================================

EXPECTED_SCHEMAS = {
    "equipment.csv": [
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
    ],

    "production.csv": [
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
    ],

    "maintenance.csv": [
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
    ],

    "quality.csv": [
        "inspection_id",
        "timestamp",
        "equipment_id",
        "batch_id",
        "product_id",
        "defect_score",
        "dimension_error_mm",
        "surface_quality_index",
        "quality_status",
    ],

    "energy.csv": [
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
    ],
}


# ============================================================
# PRIMARY KEYS
# ============================================================

PRIMARY_KEYS = {
    "equipment.csv": "equipment_id",
    "production.csv": "batch_id",
    "maintenance.csv": "maintenance_id",
    "quality.csv": "inspection_id",
    "energy.csv": "energy_id",
}


# ============================================================
# NON-NEGATIVE NUMERIC COLUMNS
# ============================================================

NON_NEGATIVE_COLUMNS = {
    "equipment.csv": [
        "installation_year",
        "rated_speed_rpm",
        "rated_torque_nm",
        "maintenance_interval_hours",
    ],

    "production.csv": [
        "air_temperature_k",
        "process_temperature_k",
        "rotational_speed_rpm",
        "torque_nm",
        "tool_wear_min",
        "operating_duration_min",
        "downtime_min",
        "production_qty",
        "cycle_time_sec",
    ],

    "maintenance.csv": [
        "tool_wear_min",
        "downtime_min",
    ],

    "quality.csv": [
        "defect_score",
        "dimension_error_mm",
        "surface_quality_index",
    ],

    "energy.csv": [
        "power_kw",
        "operating_duration_min",
        "energy_kwh",
        "production_qty",
        "specific_energy_kwh_per_unit",
    ],
}


# ============================================================
# TIMESTAMP COLUMNS
# ============================================================

TIMESTAMP_COLUMNS = {
    "production.csv": "timestamp",
    "maintenance.csv": "timestamp",
    "quality.csv": "timestamp",
    "energy.csv": "timestamp",
}


# ============================================================
# VALIDATOR CLASS
# ============================================================

class IndustrialDataValidator:

    def __init__(self, data_dir):

        self.data_dir = Path(data_dir)

        self.datasets = {}

        self.overall_pass = True

        self.output_lines = []

    # ========================================================
    # LOGGING
    # ========================================================

    def log(self, message=""):

        print(message)

        self.output_lines.append(message)

    # ========================================================
    # FILE EXISTENCE
    # ========================================================

    def validate_file_existence(self):

        self.log("\n" + "=" * 70)
        self.log("FILE EXISTENCE VALIDATION")
        self.log("=" * 70)

        all_files_exist = True

        for filename in EXPECTED_SCHEMAS:

            filepath = self.data_dir / filename

            if filepath.exists():

                self.log(f"{filename:<25} PASS")

            else:

                self.log(f"{filename:<25} FAIL - FILE NOT FOUND")

                all_files_exist = False
                self.overall_pass = False

        return all_files_exist

    # ========================================================
    # LOAD DATASETS
    # ========================================================

    def load_datasets(self):

        self.log("\n" + "=" * 70)
        self.log("LOADING DATASETS")
        self.log("=" * 70)

        for filename in EXPECTED_SCHEMAS:

            filepath = self.data_dir / filename

            if not filepath.exists():
                continue

            try:

                df = pd.read_csv(filepath)

                self.datasets[filename] = df

                self.log(
                    f"{filename:<25} "
                    f"Rows: {len(df):>7,} | "
                    f"Columns: {len(df.columns):>3}"
                )

            except Exception as e:

                self.log(
                    f"{filename:<25} FAIL - {e}"
                )

                self.overall_pass = False

    # ========================================================
    # SCHEMA VALIDATION
    # ========================================================

    def validate_schema(self):

        self.log("\n" + "=" * 70)
        self.log("SCHEMA VALIDATION")
        self.log("=" * 70)

        for filename, expected_columns in EXPECTED_SCHEMAS.items():

            if filename not in self.datasets:
                continue

            df = self.datasets[filename]

            actual_columns = list(df.columns)

            missing_columns = [
                col
                for col in expected_columns
                if col not in actual_columns
            ]

            unexpected_columns = [
                col
                for col in actual_columns
                if col not in expected_columns
            ]

            if not missing_columns and not unexpected_columns:

                self.log(
                    f"{filename:<25} PASS"
                )

            else:

                self.log(
                    f"{filename:<25} FAIL"
                )

                if missing_columns:

                    self.log(
                        f"  Missing columns: {missing_columns}"
                    )

                if unexpected_columns:

                    self.log(
                        f"  Unexpected columns: {unexpected_columns}"
                    )

                self.overall_pass = False

    # ========================================================
    # MISSING VALUE VALIDATION
    # ========================================================

    def validate_missing_values(self):

        self.log("\n" + "=" * 70)
        self.log("MISSING VALUE VALIDATION")
        self.log("=" * 70)

        for filename, df in self.datasets.items():

            missing_count = int(df.isna().sum().sum())

            if missing_count == 0:

                self.log(
                    f"{filename:<25} PASS"
                )

            else:

                self.log(
                    f"{filename:<25} FAIL - "
                    f"{missing_count} missing values"
                )

                missing_by_column = (
                    df.isna()
                    .sum()
                )

                for column, count in missing_by_column.items():

                    if count > 0:

                        self.log(
                            f"  {column}: {count}"
                        )

                self.overall_pass = False

    # ========================================================
    # PRIMARY KEY VALIDATION
    # ========================================================

    def validate_primary_keys(self):

        self.log("\n" + "=" * 70)
        self.log("PRIMARY KEY VALIDATION")
        self.log("=" * 70)

        for filename, primary_key in PRIMARY_KEYS.items():

            if filename not in self.datasets:
                continue

            df = self.datasets[filename]

            if primary_key not in df.columns:

                self.log(
                    f"{filename:<25} FAIL - "
                    f"Primary key '{primary_key}' missing"
                )

                self.overall_pass = False

                continue

            duplicate_count = int(
                df[primary_key]
                .duplicated()
                .sum()
            )

            null_count = int(
                df[primary_key]
                .isna()
                .sum()
            )

            if duplicate_count == 0 and null_count == 0:

                self.log(
                    f"{filename:<25} PASS"
                )

            else:

                self.log(
                    f"{filename:<25} FAIL"
                )

                if duplicate_count > 0:

                    self.log(
                        f"  Duplicate keys: {duplicate_count}"
                    )

                if null_count > 0:

                    self.log(
                        f"  Null keys: {null_count}"
                    )

                self.overall_pass = False

    # ========================================================
    # FOREIGN KEY VALIDATION
    # ========================================================

    def validate_foreign_keys(self):

        self.log("\n" + "=" * 70)
        self.log("FOREIGN KEY VALIDATION")
        self.log("=" * 70)

        # ----------------------------------------------------
        # Equipment references
        # ----------------------------------------------------

        if (
            "equipment.csv" in self.datasets
            and "equipment_id" in self.datasets["equipment.csv"].columns
        ):

            equipment_ids = set(
                self.datasets["equipment.csv"]["equipment_id"]
            )

            for filename in [
                "production.csv",
                "maintenance.csv",
                "quality.csv",
                "energy.csv",
            ]:

                if filename not in self.datasets:
                    continue

                if "equipment_id" not in self.datasets[filename].columns:
                    continue

                invalid_ids = set(
                    self.datasets[filename]["equipment_id"]
                ) - equipment_ids

                if len(invalid_ids) == 0:

                    self.log(
                        f"{filename:<25} Equipment FK PASS"
                    )

                else:

                    self.log(
                        f"{filename:<25} Equipment FK FAIL"
                    )

                    self.log(
                        f"  Invalid equipment IDs: "
                        f"{list(invalid_ids)[:10]}"
                    )

                    self.overall_pass = False

        # ----------------------------------------------------
        # Batch references
        # ----------------------------------------------------

        if (
            "production.csv" in self.datasets
            and "batch_id" in self.datasets["production.csv"].columns
        ):

            batch_ids = set(
                self.datasets["production.csv"]["batch_id"]
            )

            for filename in [
                "quality.csv",
                "energy.csv",
            ]:

                if filename not in self.datasets:
                    continue

                if "batch_id" not in self.datasets[filename].columns:
                    continue

                invalid_batches = set(
                    self.datasets[filename]["batch_id"]
                ) - batch_ids

                if len(invalid_batches) == 0:

                    self.log(
                        f"{filename:<25} Batch FK PASS"
                    )

                else:

                    self.log(
                        f"{filename:<25} Batch FK FAIL"
                    )

                    self.log(
                        f"  Invalid batch IDs: "
                        f"{list(invalid_batches)[:10]}"
                    )

                    self.overall_pass = False

    # ========================================================
    # NUMERIC RANGE VALIDATION
    # ========================================================

    def validate_value_ranges(self):

        self.log("\n" + "=" * 70)
        self.log("VALUE RANGE VALIDATION")
        self.log("=" * 70)

        for filename, columns in NON_NEGATIVE_COLUMNS.items():

            if filename not in self.datasets:
                continue

            df = self.datasets[filename]

            file_pass = True

            for column in columns:

                if column not in df.columns:
                    continue

                numeric_values = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

                invalid_count = int(
                    (numeric_values < 0)
                    .sum()
                )

                if invalid_count > 0:

                    file_pass = False

                    self.log(
                        f"  {filename} -> {column}: "
                        f"{invalid_count} negative values"
                    )

            if file_pass:

                self.log(
                    f"{filename:<25} PASS"
                )

            else:

                self.log(
                    f"{filename:<25} FAIL"
                )

                self.overall_pass = False

    # ========================================================
    # TIMESTAMP VALIDATION
    # ========================================================

    def validate_timestamps(self):

        self.log("\n" + "=" * 70)
        self.log("TIMESTAMP VALIDATION")
        self.log("=" * 70)

        for filename, timestamp_column in TIMESTAMP_COLUMNS.items():

            if filename not in self.datasets:
                continue

            df = self.datasets[filename]

            parsed_timestamp = pd.to_datetime(
                df[timestamp_column],
                errors="coerce"
            )

            invalid_count = int(
                parsed_timestamp.isna().sum()
            )

            if invalid_count == 0:

                self.log(
                    f"{filename:<25} PASS"
                )

            else:

                self.log(
                    f"{filename:<25} FAIL - "
                    f"{invalid_count} invalid timestamps"
                )

                self.overall_pass = False

    # ========================================================
    # ENERGY VALIDATION
    # ========================================================

    def validate_energy(self):

        self.log("\n" + "=" * 70)
        self.log("BUSINESS / INDUSTRIAL RULE VALIDATION")
        self.log("=" * 70)

        if "energy.csv" not in self.datasets:

            self.log(
                "energy.csv               SKIPPED"
            )

            return

        df = self.datasets["energy.csv"].copy()

    # ----------------------------------------------------
    # Theoretical energy:
    #
    # energy_kwh =
    # power_kw * operating_duration_min / 60
    #
    # create_data.py intentionally adds approximately
    # 3% Gaussian measurement noise.
    # ----------------------------------------------------

        expected_energy = (
            df["power_kw"]
            * df["operating_duration_min"]
            / 60.0
        )

        absolute_difference = (
            df["energy_kwh"]
            - expected_energy
        ).abs()

        relative_error = (
            absolute_difference
            / expected_energy.replace(0, np.nan)
        )

        mean_relative_error = float(
            relative_error.mean()
        )

        median_relative_error = float(
            relative_error.median()
        )

        percentile_95 = float(
            relative_error.quantile(0.95)
        )

        maximum_relative_error = float(
            relative_error.max()
        )

        # ----------------------------------------------------
        # Validation criteria
        #
        # Mean error <= 5%
        # 95th percentile <= 10%
        #
        # We intentionally do NOT use maximum error because
        # Gaussian measurement noise can produce occasional
        # larger individual deviations.
        # ----------------------------------------------------

        if (
            mean_relative_error <= 0.05
            and percentile_95 <= 0.10
        ):

            self.log(
                "Energy Physics Rule      : PASS"
            )

            self.log(
                f"  Mean relative error    : "
                f"{mean_relative_error:.2%}"
            )

            self.log(
                f"  Median relative error  : "
                f"{median_relative_error:.2%}"
            )

            self.log(
                f"  95th percentile error  : "
                f"{percentile_95:.2%}"
            )

            self.log(
                f"  Maximum relative error : "
                f"{maximum_relative_error:.2%}"
            )

        else:

            self.log(
                "Energy Physics Rule      : FAIL"
            )

            self.log(
                f"  Mean relative error    : "
                f"{mean_relative_error:.2%}"
            )

            self.log(
                f"  Median relative error  : "
                f"{median_relative_error:.2%}"
            )

            self.log(
                f"  95th percentile error  : "
                f"{percentile_95:.2%}"
            )

            self.log(
                f"  Maximum relative error : "
                f"{maximum_relative_error:.2%}"
            )

            self.overall_pass = False
    # ========================================================
    # SPECIFIC ENERGY VALIDATION
    # ========================================================

    def validate_specific_energy(self):

        if "energy.csv" not in self.datasets:

            return

        df = self.datasets["energy.csv"].copy()

        # ----------------------------------------------------
        # Generator definition:
        #
        # specific_energy =
        # energy_kwh / max(production_qty, 1)
        #
        # production_qty is clipped to >= 0 during generation.
        # ----------------------------------------------------

        expected_specific_energy = (
            df["energy_kwh"]
            / df["production_qty"].clip(lower=1)
        )

        difference = (
            df["specific_energy_kwh_per_unit"]
            - expected_specific_energy
        ).abs()

        max_difference = float(
            difference.max()
        )

        mean_difference = float(
            difference.mean()
        )

        # Because energy is saved rounded to 3 decimals
        # and specific energy to 5 decimals, a very small
        # difference is expected.
        tolerance = 0.01

        if max_difference <= tolerance:

            self.log(
                "Specific Energy Rule     : PASS"
            )

            self.log(
                f"  Maximum difference     : "
                f"{max_difference:.6f}"
            )

            self.log(
                f"  Mean difference        : "
                f"{mean_difference:.6f}"
            )

        else:

            self.log(
                "Specific Energy Rule     : FAIL"
            )

            self.log(
                f"  Maximum difference     : "
                f"{max_difference:.6f}"
            )

            self.log(
                f"  Mean difference        : "
                f"{mean_difference:.6f}"
            )

            self.overall_pass = False

    # ========================================================
    # MACHINE FAILURE VALIDATION
    # ========================================================

    def validate_machine_failure(self):

        if "production.csv" not in self.datasets:

            return

        df = self.datasets["production.csv"]

        if "machine_failure" not in df.columns:

            return

        valid_values = {0, 1}

        actual_values = set(
            df["machine_failure"].dropna().unique()
        )

        invalid_values = (
            actual_values - valid_values
        )

        if len(invalid_values) == 0:

            self.log(
                "Machine Failure Rule     : PASS"
            )

        else:

            self.log(
                "Machine Failure Rule     : FAIL"
            )

            self.log(
                f"  Invalid values: {invalid_values}"
            )

            self.overall_pass = False

    # ========================================================
    # DOWNTIME VALIDATION
    # ========================================================

    def validate_downtime(self):

        if "production.csv" not in self.datasets:

            return

        df = self.datasets["production.csv"]

        if "downtime_min" not in df.columns:

            return

        negative_downtime = (
            df["downtime_min"] < 0
        ).sum()

        if negative_downtime == 0:

            self.log(
                "Downtime Rule            : PASS"
            )

        else:

            self.log(
                "Downtime Rule            : FAIL"
            )

            self.log(
                f"  Negative downtime rows: "
                f"{negative_downtime}"
            )

            self.overall_pass = False

    # ========================================================
    # FINAL RESULT
    # ========================================================

    def print_final_result(self):

        self.log("\n" + "=" * 70)
        self.log("FINAL VALIDATION RESULT")
        self.log("=" * 70)

        if self.overall_pass:

            self.log(
                "\nOVERALL RESULT: PASS"
            )

            self.log(
                "All datasets passed validation."
            )

        else:

            self.log(
                "\nOVERALL RESULT: FAIL"
            )

            self.log(
                "One or more validation rules failed."
            )

        self.log("=" * 70)

    # ========================================================
    # RUN ALL VALIDATIONS
    # ========================================================

    def run(self):

        self.validate_file_existence()

        self.load_datasets()

        self.validate_schema()

        self.validate_missing_values()

        self.validate_primary_keys()

        self.validate_foreign_keys()

        self.validate_value_ranges()

        self.validate_timestamps()

        self.validate_energy()

        self.validate_specific_energy()

        self.validate_machine_failure()

        self.validate_downtime()

        self.print_final_result()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    validator = IndustrialDataValidator(
        PROCESSED_DIR
    )

    validator.run()