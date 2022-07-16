@echo off

IF /I %PROCESSOR_ARCHITECTURE% == AMD64 (
    SET TESSPATH=C:\Program Files ^(x86^)\Tesseract-OCR\tesseract.exe
) ELSE (
    SET TESSPATH=C:\Program Files\Tesseract-OCR\tesseract.exe
)
echo TESS_DRIVER = r'%TESSPATH%' > config.py
echo BROW_DRIVER = '%USERPROFILE:\=/%/.wdm/drivers/chromedriver/win32/ DRIVER_VERSION /chromedriver' >> config.py
rem start tesseract-setup
ECHO REQUIREMENT: Tesseract-OCR — download from
ECHO              https://github.com/UB-Mannheim/tesseract/wiki && ECHO. 

python --version 2>NUL
IF errorlevel 1 (
    IF /I %PROCESSOR_ARCHITECTURE% == AMD64 (
        rem python-3.10.4-amd64.exe
		ECHO UNSATISFIED REQUIREMENT: PYTHON X86
		ECHO INSTALL PYTHON ^(X86^)
    ) ELSE (
        rem python-3.10.4.exe
		ECHO UNSATISFIED REQUIREMENT: PYTHON
		ECHO INSTALL PYTHON
    )
) ELSE (
	ECHO is installed.
    start cmd /C "pip install --user -r requirements.txt & TIMEOUT /T 10"
    ECHO. && ECHO Setup complete.
)

PAUSE

REM SET BROWDRIVERPATH=%USERPROFILE:\=/%.wdm/drivers/chromedriver/win32/99.0.4844.51/chromedriver
REM https://superuser.com/questions/321988/how-do-i-determine-if-my-windows-is-32-bit-or-64-bit-using-a-command#:~:text=From%20an%20elevated%20command%20prompt,or%20%2264%2Dbit%22.
