# Conector con MariaDB: se usa PyMySQL (100 % Python) en lugar de mysqlclient,
# porque Smart App Control de Windows bloquea la parte compilada de mysqlclient.
# PyMySQL se presenta como mysqlclient; Django exige la versión 2.2.1 o superior.
import pymysql

pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()
