import subprocess
import sys
import os
import platform

def check_tkinter():
    print("Проверка наличия tkinter...")
    try:
        import tkinter
        print("tkinter уже установлен.")
        return True
    except ImportError:
        print("ВНИМАНИЕ: tkinter не найден!")
        print("tkinter - это встроенная библиотека Python, которая не может быть установлена через pip.")
        print("\nВарианты решения проблемы:")
        
        system = platform.system()
        if system == "Windows":
            print("1. Переустановите Python, выбрав опцию 'tcl/tk and IDLE' при установке")
            print("2. Или выполните команду в PowerShell от имени администратора:")
            print("   python -m pip install --force-reinstall --upgrade tk")
        elif system == "Linux":
            print("Установите tkinter через менеджер пакетов:")
            print("Для Ubuntu/Debian: sudo apt-get install python3-tk")
            print("Для Fedora: sudo dnf install python3-tkinter")
            print("Для Arch Linux: sudo pacman -S tk")
        elif system == "Darwin":  # macOS
            print("Установите tkinter через homebrew:")
            print("brew install python-tk")
        
        return False

def install_requirements():
    # Проверка наличия tkinter
    tkinter_installed = check_tkinter()
    if not tkinter_installed:
        response = input("\nХотите продолжить установку остальных зависимостей? (y/n): ")
        if response.lower() != 'y':
            print("Установка прервана.")
            return False
    
    print("\nУстановка основных зависимостей...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при установке зависимостей: {e}")
        return False
    
    # Проверка установки tkinterdnd2 и установка, если необходимо
    try:
        import tkinterdnd2
        print("tkinterdnd2 уже установлен.")
    except ImportError:
        print("Установка tkinterdnd2...")
        
        # Разные способы установки в зависимости от ОС
        system = platform.system()
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "git+https://github.com/pmgagne/tkinterdnd2.git"
            ])
        except:
            print("Ошибка при установке tkinterdnd2. Функция перетаскивания файлов может быть недоступна.")
    
    return True

if __name__ == "__main__":
    print("Установка зависимостей для программы...")
    success = install_requirements()
    
    if success:
        print("\nУстановка завершена! Теперь вы можете запустить программу с помощью 'python main.py'")
    else:
        print("\nУстановка завершена с ошибками. Проверьте сообщения выше и исправьте проблемы перед запуском программы.") 