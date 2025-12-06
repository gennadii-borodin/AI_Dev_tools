@echo off
echo Starting Мини-анкета application...
echo Make sure you have Python 3.12 and uvx installed
echo.
uvx --python 3.12 --with fastapi --with uvicorn --with pydantic python main.py
pause