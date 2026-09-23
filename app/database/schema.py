from app.database.connection import get_connection


def create_tables():
    """
    Create all PostgreSQL tables for the Industrial AI Operations Copilot.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # ---------------------------------------------------------
        # 1. EQUIPMENT TABLE
        # ---------------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS equipment (
                equipment_id VARCHAR(20) PRIMARY KEY,
                equipment_name VARCHAR(100) NOT NULL,
                equipment_type VARCHAR(50) NOT NULL,
                primary_product_type VARCHAR(20),
                installation_year INTEGER,
                location VARCHAR(100),
                criticality VARCHAR(20),
                rated_speed_rpm DOUBLE PRECISION,
                rated_torque_nm DOUBLE PRECISION,
                maintenance_interval_hours DOUBLE PRECISION
            );
            """
        )

        # ---------------------------------------------------------
        # 2. PRODUCTION TABLE
        # ---------------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS production (
                batch_id VARCHAR(50) PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                equipment_id VARCHAR(20) NOT NULL,
                udi INTEGER,
                product_id VARCHAR(50),
                product_type VARCHAR(20),
                shift VARCHAR(20),
                air_temperature_k DOUBLE PRECISION,
                process_temperature_k DOUBLE PRECISION,
                rotational_speed_rpm DOUBLE PRECISION,
                torque_nm DOUBLE PRECISION,
                tool_wear_min DOUBLE PRECISION,
                machine_failure INTEGER,
                operating_duration_min DOUBLE PRECISION,
                downtime_min DOUBLE PRECISION,
                production_qty DOUBLE PRECISION,
                cycle_time_sec DOUBLE PRECISION,
                operating_status VARCHAR(30),

                CONSTRAINT fk_production_equipment
                    FOREIGN KEY (equipment_id)
                    REFERENCES equipment(equipment_id)
            );
            """
        )

        # ---------------------------------------------------------
        # 3. MAINTENANCE TABLE
        # ---------------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS maintenance (
                maintenance_id VARCHAR(50) PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                equipment_id VARCHAR(20) NOT NULL,
                maintenance_type VARCHAR(30),
                failure_mode VARCHAR(100),
                severity VARCHAR(20),
                tool_wear_min DOUBLE PRECISION,
                downtime_min DOUBLE PRECISION,
                technician_team VARCHAR(50),
                parts_replaced TEXT,
                maintenance_status VARCHAR(30),

                CONSTRAINT fk_maintenance_equipment
                    FOREIGN KEY (equipment_id)
                    REFERENCES equipment(equipment_id)
            );
            """
        )

        # ---------------------------------------------------------
        # 4. QUALITY TABLE
        # ---------------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS quality (
                inspection_id VARCHAR(50) PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                equipment_id VARCHAR(20) NOT NULL,
                batch_id VARCHAR(50) NOT NULL,
                product_id VARCHAR(50),
                defect_score DOUBLE PRECISION,
                dimension_error_mm DOUBLE PRECISION,
                surface_quality_index DOUBLE PRECISION,
                quality_status VARCHAR(30),

                CONSTRAINT fk_quality_equipment
                    FOREIGN KEY (equipment_id)
                    REFERENCES equipment(equipment_id),

                CONSTRAINT fk_quality_batch
                    FOREIGN KEY (batch_id)
                    REFERENCES production(batch_id)
            );
            """
        )

        # ---------------------------------------------------------
        # 5. ENERGY TABLE
        # ---------------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS energy (
                energy_id VARCHAR(50) PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                equipment_id VARCHAR(20) NOT NULL,
                batch_id VARCHAR(50) NOT NULL,
                power_kw DOUBLE PRECISION,
                operating_duration_min DOUBLE PRECISION,
                energy_kwh DOUBLE PRECISION,
                production_qty DOUBLE PRECISION,
                specific_energy_kwh_per_unit DOUBLE PRECISION,
                energy_status VARCHAR(30),

                CONSTRAINT fk_energy_equipment
                    FOREIGN KEY (equipment_id)
                    REFERENCES equipment(equipment_id),

                CONSTRAINT fk_energy_batch
                    FOREIGN KEY (batch_id)
                    REFERENCES production(batch_id)
            );
            """
        )

        conn.commit()

        print("Database schema created successfully.")

    except Exception as e:
        conn.rollback()

        print("Failed to create database schema.")
        print(f"Error: {e}")

        raise

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    create_tables()