#!/usr/bin/env python3
# filepath: /share/utils/addbin.py

import os
import sys
import stat

def create_symlinks():
    # Get current directory
    current_dir = os.getcwd()
    
    # Find all Python files in the current directory
    python_files = [f for f in os.listdir(current_dir) if f.endswith('.py')]
    
    if not python_files:
        return
    
    # Process each Python file
    for py_file in python_files:
        source_path = os.path.join(current_dir, py_file)
        target_path = f"/bin/{py_file.rsplit('.', 1)[0]}"
        
        # Add shebang if not present
        with open(source_path, 'r') as f:
            content = f.read()
        
        if not content.startswith('#!/usr/bin/env python3'):
            with open(source_path, 'w') as f:
                f.write('#!/usr/bin/env python3\n' + content)
            print(f"[+] Added shebang to {py_file}")
        
        # Make file executable
        current_mode = os.stat(source_path).st_mode
        if not (current_mode & stat.S_IXUSR):
            os.chmod(source_path, current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            print(f"[+] Made {py_file} executable")
        
        # Create symbolic link
        try:
            if os.path.exists(target_path):
                if os.path.islink(target_path) and os.readlink(target_path) == source_path:
                    print(f"[-] Skipped {py_file}")
                    continue
                os.remove(target_path)
            os.symlink(source_path, target_path)
            print(f"[+] Linked {py_file}")
        except PermissionError:
            continue
        except Exception:
            continue

if __name__ == "__main__":
    # Check if running with sudo/root permissions
    if os.geteuid() != 0:
        print("[-] Need to be root")
        sys.exit(1)
    
    create_symlinks()