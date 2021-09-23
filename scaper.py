#!/usr/bin/env python3
import requests
from sys import argv
from os import path
from time import sleep

USED_USERNAMES_PATH = "./attempted_usernames.txt"
FREE_USERNAMES_PATH = "./free_usernames.txt"

if not (len(argv) == 3 and argv[1].isdigit()):
  print("Usage: ./scraper.py MAX_LENGTH CHARS")
  exit()

used_usernames = set()

# Save state to save some attempts
if not path.isfile(USED_USERNAMES_PATH):
  open(USED_USERNAMES_PATH, "w")
with open(USED_USERNAMES_PATH, "r+") as f:
  used_usernames = set([x.rstrip() for x in f.readlines()])

max_length = int(argv[1])


def generate_candidates(candidates, prefix, chars_left):
  if not prefix in used_usernames and not prefix in candidates:
    candidates.append(prefix)
  if len(chars_left) > 0 and len(prefix) < max_length:
    for c in chars_left:
      chars_left.remove(c)
      generate_candidates(candidates, prefix+c, chars_left)
      chars_left.append(c)
  return candidates


username_candidates = generate_candidates([], "", list(argv[2]))
free_usernames = []

for username_candidate in username_candidates:
  response = requests.get(f"http://github.com/{username_candidate}")
  if response.status_code == 404:
    free_usernames.append(username_candidate)
    print(f"{username_candidate} is available.")
    with open(FREE_USERNAMES_PATH, "w") as f:
      f.writelines([x+"\n" for x in free_usernames])
  else:
    used_usernames.add(username_candidate)
    with open(USED_USERNAMES_PATH, "w") as f:
      f.writelines([x+"\n" for x in used_usernames])
