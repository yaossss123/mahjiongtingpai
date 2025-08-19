#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麻将听牌分析器 - 图形界面版本 v3.0
支持百搭牌功能的可视化麻将分析工具
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from typing import List, Dict, Any

# 导入自定义模块
from mahjong_tingpai import MahjongTingpaiWithJoker
from asset_manager import AssetManager
from gui_components import HandPanel, TileSelector, ResultPanel

class MahjongGUI:
    """麻将听牌分析器主界面"""
    
    def __init__(self):
        # 初始化主窗口
        self.root = tk.Tk()
        self.root.title("麻将听牌分析器 v3.0 - 图形版")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # 设置图标（如果有的话）
        try:
            self.root.iconbitmap("assets/ui/icon.ico")
        except:
            pass
        
        # 初始化核心组件
        self.mahjong_engine = MahjongTingpaiWithJoker()
        self.asset_manager = AssetManager()
        
        # 界面组件
        self.hand_panel = None
        self.tile_selector = None
        self.result_panel = None
        
        # 创建界面
        self._create_menu()
        self._create_main_interface()
        
        # 绑定快捷键
        self._bind_shortcuts()
        
        print("麻将听牌分析器 v3.0 启动成功！")
    
    def _create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="新建", command=self._new_hand, accelerator="Ctrl+N")
        file_menu.add_command(label="保存手牌", command=self._save_hand, accelerator="Ctrl+S")
        file_menu.add_command(label="加载手牌", command=self._load_hand, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit, accelerator="Ctrl+Q")
        
        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="清空手牌", command=self._clear_hand, accelerator="Ctrl+C")
        edit_menu.add_command(label="撤销", command=self._undo, accelerator="Ctrl+Z")
        
        # 分析菜单
        analyze_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="分析", menu=analyze_menu)
        analyze_menu.add_command(label="开始分析", command=self._analyze_hand, accelerator="F5")
        analyze_menu.add_command(label="快速测试", command=self._quick_test)
        
        # 工具菜单
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="工具", menu=tools_menu)
        tools_menu.add_command(label="重新加载素材", command=self._reload_assets)
        tools_menu.add_command(label="下载雀魂素材", command=self._download_assets)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="使用说明", command=self._show_help)
        help_menu.add_command(label="关于", command=self._show_about)
    
    def _create_main_interface(self):
        """创建主界面"""
        # 创建主框架
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 左侧面板（手牌输入和选择器）
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        
        # 手牌显示面板
        self.hand_panel = HandPanel(left_frame, self.asset_manager, max_tiles=14)
        self.hand_panel.pack(pady=(0, 10))
        
        # 牌选择器
        self.tile_selector = TileSelector(
            left_frame, 
            self.asset_manager, 
            selection_callback=self._on_tile_selected
        )
        self.tile_selector.pack(fill="both", expand=True)
        
        # 控制按钮
        button_frame = tk.Frame(left_frame)
        button_frame.pack(fill="x", pady=10)
        
        tk.Button(button_frame, text="分析", command=self._analyze_hand,
                 bg="green", fg="white", font=('Arial', 12, 'bold')).pack(side="left", padx=2)
        tk.Button(button_frame, text="清空", command=self._clear_hand,
                 bg="red", fg="white").pack(side="left", padx=2)
        tk.Button(button_frame, text="撤销", command=self._undo).pack(side="left", padx=2)
        tk.Button(button_frame, text="示例", command=self._load_example).pack(side="left", padx=2)
        
        # 右侧面板（结果显示）
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # 结果显示面板
        self.result_panel = ResultPanel(right_frame, self.asset_manager)
        self.result_panel.pack(fill="both", expand=True)
        
        # 状态栏
        self._create_status_bar()
    
    def _create_status_bar(self):
        """创建状态栏"""
        self.status_bar = tk.Frame(self.root, relief="sunken", bd=1)
        self.status_bar.pack(side="bottom", fill="x")
        
        self.status_label = tk.Label(self.status_bar, text="就绪", anchor="w")
        self.status_label.pack(side="left", padx=5)
        
        # 手牌计数
        self.count_label = tk.Label(self.status_bar, text="手牌: 0/13", anchor="e")
        self.count_label.pack(side="right", padx=5)
    
    def _bind_shortcuts(self):
        """绑定快捷键"""
        self.root.bind('<Control-n>', lambda e: self._new_hand())
        self.root.bind('<Control-s>', lambda e: self._save_hand())
        self.root.bind('<Control-o>', lambda e: self._load_hand())
        self.root.bind('<Control-c>', lambda e: self._clear_hand())
        self.root.bind('<Control-z>', lambda e: self._undo())
        self.root.bind('<F5>', lambda e: self._analyze_hand())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
    
    def _on_tile_selected(self, tile_code: str):
        """处理牌选择事件"""
        if self.hand_panel.add_tile(tile_code):
            self._update_status()
            self.status_label.config(text=f"添加了 {self.asset_manager._get_tile_name(tile_code)}")
        else:
            messagebox.showwarning("警告", "手牌已满！最多只能有13张牌。")
    
    def _analyze_hand(self):
        """分析手牌"""
        hand = self.hand_panel.get_hand()
        
        if len(hand) == 0:
            messagebox.showwarning("警告", "请先输入手牌！")
            return
        
        if len(hand) != 13:
            messagebox.showwarning("警告", "手牌必须是13张！")
            return
        
        try:
            # 转换为字符串格式
            hand_str = ''.join(hand)
            
            # 分析手牌
            self.status_label.config(text="正在分析...")
            self.root.update()
            
            result = self.mahjong_engine.analyze_hand(hand_str)
            
            # 显示结果
            self.result_panel.update_result(result)
            
            if result.get('is_tingpai', False):
                self.status_label.config(text="分析完成 - 听牌！")
            else:
                self.status_label.config(text="分析完成 - 未听牌")
                
        except Exception as e:
            messagebox.showerror("错误", f"分析失败: {str(e)}")
            self.status_label.config(text="分析失败")
    
    def _clear_hand(self):
        """清空手牌"""
        self.hand_panel.clear()
        self._update_status()
        self.status_label.config(text="手牌已清空")
    
    def _new_hand(self):
        """新建手牌"""
        self._clear_hand()
    
    def _undo(self):
        """撤销最后一张牌"""
        hand = self.hand_panel.get_hand()
        if hand:
            # 移除最后一张牌
            for i in range(len(self.hand_panel.tiles) - 1, -1, -1):
                if self.hand_panel.tiles[i] is not None:
                    self.hand_panel.remove_tile(i)
                    break
            self._update_status()
            self.status_label.config(text="已撤销")
        else:
            messagebox.showinfo("提示", "没有可撤销的操作")
    
    def _save_hand(self):
        """保存手牌"""
        hand = self.hand_panel.get_hand()
        if not hand:
            messagebox.showwarning("警告", "没有手牌可保存！")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                data = {
                    "hand": hand,
                    "timestamp": str(tk.datetime.datetime.now()),
                    "version": "3.0"
                }
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                self.status_label.config(text=f"手牌已保存到 {filename}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def _load_hand(self):
        """加载手牌"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                hand = data.get('hand', [])
                self.hand_panel.set_hand(hand)
                self._update_status()
                
                self.status_label.config(text=f"手牌已从 {filename} 加载")
            except Exception as e:
                messagebox.showerror("错误", f"加载失败: {str(e)}")
    
    def _load_example(self):
        """加载示例手牌"""
        examples = [
            ['1m', '2m', '3m', '4p', '5p', '6p', '7s', '8s', '9s', '1z', '1z', '2z', '2z'],  # 标准听牌
            ['1m', '1m', '2p', '2p', '3s', '3s', '4z', '4z', '5z', '5z', '6z', '6z', '7z'],  # 七对子
            ['1m', '9m', '1p', '9p', '1s', '9s', '1z', '2z', '3z', '4z', '5z', '6z', 'j'],   # 国士无双
            ['1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m', '1p', '1p', 'j', 'j'],   # 百搭牌示例
        ]
        
        # 随机选择一个示例
        import random
        example = random.choice(examples)
        
        self.hand_panel.set_hand(example)
        self._update_status()
        self.status_label.config(text="已加载示例手牌")
    
    def _quick_test(self):
        """快速测试"""
        self._load_example()
        self._analyze_hand()
    
    def _reload_assets(self):
        """重新加载素材"""
        try:
            self.asset_manager.reload_assets()
            messagebox.showinfo("成功", "素材重新加载完成！")
            self.status_label.config(text="素材已重新加载")
        except Exception as e:
            messagebox.showerror("错误", f"重新加载失败: {str(e)}")
    
    def _download_assets(self):
        """下载雀魂素材"""
        messagebox.showinfo("提示", 
                          "素材下载功能待实现。\n\n" +
                          "请手动将雀魂素材放置到以下目录：\n" +
                          "assets/tiles/man/ (万子)\n" +
                          "assets/tiles/pin/ (筒子)\n" +
                          "assets/tiles/sou/ (条子)\n" +
                          "assets/tiles/honor/ (字牌)")
    
    def _show_help(self):
        """显示帮助"""
        help_text = """
麻将听牌分析器 v3.0 使用说明

1. 输入手牌：
   - 点击左侧的牌选择器选择麻将牌
   - 手牌区域会显示已选择的牌
   - 支持万子(m)、筒子(p)、条子(s)、字牌(z)和百搭牌(j)

2. 分析手牌：
   - 输入13张牌后点击"分析"按钮
   - 右侧会显示详细的分析结果
   - 包括是否听牌、可胡牌、胡牌类型等

3. 快捷键：
   - Ctrl+N: 新建手牌
   - Ctrl+S: 保存手牌
   - Ctrl+O: 加载手牌
   - Ctrl+C: 清空手牌
   - Ctrl+Z: 撤销
   - F5: 分析手牌

4. 支持的胡牌类型：
   - 标准胡牌（4面子+1对子）
   - 七对子
   - 国士无双
   - 所有类型都支持百搭牌

5. 百搭牌功能：
   - 百搭牌可以替代任何普通牌
   - 程序会自动计算最优替换方案
   - 支持多个百搭牌的组合
"""
        
        help_window = tk.Toplevel(self.root)
        help_window.title("使用说明")
        help_window.geometry("500x400")
        
        text_widget = tk.Text(help_window, wrap="word", padx=10, pady=10)
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", help_text)
        text_widget.config(state="disabled")
    
    def _show_about(self):
        """显示关于信息"""
        about_text = """
麻将听牌分析器 v3.0

一个功能强大的麻将听牌分析工具

✨ 主要特性：
• 图形化界面，操作简单直观
• 支持百搭牌功能
• 完整的国士无双判断
• 智能替换算法
• 雀魂风格界面设计

🛠️ 技术实现：
• Python 3.6+
• tkinter GUI框架
• PIL图像处理
• 高效的算法优化

📅 版本历史：
v3.0 - 图形界面版本
v2.0 - 百搭牌功能版本
v1.0 - 基础命令行版本

© 2025 麻将听牌分析器
"""
        messagebox.showinfo("关于", about_text)
    
    def _update_status(self):
        """更新状态栏"""
        hand = self.hand_panel.get_hand()
        self.count_label.config(text=f"手牌: {len(hand)}/13")
    
    def run(self):
        """运行程序"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n程序被用户中断")
        except Exception as e:
            print(f"程序运行出错: {e}")
            messagebox.showerror("严重错误", f"程序运行出错: {e}")

def main():
    """主函数"""
    print("正在启动麻将听牌分析器 v3.0...")
    
    try:
        app = MahjongGUI()
        app.run()
    except Exception as e:
        print(f"启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()