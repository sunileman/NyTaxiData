#!/bin/bash
python fetcher.py urls.txt
sed -e'1d' *.csv >> temp.csv
sed -n '/ / p' temp.csv > nytripdata.csv
rm temp.csv
