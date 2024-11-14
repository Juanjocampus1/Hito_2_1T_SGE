from Repository import EncuestaDAO


def search_by_id(idEncuesta):
    db = EncuestaDAO.Database()
    query = "SELECT * FROM ENCUESTA WHERE idEncuesta = %s"
    db.cursor.execute(query, (idEncuesta,))
    results = db.cursor.fetchall()
    db.close()
    return results