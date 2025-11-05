from setuptools import setup, find_packages

setup(
    name="correspondence-management-system",
    version="1.0.0",
    description="نظام إدارة المراسلات - لتسجيل وإدارة سجلات الوارد والصادر",
    author="فريق التطوير",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.5.0",
        "openpyxl>=3.0.0", 
        "python-docx>=0.8.0",
        "reportlab>=3.6.0",
        "fpdf>=1.7.0",
        "Pillow>=9.0.0"
    ],
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'correspondence-system=main:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8", 
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)