import os
from ase import io
from ase.atoms import Atoms

def list_cif_files():
    """列出当前目录下所有的 .cif 文件"""
    cif_files = [f for f in os.listdir() if f.endswith('.cif')]
    return cif_files

def choose_cif_file(cif_files):
    """让用户选择要转换的 .cif 文件"""
    if len(cif_files) == 1:
        return cif_files[0]
    print("检测到多个 CIF 文件，请选择一个进行转换：")
    for i, f in enumerate(cif_files):
        print(f"{i + 1}. {f}")
    while True:
        choice = input("请输入文件编号 (1-{}): ".format(len(cif_files)))
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(cif_files):
                return cif_files[choice - 1]
        print("输入无效，请重新输入。")

def convert_and_sort_cif_to_poscar(filename):
    """读取 .cif 文件，排序原子并转换为 POSCAR 格式"""
    atoms = io.read(filename)
    
    # 按元素种类（原子序数）排序
    sorted_atoms = atoms[[atom.index for atom in sorted(atoms, key=lambda a: a.number)]]

    # 输出 POSCAR 文件
    output_filename = "POSCAR"
    io.write(output_filename, sorted_atoms, format='vasp')
    
    print(f"转换完成，输出文件: {output_filename}")

def main():
    cif_files = list_cif_files()
    if not cif_files:
        print("当前目录下没有找到 .cif 文件。")
        return

    selected_file = choose_cif_file(cif_files)
    print(f"你选择的文件是: {selected_file}")
    convert_and_sort_cif_to_poscar(selected_file)

if __name__ == "__main__":
    main()
