import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import psycopg2
from config import Config 
import pdb

class Database:
    def __init__(self, autocommit=True):
        self.__connection = self.__connect()
        self.__connection.autocommit = autocommit

    def __connect(self):
        # write the command that return a connection to your database in cspostgres 
        # database server (use Config class defined in config.py).
        # remove the pass comand below
        conn = psycopg2.connect(
            dbname=Config.name,
            user=Config.user,
            password=Config.password,
            host=Config.host,
            port=Config.port
        )
        return conn
    
    def __reconnect(self):
        try:
            self.close()
        except psycopg2.Error as f:
            pass
        self.__connection = self.__connect()

    def  db_conn (self): 
        return self.__connection
    
    def close(self):
        '''Closes the connection'''
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None

    def get_cursor(self):
            for i in range(3):
                try:
                    return self.__connection.cursor()
                except Exception as e:
                    # Might need to reconnect
                    self.__reconnect()

    def __run_file(self, file_path):
        statement_parts = []
        with self.__connection.cursor() as cursor:
            # pdb.set_trace()
            with open(file_path, 'r') as f:
                for line in f:
                    if line[:2]=='--': continue
                    statement_parts.append(line)
                    if line.strip('\n').strip('\n\r').strip().endswith(';'):
                        statement = "".join( statement_parts).strip().rstrip(';')
                        if statement:
                            try:
                                # pdb.set_trace()
                                cursor.execute(statement)
                            except Exception as e:
                                print(e)
                        statement_parts = []
    
    def run_sql_script(self, sql_filename):
        if os.path.exists(sql_filename):
            self.__connect()
            self.__run_file(sql_filename)
            self.close()
        else:
            print('Invalid Path')

 # ===========================================================================
# ----------------DML  (CRUD) queries (retrieve, insert, update, delete -----
# ---------------------------------------------------------------------------



# ===========================================================================
db = Database()

if __name__ == '__main__':
    # pdb.set_trace()
    db.run_sql_script('./models/database.sql')