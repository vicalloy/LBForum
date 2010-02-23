@echo off
@call %~dp0..\lbforum_env\Scripts\activate.bat
@set mg=python.exe %~dp0..\sites\default\manage.py
@cd %~dp0..\src
@cmd
