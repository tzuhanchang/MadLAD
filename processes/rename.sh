#!/bin/bash

# Variables for text replacement
old_name="ft2"
new_name="ft1"

# Convert text to uppercase
uppercase_old=$(echo "$old_name" | tr '[:lower:]' '[:upper:]')
uppercase_new=$(echo "$new_name" | tr '[:lower:]' '[:upper:]')
uppercase_old="${uppercase_old}odd"
uppercase_new="${uppercase_new}odd"
old_name="${old_name}odd"
new_name="${new_name}odd"
echo "Uppercase old: $uppercase_old"
echo "Uppercase new: $uppercase_new"

# Rename files
for file in wwz_${old_name}_*.yaml; do
  cp "$file" "${file/$old_name/$new_name}"
done

# Replace text within files
for file in wwz_${new_name}_*.yaml; do
# for file in wwz_${new_name}*.yaml; do
    sed -i "s/$old_name/$new_name/g" "$file"
    # sed -i "s/NP/NPBIS/g" "$file"
    sed -i "s/$uppercase_old/$uppercase_new/g" "$file"
done