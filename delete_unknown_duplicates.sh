#!/bin/bash

calculate_md5() {
    md5sum "$1" | awk '{print $1}'
}

delete_file() {
    echo "deleting file: $1"
    rm "$1"
}

# array to store files and their md5sums
declare -A files_md5

for file in unknown/*; do
    # only if file
    if [[ -f "$file" ]]; then
        # calculate md5sum
        md5=$(calculate_md5 "$file")
        # add file to list
        if [[ -n "${files_md5[$md5]}" ]]; then
            # print if duplicate exists
            echo "duplicate: $file and ${files_md5[$md5]}"
            # delete if duplicate
            delete_file "$file"
        else
            # add to array if no duplucate
            files_md5[$md5]="$file"
        fi
    fi
done

