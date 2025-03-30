@echo off
echo Установка зависимостей для программы удаления подчеркиваний...
echo.

python install_dependencies.py

if %errorlevel% neq 0 (
    echo.
    echo Произошла ошибка при установке зависимостей!
    echo Убедитесь, что Python установлен и доступен в системном пути.
    echo.
    pause
    exit /b 1
)

echo.
echo Установка завершена. Теперь вы можете запустить программу с помощью run.bat
echo.
pause
exit /b 0 