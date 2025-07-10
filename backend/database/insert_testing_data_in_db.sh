#!/bin/bash

# install sqlite3 if not installed.
if ! command -v sqlite3 &> /dev/null; then
    echo "Installing sqlite3..."
    sudo apt update && sudo apt install -y sqlite3
fi

# Execute init_db() method in db_manager.py (to create the tasks_db.sqlite file).
python3 -c "from db_manager import init_db; init_db()" || {
    echo "Error al ejecutar init_db()";
    exit 1;
}

# Import data.
if [ -f "database.sql" ]; then
    sqlite3 tasks_db.sqlite < database.sql || {
        echo "Error";
        exit 1;
    }
    echo "Data inserted successfully"
else
    echo "Error: database.sql does not exists"
    exit 1
fi