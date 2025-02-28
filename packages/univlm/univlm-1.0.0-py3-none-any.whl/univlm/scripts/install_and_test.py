import os
import sys
import subprocess
from pathlib import Path

def ensure_package_structure():
    """Ensures all necessary directories exist"""
    package_root = Path(__file__).parent.parent
    scripts_dir = package_root / "scripts"
    backbone_dir = package_root / "Package_Backbone"
    
    scripts_dir.mkdir(exist_ok=True)
    backbone_dir.mkdir(exist_ok=True)
    
    return package_root, scripts_dir, backbone_dir

def run_script():
    """Runs the installation and testing process"""
    try:
        package_root, scripts_dir, backbone_dir = ensure_package_structure()
        script_path = scripts_dir / "install_and_test.sh"
        testing_path = scripts_dir / "testing.py"
        
        # Check if script exists
        if not script_path.exists():
            print("⚠️ install_and_test.sh not found in package!")
            return 1
            
        # Check if testing.py exists
        if not testing_path.exists():
            print("⚠️ testing.py not found in package!")
            return 1
            
        
        # Run the bash script with the correct paths
        env = os.environ.copy()
        env["PACKAGE_ROOT"] = str(package_root)
        env["BACKBONE_DIR"] = str(backbone_dir)
        env["TESTING_SCRIPT"] = str(testing_path)
        
        result = subprocess.run(
            ["bash", str(script_path)],
            env=env,
            check=True
        )
        
        if result.returncode == 0:
            return 0
        else:
            print("❌ Installation failed!")
            return 1
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during script execution: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_script())