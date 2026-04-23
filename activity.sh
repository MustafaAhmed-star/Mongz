#!/bin/bash

START="2026-01-01"
END="2026-04-01"

current="$START"

while [[ "$current" < "$END" ]]; do

  # أيام شغل بس (skip الجمعة والسبت مثلًا)
  day=$(date -j -f "%Y-%m-%d" "$current" "+%u")

  if [ "$day" -lt 6 ]; then

    commits=$((RANDOM % 3 + 1))

    for ((i=0; i<commits; i++)); do
      HOUR=$((RANDOM % 6 + 12))
      MINUTE=$((RANDOM % 60))

      DATE="$current $HOUR:$MINUTE:00"

      echo "$DATE" >> activity.txt

      GIT_AUTHOR_DATE="$DATE" GIT_COMMITTER_DATE="$DATE" \
      git add activity.txt && git commit -m "work update"

    done
  fi

  current=$(date -j -f "%Y-%m-%d" "$current" -v+1d +"%Y-%m-%d")

done
