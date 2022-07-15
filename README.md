# Project RAS (RGPV AUTO SCRAPER) 
![](https://img.shields.io/static/v1?label=Dev&message=Rajat&color=black&link=http://github.com/RajatMuzumdar&style=for-the-badge)
![](https://img.shields.io/static/v1?label=Dev&message=Kushagra&color=black&link=http://github.com/kushaagr&style=for-the-badge)
![](https://img.shields.io/badge/semester-project-blueviolet?&link=http://github.com/RajatMuzumdar/RGPV_AUTO_SCRAP&link=http://github.com/kushaagr/RGPV_AUTO_SCRAP&style=for-the-badge) 
![](https://img.shields.io/github/license/RajatMuzumdar/RGPV_AUTO_SCRAP?style=flat-square)

![](https://img.shields.io/tokei/lines/github/RajatMuzumdar/RGPV_AUTO_SCRAP)
![](https://img.shields.io/github/directory-file-count/RajatMuzumdar/RGPV_AUTO_SCRAP)
![](https://img.shields.io/github/languages/code-size/RajatMuzumdar/RGPV_AUTO_SCRAP)
![](https://img.shields.io/github/repo-size/RajatMuzumdar/RGPV_AUTO_SCRAP)

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
        $hideChrome (optional)
```

- Watch and Wait...

## Errors? (Troubleshoot)
- If Tessaract is not installed system-wide then find absolute path to Tesseract.exe and set "TESS_DRIVER" in config.py to the absolute path

## Screenshots
![SS1 29 Friday 15 18-33-46](https://user-images.githubusercontent.com/68564934/179230924-32ecdd4a-d499-40ee-86f7-fb19d3157a63.png)
![SS2 29 Friday 15 18-34-36](https://user-images.githubusercontent.com/68564934/179231051-be61e249-6178-4e52-a7dc-e26e642a404d.png)
![SS3 29 Friday 15 18-35-28](https://user-images.githubusercontent.com/68564934/179231060-0374ed1a-d376-40b6-89c3-ef61078b7cf8.png)
![SS4 29 Friday 15 18-35-36](https://user-images.githubusercontent.com/68564934/179231069-a20b4df3-f14e-4603-ae10-a2d75909a24d.png)
