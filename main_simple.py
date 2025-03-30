import os
import shutil
import zipfile
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import ttk
import threading

class LowLineRemoverApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Настройка окна
        self.title("Программа для удаления символов подчеркивания из имен файлов (Простая версия)")
        self.geometry("800x600")
        self.minsize(800, 600)
        
        # Переменные
        self.selected_files = []
        self.processed_files = []
        self.temp_dir = None
        
        # Создание GUI
        self.setup_ui()

    def setup_ui(self):
        # Создание фрейма для контента
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Заголовок
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Удаление символа '_' из имен файлов", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=20)

        # Фрейм для выбора файлов
        self.file_selection_frame = ctk.CTkFrame(self.main_frame)
        self.file_selection_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Кнопка выбора папки
        self.select_folder_button = ctk.CTkButton(
            self.file_selection_frame, 
            text="Выбрать папку", 
            command=self.select_folder,
            font=ctk.CTkFont(size=16),
            fg_color="#2986cc",
            hover_color="#1f5e8e",
            height=80
        )
        self.select_folder_button.pack(fill=tk.X, padx=20, pady=20)

        # Список файлов
        self.file_list_frame = ctk.CTkFrame(self.main_frame)
        self.file_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.file_list_label = ctk.CTkLabel(
            self.file_list_frame, 
            text="Выбранные файлы:", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.file_list_label.pack(anchor="w", padx=10, pady=(10, 5))

        # Фрейм с прокруткой для списка файлов
        self.file_list_scroll = ctk.CTkScrollableFrame(self.file_list_frame, height=200)
        self.file_list_scroll.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Кнопки для управления
        self.buttons_frame = ctk.CTkFrame(self.main_frame)
        self.buttons_frame.pack(fill=tk.X, padx=20, pady=10)

        self.process_button = ctk.CTkButton(
            self.buttons_frame, 
            text="Обработать файлы", 
            command=self.process_files,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2986cc",
            hover_color="#1f5e8e"
        )
        self.process_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.download_button = ctk.CTkButton(
            self.buttons_frame, 
            text="Выгрузить ZIP", 
            command=self.download_zip,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#43a047",
            hover_color="#2e7031",
            state="disabled"
        )
        self.download_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Прогресс-бар
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.main_frame, 
            variable=self.progress_var, 
            maximum=100,
            mode='determinate',
            length=100
        )
        self.progress_bar.pack(fill=tk.X, padx=20, pady=10)
        self.progress_bar.pack_forget()  # Скрыть до использования

        # Статус
        self.status_label = ctk.CTkLabel(
            self.main_frame, 
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=5)

    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Выберите папку с файлами")
        if folder_path:
            self.process_folder(folder_path)

    def process_folder(self, folder_path):
        files = []
        for root, _, filenames in os.walk(folder_path):
            for filename in filenames:
                if "_" in filename:  # Добавляем только файлы с подчеркиванием
                    file_path = os.path.join(root, filename)
                    files.append(file_path)

        if not files:
            messagebox.showinfo("Информация", "В выбранной папке нет файлов с символом подчеркивания.")
            return

        self.selected_files = files
        self.update_file_list()

    def update_file_list(self):
        # Очистка текущего списка
        for widget in self.file_list_scroll.winfo_children():
            widget.destroy()

        # Добавление файлов в список
        for i, file_path in enumerate(self.selected_files):
            file_name = os.path.basename(file_path)
            new_name = file_name.replace("_", "")
            
            file_frame = ctk.CTkFrame(self.file_list_scroll)
            file_frame.pack(fill=tk.X, pady=2)
            
            file_label = ctk.CTkLabel(
                file_frame, 
                text=f"{i+1}. {file_name} → {new_name}",
                anchor="w"
            )
            file_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Обновление статуса
        self.status_label.configure(text=f"Выбрано файлов: {len(self.selected_files)}")

    def process_files(self):
        if not self.selected_files:
            messagebox.showinfo("Информация", "Не выбрано ни одного файла.")
            return

        # Создание временной директории для обработанных файлов
        if self.temp_dir:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        
        self.temp_dir = tempfile.mkdtemp()
        self.processed_files = []

        # Показать прогресс-бар
        self.progress_bar.pack(fill=tk.X, padx=20, pady=10)
        self.progress_var.set(0)
        
        # Запуск обработки в отдельном потоке
        threading.Thread(target=self.process_files_thread).start()

    def process_files_thread(self):
        total_files = len(self.selected_files)
        
        for i, file_path in enumerate(self.selected_files):
            # Обновление прогресс-бара
            progress = int((i / total_files) * 100)
            self.progress_var.set(progress)
            self.update_status(f"Обработка: {i+1}/{total_files}")
            
            file_name = os.path.basename(file_path)
            new_name = file_name.replace("_", "")
            
            # Если имя не изменилось, пропускаем
            if new_name == file_name:
                continue
                
            # Копирование файла с новым именем
            new_path = os.path.join(self.temp_dir, new_name)
            shutil.copy2(file_path, new_path)
            self.processed_files.append(new_path)
        
        # Обновление UI в главном потоке
        self.after(0, self.finish_processing)

    def finish_processing(self):
        # Обновление прогресс-бара до 100%
        self.progress_var.set(100)
        self.update_status(f"Обработано файлов: {len(self.processed_files)}")
        
        # Активация кнопки выгрузки
        if self.processed_files:
            self.download_button.configure(state="normal")
            messagebox.showinfo("Готово", f"Обработано файлов: {len(self.processed_files)}")
        else:
            messagebox.showinfo("Информация", "Нет файлов для обработки.")

    def download_zip(self):
        if not self.processed_files:
            messagebox.showinfo("Информация", "Нет обработанных файлов для выгрузки.")
            return
            
        # Выбор места сохранения ZIP-архива
        zip_path = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("ZIP архивы", "*.zip")],
            title="Сохранить ZIP-архив как"
        )
        
        if not zip_path:
            return
            
        # Создание ZIP-архива
        try:
            self.update_status("Создание ZIP-архива...")
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in self.processed_files:
                    file_name = os.path.basename(file_path)
                    zipf.write(file_path, file_name)
                    
            self.update_status(f"ZIP-архив сохранен: {os.path.basename(zip_path)}")
            messagebox.showinfo("Успех", f"ZIP-архив успешно сохранен:\n{zip_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать ZIP-архив:\n{str(e)}")

    def update_status(self, message):
        self.status_label.configure(text=message)
        self.update_idletasks()

    def on_closing(self):
        # Очистка временных файлов
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except:
                pass
        self.destroy()

if __name__ == "__main__":
    try:
        app = LowLineRemoverApp()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
    except Exception as e:
        print(f"Критическая ошибка при запуске программы: {e}")
        input("Нажмите Enter для выхода...") 