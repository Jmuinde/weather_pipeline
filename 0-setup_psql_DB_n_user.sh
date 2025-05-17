#!/bin/bash

db_user="myuser"
db_password="Dsa2021&"
db_name="weatherdb"

# Create user if they do  not exist
sudo -u postgres psql <<EOF

DO \$\$
BEGIN 
	IF NOT EXISTS(
		SELECT FROM pg_catalog.pg_roles WHERE rolname = '${db_user}'
	)THEN
		CREATE USER "${db_user}" WITH PASSWORD '$db_password';
	END IF;
END
\$\$;

-- Create database if not exist
SELECT 'CREATE DATABASE "${db_name}" OWNER "${db_user}"'
WHERE NOT EXISTS (
		SELECT FROM pg_database WHERE datname = '${db_name}'
	)\gexec

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE "${db_name}" TO "${db_user}";

EOF


echo "Database '${db_name}' and user '${db_user}' created successfully."
