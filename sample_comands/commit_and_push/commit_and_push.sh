#!/bin/bash

source  ~/.mcmd_commands/utility/logger.sh

# Unstage all changes
print_warn "Unstaging all changes..."
git reset

# Check for modified, unversioned, and staged files
modified_files=$(git status --porcelain | grep '^ M' | awk '{print $2}')
unversioned_files=$(git status --porcelain | grep '??' | awk '{print $2}')
staged_files=$(git status --porcelain | grep '^A ' | awk '{print $2}')

# Combine all relevant files
all_files="$modified_files $unversioned_files $staged_files"

if [ -z "$all_files" ]; then
  print_warn "No modified, unversioned, or staged files found."
else
  print_log "Files found:"
  echo "$all_files"
  
  for file in $all_files; do
    promt "Do you want to add $file to the staging area? (y/n)"
    read -r add_file
    if [ "$add_file" = "y" ]; then
      print_log "Adding $file"
      git add "$file"
    elif [ "$add_file" = "n" ]; then
      if git diff --cached --name-only | grep -q "$file"; then
        print_log "Removing $file from staging area"
        git reset "$file"
      else
        print_log "$file is not staged, skipping removal."
      fi
    else
      print_error "Invalid input. Please enter 'y' or 'n'."
      exit 1
    fi
  done
fi

# Confirm commit
promt "Do you want to commit the changes? (y/n)"
read -r commit_confirm
if [ "$commit_confirm" != "y" ]; then
  print_error "Aborting commit."
  exit 1
fi

# Commit changes
promt "Enter commit message:"
read -r commit_message

if [ -z "$commit_message" ]; then
  print_error "Commit message cannot be empty. Aborting commit."
  exit 1
fi

git commit -m "$commit_message"

# Confirm push
promt "Do you want to push the changes to the remote repository? (y/n)"
read -r push_confirm
if [ "$push_confirm" != "y" ]; then
  print_log "Commit completed, but not pushing. Exiting."
  exit 0
fi

# Push changes
print_log "Pushing changes to remote repository..."
git push

print_centered "Commit and push completed." "-"
