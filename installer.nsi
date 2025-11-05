; installer.nsi

!include "MUI2.nsh"

; اسم التطبيق والإصدار
Name "نظام إدارة المراسلات"
OutFile "نظام_إدارة_المراسلات_الإصدار_2.0.exe"
InstallDir "$PROGRAMFILES\نظام إدارة المراسلات"

; إعدادات واجهة المستخدم
!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"
!define MUI_ABORTWARNING

; صفحات المثبت
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "license.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; صفحات إلغاء التثبيت
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; اللغات
!insertmacro MUI_LANGUAGE "Arabic"

Section "تثبيت النظام"

  SetOutPath "$INSTDIR"

  ; نسخ الملفات
  File /r "dist\نظام_إدارة_المراسلات\*.*"
  File "icon.ico"

  ; إنشاء اختصار في قائمة ابدأ
  CreateDirectory "$SMPROGRAMS\نظام إدارة المراسلات"
  CreateShortCut "$SMPROGRAMS\نظام إدارة المراسلات\نظام إدارة المراسلات.lnk" "$INSTDIR\نظام_إدارة_المراسلات.exe" "" "$INSTDIR\icon.ico"
  CreateShortCut "$DESKTOP\نظام إدارة المراسلات.lnk" "$INSTDIR\نظام_إدارة_المراسلات.exe" "" "$INSTDIR\icon.ico"

  ; كتابة معلومات الإصدار في السجل
  WriteRegStr HKLM "SOFTWARE\نظام إدارة المراسلات" "InstallDir" "$INSTDIR"
  WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\نظام إدارة المراسلات" "DisplayName" "نظام إدارة المراسلات"
  WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\نظام إدارة المراسلات" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\نظام إدارة المراسلات" "DisplayIcon" "$INSTDIR\icon.ico"
  WriteRegDWORD HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\نظام إدارة المراسلات" "NoModify" 1
  WriteRegDWORD HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\نظام إدارة المراسلات" "NoRepair" 1

  ; إنشاء ملف إلغاء التثبيت
  WriteUninstaller "$INSTDIR\uninstall.exe"

SectionEnd

Section "Uninstall"

  ; حذف الملفات
  RMDir /r "$INSTDIR"

  ; حذف الاختصارات
  Delete "$SMPROGRAMS\نظام إدارة المراسلات\نظام إدارة المراسلات.lnk"
  Delete "$DESKTOP\نظام إدارة المراسلات.lnk"
  RMDir "$SMPROGRAMS\نظام إدارة المراسلات"

  ; حذف من السجل
  DeleteRegKey HKLM "SOFTWARE\نظام إدارة المراسلات"
  DeleteRegKey HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\نظام إدارة المراسلات"

SectionEnd