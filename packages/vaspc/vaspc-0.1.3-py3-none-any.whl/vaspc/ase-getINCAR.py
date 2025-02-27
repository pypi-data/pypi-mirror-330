import os
import shutil
import importlib.resources

def get_incar_path():
    """获取 `INCAR_opt` 在已安装包内的正确路径"""
    try:
        incar_path = importlib.resources.files("vaspc").joinpath("INCAR_temp", "INCAR-opt")
        return str(incar_path)
    except Exception:
        return None

# 获取 `INCAR_opt` 的路径
INCAR_SOURCE = get_incar_path()

# 目标路径（复制到当前目录）
INCAR_DEST = os.path.join(os.getcwd(), "INCAR")

# 复制文件
if INCAR_SOURCE and os.path.exists(INCAR_SOURCE):
    try:
        shutil.copy(INCAR_SOURCE, INCAR_DEST)
        print(f"Successfully copied INCAR_opt to {INCAR_DEST}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print(f"Error: {INCAR_SOURCE} not found.")
