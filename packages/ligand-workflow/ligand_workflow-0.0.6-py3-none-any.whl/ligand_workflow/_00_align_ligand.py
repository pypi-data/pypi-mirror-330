# -*- coding: utf-8 -*-
import os
from pymol import cmd

def load_structures(input_folder):
    """
    加载指定文件夹中的所有PDB文件，并返回结构列表。
    """
    structures = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".pdb"):
                structures.append(os.path.join(root, file))
    return structures

def get_reference_structure(structures, config_file):
    """
    从配置文件中读取参考结构名称，并找到它在structures中的位置。
    """
    with open(config_file, 'r') as f:
        reference_name = f.readline().strip()
    
    # 在 structures 中找到匹配的模型文件并返回
    for structure in structures:
        if reference_name in structure:  # 匹配参考结构
            return structure
    raise ValueError(f"Reference structure {reference_name} not found in the input folder.")

def load_and_align_structures(input_folder, config_file):
    """
    对比并对齐所有结构文件，align到参考结构。
    
    input_folder : str : PDB 文件所在文件夹的路径
    config_file : str : 包含参考结构名称的配置文件
    """
    # 加载所有结构
    structures = load_structures(input_folder)
    
    # 获取参考结构
    reference = get_reference_structure(structures, config_file)

    # 从结构列表中删除参考模型
    structures.remove(reference)

    # 加载参考结构
    cmd.load(reference)

    # 遍历其他结构并对齐
    for structure in structures:
        structure_name = os.path.basename(structure).replace(".pdb", "")
        reference_name = os.path.basename(reference).replace(".pdb", "")
        if structure_name != reference:
            print(f"Aligning {structure_name} to reference {reference}...")

            # 加载结构并选择其ligand
            cmd.load(structure)

            # 选择 ligand 和参考结构中的 ligand
            cmd.select("ligand1", f"{structure_name} and segment B and chain A")
            cmd.select("ligand2", f"{reference_name} and segment B and chain A")

            # 对齐到参考结构
            cmd.align("ligand1", "ligand2")
            
            # 删除当前加载的结构，为下一个结构准备
            cmd.delete(structure_name)

            print(f"Finished aligning {structure_name} to {reference}.")
        else:
            print(f"Skipping alignment for reference structure {reference}.")

# 调用此函数时，直接传入文件夹路径和配置文件路径
def align_ligands(input_folder, config_file):
    """
    主函数，执行所有结构的对齐。
    
    input_folder : str : 包含PDB文件的文件夹路径
    config_file : str : 包含参考结构名称的配置文件
    """
    load_and_align_structures(input_folder, config_file)
