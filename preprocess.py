# inspired by and based on https://github.com/sspaeti/second-brain-public
import os, sys, argparse
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

regexp_md_attachment = r"\[\[((?:.+)\.(?:\S+))(?:\|\d+)?\]\]" # attachments (maybe)
h1_regex = r"(?m)^# (.*)" # finds entire h1 line

def find_and_copy_published(source_path: str, copy_to_path: str):
  """
  - find `published: true` frontmatter in private folder and move it to public folder.
  - copies h1 title (`# ..`) into frontmatter as YAML title if no title exists
  """
  for root, dirs, files in os.walk(source_path):
    for file in files:
      # print(file)
      if file.endswith(".md"):
        file_path = os.path.join(root, file)
        # use published frontmatter instead
        with open(file_path, "r") as f:
          fmt = frontmatter.load(f)
          # print(fmt.metadata)
        if ("published" in fmt.metadata.keys()) and (fmt.metadata["published"] == True):

          # destination should be lower-case (spaces will be handled by hugo with `urlize`)
          # file_name_lower = os.path.basename(file_path).lower() # HACK unnecessary?

          # print(f"publish: {file_path}")
          # copy that file to the publish notes directory
          shutil.copy(
            # file_path, os.path.join(copy_to_path, file_name_lower) # HACK unnecessary?
            file_path, os.path.join(copy_to_path, file)
          )
          
          # add h1 as title frontmatter if none exists
          add_h1_as_title_frontmatter(
            os.path.join(copy_to_path, file)
          )

def add_h1_as_title_frontmatter(file_path: str):
  # print(f"start converting {file_path}")
  with open(file_path, "r") as f:

    # read line by line and search for h1
    # copy text of h1
    with open(file_path, "r") as f:
      lines = f.readlines()
      for i, line in enumerate(lines):
        result = re.findall(h1_regex, line)
        # print(result)
        if result:
          # print(f"found h1 in {file_path} line: {line}")
          break

    # put in frontmatter and delete h1 line if any
    if len(result) > 0:
      with open(file_path, "r") as f:
        frontmatter_post = frontmatter.load(f)
        if not "title" in frontmatter_post.keys():
          # add h1 header to `title` to frontmatter
          frontmatter_post["title"] = result[0]
          # overwrite current file with added title
          with open(file_path, "wb") as f:
            frontmatter.dump(frontmatter_post, f)
          delete_line(file_path, i+1)

def delete_line(file_path: str, line_to_delete: int):
  # from https://pynative.com/python-delete-lines-from-file/
  lines = []
  # read file
  with open(file_path, 'r') as f:
      # read an store all lines into list
      lines = f.readlines()

  # Write file
  with open(file_path, 'w') as f:
      # iterate each line
      for number, line in enumerate(lines):
          # delete line 5 and 8. or pass any Nth line you want to remove
          # note list index starts from 0
          if number != line_to_delete:
              f.write(line)
  
  print(f"deleted line {line_to_delete} from {file_path}")

def find_attachment_and_copy(file_name: str, root_path: str, target_attachment_path: str):
  files = glob.glob(root_path + "/**/" + file_name, recursive=True)
  # print(files)
  for file in files:
    shutil.copy(file, os.path.join(target_attachment_path, file_name))
    print(f"attachment `{file}` copied to {target_attachment_path}")

# BUG: links like [[something 3.0]] are identified as file
def walk_through_markdown_for_attachments(file_path: str, root_path: str, target_attachment_path: str):
  # search for attachments in markdown file
  file_content = open(file_path, "r").read()
  attachments = re.findall(regexp_md_attachment, file_content)
  if attachments:
    print(f"ATTACHMENT SEARCH RESULT for {file_path}", attachments)
    for attachment in attachments:
      attachment = re.sub(r"\|\d+", "", attachment)
      print(attachment);
      if attachment:
        # TODO excalidraw not handelled correctly. Maybe try https://github.com/tommywalkie/excalidraw-cli to turn excalidraw into svg first.
        # find attachment recursively in folder and copy to public attachment folder
        find_attachment_and_copy(os.path.basename(attachment), root_path, target_attachment_path)
  pass

if __name__ == "__main__":
  # set variables
  parser = argparse.ArgumentParser()
  parser.add_argument('--source_path', required = True) # obsidian vault
  parser.add_argument('--target_path', required = True) # whereever hugo looks for content
  parser.add_argument('--target_attachment_path', required = True) # whereever hugo looks for attachments
  args = parser.parse_args()
  
  find_and_copy_published(args.source_path, args.target_path)
  
  # loop through public files and add referenced attachments, fix h1 headers and ..
  for root, dirs, files in os.walk(args.target_path):
    for file in files:
      if file.endswith(".md"):
        file_path = os.path.join(root, file)
        walk_through_markdown_for_attachments(file_path, args.source_path, args.target_attachment_path)
        # print(f"converted: {file_path}")
        
# TODO find inline tags and add to frontmatter