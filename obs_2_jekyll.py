import argparse
import re
import os
from pathlib import Path
from datetime import datetime
import shutil
import yaml


parser = argparse.ArgumentParser()
parser.add_argument('md_path', help='file path')
args = parser.parse_args()

config = yaml.safe_load(open("config.yaml"))

IMAGE_SOURCE_PATH = Path(config["IMAGE_SOURCE_PATH"])
JEKYLL_PATH = Path(config['JEKYLL_PATH'])
IMAGE_PATH = "/images/"
IMAGE_COPY_PATH = JEKYLL_PATH.joinpath("images/")
POST_PATH = JEKYLL_PATH.joinpath("_posts/")
INPUT_PATH = Path(args.md_path)
AUTHOR = config['AUTHOR']

image_pattern = r'\[\[(.*?)\]\]'

def copy_image_to_blog(image_name):
    source_path = IMAGE_SOURCE_PATH.joinpath(image_name)
    dest_path = IMAGE_COPY_PATH.joinpath(image_name)
    shutil.copy2(source_path, dest_path)

def check_line(line):
    if line.startswith("![["):
        image_start = "![image](" + IMAGE_PATH
        image_end = ")\n"
        match = re.search(image_pattern, line)
        if match:
            copy_image_to_blog(match.group(1))
            return image_start + match.group(1) + image_end

    return line


def main():
    with open(INPUT_PATH, "r") as md_file:
        lines_list = md_file.readlines()

    new_lines = [
        "---\n",
        "layout: post\n",
        f"author: {AUTHOR}\n",
        "---\n",
        "\n"
        ]

    for line in lines_list:
        new_lines.append(check_line(line))

    def create_new_file_name(path: Path):
        base_name = path.stem
        base_name = base_name.replace(" ","-").replace("_","-")
        c_time = os.path.getctime(args.md_path)
        dt_c = datetime.fromtimestamp(c_time)
        date_string = dt_c.strftime("%Y-%m-%d") + "-[" + AUTHOR + "]-"
        return POST_PATH.joinpath(date_string + base_name + ".md")

    jekyll_md_file = create_new_file_name(INPUT_PATH)

    with open(jekyll_md_file, "w+") as new_md_file:
        new_md_file.writelines(new_lines)

if __name__ == "__main__":
    main()

