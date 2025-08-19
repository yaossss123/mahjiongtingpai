#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麻将听牌分析器 v3.0 启动脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """检查依赖包"""
    missing_packages = []
    
    try:
        import PIL
    except ImportError:
        missing_packages.append("Pillow")
    
    try:
        import requests
    except ImportError:
        missing_packages.append("requests")
    
    if missing_packages:
        print("缺少以下依赖包:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        print("\n请运行以下命令安装:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    return True

def main():
    """主函数"""
    print("正在检查依赖包...")
    
    if not check_dependencies():
        input("\n按回车键退出...")
        return
    
    try:
        print("正在启动麻将听牌分析器 v3.0...")
        from mahjong_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"导入错误: {e}")
        print("\n可能的解决方案:")
        print("1. 确保所有文件都在同一目录下")
        print("2. 重新安装依赖包: pip install Pillow requests")
        print("3. 检查Python版本是否兼容 (推荐Python 3.7+)")
        input("\n按回车键退出...")
    except Exception as e:
        print(f"启动失败: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")

if __name__ == "__main__":
    main()