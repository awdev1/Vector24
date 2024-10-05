from cx_Freeze import setup, Executable

# Define your script and options
setup(
    name="Vector24",
    version="1.0",
    description="Description of your application",
    executables=[Executable("main.py", icon="icon.ico")],
)
