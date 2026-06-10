#!/bin/bash
# Запустите этот скрипт один раз из папки проекта:
#   bash create_desktop_app.sh
# На рабочем столе появится приложение "RX Portal.app"

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_PATH="$HOME/Desktop/RX Portal.app"

# AppleScript для запуска портала
APPLESCRIPT="
on run
    set projectDir to \"$PROJECT_DIR\"
    tell application \"Terminal\"
        activate
        set w to do script \"cd '\" & projectDir & \"' && git pull origin claude/notebooklm-py-xgrxa7 2>/dev/null | tail -1; echo 'Запускаю сервер...'; caffeinate -i python3 run.py\"
        set custom title of w to \"RX Training Portal\"
    end tell
    delay 4
    open location \"http://localhost:8000\"
end run
"

# Компилируем в .app
osacompile -o "$APP_PATH" -e "$APPLESCRIPT"

# Меняем иконку на что-то более красивое (используем системную иконку интернета)
ICON_SOURCE="/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/BookmarkIcon.icns"
if [ -f "$ICON_SOURCE" ]; then
    cp "$ICON_SOURCE" "$APP_PATH/Contents/Resources/applet.icns"
fi

# Обновить иконку в Dock/Finder
touch "$APP_PATH"
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f "$APP_PATH" 2>/dev/null || true

echo ""
echo "✓ Готово! На рабочем столе появилось приложение: RX Portal"
echo "  Двойной клик → откроется терминал и браузер автоматически."
