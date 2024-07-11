import os
import pypandoc
from pypandoc.pandoc_download import download_pandoc


def _install_pandoc(current_dir: str = "./"):
    for filename in os.listdir(current_dir):
        if filename.startswith("pandoc") and filename.endswith(".deb"):
            return False
    return True


def convert_to_md(file_path: str):
    if _install_pandoc():
        download_pandoc()

    file = os.path.basename(file_path)
    file_name, _ = os.path.splitext(file)

    output_path = os.path.join("output", file_name)
    return pypandoc.convert_file(file_path, "md", outputfile=output_path + ".md")
