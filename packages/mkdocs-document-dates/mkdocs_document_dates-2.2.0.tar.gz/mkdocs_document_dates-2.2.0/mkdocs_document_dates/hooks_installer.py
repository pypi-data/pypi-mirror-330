import os
import sys
import shutil
import subprocess
from pathlib import Path
import platform

def get_config_dir():
    """获取用户配置目录"""
    system = platform.system().lower()
    if system.startswith('win'):
        return Path(os.getenv('APPDATA', str(Path.home() / 'AppData' / 'Roaming')))
    else:  # macOS 和 Linux 统一使用 ~/.config
        return Path.home() / '.config'

def install():
    """安装 git hooks"""
    try:
        # 检查 git 是否可用
        try:
            subprocess.run(['git', '--version'], check=True, capture_output=True, encoding='utf-8')
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("提示: 未检测到 Git，跳过 hooks 安装")
            return False
        
        # 准备配置目录
        config_dir = get_config_dir() / 'mkdocs-document-dates' / 'hooks'
        try:
            config_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            print(f"错误: 无权限创建目录: {config_dir}")
            return False
        except Exception as e:
            print(f"错误: 创建目录失败: {config_dir}, 原因: {e}")
            return False

        hook_path = config_dir / 'pre-commit'

        # 复制 hook 文件
        source_hook = Path(__file__).parent / 'hooks' / 'pre-commit'
        if not source_hook.exists():
            print(f"错误: 源 hook 文件不存在: {source_hook}")
            return False
            
        try:
            shutil.copy2(source_hook, hook_path)
        except PermissionError:
            print(f"错误: 无权限复制文件到: {hook_path}")
            return False
        except Exception as e:
            print(f"错误: 复制文件失败, 原因: {e}")
            return False

        # 设置文件权限（Unix-like 系统）
        if not platform.system().lower().startswith('win'):
            try:
                os.chmod(config_dir, 0o755)
                os.chmod(hook_path, 0o755)
            except OSError as e:
                print(f"警告: 设置权限时出错: {e}")

        # 配置 git hooks 路径
        try:
            subprocess.run(['git', 'config', '--global', 'core.hooksPath', 
                          str(config_dir)], check=True, encoding='utf-8')
            print(f"Git hooks 已安装到: {config_dir}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"错误: 设置 git hooks 路径失败: {e}")
            return False
            
    except Exception as e:
        print(f"安装 hooks 时出错: {e}")
        return False

if __name__ == '__main__':
    install()