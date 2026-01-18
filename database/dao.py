from database.DB_connect import DBConnect
from model.state import State

class DAO:
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM esempio """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_year():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
                    SELECT DISTINCT
                        YEAR(s_datetime) as anno
                    FROM 
                        sighting 
                """

        cursor.execute(query)

        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_shape(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
                    SELECT DISTINCT
                        YEAR(s_datetime), shape
                    FROM 
                        sighting
                    WHERE
                        YEAR(s_datetime) = %s
                    ORDER BY 
                        shape ASC
                """

        cursor.execute(query, (anno,))

        for row in cursor:
            if row["shape"] == "":
                result.append("...")
            else:
                result.append(row["shape"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_states():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
                        SELECT 
                            *
                        FROM 
                            state
                        ORDER BY id ASC
                    """

        cursor.execute(query)

        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connessioni():
        conn = DBConnect.get_connection()

        result = set()

        cursor = conn.cursor(dictionary=True)
        query = """ 
                    SELECT 
                        * 
                    FROM 
                        neighbor
                """

        cursor.execute(query)

        for row in cursor:
            result.add((row["state1"], row["state2"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_peso_nodo(shape,year,nodo):
        conn = DBConnect.get_connection()

        result = 0

        cursor = conn.cursor(dictionary=True)
        query = """ 
                        SELECT
                            COUNT(*) as avvistamenti
                        FROM
                            sighting
                        WHERE
                            shape = %s
                            AND YEAR(`s_datetime`) = %s
                            AND state = %s
                    """

        cursor.execute(query, (shape,year,nodo))
        row = cursor.fetchone()
        result = int(row["avvistamenti"])

        cursor.close()
        conn.close()
        return result