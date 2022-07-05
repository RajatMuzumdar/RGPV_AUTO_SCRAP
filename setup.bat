python --version 2>NUL
IF errorlevel 1 (
    IF /I %PROCESSOR_ARCHITECTURE% == AMD64 (
rem         python-3.10.4-amd64.exe
		echo UNSATISFIED REQUIREMENT: PYTHON X86
    ) ELSE (
rem         python-3.10.4.exe
		echo UNSATISFIED REQUIREMENT: PYTHON
    )
) ELSE (
	pip install -r requirements-novernum.txt
)

rem start tesseract-setup
ECHO REQUIREMENT: Tesseract-OCR

IF /I %PROCESSOR_ARCHITECTURE% == AMD64 (
    SET TESSPATH=C:\Program Files ^(x86^)\Tesseract-OCR\tesseract.exe
) ELSE (
    SET TESSPATH=C:\Program Files\Tesseract-OCR\tesseract.exe
)

echo TESS_DRIVER = r'%TESSPATH%' > config.py
echo BROW_DRIVER = '%USERPROFILE:\=/%/.wdm/drivers/chromedriver/win32/ DRIVER_VERSION /chromedriver' >> config.py


REM SET BROWDRIVERPATH=%USERPROFILE:\=/%.wdm/drivers/chromedriver/win32/99.0.4844.51/chromedriver

REM https://superuser.com/questions/321988/how-do-i-determine-if-my-windows-is-32-bit-or-64-bit-using-a-command#:~:text=From%20an%20elevated%20command%20prompt,or%20%2264%2Dbit%22.
