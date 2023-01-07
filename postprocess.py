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

Fix missing orphans by adding self link
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
          .replace("?", "")
          .replace("&", "")
          .replace("!", "")
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


# === Remove false links ===

for key in links_index.keys():
  if md_file_existence_heuristic(existing_files, key):
    processed_data["index"]["links"][key] = []
  else:
    # print(f'removing {key}')
    continue
  for i, entry in enumerate(links_index[key]):
    if md_file_existence_heuristic(existing_files, entry["target"]):
      processed_data["index"]["links"][key] += [entry]
    else:
      # print(f'removing {entry}')
      continue
      
for key in backlinks_index.keys():
  if md_file_existence_heuristic(existing_files, key):
    processed_data["index"]["backlinks"][key] = []
  else:
    # print(f'removing {key}')
    continue
  for i, entry in enumerate(backlinks_index[key]):
    if md_file_existence_heuristic(existing_files, entry["target"]):
      processed_data["index"]["backlinks"][key] += [entry]
    else:
      # print(f'removing {entry}')
      continue
      
for i, entry in enumerate(links_list):
  if md_file_existence_heuristic(existing_files, entry["target"]) and ((entry["source"] == "/") or md_file_existence_heuristic(existing_files, entry["source"])):
    processed_data["links"] += [entry]
  else:
    # print(f'removing {entry}') 
    continue

# Print deletion summary
print(f'POSTPROCESS: removed {len(data["index"]["links"]) - len(processed_data["index"]["links"])} false outbound links from index of {len(data["index"]["links"])} links')
print(f'POSTPROCESS: removed {len(data["index"]["backlinks"]) - len(processed_data["index"]["backlinks"])} false backlinks from index of {len(data["index"]["backlinks"])} links')
print(f'POSTPROCESS: removed {len(data["links"]) - len(processed_data["links"])} false links of {len(data["links"])} links')



# === fix orphans ===
linked_nodes = set([entry["source"] for entry in processed_data["links"]]).union(set([entry["target"] for entry in processed_data["links"]]))
orphans_added = 0

for key in links_index.keys():
  if key not in linked_nodes:
    processed_data["links"] += [{
      "source": key,
      "target": key,
      "text": key
    }]
    orphans_added += 1
    # print(f"add self link for {key}")

print(f'POSTPROCESS: added {orphans_added} orphans to the graph')
# BUG doen't work if orphan is orphan in Obsidian. i.e. only work for those orphaned because of false link removal

# Writing to sample.json
json_object = json.dumps(processed_data, indent=2)
with open("./assets/indices/linkIndex.json", "w") as outfile:
  outfile.write(json_object)