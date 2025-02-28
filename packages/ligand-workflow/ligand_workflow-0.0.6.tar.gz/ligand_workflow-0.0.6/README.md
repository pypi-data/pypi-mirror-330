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

### 使用说明

#### 1. 配体对齐

对齐多个结构文件的配体到参考结构的配体。运行以下命令：

```bash
ligand-align -i <input_folder> -c <config_file>
```

- <input_folder>: 包含 PDB 文件的文件夹路径。-
- <config_file>: 配置文件，指定参考结构和配体选择条件。

#### 2. 计算接触

计算分子之间的极性接触并输出结果：

```bash
ligand-contacts -i <input_folder> -c <config_file> -o <output_file>
```

- <input_folder>: 包含 PDB 文件的文件夹路径。
- <config_file>: 配置文件，指定配体选择条件。
- <output_file>: 输出的 JSON 文件路径。

#### 3. JSON 转 CSV

将 JSON 文件转换为 CSV 格式的表格：

```bash
json-to-csv -j <input_json> -o <output_csv> -x <xray_identifier>
```

- <input_json>: 输入的 JSON 文件路径。
- <output_csv>: 输出的 CSV 文件路径。
- <xray_identifier>: 用于识别 x‑ray 组的标识符。

#### 示例

#### 1. 配体对齐：

假设你有一个包含多个 PDB 文件的文件夹 pdbs/ 和一个配置文件 config.txt，你可以使用以下命令将所有文件与参考结构进行对齐：

```bash
ligand-align -i pdbs/ -c config.txt
```

#### 2. 计算接触：

如果你有多个 PDB 文件，并想计算它们的接触并输出到一个 JSON 文件：

```bash
ligand-contacts -i pdbs/ -c config.txt -o contacts.json
```

#### 3. JSON 转 CSV：

如果你有一个包含接触数据的 JSON 文件 contacts.json，并希望将其转换为 CSV 文件：

```bash
json-to-csv -j contacts.json -o contacts.csv -c config.txt
```

#### 4. 统一调用

如果你想将所有步骤组合在一起，你可以使用以下命令：

```bash
ligand-workflow -i pdbs/ -c config.txt -o contacts.json -x xray
```
