#!/bin/bash
echo ""
echo "Running Python RonarServer"
echo ""

BASE_DIR=`dirname $0`

echo BASE_DIR

(cd ${BASE_DIR}/../ && python -m ronarlistener >/dev/null 2>&1)

echo "BASE_DIR"

exit 0
