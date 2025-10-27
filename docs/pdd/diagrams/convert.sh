#!/bin/sh
for file in *.mmd; do
    svg="${file%.mmd}.svg"
    if [ ! -f "$svg" ] || [ "$file" -nt "$svg" ]; then
        echo "Converting $file..."
        mmdc -i "$file" -o "$svg"
    else
        echo "Skipping $file (up to date)"
    fi
done
echo "Conversion complete!"
