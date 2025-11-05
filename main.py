import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import os
import shutil
import sys
import pandas as pd

# إضافة المسارات إلى sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'gui'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from database import DatabaseManager
from utils.file_manager import FileManager
from utils.export_manager import ExportManager
from utils.printer import PrinterManager
from gui.main_window import MainWindow

class CorrespondenceManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_environment()
        
        # تهيئة المديرين
        self.db_manager = DatabaseManager()
        self.file_manager = FileManager()
        self.export_manager = ExportManager(self.db_manager)
        self.printer_manager = PrinterManager(self.db_manager, self.export_manager)
        
        # التحقق من المكتبات المطلوبة
        if not self.check_required_libraries():
            return
        
        # إنشاء الواجهة الرئيسية
        try:
            self.main_window = MainWindow(self.root, self.db_manager, self.file_manager, 
                                        self.export_manager, self.printer_manager)
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحميل الواجهة: {e}")
            self.root.destroy()
            return

    def setup_environment(self):
        """إعداد بيئة التطبيق"""
        # إنشاء المجلدات المطلوبة
        folders = ['data', 'data/attachments', 'backups', 'reports', 'temp']
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
        
        # إعداد النافذة الرئيسية
        self.root.title("نظام إدارة المراسلات - الإصدار 2.0")
        self.root.geometry("1200x700")
        
        # تحسين مظهر الواجهة
        self.setup_styles()
        
        # مركزية النافذة
        self.center_window()

    def setup_styles(self):
        """إعداد أنماط الواجهة"""
        style = ttk.Style()
        
        # محاولة استخدام tema حديث
        try:
            style.theme_use('vista')
        except:
            try:
                style.theme_use('clam')
            except:
                pass
        
        # تخصيص الأنماط
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'), foreground='#2C3E50')
        style.configure('Stats.TLabel', font=('Arial', 10, 'bold'))
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'))

    def center_window(self):
        """مركزية النافذة على الشاشة"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def check_required_libraries(self):
        """التحقق من المكتبات المطلوبة"""
        required_libraries = {
            'pandas': 'pandas',
            'openpyxl': 'openpyxl', 
            'docx': 'python-docx',
            'reportlab': 'reportlab'
        }
        
        missing_libraries = []
        
        for import_name, package_name in required_libraries.items():
            try:
                __import__(import_name)
            except ImportError:
                missing_libraries.append(package_name)
        
        if missing_libraries:
            missing_text = "\n".join(missing_libraries)
            messagebox.showerror(
                "مكتبات مفقودة", 
                f"المكتبات التالية غير مثبتة:\n{missing_text}\n\n"
                f"يرجى تثبيتها باستخدام:\n"
                f"pip install {' '.join(missing_libraries)}"
            )
            return False
        
        return True

    def run(self):
        """تشغيل التطبيق"""
        try:
            # تكبير النافذة بعد تحميل كل شيء
            self.root.after(100, self.maximize_window)
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ غير متوقع: {e}")

    def maximize_window(self):
        """تكبير النافذة"""
        self.root.state('zoomed')

def main():
    """الدالة الرئيسية"""
    try:
        # التحقق من إصدار Python
        if sys.version_info < (3, 7):
            messagebox.showerror("خطأ", "يتطلب النظام Python 3.7 أو أحدث")
            return
        
        # إنشاء وتشغيل التطبيق
        app = CorrespondenceManagementSystem()
        app.run()
        
    except ImportError as e:
        messagebox.showerror("خطأ استيراد", f"خطأ في استيراد المكتبات: {e}")
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ غير متوقع: {e}")

if __name__ == "__main__":
    main()