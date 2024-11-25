#!/bin/bash

# Variables for text replacement
old_name="gen/"
new_name="/gen"

# Convert text to uppercase
# uppercase_old=$(echo "$old_name" | tr '[:lower:]' '[:upper:]')
# uppercase_new=$(echo "$new_name" | tr '[:lower:]' '[:upper:]')
# uppercase_old="${uppercase_old}odd"
# uppercase_new="${uppercase_new}odd"
# old_name="${old_name}odd"
# new_name="${new_name}odd"
# echo "Uppercase old: $uppercase_old"
# echo "Uppercase new: $uppercase_new"

# Rename files
# for file in wwz_${old_name}_*.yaml; do
#   cp "$file" "${file/$old_name/$new_name}"
# done

# Replace text within files
# for file in wwz_sm.yaml; do
# # for file in wwz_${new_name}*.yaml; do
#     sed -i "s/$old_name*/*$new_name/g" "$file"
#     # sed -i "s/NP/NPBIS/g" "$file"
#     # sed -i "s/$uppercase_old/$uppercase_new/g" "$file"
# done

# Variables for text replacement
old_prefix="gen/"
new_suffix="/gen"

# Loop through all files and replace text
for file in *.yaml; do
    # sed -i "s|\([^"]${old_prefix}*")|\1${new_suffix}|g" "$file"
    # sed -i -E "s|gen/([A-Za-z]+_[A-Za-z]+)|\1/gen|g" "$file"
    sed -i -E 's|([A-Za-z]+_[A-Za-z0-9]+_[A-Za-z]+_[A-Za-z]+)"/gen|\1/gen"|g' "$file"
done