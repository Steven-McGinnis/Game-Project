import cx_Freeze

executables = [
    cx_Freeze.Executable("start_screen.py"),
    cx_Freeze.Executable("main.py")
]

cx_Freeze.setup(
    name="Zombie Survival",
    options={
        "build_exe": {
            "packages":["pygame", "OpenGL", "PIL", "numpy", "pubsub", "memory_profiler", "re"],
            "include_files":["localizations.dat", "textures", "sounds"],
        }
    },
    executables = executables
)
