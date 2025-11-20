"""Paquete raíz `src`.

Instalar PyMySQL como reemplazo de MySQLdb para evitar compilar extensiones C
en Windows (si PyMySQL está instalado).
"""
try:
	import pymysql
	pymysql.install_as_MySQLdb()
except Exception:
	# Si PyMySQL no está disponible en el entorno, no fallamos aquí;
	# la instalación de dependencias la manejará el desarrollador.
	pass
