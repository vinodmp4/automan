from cx_Freeze import setup, Executable
setup(name = "AutoMan",
      version = "0.0.1.0",
      description="AutoMan pre-alpha",
      executables=[Executable("AutoMan.py")])
