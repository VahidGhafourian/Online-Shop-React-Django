#!/bin/bash
# Replace environment variables in SQL template
envsubst < /docker-entrypoint-initdb.d/init_db_template.sql > /docker-entrypoint-initdb.d/init_db.sql

# Execute the original entrypoint script of PostgreSQL
exec docker-entrypoint.sh postgres
