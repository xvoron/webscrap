#!/bin/bash

until nc -z db 5432; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

echo "PostgreSQL is now ready. Starting Python applications..."
