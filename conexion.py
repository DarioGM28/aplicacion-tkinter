from mysql.connector import pooling
from mysql.connector import Error

class Conexion:
    #CONSTANTES DE CONEXION (TAMBIEN SON CONSTANTES DE CLASE)
    DATABASE = 'zona_fit_db'
    USERNAME = 'root'
    PASSWORD = 'admin1234.'
    DB_PORT = '3306'
    HOST = 'localhost'
    POOL_SIZE = 5
    POOL_NAME = 'zona_fit_pool'
    pool = None

    @classmethod
    def obtener_pool(cls): #PARA ACCEDER A LAS CONTANTES DE CLASE
        if cls.pool is None: #se crea el objeto pool, si no existe
            try:
                cls.pool = pooling.MySQLConnectionPool(
                    pool_name = cls.POOL_NAME,
                    pool_size = cls.POOL_SIZE,
                    host = cls.HOST,
                    port = cls.DB_PORT,
                    user = cls.USERNAME,
                    password = cls.PASSWORD,
                    database = cls.DATABASE
                )
                return cls.pool
            except Error as e:
                print(f'Ocurrior un error al obtener pool, ERROR: {e}')
        else:
            return cls.pool

    @classmethod
    def obtener_conexion(cls):
        return cls.obtener_pool().get_connection()

    @classmethod
    def liberar_conexion(cls, conexion):
        conexion.close()

if __name__ == '__main__':
    #creamos un objeto pool
    pool = Conexion.obtener_pool()
    print(pool)
    conexion1 = pool.get_connection() #se crea la conexion
    print(conexion1)
    Conexion.liberar_conexion(conexion1) # se libera la conexion
    print('Se ha liberado la conexion1')