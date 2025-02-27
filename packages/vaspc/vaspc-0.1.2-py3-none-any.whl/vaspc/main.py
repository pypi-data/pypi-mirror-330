import os
import subprocess
import importlib.resources

def get_script_path(script_name):
    """获取安装包内 `scripts` 目录下的 Python 脚本路径"""
    try:
        script_path = importlib.resources.files("vaspc").joinpath(script_name)
        return str(script_path)
    except Exception:
        return None

def run_script(script_name):
    """运行指定的 Python 脚本"""
    script_path = get_script_path(script_name)
    if script_path and os.path.exists(script_path):
        print(f"Running {script_name}...")
        subprocess.run(["python", script_path], check=True)
    else:
        print(f"Error: {script_name} not found!")

def main():
    """运行所有脚本"""
    run_script("ase-convert.py")
    run_script("ase-getINCAR.py")
    run_script("ase-getpotcar.py")
    print("✅ All scripts executed successfully.")

if __name__ == "__main__":
    main()
