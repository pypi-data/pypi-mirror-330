import os
import argparse
from ase.io import read

# 设置 VASP 赝势库路径（修改为你的路径）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
POTCAR_DIR = os.path.join(SCRIPT_DIR, "POTCAR")

def get_available_variants(element):
    """仅列出指定元素的 `POTCAR` 版本，避免误匹配其他以 `element` 开头的元素"""
    variants = []
    for item in os.listdir(POTCAR_DIR):
        # 确保 item 是目录，并且严格匹配元素名称
        base_name = item.split('_')[0]  # 提取元素名称（忽略后缀）
        if base_name == element and os.path.isdir(os.path.join(POTCAR_DIR, item)):
            variants.append(item[len(element):])  # 仅提取后缀（如 `_pv`, `_h`）

    return sorted(variants)  # 返回排序后的后缀




def choose_potcar_variant(element):
    """让用户选择 `POTCAR` 版本"""
    variants = get_available_variants(element)
    
    if not variants:
        print(f"⚠️  未找到 {element} 的任何 `POTCAR` 版本，使用默认版本。")
        return ""

    print(f"\n🔍 检测到 {element} 的可用 `POTCAR` 版本：")
    for idx, variant in enumerate(variants):
        print(f"  {idx + 1}. {element}{variant}")

    while True:
        choice = input(f"请选择 {element} 的 `POTCAR` 版本 (1-{len(variants)}, 默认=1): ").strip()
        if not choice:
            return variants[0]  # 默认选第一个
        if choice.isdigit() and 1 <= int(choice) <= len(variants):
            return variants[int(choice) - 1]
        print("❌ 无效输入，请重新选择！")


def get_elements_from_poscar(poscar_file):
    """从 `POSCAR` 文件中提取元素，保持元素顺序"""
    atoms = read(poscar_file, format="vasp")
    return list(dict.fromkeys(atoms.get_chemical_symbols()))  # 保持出现顺序



def generate_potcar(elements, interactive=False):
    """自动合并 `POTCAR` 文件，并根据用户选择的后缀合并"""
    potcar_path = "POTCAR"
    
    with open(potcar_path, "wb") as potcar_out:
        for element in elements:
            # 用户交互选择
            if interactive:
                variant = choose_potcar_variant(element)
            else:
                variant = ""

            potcar_file = os.path.join(POTCAR_DIR, element + variant, "POTCAR")

            if not os.path.exists(potcar_file):
                print(f"❌ 错误: 赝势文件 {potcar_file} 不存在，请检查 VASP 赝势库。")
                return
            
            with open(potcar_file, "rb") as potcar_in:
                potcar_out.write(potcar_in.read())

    print(f"✅ `POTCAR` 生成成功: {potcar_path}")


def main():
    parser = argparse.ArgumentParser(description="自动选择并生成 `POTCAR` 文件")
    parser.add_argument("-c", "--choose", action="store_true", help="交互式选择 `POTCAR` 版本")
    args = parser.parse_args()

    poscar_file = "POSCAR"  # 你的 POSCAR 文件
    if not os.path.exists(poscar_file):
        print(f"❌ 错误: `{poscar_file}` 文件不存在！")
        return

    elements = get_elements_from_poscar(poscar_file)
    print(f"📌 检测到的元素: {elements}")
    
    generate_potcar(elements, interactive=args.choose)


if __name__ == "__main__":
    main()
