param(
    [switch]$Force
)

if ($Force -and (Test-Path "alembic")) {
    Remove-Item "alembic" -Recurse -Force
}

if (-not (Test-Path "alembic")) {
    alembic init alembic
}

Copy-Item "scripts\alembic_env.py" "alembic\env.py" -Force

Write-Host "Alembic initialized and env.py configured."
