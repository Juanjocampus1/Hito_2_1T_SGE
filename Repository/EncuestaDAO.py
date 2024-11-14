from Config.db_connection import connect_db

class Database:
    def __init__(self):
        self.conn = connect_db()
        self.cursor = self.conn.cursor()

    def create_record(self, data):
        query = """ 
        INSERT INTO ENCUESTA (edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, BebidasDestiladasSemana, VinosSemana, PerdidasControl, DiversionDependenciaAlcohol, ProblemasDigestivos, TensionAlta, DolorCabeza)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, data)
        self.conn.commit()

    def read_records(self):
        self.cursor.execute("SELECT * FROM ENCUESTA")
        results = self.cursor.fetchall()
        return results

    def update_record(self, idEncuesta, data):
        query = """
        UPDATE ENCUESTA SET edad=%s, Sexo=%s, BebidasSemana=%s, CervezasSemana=%s, BebidasFinSemana=%s, BebidasDestiladasSemana=%s, VinosSemana=%s, PerdidasControl=%s, DiversionDependenciaAlcohol=%s, ProblemasDigestivos=%s, TensionAlta=%s, DolorCabeza=%s
        WHERE idEncuesta=%s
        """
        self.cursor.execute(query, data + (idEncuesta,))
        self.conn.commit()

    def delete_record(self, idEncuesta):
        query = "DELETE FROM ENCUESTA WHERE idEncuesta=%s"
        self.cursor.execute(query, (idEncuesta,))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()