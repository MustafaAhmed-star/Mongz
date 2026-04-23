#!/bin/bash

START_DATE="2026-01-01"
END_DATE="2026-04-01"

TOTAL_COMMITS=$(git rev-list --count HEAD)
echo "Total commits: $TOTAL_COMMITS"

START_TS=$(date -j -f "%Y-%m-%d" "$START_DATE" "+%s")
END_TS=$(date -j -f "%Y-%m-%d" "$END_DATE" "+%s")

TOTAL_DAYS=$(( (END_TS - START_TS) / 86400 ))
echo "Total days range: $TOTAL_DAYS"

STEP=$(( TOTAL_DAYS / TOTAL_COMMITS ))
[ $STEP -eq 0 ] && STEP=1

echo "Step days: $STEP"

i=0

git filter-branch --env-filter '
i='"$i"'
START_TS='"$START_TS"'
STEP='"$STEP"'

NEW_TS=$((START_TS + (i * STEP * 86400)))

HOUR=$((RANDOM % 8 + 10))
MINUTE=$((RANDOM % 60))
SECOND=$((RANDOM % 60))

FINAL_DATE=$(date -r $NEW_TS "+%Y-%m-%d")" $HOUR:$MINUTE:$SECOND"

export GIT_AUTHOR_DATE="$FINAL_DATE"
export GIT_COMMITTER_DATE="$FINAL_DATE"

i=$((i + 1))
' -- --all

echo "Dates updated successfully!"#!/bin/bash

START_DATE="2026-01-01"
END_DATE="2026-04-01"

TOTAL_COMMITS=$(git rev-list --count HEAD)
echo "Total commits: $TOTAL_COMMITS"

START_TS=$(date -j -f "%Y-%m-%d" "$START_DATE" "+%s")
END_TS=$(date -j -f "%Y-%m-%d" "$END_DATE" "+%s")

TOTAL_DAYS=$(( (END_TS - START_TS) / 86400 ))
echo "Total days range: $TOTAL_DAYS"

STEP=$(( TOTAL_DAYS / TOTAL_COMMITS ))
[ $STEP -eq 0 ] && STEP=1

echo "Step days: $STEP"

i=0

git filter-branch --env-filter '
i='"$i"'
START_TS='"$START_TS"'
STEP='"$STEP"'

NEW_TS=$((START_TS + (i * STEP * 86400)))

HOUR=$((RANDOM % 8 + 10))
MINUTE=$((RANDOM % 60))
SECOND=$((RANDOM % 60))

FINAL_DATE=$(date -r $NEW_TS "+%Y-%m-%d")" $HOUR:$MINUTE:$SECOND"

export GIT_AUTHOR_DATE="$FINAL_DATE"
export GIT_COMMITTER_DATE="$FINAL_DATE"

i=$((i + 1))
' -- --all

echo "Dates updated successfully!"#!/bin/bash

START_DATE="2026-01-01"
END_DATE="2026-04-01"

TOTAL_COMMITS=$(git rev-list --count HEAD)
echo "Total commits: $TOTAL_COMMITS"

START_TS=$(date -j -f "%Y-%m-%d" "$START_DATE" "+%s")
END_TS=$(date -j -f "%Y-%m-%d" "$END_DATE" "+%s")

TOTAL_DAYS=$(( (END_TS - START_TS) / 86400 ))
echo "Total days range: $TOTAL_DAYS"

STEP=$(( TOTAL_DAYS / TOTAL_COMMITS ))
[ $STEP -eq 0 ] && STEP=1

echo "Step days: $STEP"

i=0

git filter-branch --env-filter '
i='"$i"'
START_TS='"$START_TS"'
STEP='"$STEP"'

NEW_TS=$((START_TS + (i * STEP * 86400)))

HOUR=$((RANDOM % 8 + 10))
MINUTE=$((RANDOM % 60))
SECOND=$((RANDOM % 60))

FINAL_DATE=$(date -r $NEW_TS "+%Y-%m-%d")" $HOUR:$MINUTE:$SECOND"

export GIT_AUTHOR_DATE="$FINAL_DATE"
export GIT_COMMITTER_DATE="$FINAL_DATE"

i=$((i + 1))
' -- --all

echo "Dates updated successfully!"#!/bin/bash

START_DATE="2026-01-01"
END_DATE="2026-04-01"

TOTAL_COMMITS=$(git rev-list --count HEAD)
echo "Total commits: $TOTAL_COMMITS"

START_TS=$(date -j -f "%Y-%m-%d" "$START_DATE" "+%s")
END_TS=$(date -j -f "%Y-%m-%d" "$END_DATE" "+%s")

TOTAL_DAYS=$(( (END_TS - START_TS) / 86400 ))
echo "Total days range: $TOTAL_DAYS"

STEP=$(( TOTAL_DAYS / TOTAL_COMMITS ))
[ $STEP -eq 0 ] && STEP=1

echo "Step days: $STEP"

i=0

git filter-branch --env-filter '
i='"$i"'
START_TS='"$START_TS"'
STEP='"$STEP"'

NEW_TS=$((START_TS + (i * STEP * 86400)))

HOUR=$((RANDOM % 8 + 10))
MINUTE=$((RANDOM % 60))
SECOND=$((RANDOM % 60))

FINAL_DATE=$(date -r $NEW_TS "+%Y-%m-%d")" $HOUR:$MINUTE:$SECOND"

export GIT_AUTHOR_DATE="$FINAL_DATE"
export GIT_COMMITTER_DATE="$FINAL_DATE"

i=$((i + 1))
' -- --all

