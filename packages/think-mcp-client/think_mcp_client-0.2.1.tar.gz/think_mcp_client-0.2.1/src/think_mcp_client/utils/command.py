import os
import platform
import shutil
from pathlib import Path
from typing import Optional, List, Tuple

from think_llm_client.utils.logger import logging

# 获取 logger
logger = logging.getLogger("think-mcp-client")

# 定义各个系统的命令搜索路径及其优先级
SYSTEM_PATHS = {
    "darwin": [  # macOS
        ("/opt/homebrew/bin", "Apple Silicon 的 Homebrew 路径 - 最高优先级"),
        ("/usr/local/bin", "Intel Mac 的 Homebrew 路径"),
        ("/usr/bin", "系统二进制文件路径"),
        (str(Path.home() / ".local/bin"), "用户安装的二进制文件路径 - 最低优先级")
    ],
    "linux": [
        ("/usr/local/bin", "本地编译软件路径 - 最高优先级"),
        ("/usr/bin", "系统包路径"),
        ("/bin", "基本命令路径"),
        ("/snap/bin", "Snap 包路径"),
        ("/usr/local/sbin", "系统管理命令路径"),
        (str(Path.home() / ".local/bin"), "用户安装的二进制文件路径 - 最低优先级")
    ],
    "windows": [
        (str(Path.home() / "AppData/Local/Programs/Python/Scripts"), "Python 脚本路径 - 最高优先级"),
        (str(Path.home() / "AppData/Local/Programs"), "本地程序路径"),
        (str(Path.home() / "AppData/Roaming/npm"), "npm 全局包路径"),
        ("C:/Program Files", "64位程序路径"),
        ("C:/Program Files (x86)", "32位程序路径 - 最低优先级")
    ]
}


def find_command_path(command: str) -> str:
    """
    查找命令的完整路径。根据不同操作系统，按照预定义的优先级在常用的二进制目录下查找。
    优先级顺序见 SYSTEM_PATHS 字典中各路径的定义顺序。
    
    Args:
        command: 要查找的命令名称

    Returns:
        str: 命令的完整路径，如果找不到则返回原始命令
    """
    def _check_system_paths(cmd: str) -> Optional[str]:
        """根据不同操作系统按优先级检查常用的二进制目录"""
        system = platform.system().lower()
        
        if system not in SYSTEM_PATHS:
            logger.warning(f"未知的操作系统: {system}")
            return None

        # 获取当前系统的路径列表
        paths = SYSTEM_PATHS[system]
        
        # 按优先级检查每个路径
        for base_path, description in paths:
            # 对于 Windows，需要检查 .exe 扩展名
            if system == "windows":
                cmd_path = os.path.join(base_path, f"{cmd}.exe")
                if os.path.isfile(cmd_path) and os.access(cmd_path, os.X_OK):
                    logger.debug(f"在 {description} 中找到命令 {cmd}: {cmd_path}")
                    return cmd_path
            
            cmd_path = os.path.join(base_path, cmd)
            if os.path.isfile(cmd_path) and os.access(cmd_path, os.X_OK):
                logger.debug(f"在 {description} 中找到命令 {cmd}: {cmd_path}")
                return cmd_path
            else:
                logger.debug(f"在 {description} 中未找到命令 {cmd}")

        return None

    # 首先检查系统特定的二进制目录
    if cmd_path := _check_system_paths(command):
        return cmd_path
    
    # 然后检查命令是否在 PATH 中
    if cmd_path := shutil.which(command):
        logger.debug(f"在 PATH 中找到命令 {command}: {cmd_path}")
        return cmd_path

    # 如果找不到完整路径，返回原始命令
    logger.debug(f"未找到命令 {command} 的完整路径，使用原始命令")
    return command
