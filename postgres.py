# Import para uso do Postgres.
import psycopg2 
from psycopg2 import Error

class ConPostgres(object):
    _db=None    
    def __init__(self, mhost, db, usr, pwd):
     self._db = psycopg2.connect(host=mhost, database=db, user=usr,  password=pwd)

    def manipulate(self, sql):
        try:
            cur=self._db.cursor()
            cur.execute(sql)
            cur.close();
            self._db.commit()
        except:
            return False;
        return True;
    
    def consult(self, sql):
        try:
            cur=self._db.cursor()
            cur.execute(sql)
            rs=cur.fetchall();
        except:
            return None
        return rs
    def nextPK(self, tabela, chave):
        sql='select max('+chave+') from '+tabela
        rs = self.consult(sql)
        pk = rs[0][0]  
        return pk+1
    def currentPK(self, tabela, chave):
        sql='select max('+chave+') from '+tabela
        rs = self.consult(sql)
        pk = rs[0][0]  
        return pk
    def disconnect(self):
        self._db.close()