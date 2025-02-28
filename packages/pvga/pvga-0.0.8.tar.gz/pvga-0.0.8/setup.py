from setuptools import setup, find_packages

setup(
    name='pvga',  # 确保包名有效
    version='0.0.8',
    description='PVGA is a powerful virus-focused assembler that does both assembly and polishing.',
    author='zhisong',
    author_email='songzhics@gmail.com',
    url='https://github.com/SoSongzhi/PVGA',
    
    # 使用 find_packages 自动发现包
    package_dir={"": "src"},  # 指定根目录为 src
    packages=find_packages(where="src"),  # 自动发现 src 下的包
    
    # 使用 entry_points 替代 scripts
    entry_points={
        "console_scripts": [
            "pvga=pvga:main"  # 定义命令行工具
        ]
    },
    
    # 其他可选配置
    python_requires='>=3.7',  # 指定 Python 版本要求
    install_requires=[  # 添加依赖项
        # 'numpy>=1.20.0',
        # 'pandas>=1.3.0',
    ],
)