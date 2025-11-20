<#
.\scripts\setup_mysql.ps1

Script para crear una base de datos y un usuario en MySQL usando el cliente `mysql`.
Por seguridad solicita la contraseña del usuario root si no se pasa como parámetro.

Ejemplo de uso:

  # Preguntar la contraseña de root interactiva
  .\scripts\setup_mysql.ps1 -AskRootPassword

  # Pasar la contraseña en la invocación (no recomendado en shell compartida)
  .\scripts\setup_mysql.ps1 -RootPassword "root_password"

Parámetros por defecto creados para este proyecto:
DbName = evaluacion360
DbUser = evaluacion_user
DbPass = 123456789
#>

param(
    [string]$RootUser = "root",
    [string]$RootPassword = $null,
    [string]$DbName = "evaluacion360",
    [string]$DbUser = "evaluacion_user",
    [string]$DbPass = "123456789",
    [string]$DbHost = "localhost",
    [int]$Port = 3306,
    [switch]$AskRootPassword
)

function Convert-SecureStringToPlainText($secureString) {
    $ptr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString)
    try { [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
    finally { [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
}

if ($AskRootPassword -and -not $RootPassword) {
    $secure = Read-Host -AsSecureString "Introduce la contraseña del usuario root para MySQL"
    $RootPassword = Convert-SecureStringToPlainText $secure
}

$mysql = Get-Command mysql.exe -ErrorAction SilentlyContinue
if (-not $mysql) {
    Write-Error "No se encontró el cliente 'mysql' en PATH. Instala MySQL y asegúrate de que 'mysql' esté en PATH o ejecuta este script desde una terminal que pueda invocarlo."
    exit 1
}

if (-not $RootPassword) {
    Write-Host "No se proporcionó contraseña root. Intentando ejecutar sin contraseña (puede fallar)."
}

$queries = @"
CREATE DATABASE IF NOT EXISTS $DbName CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
CREATE USER IF NOT EXISTS '$DbUser'@'$DbHost' IDENTIFIED BY '$DbPass';
GRANT ALL PRIVILEGES ON $DbName.* TO '$DbUser'@'$DbHost';
FLUSH PRIVILEGES;
"@

Write-Host "Ejecutando creación de base de datos y usuario en ${DbHost}:${Port} ..."

try {
    if ($RootPassword) {
        $proc = Start-Process -FilePath $mysql.Path -ArgumentList "-u", $RootUser, "-p$RootPassword", "-h", $DbHost, "-P", $Port, "-e", $queries -NoNewWindow -Wait -PassThru -RedirectStandardOutput "\stdout.txt" -RedirectStandardError "\stderr.txt"
        $rc = $proc.ExitCode
    } else {
        # Intentar sin password; el cliente pedirá si es necesario
        $proc = Start-Process -FilePath $mysql.Path -ArgumentList "-u", $RootUser, "-h", $DbHost, "-P", $Port, "-e", $queries -NoNewWindow -Wait -PassThru -RedirectStandardOutput "\stdout.txt" -RedirectStandardError "\stderr.txt"
        $rc = $proc.ExitCode
    }
    if ($rc -eq 0) {
        Write-Host "Base de datos '$DbName' y usuario '$DbUser' creados/actualizados correctamente."
    } else {
        Write-Error "El comando mysql devolvió código $rc. Revisar stdout/stderr en las rutas del script."
        Get-Content .\stderr.txt -ErrorAction SilentlyContinue
    }
} catch {
    Write-Error "Error al ejecutar el cliente mysql: $_"
}
