import os
import shutil
import subprocess
from setuptools.command.install import install
from app.log_util import Log
from app.settings import get_settings,compare_and_update_settings

log = Log()

class CustomInstallCommand(install):
    def run(self):
        # Run the standard install process
        super().run()
        compare_and_update_settings(get_settings("MCMD_COMMANDS_DIR","settings"),"settings")

        src_dir = os.path.abspath('sample_comands')
        setting_dir=os.path.abspath('settings')
        dest_dir = os.path.expanduser(get_settings("MCMD_COMMANDS_DIR",setting_dir))

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
        log.warn("************Sample commands moved**************")
