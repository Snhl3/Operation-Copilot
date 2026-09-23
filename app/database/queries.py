from app.database.connection import get_connection


def execute_query(query: str, params=None):
    """
    Execute a SQL query and return all results.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        results = cursor.fetchall()

        return results

    finally:
        cursor.close()
        conn.close()


def get_equipment_count():
    """
    Return the total number of equipment units.
    """

    query = """
        SELECT COUNT(*)
        FROM equipment;
    """

    return execute_query(query)


def get_total_production():
    """
    Return total production quantity.
    """

    query = """
        SELECT
            SUM(production_qty) AS total_production
        FROM production;
    """

    return execute_query(query)


def get_equipment_production():
    """
    Return total production by equipment.
    """

    query = """
        SELECT
            equipment_id,
            SUM(production_qty) AS total_production
        FROM production
        GROUP BY equipment_id
        ORDER BY total_production DESC;
    """

    return execute_query(query)


def get_equipment_downtime():
    """
    Return total downtime by equipment.
    """

    query = """
        SELECT
            equipment_id,
            SUM(downtime_min) AS total_downtime_min
        FROM production
        GROUP BY equipment_id
        ORDER BY total_downtime_min DESC;
    """

    return execute_query(query)


def get_equipment_failures():
    """
    Return machine failure count by equipment.
    """

    query = """
        SELECT
            equipment_id,
            SUM(machine_failure) AS failure_count
        FROM production
        GROUP BY equipment_id
        ORDER BY failure_count DESC;
    """

    return execute_query(query)


def get_maintenance_summary():
    """
    Return maintenance event count by equipment.
    """

    query = """
        SELECT
            equipment_id,
            COUNT(*) AS maintenance_events
        FROM maintenance
        GROUP BY equipment_id
        ORDER BY maintenance_events DESC;
    """

    return execute_query(query)


def get_average_quality():
    """
    Return average quality metrics.
    """

    query = """
        SELECT
            AVG(defect_score) AS average_defect_score,
            AVG(dimension_error_mm) AS average_dimension_error,
            AVG(surface_quality_index) AS average_surface_quality
        FROM quality;
    """

    return execute_query(query)


def get_equipment_energy():
    """
    Return total energy consumption by equipment.
    """

    query = """
        SELECT
            equipment_id,
            SUM(energy_kwh) AS total_energy_kwh
        FROM energy
        GROUP BY equipment_id
        ORDER BY total_energy_kwh DESC;
    """

    return execute_query(query)


def get_specific_energy_by_equipment():
    """
    Return average specific energy consumption by equipment.
    """

    query = """
        SELECT
            equipment_id,
            AVG(specific_energy_kwh_per_unit)
                AS average_specific_energy
        FROM energy
        GROUP BY equipment_id
        ORDER BY average_specific_energy DESC;
    """

    return execute_query(query)


def get_equipment_kpi():
    """
    Return a combined equipment-level KPI summary.

    Combines production, downtime, failures,
    energy consumption and quality.
    """

    query = """
        SELECT
            e.equipment_id,
            e.equipment_name,

            COALESCE(p.total_production, 0)
                AS total_production,

            COALESCE(p.total_downtime_min, 0)
                AS total_downtime_min,

            COALESCE(p.failure_count, 0)
                AS failure_count,

            COALESCE(en.total_energy_kwh, 0)
                AS total_energy_kwh,

            COALESCE(q.average_defect_score, 0)
                AS average_defect_score

        FROM equipment e

        LEFT JOIN (
            SELECT
                equipment_id,
                SUM(production_qty) AS total_production,
                SUM(downtime_min) AS total_downtime_min,
                SUM(machine_failure) AS failure_count
            FROM production
            GROUP BY equipment_id
        ) p
            ON e.equipment_id = p.equipment_id

        LEFT JOIN (
            SELECT
                equipment_id,
                SUM(energy_kwh) AS total_energy_kwh
            FROM energy
            GROUP BY equipment_id
        ) en
            ON e.equipment_id = en.equipment_id

        LEFT JOIN (
            SELECT
                equipment_id,
                AVG(defect_score) AS average_defect_score
            FROM quality
            GROUP BY equipment_id
        ) q
            ON e.equipment_id = q.equipment_id

        ORDER BY total_production DESC;
    """

    return execute_query(query)


if __name__ == "__main__":

    print("\n--- Equipment Count ---")

    print(get_equipment_count())

    print("\n--- Total Production ---")

    print(get_total_production())

    print("\n--- Top Equipment by Production ---")

    for row in get_equipment_production()[:5]:
        print(row)

    print("\n--- Top Equipment by Downtime ---")

    for row in get_equipment_downtime()[:5]:
        print(row)

    print("\n--- Top Equipment by Failures ---")

    for row in get_equipment_failures()[:5]:
        print(row)

    print("\n--- Maintenance Summary ---")

    for row in get_maintenance_summary()[:5]:
        print(row)

    print("\n--- Average Quality ---")

    print(get_average_quality())

    print("\n--- Top Equipment by Energy ---")

    for row in get_equipment_energy()[:5]:
        print(row)

    print("\n--- Top Equipment by Specific Energy ---")

    for row in get_specific_energy_by_equipment()[:5]:
        print(row)

    print("\n--- Equipment KPI ---")

    for row in get_equipment_kpi()[:5]:
        print(row)