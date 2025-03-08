import os
import pathlib
import shutil
import sys
import zipfile

from cx_Freeze import Freezer, Executable

FILE_ROOT_PATH = pathlib.Path(__file__).parent

# Define the entry point of your application
executable = Executable(
  script="pymol/__init__.py",  # Replace with your script name
  target_name="Open-Source-PyMOL",  # Optional: Set the name of the .exe file
  #base="Win32GUI",  # Uncomment to suppress command window
  icon=pathlib.Path(FILE_ROOT_PATH.parent / "alternative_design" / "logo.ico")
)

# Create a freezer instance
freezer = Freezer(
  executables=[executable],
  includes=[
    "PyQt5.uic", "pymol.povray", "pymol.parser"
  ],
  excludes=[],  # Exclude unnecessary modules
  include_files=[],  # Include additional files
  zip_exclude_packages=[]
)


def remove_dist_info_folders(directory: pathlib.Path):
  """
  Remove all folders ending with .dist-info from the specified directory.

  Args:
      directory (str): The path to the directory to search.
  """
  for root, dirs, files in os.walk(str(directory)):
    for dir_name in dirs:
      if dir_name.endswith(".dist-info"):
        dist_info_path = os.path.join(root, dir_name)
        shutil.rmtree(dist_info_path)


if __name__ == '__main__':
  if sys.platform == "darwin":
    tmp_extension = "macosx-10.9"
    tmp_os_name = "macos"
    tmp_cmd_os_name = "darwin"
  else:
    tmp_extension = "linux"
    tmp_os_name = "linux"
    tmp_cmd_os_name = "x86_64-linux-gnu"
  freezer.freeze()
  with zipfile.ZipFile(pathlib.Path(f"{FILE_ROOT_PATH}/build/exe.{tmp_extension}-x86_64-3.11/lib/library.zip"), 'r') as zip_ref:
    zip_ref.extractall(pathlib.Path(f"{FILE_ROOT_PATH}/build/exe.{tmp_extension}-x86_64-3.11/lib"))
  _CMD_FROM_BUILD_DIR = pathlib.Path(FILE_ROOT_PATH.parent / "buildDir" / f"_cmd.cpython-311-{tmp_cmd_os_name}.so")
  _CMD_FROM_PRE_BUILT_DIR = pathlib.Path(FILE_ROOT_PATH.parent / f"pre-built/{tmp_os_name}" / f"_cmd.cpython-311-{tmp_cmd_os_name}.so")
  if _CMD_FROM_BUILD_DIR.exists():
    shutil.copy(
      _CMD_FROM_BUILD_DIR,
      pathlib.Path(FILE_ROOT_PATH / f"build/exe.{tmp_extension}-x86_64-3.11/lib/pymol" / f"_cmd.cpython-311-{tmp_cmd_os_name}.so")
    )
  else:
    shutil.copy(
      _CMD_FROM_PRE_BUILT_DIR,
      pathlib.Path(FILE_ROOT_PATH / f"build/exe.{tmp_extension}-x86_64-3.11/lib/pymol" / f"_cmd.cpython-311-{tmp_cmd_os_name}.so")
    )
  for tmp_shared_object in os.listdir(pathlib.Path(FILE_ROOT_PATH.parent / f"pre-built/{tmp_os_name}/lib_64")):
    shutil.copy(
      pathlib.Path(FILE_ROOT_PATH.parent / f"pre-built/{tmp_os_name}/lib_64" / tmp_shared_object),
      pathlib.Path(FILE_ROOT_PATH / f"build/exe.{tmp_extension}-x86_64-3.11/lib" / tmp_shared_object)
    )
  remove_dist_info_folders(pathlib.Path(FILE_ROOT_PATH / f"build/exe.{tmp_extension}-x86_64-3.11/lib"))
  shutil.copytree(
    str(pathlib.Path(FILE_ROOT_PATH / "pymol/wizard")),
    str(pathlib.Path(FILE_ROOT_PATH / f"build/exe.{tmp_extension}-x86_64-3.11/lib/pymol/wizard")),
    dirs_exist_ok=True
  )
  shutil.copytree(
    str(pathlib.Path(FILE_ROOT_PATH / "pymol/data/startup")),
    str(pathlib.Path(FILE_ROOT_PATH / f"build/exe.{tmp_extension}-x86_64-3.11/lib/pymol/data/startup")),
    dirs_exist_ok=True
  )
