@echo off
title Egg Price Pipeline

echo =====================================
echo Starting Egg Price Data Pipeline
echo =====================================
echo.

call D:\egg_price_procject\.venv\Scripts\activate.bat

python -u D:\egg_price_procject\data_scrap\egg_scraper.py

if %ERRORLEVEL% neq 0 goto error

python -u D:\egg_price_procject\data_scrap\festival_generator.py

if %ERRORLEVEL% neq 0 goto error

python -u D:\egg_price_procject\data_scrap\weather_scraper.py

if %ERRORLEVEL% neq 0 goto error

python -u D:\egg_price_procject\analysis\feature_extraction.py

if %ERRORLEVEL% neq 0 goto error

echo.
echo =====================================
echo ALL SCRIPTS COMPLETED SUCCESSFULLY
echo =====================================
pause
exit

:error
echo.
echo =====================================
echo PIPELINE FAILED
echo =====================================
pause