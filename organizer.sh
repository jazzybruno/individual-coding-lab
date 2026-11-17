#!/bin/bash

FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

if [ ! -f "$FILE" ]; then
    echo "Error: $FILE not found in $(pwd). Nothing to archive."
    exit 1
fi

if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created the $ARCHIVE_DIR directory."
fi

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
ARCHIVED="grades_${TIMESTAMP}.csv"

mv "$FILE" "$ARCHIVE_DIR/$ARCHIVED"
touch "$FILE"

echo "[$TIMESTAMP] Archived $FILE -> $ARCHIVE_DIR/$ARCHIVED" >> "$LOG_FILE"

echo "Archived $FILE as $ARCHIVE_DIR/$ARCHIVED"
echo "Created a new empty $FILE"
echo "Logged to $LOG_FILE"
