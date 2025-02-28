#!/bin/bash

# Determine the max number of available CPU cores
WORKERS=$(python3 -c "import multiprocessing; print(multiprocessing.cpu_count())")

# Start Uvicorn with the calculated number of workers
exec uvicorn spartaqube_app.asgi:application --host 0.0.0.0 --port 8665 --loop uvloop --http httptools --log-level warning --workers $WORKERS
