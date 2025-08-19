#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI组件库
包含麻将程序所需的各种界面组件
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Optional
from asset_manager import AssetManager

class TileWidget:
    """麻将牌显示组件"""
    
    def __init__(self, parent, asset_manager: AssetManager, 
                 tile_code: Optional[str] = None, 
                 clickable: bool = True,
                 click_callback: Optional[Callable] = None):
        self.parent = parent
        self.asset_manager = asset_manager
        self.tile_code = tile_code
        self.clickable = clickable
        self.click_callback = click_callback
        self.selected = False
        
        # 创建框架
        self.frame = tk.Frame(parent, relief="raised", borderwidth=1)
        
        # 创建标签
        self.label = tk.Label(self.frame, cursor="hand2" if clickable else "")
        self.label.pack()
        
        # 绑定点击事件
        if clickable:
            self.label.bind("<Button-1>", self._on_click)
            self.frame.bind("<Button-1>", self._on_click)
        
        # 更新显示
        self.update_display()
    
    def _on_click(self, event):
        """处理点击事件"""
        if self.clickable and self.click_callback:
            self.click_callback(self)
    
    def update_display(self):
        """更新牌面显示"""
        if self.tile_code:
            image = self.asset_manager.get_tile_image(self.tile_code)
            if image:
                self.label.config(image=image)
                self.label.image = image  # 保持引用
            else:
                # 显示文字
                tile_name = self.asset_manager._get_tile_name(self.tile_code)
                self.label.config(image="", text=tile_name, 
                                width=8, height=4, bg="white")
        else:
            # 显示空位
            self.label.config(image="", text="+", 
                            width=8, height=4, bg="lightgray")
        
        # 更新选中状态
        if self.selected:
            self.frame.config(relief="sunken", bg="yellow")
        else:
            self.frame.config(relief="raised", bg="white")
    
    def set_tile(self, tile_code: Optional[str]):
        """设置牌码"""
        self.tile_code = tile_code
        self.update_display()
    
    def set_selected(self, selected: bool):
        """设置选中状态"""
        self.selected = selected
        self.update_display()
    
    def pack(self, **kwargs):
        """打包组件"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """网格布局"""
        self.frame.grid(**kwargs)

class HandPanel:
    """手牌显示面板"""
    
    def __init__(self, parent, asset_manager: AssetManager, max_tiles: int = 14):
        self.parent = parent
        self.asset_manager = asset_manager
        self.max_tiles = max_tiles
        self.tiles: List[Optional[str]] = [None] * max_tiles
        self.tile_widgets: List[TileWidget] = []
        
        # 创建主框架
        self.frame = tk.LabelFrame(parent, text="手牌", font=('Arial', 12, 'bold'))
        
        # 创建牌位
        self._create_tile_slots()
    
    def _create_tile_slots(self):
        """创建牌位"""
        # 创建牌位框架
        tiles_frame = tk.Frame(self.frame)
        tiles_frame.pack(pady=10)
        
        # 创建牌位组件
        for i in range(self.max_tiles):
            tile_widget = TileWidget(
                tiles_frame, 
                self.asset_manager,
                clickable=True,
                click_callback=self._on_tile_click
            )
            tile_widget.grid(row=0, column=i, padx=2, pady=2)
            self.tile_widgets.append(tile_widget)
    
    def _on_tile_click(self, tile_widget: TileWidget):
        """处理牌位点击"""
        # 找到点击的牌位索引
        index = self.tile_widgets.index(tile_widget)
        
        # 如果有牌，则移除；如果没牌，则等待添加
        if self.tiles[index] is not None:
            self.remove_tile(index)
        else:
            # 这里可以触发牌选择器
            print(f"点击了空牌位 {index}")
    
    def add_tile(self, tile_code: str) -> bool:
        """添加牌到手牌"""
        # 找到第一个空位
        for i, tile in enumerate(self.tiles):
            if tile is None:
                self.tiles[i] = tile_code
                self.tile_widgets[i].set_tile(tile_code)
                return True
        return False  # 手牌已满
    
    def remove_tile(self, index: int):
        """移除指定位置的牌"""
        if 0 <= index < len(self.tiles):
            self.tiles[index] = None
            self.tile_widgets[index].set_tile(None)
    
    def set_hand(self, tiles: List[str]):
        """设置整手牌"""
        # 清空当前手牌
        self.clear()
        
        # 添加新牌
        for tile_code in tiles[:self.max_tiles]:
            self.add_tile(tile_code)
    
    def get_hand(self) -> List[str]:
        """获取当前手牌"""
        return [tile for tile in self.tiles if tile is not None]
    
    def clear(self):
        """清空手牌"""
        for i in range(len(self.tiles)):
            self.tiles[i] = None
            self.tile_widgets[i].set_tile(None)
    
    def pack(self, **kwargs):
        """打包组件"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """网格布局"""
        self.frame.grid(**kwargs)

class TileSelector:
    """牌选择器"""
    
    def __init__(self, parent, asset_manager: AssetManager, 
                 selection_callback: Optional[Callable] = None):
        self.parent = parent
        self.asset_manager = asset_manager
        self.selection_callback = selection_callback
        
        # 创建主框架
        self.frame = tk.LabelFrame(parent, text="选择麻将牌", font=('Arial', 12, 'bold'))
        
        # 创建选择器
        self._create_selector()
    
    def _create_selector(self):
        """创建牌选择器界面"""
        # 万子
        man_frame = tk.LabelFrame(self.frame, text="万子")
        man_frame.pack(fill="x", padx=5, pady=2)
        
        for i in range(1, 10):
            tile_code = f"{i}m"
            btn = tk.Button(man_frame, 
                          command=lambda tc=tile_code: self._select_tile(tc))
            
            image = self.asset_manager.get_tile_image(tile_code)
            if image:
                btn.config(image=image)
                btn.image = image
            else:
                btn.config(text=self.asset_manager._get_tile_name(tile_code))
            
            btn.pack(side="left", padx=1)
        
        # 筒子
        pin_frame = tk.LabelFrame(self.frame, text="筒子")
        pin_frame.pack(fill="x", padx=5, pady=2)
        
        for i in range(1, 10):
            tile_code = f"{i}p"
            btn = tk.Button(pin_frame, 
                          command=lambda tc=tile_code: self._select_tile(tc))
            
            image = self.asset_manager.get_tile_image(tile_code)
            if image:
                btn.config(image=image)
                btn.image = image
            else:
                btn.config(text=self.asset_manager._get_tile_name(tile_code))
            
            btn.pack(side="left", padx=1)
        
        # 条子
        sou_frame = tk.LabelFrame(self.frame, text="条子")
        sou_frame.pack(fill="x", padx=5, pady=2)
        
        for i in range(1, 10):
            tile_code = f"{i}s"
            btn = tk.Button(sou_frame, 
                          command=lambda tc=tile_code: self._select_tile(tc))
            
            image = self.asset_manager.get_tile_image(tile_code)
            if image:
                btn.config(image=image)
                btn.image = image
            else:
                btn.config(text=self.asset_manager._get_tile_name(tile_code))
            
            btn.pack(side="left", padx=1)
        
        # 字牌
        honor_frame = tk.LabelFrame(self.frame, text="字牌")
        honor_frame.pack(fill="x", padx=5, pady=2)
        
        for i in range(1, 8):
            tile_code = f"{i}z"
            btn = tk.Button(honor_frame, 
                          command=lambda tc=tile_code: self._select_tile(tc))
            
            image = self.asset_manager.get_tile_image(tile_code)
            if image:
                btn.config(image=image)
                btn.image = image
            else:
                btn.config(text=self.asset_manager._get_tile_name(tile_code))
            
            btn.pack(side="left", padx=1)
        
        # 百搭牌
        joker_frame = tk.LabelFrame(self.frame, text="特殊牌")
        joker_frame.pack(fill="x", padx=5, pady=2)
        
        joker_btn = tk.Button(joker_frame, 
                            command=lambda: self._select_tile('j'))
        
        joker_image = self.asset_manager.get_tile_image('j')
        if joker_image:
            joker_btn.config(image=joker_image)
            joker_btn.image = joker_image
        else:
            joker_btn.config(text="百搭")
        
        joker_btn.pack(side="left", padx=1)
    
    def _select_tile(self, tile_code: str):
        """选择牌"""
        if self.selection_callback:
            self.selection_callback(tile_code)
    
    def pack(self, **kwargs):
        """打包组件"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """网格布局"""
        self.frame.grid(**kwargs)

class ResultPanel:
    """结果显示面板"""
    
    def __init__(self, parent, asset_manager: AssetManager):
        self.parent = parent
        self.asset_manager = asset_manager
        
        # 创建主框架
        self.frame = tk.LabelFrame(parent, text="分析结果", font=('Arial', 12, 'bold'))
        
        # 创建结果显示区域
        self._create_result_area()
    
    def _create_result_area(self):
        """创建结果显示区域"""
        # 听牌状态
        self.status_label = tk.Label(self.frame, text="请输入手牌进行分析", 
                                   font=('Arial', 14), fg="blue")
        self.status_label.pack(pady=5)
        
        # 可胡牌显示
        winning_frame = tk.LabelFrame(self.frame, text="可胡牌")
        winning_frame.pack(fill="x", padx=5, pady=5)
        
        self.winning_tiles_frame = tk.Frame(winning_frame)
        self.winning_tiles_frame.pack(pady=5)
        
        # 胡牌类型
        self.type_label = tk.Label(self.frame, text="", font=('Arial', 12))
        self.type_label.pack(pady=5)
        
        # 详细信息
        self.detail_text = tk.Text(self.frame, height=8, width=60)
        self.detail_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 添加滚动条
        scrollbar = tk.Scrollbar(self.detail_text)
        scrollbar.pack(side="right", fill="y")
        self.detail_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.detail_text.yview)
    
    def update_result(self, result: dict):
        """更新分析结果"""
        # 清空之前的结果
        self._clear_result()
        
        if result.get('is_tingpai', False):
            self.status_label.config(text="✅ 听牌", fg="green")
            
            # 显示可胡牌
            winning_tiles = result.get('winning_tiles', [])
            self._display_winning_tiles(winning_tiles)
            
            # 显示胡牌类型
            winning_types = result.get('winning_types', {})
            if winning_types:
                type_text = "胡牌类型: " + ", ".join(winning_types.keys())
                self.type_label.config(text=type_text, fg="green")
        else:
            self.status_label.config(text="❌ 未听牌", fg="red")
            self.type_label.config(text="")
        
        # 显示详细信息
        self._display_details(result)
    
    def _display_winning_tiles(self, winning_tiles: List[str]):
        """显示可胡牌"""
        for i, tile_code in enumerate(winning_tiles):
            tile_widget = TileWidget(
                self.winning_tiles_frame,
                self.asset_manager,
                tile_code,
                clickable=False
            )
            tile_widget.grid(row=0, column=i, padx=2, pady=2)
    
    def _display_details(self, result: dict):
        """显示详细信息"""
        self.detail_text.delete(1.0, tk.END)
        
        # 手牌统计
        hand_stats = result.get('hand_stats', {})
        if hand_stats:
            self.detail_text.insert(tk.END, "=== 手牌统计 ===\n")
            for suit, count in hand_stats.items():
                self.detail_text.insert(tk.END, f"{suit}: {count}张\n")
            self.detail_text.insert(tk.END, "\n")
        
        # 听牌详情
        if result.get('is_tingpai', False):
            self.detail_text.insert(tk.END, "=== 听牌详情 ===\n")
            winning_types = result.get('winning_types', {})
            for tile, types in winning_types.items():
                tile_name = self.asset_manager._get_tile_name(tile)
                self.detail_text.insert(tk.END, f"{tile_name}({tile}): {', '.join(types)}\n")
            self.detail_text.insert(tk.END, "\n")
        
        # 百搭牌信息
        joker_info = result.get('joker_info', {})
        if joker_info:
            self.detail_text.insert(tk.END, "=== 百搭牌信息 ===\n")
            self.detail_text.insert(tk.END, f"百搭牌数量: {joker_info.get('count', 0)}\n")
            replacements = joker_info.get('possible_replacements', [])
            if replacements:
                self.detail_text.insert(tk.END, "可能的替换方案:\n")
                for replacement in replacements[:5]:  # 只显示前5个
                    self.detail_text.insert(tk.END, f"  {replacement}\n")
    
    def _clear_result(self):
        """清空结果显示"""
        # 清空可胡牌显示
        for widget in self.winning_tiles_frame.winfo_children():
            widget.destroy()
    
    def pack(self, **kwargs):
        """打包组件"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """网格布局"""
        self.frame.grid(**kwargs)

# 测试代码
if __name__ == "__main__":
    root = tk.Tk()
    root.title("GUI组件测试")
    
    # 初始化资源管理器
    asset_manager = AssetManager()
    
    # 测试手牌面板
    hand_panel = HandPanel(root, asset_manager)
    hand_panel.pack(pady=10)
    
    # 添加一些测试牌
    test_hand = ['1m', '2m', '3m', '4p', '5p', '6p', '7s', '8s', '9s', '1z', '1z', '2z', 'j']
    hand_panel.set_hand(test_hand)
    
    root.mainloop()