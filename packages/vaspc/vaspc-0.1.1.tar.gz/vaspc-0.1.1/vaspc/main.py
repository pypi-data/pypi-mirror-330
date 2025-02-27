import os
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(script_name):
    """运行指定的 Python 脚本"""
    script_path = os.path.join(SCRIPT_DIR, script_name)
    if os.path.exists(script_path):
        print(f"Running {script_name}...")
        subprocess.run(["python", script_path], check=True)
    else:
        print(f"Error: {script_name} not found!")


def main():
    """运行所有脚本"""
    run_script("ase-convert.py")
    run_script("ase-getINCAR.py")
    run_script("ase-getpotcar.py")
    print("All scripts executed successfully.")

if __name__ == "__main__":
    main()
