from db import get_connection

def obtener_cartuchos_activos():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT color, fecha_inicio
                FROM cartuchos
                WHERE activo = true
            """)
            return {row[0]: row[1] for row in cur.fetchall()}

def cambiar_cartucho(color, fecha):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE cartuchos
                SET activo = false, fecha_fin = %s
                WHERE color = %s AND activo = true
            """, (fecha, color))

            cur.execute("""
                INSERT INTO cartuchos (color, fecha_inicio, activo)
                VALUES (%s, %s, true)
            """, (color, fecha))

def guardar_copias(fecha, bn, color, descripcion):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO copias (fecha, copias_bn, copias_color, descripcion)
                VALUES (%s, %s, %s, %s)
            """, (fecha, bn, color, descripcion))

def reporte_cartuchos():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    c.color,
                    c.fecha_inicio,
                    COALESCE(c.fecha_fin, CURRENT_DATE),
                    SUM(
                        CASE
                            WHEN c.color = 'K'
                            THEN co.copias_bn + co.copias_color
                            ELSE co.copias_color
                        END
                    )
                FROM cartuchos c
                LEFT JOIN copias co
                  ON co.fecha BETWEEN c.fecha_inicio
                  AND COALESCE(c.fecha_fin, CURRENT_DATE)
                GROUP BY c.id
                ORDER BY c.color, c.fecha_inicio
            """)
            return cur.fetchall()

def historial_copias():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT fecha, copias_bn, copias_color, descripcion
                FROM copias
                ORDER BY fecha DESC
                LIMIT 20
            """)
            return cur.fetchall()
