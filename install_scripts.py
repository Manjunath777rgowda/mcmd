import os
import shutil
import subprocess
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        # Run the standard install process
        super().run()

        # Define source and destination directories
        src_dir = 'sample_comands'
        dest_dir = os.path.expanduser('~/.mcmd_commands')

        # Create destination directory if it doesn't exist
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        # Copy all contents from source to destination
        for item in os.listdir(src_dir):
            s = os.path.join(src_dir, item)
            d = os.path.join(dest_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
    
        subprocess.run(['chmod', '-R', '+x', dest_dir])
        print("************Sample files moved**************")
