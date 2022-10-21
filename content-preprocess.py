# inspired by and based on https://github.com/sspaeti/second-brain-public

import os
from datetime import datetime
import shutil
from pathlib import Path
import re
import glob
import frontmatter

# - loop through directly recursively through the directory and find all the .md files
# - then loop through the files and find all the published notes
# - if file found, move it to public folder
# - copy first h1 to frontmatter as title

# git = os.getenv("git")
# secondbrain = os.getenv("secondbrain")
# secondbrain_public = os.getenv("public_secondbrain")


# define paths
# second_brain_path = str(secondbrain)  # "/tmp/second-brain-tmp"
# public_folder_path_copy = str(secondbrain_public)
# public_brain_image_path = os.path.join(public_folder_path_copy, "images")

# for now. works locally
second_brain_path = str('content-source/100 Vault')
public_folder_path_copy = str('content')
public_brain_image_path = os.path.join('content', "images")

regexp_md_images = "!\[\[(.*?)\]\](.*)\s" # BUG breaks videos it seems
h1 = "(?m)^# (.*)" # finds entire h1 line

def find_and_copy_published(second_brain_path: str, copy_to_path: str):
  """
  - find `published: true` frontmatter in private folder and move it to public folder.
  - copies h1 title (`# ..`) into frontmatter as YAML title
  """
  for root, dirs, files in os.walk(second_brain_path):
    for file in files:
      print(file)
      if file.endswith(".md"):
        file_path = os.path.join(root, file)
        # use published frontmatter instead
        with open(file_path, "r") as f:
          fmt = frontmatter.load(f)
          # print(fmt.metadata)
        if ("published" in fmt.metadata.keys()) and (fmt.metadata["published"] == True):

          # destination should be lower-case (spaces will be handled by hugo with `urlize`)
          # file_name_lower = os.path.basename(file_path).lower() # HACK unnecessary?

          print(f"publish: {file_path}")
          # copy that file to the publish notes directory
          shutil.copy(
            # file_path, os.path.join(copy_to_path, file_name_lower) # HACK unnecessary?
            file_path, os.path.join(copy_to_path, file)
          )
          
          # add h1 as title frontmatter
          add_h1_as_title_frontmatter(
            os.path.join(copy_to_path, file)
          )

def add_h1_as_title_frontmatter(file_path: str):
  print(f"start converting {file_path}")
  with open(file_path, "r") as f:

    # read line by line and search for h1
    # copy text of h1
    with open(file_path, "r") as f:
      lines = f.readlines()
      for line in lines:
        result = re.findall(h1, line)
        # print(result)
        if result:
          print(f"found h1 in {file_path} line: {line}")
          break

    # put in frontmatter if any
    if len(result) > 0:
      with open(file_path, "r") as f:
        frontmatter_post = frontmatter.load(f)
        # add h1 header to `title` to frontmatter
        frontmatter_post["title"] = result[0]
        # overwrite current file with added title
        with open(file_path, "wb") as f:
          frontmatter.dump(frontmatter_post, f)

# TODO test this
def find_image_and_copy(image_name: str, root_path: str, public_brain_image_path: str):
  text_files = glob.glob(root_path + "/**/" + image_name, recursive=True)
  for file in text_files:
    shutil.copy(file, public_brain_image_path)
    # print(f"image `{file}` copied to {public_brain_image_path}")

# TODO test this
def list_images_from_markdown(file_path: str):
  # search for images in markdown file
  file_content = open(file_path, "r").read()
  images = re.search(regexp_md_images, file_content)
  if images:
    for image in images.groups():
      if image:
        # find image recursively in folder and copy to public image folder
        find_image_and_copy(image, second_brain_path, public_folder_path_copy)
  # print(f"image: {file_path}, ln: {line}")
  pass

if __name__ == "__main__":
  find_and_copy_published(second_brain_path, public_folder_path_copy)
  
  # loop through public files and add referenced images, fix h1 headers and ..
  for root, dirs, files in os.walk(public_folder_path_copy):
    for file in files:
      if file.endswith(".md"):
        file_path = os.path.join(root, file)
        list_images_from_markdown(file_path)
        # print(f"converted: {file_path}")
        
# TODO find inline tags and add to frontmatter