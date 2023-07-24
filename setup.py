import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Game",
    options={
        "build_exe": {
            "packages":["pygame", "OpenGL", "PIL", "numpy", "pubsub"],
            "include_files":["localizations.dat", "textures"],
        }
    },
    executables = executables
)
