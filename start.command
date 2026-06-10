#!/bin/bash
# Перейти в папку скрипта (где бы он ни лежал)
cd "$(dirname "$0")"

echo "=== RX Training Portal ==="
echo "Обновляю код..."
git pull origin claude/notebooklm-py-xgrxa7 2>/dev/null && echo "Обновлено." || echo "Код актуален."

echo "Запускаю сервер..."
# Открыть браузер через 4 секунды после запуска сервера
(sleep 4 && open http://localhost:8000) &

# Запустить сервер (caffeinate не даёт Mac уснуть)
caffeinate -i python3 run.py
