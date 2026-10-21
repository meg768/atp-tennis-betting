# ATP Tennis Betting

Separat projekt för bettingdelen från `atp-tennis-chat`.

## Databas

Direktanslutning till ATP-databasen i MariaDB via `scripts/database.py`.
Anslutningsuppgifterna finns i en lokal `.env` som ignoreras av Git.
`.env.example` visar vilka inställningar som behövs.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
echo 'SELECT 1 AS connection_ok;' | .venv/bin/python scripts/database.py
```

SQL kan också läsas från en fil:

```sh
.venv/bin/python scripts/database.py query.sql
```

Använd databasen för läsning och analys. Ändringar av data eller schema kräver
en uttrycklig instruktion från Magnus. Hjälpskriptet begränsar inte SQL till
läsning; databasbehörigheterna avgör vilka operationer som kan utföras.
