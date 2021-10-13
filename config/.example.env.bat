@ECHO OFF
call virtualenv venv
call venv/Scripts/activate

set POSTGRES_DB=chat_db
set POSTGRES_USER=admin
set POSTGRES_PASSWORD=root
set POSTGRES_HOST=localhost
set POSTGRES_PORT=5416

set TELEGRAM_ACCESS_TOKEN=
set TELEGRAM_CHAT_ID=