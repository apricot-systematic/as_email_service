#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

/venv/bin/python /app/manage.py migrate
/venv/bin/python /app/manage.py run_huey
