#!/bin/bash

# Unstage all changes
echo "Unstaging all changes..."
git reset

# Check for modified, unversioned, and staged files
modified_files=$(git status --porcelain | grep '^ M' | awk '{print $2}')
unversioned_files=$(git status --porcelain | grep '??' | awk '{print $2}')
staged_files=$(git status --porcelain | grep '^A ' | awk '{print $2}')

# Combine all relevant files
all_files="$modified_files $unversioned_files $staged_files"

if [ -z "$all_files" ]; then
  echo "No modified, unversioned, or staged files found."
else
  echo "Files found:"
  echo "$all_files"
  
  for file in $all_files; do
    echo "Do you want to add $file to the staging area? (y/n)"
    read -r add_file
    if [ "$add_file" = "y" ]; then
      echo "Adding $file"
      git add "$file"
    elif [ "$add_file" = "n" ]; then
      if git diff --cached --name-only | grep -q "$file"; then
        echo "Removing $file from staging area"
        git reset "$file"
      else
        echo "$file is not staged, skipping removal."
      fi
    else
      echo "Invalid input. Please enter 'y' or 'n'."
      exit 1
    fi
  done
fi

# Confirm commit
echo "Do you want to commit the changes? (y/n)"
read -r commit_confirm
if [ "$commit_confirm" != "y" ]; then
  echo "Aborting commit."
  exit 1
fi

# Commit changes
echo "Enter commit message:"
read -r commit_message

if [ -z "$commit_message" ]; then
  echo "Commit message cannot be empty. Aborting commit."
  exit 1
fi

git commit -m "$commit_message"

# Confirm push
echo "Do you want to push the changes to the remote repository? (y/n)"
read -r push_confirm
if [ "$push_confirm" != "y" ]; then
  echo "Commit completed, but not pushing. Exiting."
  exit 0
fi

# Push changes
echo "Pushing changes to remote repository..."
git push

echo "Commit and push completed."
