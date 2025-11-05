import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="data/database.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """إنشاء اتصال بقاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def init_database(self):
        """تهيئة قاعدة البيانات والجداول"""
        os.makedirs("data/attachments", exist_ok=True)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # جدول جهات الوارد
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS incoming_sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول جهات الصادر
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS outgoing_destinations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول أنواع الوارد
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS incoming_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الموظفين - مع إضافة الأعمدة الجديدة إذا لم تكن موجودة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT,
                position TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # إضافة الأعمدة الجديدة إذا لم تكن موجودة
        self.add_missing_columns(cursor)
        
        # جدول الاختصاصات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS specializations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول سجلات الوارد
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS incoming_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_number TEXT UNIQUE NOT NULL,
                incoming_number TEXT NOT NULL,
                serial_number TEXT NOT NULL,
                title TEXT NOT NULL,
                incoming_source_id INTEGER,
                incoming_type_id INTEGER,
                employee_id INTEGER,
                specialization_id INTEGER,
                registration_date DATE DEFAULT CURRENT_DATE,
                details TEXT,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (incoming_source_id) REFERENCES incoming_sources (id),
                FOREIGN KEY (incoming_type_id) REFERENCES incoming_types (id),
                FOREIGN KEY (employee_id) REFERENCES employees (id),
                FOREIGN KEY (specialization_id) REFERENCES specializations (id)
            )
        ''')
        
        # جدول سجلات الصادر
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS outgoing_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_number TEXT UNIQUE NOT NULL,
                outgoing_number TEXT NOT NULL,
                serial_number TEXT NOT NULL,
                title TEXT NOT NULL,
                outgoing_destination_id INTEGER,
                employee_id INTEGER,
                specialization_id INTEGER,
                registration_date DATE DEFAULT CURRENT_DATE,
                details TEXT,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (outgoing_destination_id) REFERENCES outgoing_destinations (id),
                FOREIGN KEY (employee_id) REFERENCES employees (id),
                FOREIGN KEY (specialization_id) REFERENCES specializations (id)
            )
        ''')
        
        # جدول المرفقات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attachments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id INTEGER NOT NULL,
                record_type TEXT NOT NULL, -- 'incoming' or 'outgoing'
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_size INTEGER,
                file_type TEXT,
                upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                description TEXT
            )
        ''')
        
        # جدول إعدادات النظام
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key TEXT UNIQUE NOT NULL,
                setting_value TEXT,
                description TEXT,
                updated_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # إدخال بيانات أولية
        self.insert_initial_data(cursor)
        
        conn.commit()
        conn.close()
    
    def add_missing_columns(self, cursor):
        """إضافة الأعمدة المفقودة إلى الجداول الموجودة"""
        try:
            # التحقق من وجود الأعمدة في جدول الموظفين وإضافتها إذا لم تكن موجودة
            columns_to_add = [
                ('email', 'TEXT'),
                ('phone', 'TEXT'),
                ('fax_count', 'INTEGER DEFAULT 0'),
                ('email_count', 'INTEGER DEFAULT 0')
            ]
            
            for column_name, column_type in columns_to_add:
                try:
                    cursor.execute(f"ALTER TABLE employees ADD COLUMN {column_name} {column_type}")
                    print(f"تم إضافة العمود {column_name} إلى جدول الموظفين")
                except sqlite3.OperationalError as e:
                    if "duplicate column name" not in str(e):
                        print(f"خطأ في إضافة العمود {column_name}: {e}")
        except Exception as e:
            print(f"خطأ في إضافة الأعمدة المفقودة: {e}")
    
    def insert_initial_data(self, cursor):
        """إدخال البيانات الأولية للكيانات المرجعية"""
        
        # جهات الوارد
        incoming_sources = [
            ('وزارة الداخلية', 'جهات حكومية - وزارة الداخلية'),
            ('وزارة الصحة', 'جهات حكومية - وزارة الصحة'),
            ('القطاع الخاص', 'شركات ومؤسسات القطاع الخاص'),
            ('جهات أجنبية', 'جهات دولية وأجنبية'),
            ('جامعات', 'مؤسسات تعليمية وجامعات')
        ]
        
        cursor.executemany(
            'INSERT OR IGNORE INTO incoming_sources (name, description) VALUES (?, ?)',
            incoming_sources
        )
        
        # جهات الصادر
        outgoing_destinations = [
            ('رئاسة الوزراء', 'جهات حكومية - رئاسة الوزراء'),
            ('البنك المركزي', 'مؤسسات مالية'),
            ('الجامعات', 'مؤسسات تعليمية'),
            ('المستشفيات', 'مؤسسات صحية'),
            ('الشركات', 'قطاع خاص وشركات')
        ]
        
        cursor.executemany(
            'INSERT OR IGNORE INTO outgoing_destinations (name, description) VALUES (?, ?)',
            outgoing_destinations
        )
        
        # أنواع الوارد
        incoming_types = [
            ('خطاب رسمي', 'مراسلات رسمية'),
            ('مذكرة', 'مذكرات داخلية'),
            ('تقرير', 'تقارير متنوعة'),
            ('بريد إلكتروني', 'مراسلات إلكترونية'),
            ('فاكس', 'مراسلات فاكس')
        ]
        
        cursor.executemany(
            'INSERT OR IGNORE INTO incoming_types (name, description) VALUES (?, ?)',
            incoming_types
        )
        
        # الموظفين - بدون الحقول الجديدة أولاً
        employees = [
            ('أحمد محمد', 'الإدارة', 'مدير', 1),
            ('فاطمة علي', 'الشؤون المالية', 'محاسب', 1),
            ('خالد إبراهيم', 'التقنية', 'مطور نظم', 1),
            ('سارة عبدالله', 'الشؤون الإدارية', 'سكرتيرة', 1),
            ('محمد حسن', 'التسويق', 'مسؤول تسويق', 1)
        ]
        
        cursor.executemany(
            'INSERT OR IGNORE INTO employees (name, department, position, is_active) VALUES (?, ?, ?, ?)',
            employees
        )
        
        # تحديث الموظفين الموجودين بإضافة البيانات الجديدة
        updated_employees = [
            ('ahmed@company.com', '0123456789', 1),
            ('fatima@company.com', '0123456790', 2),
            ('khaled@company.com', '0123456791', 3),
            ('sara@company.com', '0123456792', 4),
            ('mohamed@company.com', '0123456793', 5)
        ]
        
        for i, (email, phone, emp_id) in enumerate(updated_employees):
            try:
                cursor.execute(
                    'UPDATE employees SET email = ?, phone = ? WHERE id = ?',
                    (email, phone, emp_id)
                )
            except sqlite3.OperationalError:
                # إذا لم تكن الأعمدة موجودة بعد، تخطى التحديث
                pass
        
        # الاختصاصات
        specializations = [
            ('إداري', 'شؤون إدارية'),
            ('مالي', 'شؤون مالية'),
            ('تقني', 'شؤون تقنية'),
            ('قانوني', 'شؤون قانونية'),
            ('تسويقي', 'شؤون تسويقية')
        ]
        
        cursor.executemany(
            'INSERT OR IGNORE INTO specializations (name, description) VALUES (?, ?)',
            specializations
        )
        
        # إعدادات النظام
        settings = [
            ('company_name', 'شركة التقنية المتطورة', 'اسم الشركة'),
            ('system_language', 'ar', 'لغة النظام'),
            ('date_format', 'YYYY-MM-DD', 'تنسيق التاريخ'),
            ('backup_auto', '1', 'نسخ احتياطي تلقائي')
        ]
        
        cursor.executemany(
            'INSERT OR IGNORE INTO system_settings (setting_key, setting_value, description) VALUES (?, ?, ?)',
            settings
        )
    
    def execute_query(self, query, params=None):
        """تنفيذ استعلام مع معالجة الأخطاء"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.lastrowid
            
            conn.close()
            return result
        except Exception as e:
            print(f"خطأ في قاعدة البيانات: {e}")
            return None
    
    def execute_many(self, query, params_list):
        """تنفيذ استعلام متعدد"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"خطأ في قاعدة البيانات: {e}")
            return False
    
    def get_employee_stats(self, employee_id, start_date=None, end_date=None):
        """الحصول على إحصائيات الموظف"""
        try:
            # إحصائيات الفاكسات (الصادر)
            fax_query = """
            SELECT COUNT(*) FROM outgoing_records 
            WHERE employee_id = ?
            """
            fax_params = [employee_id]
            
            # إحصائيات الإيميلات (الوارد من نوع إيميل)
            email_query = """
            SELECT COUNT(*) FROM incoming_records 
            WHERE employee_id = ? 
            AND incoming_type_id IN (SELECT id FROM incoming_types WHERE name LIKE '%إيميل%' OR name LIKE '%email%')
            """
            email_params = [employee_id]
            
            if start_date and end_date:
                fax_query += " AND registration_date BETWEEN ? AND ?"
                email_query += " AND registration_date BETWEEN ? AND ?"
                fax_params.extend([start_date, end_date])
                email_params.extend([start_date, end_date])
            
            fax_count_result = self.execute_query(fax_query, fax_params)
            email_count_result = self.execute_query(email_query, email_params)
            
            fax_count = fax_count_result[0][0] if fax_count_result and fax_count_result[0] else 0
            email_count = email_count_result[0][0] if email_count_result and email_count_result[0] else 0
            
            return {
                'fax_count': fax_count,
                'email_count': email_count,
                'total': fax_count + email_count
            }
        except Exception as e:
            print(f"خطأ في الحصول على إحصائيات الموظف: {e}")
            return {'fax_count': 0, 'email_count': 0, 'total': 0}
    
    def update_employee_counts(self, employee_id):
        """تحديث عدادات الموظف"""
        try:
            stats = self.get_employee_stats(employee_id)
            # التحقق من وجود الأعمدة أولاً
            result = self.execute_query("PRAGMA table_info(employees)")
            columns = [row[1] for row in result] if result else []
            
            if 'fax_count' in columns and 'email_count' in columns:
                self.execute_query(
                    "UPDATE employees SET fax_count = ?, email_count = ? WHERE id = ?",
                    (stats['fax_count'], stats['email_count'], employee_id)
                )
            return True
        except Exception as e:
            print(f"خطأ في تحديث عدادات الموظف: {e}")
            return False
    
    def backup_database(self, backup_path):
        """إنشاء نسخة احتياطية من قاعدة البيانات"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            return True
        except Exception as e:
            print(f"خطأ في النسخ الاحتياطي: {e}")
            return False
    
    def restore_database(self, backup_path):
        """استعادة قاعدة البيانات من نسخة احتياطية"""
        try:
            import shutil
            shutil.copy2(backup_path, self.db_path)
            return True
        except Exception as e:
            print(f"خطأ في استعادة النسخة الاحتياطية: {e}")
            return False