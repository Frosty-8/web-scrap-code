# Variables
PYTHON = python
PIP = pip
VENV = venv
MAIN_SCRIPT = app.py

.PHONY: all install run clean

all: install run

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV)\Scripts\pip install --upgrade pip
	$(VENV)\Scripts\pip install -r requirements.txt

install-lib:
	$(VENV)\Scripts\pip install -r requirements.txt

run:
	powershell -Command "& { . $(VENV)\Scripts\Activate.ps1; python $(MAIN_SCRIPT) }"

clean:
	if exist $(VENV) rmdir /s /q $(VENV)
	if exist __pycache__ rmdir /s /q __pycache__
	del /s /q *.pyc *.pyo 2>nul