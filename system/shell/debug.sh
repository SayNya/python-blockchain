#!/bin/bash

export $(grep -v '^#' .env | xargs)
PYTHONPATH=$1 uvicorn --loop=uvloop --debug --port "$APP_PORT" --reload --log-level=debug --host "$APP_HOST" main:app
