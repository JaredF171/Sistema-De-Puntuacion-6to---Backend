-- Script para crear la base de datos y el usuario para el proyecto
-- Úsalo en MySQL Workbench: abre una conexión con un usuario con privilegios (root), pega y ejecuta.

-- Cambia la contraseña si no quieres usar '123456789'
SET @DB_NAME = 'evaluacion360';
SET @DB_USER = 'evaluacion_user';
SET @DB_PASS = '123456789';

-- Crear la base de datos con codificación UTF8MB4
CREATE DATABASE IF NOT EXISTS `evaluacion360` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario (host '%' permite conexiones desde cualquier IP; usa 'localhost' si lo prefieres)
-- Aquí creamos el usuario usando el plugin `mysql_native_password` para mayor compatibilidad
-- (evita problemas con clientes antiguos o adaptadores que no soportan caching_sha2_password).

-- NOTA: cambiamos a nombres literales para evitar complejidad con variables en scripts SQL ejecutados
-- desde herramientas gráficas como MySQL Workbench.
DROP USER IF EXISTS 'evaluacion_user'@'%';
CREATE USER IF NOT EXISTS 'evaluacion_user'@'%' IDENTIFIED WITH mysql_native_password BY '123456789';

-- Otorgar todos los privilegios en la base de datos al usuario
GRANT ALL PRIVILEGES ON `evaluacion360`.* TO 'evaluacion_user'@'%';

FLUSH PRIVILEGES;

-- Ver comprobación rápida
SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'evaluacion360';
SELECT User, Host, plugin FROM mysql.user WHERE User = 'evaluacion_user';
