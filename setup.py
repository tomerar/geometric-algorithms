from cx_Freeze import setup, Executable

base = None    

executables = [Executable("main.py", base=base)]

packages = ["idna", "pandas", "matplotlib", "numpy", "pathlib", "xlsxwriter", "tkinter"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "geo_algos",
    options = options,
    version = "0.5",
    description = 'algo_project',
    executables = executables
)