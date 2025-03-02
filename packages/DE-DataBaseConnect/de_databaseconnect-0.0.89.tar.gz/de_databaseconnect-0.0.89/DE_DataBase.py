import os
import sqlalchemy
import cx_Oracle as ora
import sqlite3 as sq3
import psycopg2 as ps2
import mysql.connector as mysql
import pymssql as mssql
import redshift_connector as reds
import fdb
import jaydebeapi as dby
import jpype
#import azure

# Reponsabilidades desta classe:
# Apenas se conectar a uma das bases de dados abaixo especificadas
# Bases conhecidas: SQLITE, ORACLE, MYSQL, POSTGRES, MSSQL, RED_SHIFT

class DATABASE:
    def __init__(self):
        self._connection_is_valid = True
        self._DATABASE_ERROR = None

    def ORACLE_SQLA(self, string_connect: dict):
        conn = None
        try:
            # Definindo a Library ORACLE
            if string_connect["path_library"] is None:
                pathlib = os.getenv("ORACLE_LIB")
            else:
                pathlib = string_connect["path_library"]

            # Consistindo se a biblioteca do oracle ja esta iniciada
            try:
                ora.init_oracle_client(lib_dir=pathlib)
            except:
                pass
                # não faz nada (e para deixar assim se nao da erro)
            # Validando se foi passado um driver para conexao
            if string_connect["driver_conexao"] is None:
                string_connect["driver_conexao"] = "cx_oracle"
            database = string_connect["database"]
            driver = string_connect["driver_conexao"]
            user = string_connect["username"]
            pwd = string_connect["password"]
            host = string_connect["host"]
            port = string_connect["port"]
            string_connect["instance"] = ora.makedsn(host, port, string_connect["instance"])
            # Validando o tipo de conexao (SID ou SERVICE_NAME) apenas oracle
            if string_connect["type_conection"].upper() == "SERVICE_NAME":
                string_connect["instance"] = string_connect["instance"].replace("SID", "SERVICE_NAME")
            dnsName = string_connect["instance"]
            str_cnn = f"""{database.lower()}{driver}://{user}:{pwd}@{dnsName}"""
            engine = sqlalchemy.create_engine(str_cnn)
            conn = engine.connect()
            self._connection_is_valid = True
            self._nome_database = string_connect["database"]
        except Exception as error:
            self._connection_is_valid = False
            self._DATABASE_ERROR = conn.DatabaseError
            conn = self._DATABASE_ERROR
        finally:
            return conn

    def CACHE_JDBC(self, string_connect: dict):
        msg, result = None, None
        try:
            JHOME = jpype.getDefaultJVMPath()
            jpype.startJVM(JHOME, "-Djava.class.path=C:/Projetos/DE_DataBaseConnect/drivers/CacheDB.jar")
            username = string_connect["username"]
            password = string_connect["password"]
            host = string_connect["host"]
            port = string_connect["port"]
            instance = string_connect["instance"]
            cache_url = f"""jdbc:Cache://{host}:{port}/{instance}"""
            result = dby.connect("com.intersys.jdbc.CacheDriver", cache_url, [username, password])
            self._nome_database = string_connect["database"]
        except Exception as error:
            msg = error
            result = msg
        finally:
            return result

    def ORACLE_JDBC(self, string_connect: dict):
        msg, result = None, None
        try:
            JHOME = jpype.getDefaultJVMPath()
            jpype.startJVM(JHOME, "-Djava.class.path=C:/Projetos/DE_DataBaseConnect/drivers/ojdbc8.jar")
            username = string_connect["username"]
            password = string_connect["password"]
            host = string_connect["host"]
            port = string_connect["port"]
            instance = string_connect["instance"]
            oracle_url = f"""jdbc:oracle:thin:{username}/{password}@{host}:{port}/{instance}"""
            result = dby.connect("oracle.jdbc.driver.OracleDriver", oracle_url)
        except Exception as error:
            msg = error
            result = msg
        finally:
            return result

    def ORACLE(self, string_connect: dict):
        pathlib, conn = None, None
        try:
            # Definindo a Library ORACLE
            if "library" in string_connect.keys():
                if string_connect["library"] is None:
                    pathlib = os.getenv("ORACLE_LIB")
                else:
                    pathlib = string_connect["library"]
            else:
                pathlib = os.getenv("ORACLE_LIB")

            # Consistindo se a biblioteca do oracle ja esta iniciada
            try:
                ora.init_oracle_client(lib_dir=pathlib)
            except:
                pass
                # não faz nada (e para deixar assim se nao da erro)

            # Definindo o tipo de instancia SID/SERVICE_NAME
            if string_connect["type_conection"].upper() == "SID":
                dnsName = ora.makedsn(host=string_connect["host"], port=string_connect["port"], sid=string_connect["instance"])
            else:
                dnsName = ora.makedsn(host=string_connect["host"], port=string_connect["port"], service_name=string_connect["instance"])

            # Efetuando a conexao com a instancia do BANCO
            conn = ora.connect(string_connect["username"], string_connect["password"], dnsName, threaded=True)
            self._connection_is_valid = True
            self._nome_database = string_connect["database"]
        except Exception as error:
            self._connection_is_valid = False
            msg = f"""Falha ao tentar se conectar com o banco de dados ORACLE [{string_connect["name"]}].\nException Error: {error} """
            self._DATABASE_ERROR = msg
            conn = msg
        finally:
            return conn

    def SQLITE(self, database, **kwargs):
        DATABASE_NAME, result, msg, conn = None, False, None, None
        try:
            if os.path.isfile(database):
                if "check_same_thread" in kwargs.keys():
                    __check_same_thread = kwargs.get("check_same_thread")
                else:
                    __check_same_thread = True
                conn = sq3.connect(database, check_same_thread=__check_same_thread)
                self._connection_is_valid = True
            else:
                msg = f"""SQLITE [{database}]- Não existe no local informado!"""
                raise Exception(msg)
            self._nome_database = 'SQLITE'
        except Exception as error:
            conn = error
            self._connection_is_valid = False
            self._DATABASE_ERROR = conn.DatabaseError
        finally:
            return conn

    # ----------------------------------------------------------------
    # Falta driver
    def SQLCIPHER(self, database, password):
        DATABASE_NAME, result, msg, conn = None, False, None, None
        try:
            if os.path.isfile(database):
                #conn = sqch.connect(database, password=password)
                self._connection_is_valid = True
                self._nome_database = 'SQLCIPHER'
            else:
                msg = f"""SQLITE [{database}]- Não existe no local informado!"""
                raise Exception(msg)
        except Exception as error:
            conn = error
            self._connection_is_valid = False
            self._DATABASE_ERROR = True
        finally:
            return conn

    def POSTGRES(self, string_connect: dict):
        msg, conn = None, None
        try:
            # Efetuando a conexao com a instancia do BANCO
            conn = ps2.connect(user=string_connect["username"], password=string_connect["password"], database=string_connect["instance"], host=string_connect["host"])
            self._connection_is_valid = True
            self._nome_database = string_connect["database"]
        except Exception as error:
            conn = f"""Falha ao tentar se conectar com o banco de dados POSTGRES.\n """
            self._connection_is_valid = False
            self._DATABASE_ERROR = conn.DatabaseError
        finally:
            return conn

    def MSSQL(self, string_connect: dict):
        msg, conn = None, None
        try:
            # Efetuando a conexao com a instancia do BANCO
            conn = mssql.connect(user=string_connect["username"], password=string_connect["password"], database=string_connect["instance"], server=string_connect["host"])
            self._connection_is_valid = True
            self._nome_database = string_connect["database"]
        except Exception as error:
            conn = error
            self._connection_is_valid = False
            self._DATABASE_ERROR = conn.DatabaseError
        finally:
            return conn

    def MYSQL(self, string_connect: dict):
        msg, conn = None, None
        try:
            # Efetuando a conexao com a instancia do BANCO
            conn = mysql.connect(user=string_connect["username"], password=string_connect["password"], database=string_connect["instance"], host=string_connect["host"])
            self._connection_is_valid = True
            self._nome_database = string_connect["database"]
        except Exception as error:
            conn = error
            self._connection_is_valid = False
            self._DATABASE_ERROR = conn.DatabaseError
        finally:
            return conn

    # ----------------------------------------------------------------
    # Falta driver - maquina local não permite
    def FIREBIRD(self, string_connect: dict):
        msg, conn = None, None
        try:
            user = string_connect["username"]
            pwd = string_connect["password"]
            host = string_connect["host"]
            port = string_connect["port"]
            instance = string_connect["instance"]
            conn = fdb.connect(host=host, database=instance, user=user, password=pwd, port=port)
            self._connection_is_valid = True
            self._nome_database = string_connect["database"]
        except Exception as error:
            conn = error
            self._connection_is_valid = False
            self._DATABASE_ERROR = conn.DatabaseError
        finally:
            return conn

    def REDSHIFT(self, string_connect: dict):
        conn = None
        try:
            conn = reds.connect(host=string_connect["host"],
                                database=string_connect["instance"],
                                user=string_connect["username"],
                                password=string_connect["password"]
                            )
            self._connection_is_valid = True
            self._nome_database = string_connect["database"]
        except Exception as error:
            self._connection_is_valid = False
            self._DATABASE_ERROR = conn.DatabaseError
            conn = error
        finally:
            return conn

    # ----------------------------------------------------------------
    # Falta tudo (Instalar driver ODBC) Maquina local não permite
    def INFORMIX(self, string_connect: dict):
        try:
            pass
            self._connection_is_valid = True
        except Exception as error:
            self._connection_is_valid = False
            self._DATABASE_ERROR = True
        finally:
            pass

    # def AZURE(self, string_connect: dict):
    #     conn = None
    #     try:
    #         from azure.storage.filedatalake import DataLakeServiceClient as az
    #
    #         conn = az.connect(host=string_connect["host"],
    #                           database=string_connect["instance"],
    #                           user=string_connect["username"],
    #                           password=string_connect["password"]
    #                           )
    #         self._connection_is_valid = True
    #         self._nome_database = string_connect["database"]
    #     except Exception as error:
    #         self._connection_is_valid = False
    #         self._DATABASE_ERROR = conn.DatabaseError
    #         conn = error
    #     finally:
    #         return conn

    def METADATA(self,
                     conexao: object,
                     database: str,
                     nome_tabela: str,
                     owner: str = "",
                     alias: str = 'x',
                     quoted: bool = False,
                     rowid: bool = False,
                     join: str = None,
                     where: str = None,
                     orderby: str = None,
                     limit: int = 0
                     ) -> str:
        try:
            querys = {"ORACLE":   f"""Select * from all_tab_columns where table_owner = '{owner}' and table_name = '{nome_tabela}' order by column_id""""",
                      "POSTGRES": f"""Select * from information_schema.columns where table_schema = '{owner}' and table_name = '{nome_tabela}' order by ordinal_position""",
                      "SQLITE":   f"""Select * from pragma_table_info('{nome_tabela}') order by cid""",
                      "MYSQL":    f"""Select * from information_schema.columns where table_name = '{nome_tabela}' order by ordinal_position""",
                      "REDSHIFT": f"""Select column_name from information_schema.columns where table_schema = '{owner}' and table_name = '{nome_tabela}' order by ordinal_position""",
                      "CACHE":    f"""Select * from information_schema.columns where table_schema = '{owner}' and table_name = '{nome_tabela}'""",
                      "MSSQL":    f"""select t.name Tabela
                                            ,ac.name Coluna
                                            ,ac.column_id 
                                            ,sep.value Comment
                                            ,t2.name Data_Type
                                        from sys.schemas s 
                                        join sys.tables t 
                                          on t.schema_id = s.schema_id 
                                        join sys.all_columns ac 
                                          on ac.object_id = t.object_id 
                                        join sys.types t2 
                                          on t2.system_type_id = ac.system_type_id 
                                        left join sys.extended_properties sep 
                                          on sep.major_id = t.object_id
                                             and sep.minor_id = ac.column_id
                                             and sep.name = 'MS_Description'
                                       where s.name = ISNULL('{owner}', 'dbo')
                                         and t.name = '{nome_tabela}'
                                       order by t.name, ac.column_id
                                    """
                      }
            qry = querys[database.upper()]
            cur = conexao.cursor()
            cur.execute(qry)
            column_list = []
            for col in cur.fetchall():
                if database == "ORACLE":
                    pass
                elif database == "POSTGRES":
                    pass
                elif database == "SQLITE":
                    pass
                elif database == "MYSQL":
                    pass
                elif database == "REDSHIFT":
                    # consistindo se o nome da coluna esta com datatype = bytes
                    if isinstance(col[0], bytes):
                        column = col[0].decode()
                    else:
                        column = col[0]
                # QUOTED
                if quoted:
                    column = f"""{alias}.\"{column}\""""
                else:
                    column = f"""{alias}.{column}"""
                column_list.append(column)
            # ROWID
            if rowid:
                # -----------------------------------------
                # Banco SQLITE
                if database == "SQLITE":
                    column_list.append(f"""{alias}.ROWID ROWID_TABELA""")
                # -----------------------------------------
                # Banco ORACLE
                elif database == "ORACLE":
                    column_list.append(f"""rowidtochar({alias}.Rowid) "ROWID_TABELA" """)
                # -----------------------------------------
                # Banco MYSQL
                elif database == "MYSQL":
                    # não implementado
                    # tem que identificar qual a coluna do MYSQL que representa esta informação
                    pass
                # -----------------------------------------
                # Banco POSTGRES
                elif database == "POSTGRES":
                    column_list.append(f"""{alias}.row_number() OVER () ROWID_TABELA""")
                # -----------------------------------------
                # Banco CACHE
                elif database == "CACHE":
                    # não implementado
                    # tem que identificar qual a coluna do CACHE que representa esta informação
                    pass
            # Estruturando as colunas
            colunas = "\n      ,".join(column_list)
            select = f"""select {colunas}"""

            # NOME TABELA
            if quoted:
                tabela = f"""\n  from \"{owner}\".\"{nome_tabela.strip()}\" {alias.strip()}"""
            else:
                tabela = f"""\n  from {owner}.{nome_tabela.strip()} {alias.strip()}"""

            # JOIN
            if join is None:
                join = ""
            else:
                join = f"""\n  {join}"""

            # WHERE
            if where is None:
                if database == "ORACLE" and limit > 0:
                    where = f"""\n where rownum <= {limit}"""
                else:
                    where = ""
            else:
                if database == "ORACLE" and limit > 0:
                    where = f"""\n {where.strip()}\n  and rownum <= {limit}"""
                else:
                    where = f"""\n {where.strip()}"""

            # ORDERBY
            if orderby is None:
                orderby = ""
            else:
                orderby = f"""\n {orderby.strip()}"""

            # LIMIT
            if database in ["MYSQL", "SQLITE", "POSTGRES", "REDSHIFT", 'CACHE']:
                if limit > 0:
                    limit = f"""\n TOP {limit}"""
                else:
                    limit = ""
            else:
                limit = ""

            if database in ["CACHE"]:
                qry = f"""{select}{limit}{tabela}{join}{where}{orderby}""".lstrip()
            else:
                qry = f"""{select}{tabela}{join}{where}{orderby}{limit}""".lstrip()
            msg = qry
        except Exception as error:
            msg = error + qry
        finally:
            return msg

    @property
    def CONNECTION_VALID(self):
        return self._connection_is_valid

    @property
    def NOME_DATABASE(self):
        return self._nome_database.upper()

    @property
    def DATABASE_ERROR(self):
        return self._DATABASE_ERROR

if __name__ == "__main__":
    pass
