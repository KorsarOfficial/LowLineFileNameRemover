@echo off
echo Запуск упрощенной версии программы для удаления подчеркиваний из имен файлов...
echo.

python main_simple.py

if %errorlevel% neq 0 (
    echo.
    echo Произошла ошибка при запуске программы!
    echo Убедитесь, что Python установлен и доступен в системном пути.
    echo.
    echo Попробуйте сначала установить зависимости:
    echo python install_dependencies.py
    echo.
    pause
    exit /b 1
)

exit /b 0 