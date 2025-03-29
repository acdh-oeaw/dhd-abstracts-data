#!/bin/bash
YEARS=(2016 2017 2018 2019 2020 2022 2023 2024)
BASE_URL=https://github.com/DHd-Verband/DHd-Abstracts-

for year in "${YEARS[@]}"
do
    url=${BASE_URL}${year}/archive/refs/heads/main.zip
    echo "Downloading data for year: ${year} from ${url}"
    wget ${url}
    unzip main.zip -d tmp
    counter=1
    find tmp -path "*/XML-*/*.xml" -type f | while read file; do
        new_name=$(printf "abstract-%d-%05d.xml" "$year" "$counter")
        mkdir -p data/editions
        cp "$file" "data/editions/$new_name"
        ((counter++))
    done
    rm -rf tmp
    rm -rf main.zip
    
done