# __init__.py (in univlm/scripts directory)
from .install_and_test import run_script

# install_and_test.py (in univlm/scripts directory)
def run_script():
    import os
    import sys
    
    def create_directories():
        """Create necessary package directories."""
        package_path = os.path.dirname(os.path.dirname(__file__))
        scripts_dir = os.path.join(package_path, "scripts")
        os.makedirs(scripts_dir, exist_ok=True)
        return package_path, scripts_dir

    def setup_package():
        """Set up the package structure and run installation."""
        package_path, scripts_dir = create_directories()
        
        print("✅ Package directories created successfully")
        
        # Your existing installation logic goes here
        try:
            import vllm
            print("✅ vLLM is already installed")
        except ImportError:
            print("📥 Installing vLLM...")
            os.system("pip install vllm")
        
        print("✅ Setup completed successfully")

    try:
        setup_package()
    except Exception as e:
        print(f"❌ Error during setup: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_script()