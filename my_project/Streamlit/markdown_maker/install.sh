#!/bin/bash
set -e

pip install -r requirements.txt

if [ -z "$OPENAI_API_KEY" ]; then
  echo "환경변수 OPENAI_API_KEY가 필요합니다. (예: export OPENAI_API_KEY=sk-xxxxxx)"
  exit 1
fi

grep -v '^OPENAI_API_KEY=' .env 2>/dev/null > .env.tmp || true
echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> .env.tmp
mv .env.tmp .env
echo "OPENAI_API_KEY가 .env에 저장되었습니다."