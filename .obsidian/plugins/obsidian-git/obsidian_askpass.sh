#!/bin/sh

PROMPT="$1"
TEMP_FILE="$OBSIDIAN_GIT_CREDENTIALS_INPUT"

cleanup() {
    rm -f "$TEMP_FILE" "$TEMP_FILE.response"
}
trap cleanup EXIT

echo "$PROMPT" > "$TEMP_FILE"

TIMEOUT=30
START=$(date +%s)
while [ ! -e "$TEMP_FILE.response" ]; do
    if [ ! -e "$TEMP_FILE" ]; then
        echo "Trigger file got removed: Abort" >&2
        exit 1
    fi
    if [ $(($(date +%s) - START)) -ge $TIMEOUT ]; then
        echo "Timeout waiting for response" >&2
        exit 1
    fi
    sleep 0.1
done

RESPONSE=$(cat "$TEMP_FILE.response")

echo "$RESPONSE"
