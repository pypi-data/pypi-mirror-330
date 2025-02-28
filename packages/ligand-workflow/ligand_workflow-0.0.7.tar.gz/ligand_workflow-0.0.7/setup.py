from setuptools import setup, find_packages

setup(
    name='ligand_workflow',
    version='0.0.7',
    packages=find_packages(),
    install_requires=[
        'pymol',
        'numpy',
        'argparse',

    ],
    entry_points={
        'console_scripts': [
            # 主工作流入口
            'ligand-workflow=ligand_workflow.90_ligand_workflow:main',  # 启动主工作流（包括对齐、计算接触、转换JSON到CSV）
            
            # 对齐入口，调用 align_ligands 函数
            'ligand-align=ligand_workflow._00_align_ligand:align_ligands',  # 调用 align_ligands 函数用于对齐

            # 计算接触
            'ligand-contacts=ligand_workflow._10_calculate_contacts:main',  # 计算接触

            # JSON 转换为 CSV
            'json-to-csv=ligand_workflow._20_convert_json_to_csv:main',  # 转换 JSON 到 CSV
        ],
    },
    author='Hao Sun',
    author_email='sun_hao@gzlab.ac.cn',
    description='A workflow for aligning ligands and calculating contacts.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/OOAAHH/ligand_workflow',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
