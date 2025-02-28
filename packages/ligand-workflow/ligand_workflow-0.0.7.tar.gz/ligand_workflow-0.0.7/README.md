# Ligand Workflow

`ligand_workflow` 是一个用于处理和分析分子对接数据的工作流工具。它包括多个功能模块，能够帮助你对齐配体，计算分子间接触并将 JSON 格式的数据转换为 CSV 表格，便于进一步分析。

## 功能

- **ligand-align**: 对齐多个结构中的配体到参考结构的配体（基于pymol的）。
- **ligand-contacts**: 计算分子之间的极性接触并输出结果（基于pymol的）。
- **json-to-csv**: 将包含多个 PDB 文件的 JSON 数据转换为 CSV 格式，便于后续分析和展示。

## 安装

你可以使用 `pip` 从 PyPI 安装该包，也可以从源代码安装。

### 通过 PyPI 安装

```bash
pip install ligand_workflow
```

## 用法
依托于config file进行工作流配置，config file的格式如下：

```plaintxt
6GZR.1-10_09 #这是x-ray结构的文件名
resn FH8 and chain A and resi 101 #这是需要处理的配体的筛选条件
chain A and polymer # 这是需要处理的RNA/DNA/蛋白质的筛选条件
```

### 设计

![img](structure.png)

### 使用说明

```python
from ligand_workflow import ligand_workflow

input_folder = "tests/testOut"
output_csv = "tests/testOut.csv"
output_json = "tests/testOut.json"
config_file = "tests/config.txt"

# Call the ligand_workflow function
ligand_workflow(input_folder=input_folder, output_csv=output_csv, output_json=output_json, config_file=config_file)
```
