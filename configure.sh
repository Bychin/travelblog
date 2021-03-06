#!/bin/bash

py_version=$(python --version 2>&1)

if [[ $py_version < *3\.6\.0 ]]
then 
echo "Python 3.6.0 or greater required. Your version: $py_version"
exit 1
else
echo "$py_version
.
."
fi

pip3 install -r requirements.txt

python3.6 manage.py makemigrations
python3.6 manage.py migrate

python3.6 manage.py test

echo ".
.
.
.
.
configured"
exit 0
