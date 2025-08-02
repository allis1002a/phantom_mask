#!/bin/bash

python3 ./scripts/conver_to_schema.py
python3 ./scripts/init_db.py

exec uvicorn --host 0.0.0.0 --port 80 app.main:app