"""MkDocs Document Dates Plugin."""

__version__ = '2.0.0'

from .hooks_installer import install

# 在包被导入时自动执行 hooks 安装
try:
    result = install()
    if not result:
        print("提示: Git hooks 安装被跳过（可能是因为未检测到 Git 或不在 Git 仓库中）")
except Exception as e:
    print(f"警告: Git hooks 安装失败: {e}")