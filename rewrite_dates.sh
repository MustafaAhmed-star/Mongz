#!/bin/ba
# عدد الأيام من Jan → Apr
START_DATE="2026-01-01"
END_DATE="2026-04-01"

# عدد الـ commits
TOTAL_COMMITS=$(git rev-list --count HEAD)

echo "Total commits: $TOTAL_COMMITS"

# احسب الفرق بالأيام
TOTAL_DAYS=$(( ( $(date -d "$END_DATE" +%s) - $(date -d "$START_DATE" +%s) ) / 86400 ))

echo "Total days range: $TOTAL_DAYS"

# احسب step
STEP=$(( TOTAL_DAYS / TOTAL_COMMITS "

INDEX=0

git filter-branch --env-filter '
    INDEX='$INDEX'
    START_DATE="'$START_DATE'"
    STEP='$STEP'

    NEW_DATE=$(date -d "$START_DATE +$((INDEX * STEP)) days" +"%Y-%m-%d")

    # ساعات عشوائية (شكل طبيعي)
    HOUR=$((RANDOM % 8 + 10))   # من 10 صباحًا إلى 6 مساءً
    MINUTE=$((RANDOM % 60))
    SECOND=$((RANDOM % 60))

    FINAL_DATE="$NEW_DATE $HOUR:$MINUTE:$SECOND"

    export GIT_AUTHOR_DATE="$FINAL_DATE"
    export GIT_COMMITTER_DATE="
