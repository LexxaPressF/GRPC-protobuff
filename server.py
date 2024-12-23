import grpc
from concurrent import futures
import sqlite3
import glossary_pb2
import glossary_pb2_grpc

class GlossaryService(glossary_pb2_grpc.GlossaryServiceServicer):
    def __init__(self, db_path='/app/data/glossary.db'):
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS glossary (
                                key TEXT PRIMARY KEY,
                                description TEXT)''')
            conn.commit()

    def _execute_query(self, query, params=(), fetch_one=False):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            if fetch_one:
                return cursor.fetchone()
            return cursor.fetchall()

    def GetAllTerms(self, request, context):
        rows = self._execute_query('SELECT key, description FROM glossary')
        terms = [glossary_pb2.Term(key=row[0], description=row[1]) for row in rows]
        return glossary_pb2.TermList(terms=terms)

    def GetTerm(self, request, context):
        key = request.key
        row = self._execute_query('SELECT description FROM glossary WHERE key = ?', (key,), fetch_one=True)
        if row:
            return glossary_pb2.Term(key=key, description=row[0])
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Term not found')
        return glossary_pb2.Term()

    def AddTerm(self, request, context):
        key = request.key
        try:
            self._execute_query('INSERT INTO glossary (key, description) VALUES (?, ?)', (key, request.description))
        except sqlite3.IntegrityError:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('Term already exists')
        return glossary_pb2.Empty()

    def UpdateTerm(self, request, context):
        key = request.key
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE glossary SET description = ? WHERE key = ?', (request.description, key))
            if cursor.rowcount == 0:  # Проверка, было ли обновление
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Term not found')
                return glossary_pb2.Empty()
        return glossary_pb2.Empty()

    def DeleteTerm(self, request, context):
        key = request.key
        deleted = self._execute_query('DELETE FROM glossary WHERE key = ?', (key,))
        if deleted:
            return glossary_pb2.Empty()
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Term not found')
        return glossary_pb2.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_service = GlossaryService(db_path='/app/data/glossary.db')
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(glossary_service, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