echo "Dates updated successfully!"#!/bin/bash

START_DATE="2026-01-01"
END_DATE="2026-04-01"

TOTAL_COMMITS=$(git rev-list --count HEAD)
echo "Total commits: $TOTAL_COMMITS"

START_TS=$(date -j -f "%Y-%m-%d" "$START_DATE" "+%s")
END_TS=$(date -j -f "%Y-%m-%d" "$END_DATE" "+%s")

TOTAL_DAYS=$(( (END_TS - START_TS) / 86400 ))
echo "Total days range: $TOTAL_DAYS"

STEP=$(( TOTAL_DAYS / TOTAL_COMMITS ))
[ $STEP -eq 0 ] && STEP=1

echo "Step days: $STEP"

i=0

git filter-branch --env-filter '
i='"$i"'
START_TS='"$START_TS"'
STEP='"$STEP"'

NEW_TS=$((START_TS + (i * STEP * 86400)))

HOUR=$((RANDOM % 8 + 10))
MINUTE=$((RANDOM % 60))
SECOND=$((RANDOM % 60))

FINAL_DATE=$(date -r $NEW_TS "+%Y-%m-%d")" $HOUR:$MINUTE:$SECOND"

export GIT_AUTHOR_DATE="$FINAL_DATE"
export GIT_COMMITTER_DATE="$FINAL_DATE"

i=$((i + 1))
' -- --all

echo "Dates updated successfully!"#!/bin/bash

START_DATE="2026-01-01"
END_DATE="2026-04-01"

TOTAL_COMMITS=$(git rev-list --count HEAD)
echo "Total commits: $TOTAL_COMMITS"

START_TS=$(date -j -f "%Y-%m-%d" "$START_DATE" "+%s")
END_TS=$(date -j -f "%Y-%m-%d" "$END_DATE" "+%s")

TOTAL_DAYS=$(( (END_TS - START_TS) / 86400 ))
echo "Total days range: $TOTAL_DAYS"

STEP=$(( TOTAL_DAYS / TOTAL_COMMITS ))
[ $STEP -eq 0 ] && STEP=1

echo "Step days: $STEP"

i=0

git filter-branch --env-filter '
i='"$i"'
START_TS='"$START_TS"'
STEP='"$STEP"'

NEW_TS=$((START_TS + (i * STEP * 86400)))

HOUR=$((RANDOM % 8 + 10))
MINUTE=$((RANDOM % 60))
SECOND=$((RANDOM % 60))

FINAL_DATE=$(date -r $NEW_TS "+%Y-%m-%d")" $HOUR:$MINUTE:$SECOND"

export GIT_AUTHOR_DATE="$FINAL_DATE"
export GIT_COMMITTER_DATE="$FINAL_DATE"

i=$((i + 1))
' -- --all

echo "Dates updated successfully!"#!/bin/bash

START_DATE="2026-01-01"
END_DATE="2026-04-01"

TOTAL_COMMITS=$(git rev-list --count HEAD)
echo "Total commits: $TOTAL_COMMITS"

START_TS=$(date -j -f "%Y-%m-%d" "$START_DATE" "+%s")
END_TS=$(date -j -f "%Y-%m-%d" "$END_DATE" "+%s")

TOTAL_DAYS=$(( (END_TS - START_TS) / 86400 ))
echo "Total days range: $TOTAL_DAYS"

STEP=$(( TOTAL_DAYS / TOTAL_COMMITS ))
[ $STEP -eq 0 ] && STEP=1

echo "Step days: $STEP"

i=0

git filter-branch --env-filter '
i='"$i"'
START_TS='"$START_TS"'
STEP='"$STEP"'

NEW_TS=$((START_TS + (i * STEP * 86400)))

HOUR=$((RANDOM % 8 + 10))
MINUTE=$((RANDOM % 60))
SECOND=$((RANDOM % 60))

FINAL_DATE=$(date -r $NEW_TS "+%Y-%m-%d")" $HOUR:$MINUTE:$SECOND"

export GIT_AUTHOR_DATE="$FINAL_DATE"
export GIT_COMMITTER_DATE="$FINAL_DATE"

i=$((i + 1))
' -- --all

echo "Dates updated successfully!"#!/bin/bash

START_DATE="2026-01-01"
END_DATE="2026-04-01"

TOTAL_COMMITS=$(git rev-list --count HEAD)
echo "Total commits: $TOTAL_COMMITS"

START_TS=$(date -j -f "%Y-%m-%d" "$START_DATE" "+%s")
END_TS=$(date -j -f "%Y-%m-%d" "$END_DATE" "+%s")

TOTAL_DAYS=$(( (END_TS - START_TS) / 86400 ))
echo "Total days range: $TOTAL_DAYS"

STEP=$(( TOTAL_DAYS / TOTAL_COMMITS ))
[ $STEP -eq 0 ] && STEP=1

echo "Step days: $STEP"

i=0

git filter-branch --env-filter '
i='"$i"'
START_TS='"$START_TS"'
STEP='"$STEP"'

NEW_TS=$((START_TS + (i * STEP * 86400)))

HOUR=$((RANDOM % 8 + 10))
MINUTE=$((RANDOM % 60))
SECOND=$((RANDOM % 60))

FINAL_DATE=$(date -r $NEW_TS "+%Y-%m-%d")" $HOUR:$MINUTE:$SECOND"

export GIT_AUTHOR_DATE="$FINAL_DATE"
export GIT_COMMITTER_DATE="$FINAL_DATE"

i=$((i + 1))
' -- --all

echo "Dates updated successfully!"
