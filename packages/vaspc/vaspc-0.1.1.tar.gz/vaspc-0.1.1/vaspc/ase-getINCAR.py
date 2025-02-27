import os
import shutil

# 获取当前脚本所在的目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 构造 INCAR_opt 文件的路径
INCAR_SOURCE = os.path.join(SCRIPT_DIR, "INCAR_temp", "INCAR-opt")

# 目标路径（复制到当前目录）
INCAR_DEST = os.path.join(os.getcwd(), "INCAR")

# 复制文件
try:
    shutil.copy(INCAR_SOURCE, INCAR_DEST)
    print(f"Successfully copied INCAR_opt to {INCAR_DEST}")
except FileNotFoundError:
    print(f"Error: {INCAR_SOURCE} not found.")
except Exception as e:
    print(f"Error: {e}")
