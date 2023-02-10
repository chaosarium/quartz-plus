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
# - add inline tags to metadata

regexp_md_attachment = r"\[\[((?:.+)\.(?:\S+))(?:\|\d+)?\]\]" # attachments (maybe)
h1_regex = r"(?m)^# (.*)" # finds entire h1 line

# === ACTIONS ===

def find_attachment_and_copy(file_name: str, root_path: str, target_attachment_path: str):
  files = glob.glob(root_path + "/**/" + file_name, recursive=True)
  # print(files)
  for file in files:
    shutil.copy(file, os.path.join(target_attachment_path, file_name))
    # print(f"attachment `{file}` copied to {target_attachment_path}")

# read a md file and add inline tags to frontmatter
def add_inline_tag_to_yaml(md_file_path):
  with open(md_file_path, "r") as f_r:
    md_frontmatter = frontmatter.load(f_r)
    
  with open(md_file_path, "r") as f_r:
    md_text = f_r.read()

  if not "tags" in md_frontmatter.keys():
    tags_field = []
  else:
    tags_field = md_frontmatter["tags"]
    if type(tags_field) != "list":
      tags_field = [tags_field]
  
  inline_tags = get_inline_tags(md_text)
  tags_field = list(set(tags_field + inline_tags))
  md_frontmatter["tags"] = tags_field
    
  with open(md_file_path, "wb") as f_w:
    frontmatter.dump(md_frontmatter, f_w)
    
  return

def walk_through_markdown_for_attachments(md_file_path: str, root_path: str, target_attachment_path: str):
  # BUG: links like [[something 3.0]] are identified as file
  # search for attachments in markdown file
  file_content = open(md_file_path, "r").read()
  attachments = re.findall(regexp_md_attachment, file_content)
  if attachments:
    print(f"ATTACHMENT SEARCH RESULT for {md_file_path}", attachments)
    for attachment in attachments:
      attachment = re.sub(r"\|\d+", "", attachment)
      # print(attachment)
      if attachment:
        # TODO excalidraw not handelled correctly. Maybe try https://github.com/tommywalkie/excalidraw-cli to turn excalidraw into svg first.
        # find attachment recursively in folder and copy to public attachment folder
        find_attachment_and_copy(os.path.basename(attachment), root_path, target_attachment_path)

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

def add_h1_or_filename_as_title_frontmatter(md_file_path: str):
  with open(md_file_path, "r") as f_r:
    md_frontmatter = frontmatter.load(f_r)
    
    if not "title" in md_frontmatter.keys():
      # read line by line and search for h1
      with open(md_file_path, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
          result = re.findall(h1_regex, line)
          if result:
            # print(f"found h1 in {md_file_path} line: {line}")
            
            # put in frontmatter and delete h1 line if any
            # add h1 header to `title` to frontmatter
            md_frontmatter["title"] = result[0]
            # overwrite current file with added title
            with open(md_file_path, "wb") as f:
              frontmatter.dump(md_frontmatter, f)
            delete_line(md_file_path, i+1)
            break
        if not result:
          # none found, use filename
          md_frontmatter["title"] = Path(md_file_path).stem
          # overwrite current file with added title
          with open(md_file_path, "wb") as f:
            frontmatter.dump(md_frontmatter, f)

# === HELPERS ===

def get_inline_tags(md_text):
  # modified from https://github.com/obsidian-html/obsidian-html/blob/b9f5869cd9453db7909174bb004b5d309702c545/obsidianhtml/parser/MarkdownPage.py
  return [x[1:].replace('.','') for x in re.findall("(?<!\S)#[\w/\-]*[a-zA-Z\-_/][\w/\-]*", md_text)]

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

# === RUN ===

if __name__ == "__main__":
  # set variables
  parser = argparse.ArgumentParser()
  parser.add_argument('--source_path', required = True) # obsidian vault
  parser.add_argument('--target_path', required = True) # whereever hugo looks for content
  parser.add_argument('--target_attachment_path', required = True) # whereever hugo looks for attachments
  args = parser.parse_args()
  
  find_and_copy_published(args.source_path, args.target_path)
  
  # loop through md in the published content dir
  for root, dirs, files in os.walk(args.target_path):
    for file in files:
      if file.endswith(".md"):
        md_file_path = os.path.join(root, file)
        print('proc', md_file_path)
        
        # copy referenced attachments
        walk_through_markdown_for_attachments(md_file_path, args.source_path, args.target_attachment_path)
        
        # add h1 as title frontmatter if none exists
        add_h1_or_filename_as_title_frontmatter(md_file_path)
        
        # add inline tags as frontmatter
        add_inline_tag_to_yaml(md_file_path)