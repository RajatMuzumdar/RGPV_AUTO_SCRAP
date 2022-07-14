# Project RAS (RGPV AUTO SCRAPER)

## What is this?
A python script which scrapes results from [RGPV results](http://result.rgpv.ac.in/Result/ProgramSelect.aspx) website and extracts them to an excel sheet (.xlsx file)

## How to use it?
- Install [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)
- Also make sure you have Python (>= 3.5) installed
- Run setup.bat
- Run main.py or run.bat
- Provide input when prompted in format:  

```
    >>? $BranchName 
        $EnrollmentNumberCommonPart 
        $RollNosFrom $To
```

- Watch and Wait...

## Errors? (Troubleshoot)
- If Tessaract is not installed system-wide then find absolute path to Tesseract.exe and set "TESS_DRIVER" in config.py to the absolute path
