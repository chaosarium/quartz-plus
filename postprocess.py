""" 
gets rid of dead links indexed by Obsidian-Hugo. Definitely not the most efficient thing to do, but hopefully it gets the job done. 

the index file usually at "assets/indices/linkIndex.json"

Basic idea:

- read linkIndex.json
- loop through each index entry
  - loop through each links entry
    - loop through each node
      - convert character encoding
      - get rid of link that don't correspond to file in "content"
  - loop through each backlinks entry
    - loop through each node
      - convert character encoding
      - get rid of link that don't correspond to file in "content"
- loop through each link entry
  - convert character encoding
  - get rid of link that don't correspond to file in "content"

Also, Obsidian-Hugo seems to mistake internal block or section references as references to root, so all links target at "/" will get removed
"""

import json
import urllib.parse
import os
import re

INDEX_FILE = "./assets/indices/linkIndex.json"
CONTENT_FOLDER = "./content"

def decode_url_encoding(s) -> str:
  return urllib.parse.unquote(s)

def load_json(path) -> dict:
  f = open(path)
  data = json.load(f)
  f.close()
  return data

def strip_name(s) -> str:
  # gets rid of symbols, spaces, etc.
  return (s.replace(".md", "")
          .replace("/", "")
          .replace(" ",  "")
          .replace("-",  "")
          .replace("/",  "")
          .replace("\\", "")
          .replace("%",  "")
          .replace(":",  "")
          .replace("(",  "")
          .replace(")",  "")
          .replace("|",  "")
          .replace('"',  "")
          .replace("'",  "")
          .replace(".",  "")
          .replace(",",  "")
          .replace(";",  "")
          )

def md_file_existence_heuristic(existing_files_set, encoded_url) -> bool:
  if encoded_url == "/":
    return True
  return strip_name(encoded_url) in existing_files_set

data = load_json(INDEX_FILE)
existing_files = set([strip_name(file) for file in os.listdir(CONTENT_FOLDER)])

links_index: dict = data["index"]["links"]
backlinks_index: dict = data["index"]["backlinks"]
links_list: list = data["links"]

processed_data =  {"index": {
                      "links": {},
                      "backlinks": {},
                    },
                    "links": [],
                  }

for key in links_index.keys():
  if md_file_existence_heuristic(existing_files, key):
    processed_data["index"]["links"][key] = []
  else:
    continue
  for i, entry in enumerate(links_index[key]):
    if md_file_existence_heuristic(existing_files, entry["target"]) and entry["target"] != "/":
      processed_data["index"]["links"][key] += [entry]
      
for key in backlinks_index.keys():
  if md_file_existence_heuristic(existing_files, key):
    processed_data["index"]["backlinks"][key] = []
  else:
    continue
  for i, entry in enumerate(backlinks_index[key]):
    if md_file_existence_heuristic(existing_files, entry["target"]) and entry["target"] != "/":
      processed_data["index"]["backlinks"][key] += [entry]
      
for i, entry in enumerate(links_list):
  if md_file_existence_heuristic(existing_files, entry["target"]) and md_file_existence_heuristic(existing_files, entry["source"]):
    processed_data["links"] += [entry]
    
json_object = json.dumps(processed_data, indent=2)

# Writing to sample.json
with open("./assets/indices/linkIndex.json", "w") as outfile:
  outfile.write(json_object)