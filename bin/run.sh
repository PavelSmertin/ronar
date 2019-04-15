#!/bin/bash
echo ""
echo "Running Python RonarServer"
echo ""

BASE_DIR=`dirname $0`

(cd ${BASE_DIR}/../ && python3 -m ronarlistener >/dev/null 2>&1)

exit 0
