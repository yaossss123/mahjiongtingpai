#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麻将图片资源管理器
负责加载、缓存和管理所有麻将牌面图片
"""

import os
import tkinter as tk
from PIL import Image, ImageTk
from typing import Dict, Optional
import requests
from io import BytesIO

class AssetManager:
    """图片资源管理器"""
    
    def __init__(self, assets_dir: str = "assets"):
        self.assets_dir = assets_dir
        self.tile_images: Dict[str, ImageTk.PhotoImage] = {}
        self.tile_size = (64, 88)  # 标准麻将牌尺寸
        
        # 确保资源目录存在
        self._ensure_directories()
        
        # 初始化默认图片
        self._create_default_images()
        
        # 加载所有图片
        self.load_all_images()
    
    def _ensure_directories(self):
        """确保所有必要的目录存在"""
        directories = [
            self.assets_dir,
            os.path.join(self.assets_dir, "tiles"),
            os.path.join(self.assets_dir, "tiles", "man"),
            os.path.join(self.assets_dir, "tiles", "pin"),
            os.path.join(self.assets_dir, "tiles", "sou"),
            os.path.join(self.assets_dir, "tiles", "honor"),
            os.path.join(self.assets_dir, "ui")
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def _create_default_images(self):
        """创建默认的占位图片"""
        # 创建默认牌面图片（如果没有找到实际图片）
        default_image = Image.new('RGB', self.tile_size, color='lightgray')
        self.default_tile_image = ImageTk.PhotoImage(default_image)
    
    def load_all_images(self):
        """加载所有麻将牌图片"""
        # 定义所有牌的代码
        all_tiles = [
            # 万子 (man)
            '1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m',
            # 筒子 (pin)
            '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p',
            # 条子 (sou)
            '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s',
            # 字牌 (honor)
            '1z', '2z', '3z', '4z', '5z', '6z', '7z'
        ]
        
        # 加载普通牌
        for tile_code in all_tiles:
            self._load_tile_image(tile_code)
        
        # 加载特殊牌
        self._load_special_images()
    
    def _load_tile_image(self, tile_code: str):
        """加载单个牌的图片"""
        # 确定图片路径
        suit = tile_code[1]  # m, p, s, z
        number = tile_code[0]
        
        suit_dirs = {'m': 'man', 'p': 'pin', 's': 'sou', 'z': 'honor'}
        suit_dir = suit_dirs.get(suit, 'tiles')
        
        image_path = os.path.join(self.assets_dir, "tiles", suit_dir, f"{tile_code}.png")
        
        try:
            if os.path.exists(image_path):
                image = Image.open(image_path)
                # 修复：使用兼容的重采样方法
                try:
                    image = image.resize(self.tile_size, Image.Resampling.LANCZOS)
                except AttributeError:
                    # 兼容旧版本 Pillow
                    image = image.resize(self.tile_size, Image.LANCZOS)
                self.tile_images[tile_code] = ImageTk.PhotoImage(image)
            else:
                # 使用默认图片并添加文字标识
                self._create_text_tile(tile_code)
        except Exception as e:
            print(f"加载图片失败 {image_path}: {e}")
            self._create_text_tile(tile_code)
    
    def _create_text_tile(self, tile_code: str):
        """创建带文字的默认牌面"""
        from PIL import ImageDraw, ImageFont
        
        # 创建基础图片
        image = Image.new('RGB', self.tile_size, color='white')
        draw = ImageDraw.Draw(image)
        
        # 绘制边框
        draw.rectangle([0, 0, self.tile_size[0]-1, self.tile_size[1]-1], 
                      outline='black', width=2)
        
        # 添加文字
        tile_name = self._get_tile_name(tile_code)
        
        try:
            # 尝试使用系统字体
            font = ImageFont.truetype("msyh.ttc", 16)  # 微软雅黑
        except:
            try:
                font = ImageFont.truetype("arial.ttf", 14)
            except:
                font = ImageFont.load_default()
        
        # 计算文字位置
        try:
            bbox = draw.textbbox((0, 0), tile_name, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            # 兼容旧版本 PIL
            text_width, text_height = draw.textsize(tile_name, font=font)
        
        x = (self.tile_size[0] - text_width) // 2
        y = (self.tile_size[1] - text_height) // 2
        
        # 绘制文字
        draw.text((x, y), tile_name, fill='black', font=font)
        
        # 转换为PhotoImage
        self.tile_images[tile_code] = ImageTk.PhotoImage(image)
    
    def _load_special_images(self):
        """加载特殊图片（百搭牌、牌背等）"""
        # 百搭牌
        joker_path = os.path.join(self.assets_dir, "tiles", "joker.png")
        if os.path.exists(joker_path):
            image = Image.open(joker_path)
            try:
                image = image.resize(self.tile_size, Image.Resampling.LANCZOS)
            except AttributeError:
                image = image.resize(self.tile_size, Image.LANCZOS)
            self.tile_images['j'] = ImageTk.PhotoImage(image)
        else:
            self._create_joker_tile()
        
        # 牌背
        back_path = os.path.join(self.assets_dir, "tiles", "back.png")
        if os.path.exists(back_path):
            image = Image.open(back_path)
            try:
                image = image.resize(self.tile_size, Image.Resampling.LANCZOS)
            except AttributeError:
                image = image.resize(self.tile_size, Image.LANCZOS)
            self.tile_images['back'] = ImageTk.PhotoImage(image)
        else:
            self._create_back_tile()
    
    def _create_joker_tile(self):
        """创建百搭牌图片"""
        from PIL import ImageDraw, ImageFont
        
        image = Image.new('RGB', self.tile_size, color='gold')
        draw = ImageDraw.Draw(image)
        
        # 绘制边框
        draw.rectangle([0, 0, self.tile_size[0]-1, self.tile_size[1]-1], 
                      outline='red', width=3)
        
        # 添加百搭标识
        try:
            font = ImageFont.truetype("msyh.ttc", 14)
        except:
            font = ImageFont.load_default()
        
        text = "百搭"
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            text_width, text_height = draw.textsize(text, font=font)
        
        x = (self.tile_size[0] - text_width) // 2
        y = (self.tile_size[1] - text_height) // 2
        
        draw.text((x, y), text, fill='red', font=font)
        
        self.tile_images['j'] = ImageTk.PhotoImage(image)
    
    def _create_back_tile(self):
        """创建牌背图片"""
        from PIL import ImageDraw
        
        image = Image.new('RGB', self.tile_size, color='darkblue')
        draw = ImageDraw.Draw(image)
        
        # 绘制花纹
        for i in range(0, self.tile_size[0], 8):
            for j in range(0, self.tile_size[1], 8):
                if (i + j) % 16 == 0:
                    draw.rectangle([i, j, i+4, j+4], fill='lightblue')
        
        self.tile_images['back'] = ImageTk.PhotoImage(image)
    
    def _get_tile_name(self, tile_code: str) -> str:
        """获取牌的中文名称"""
        tile_names = {
            # 万子
            '1m': '一万', '2m': '二万', '3m': '三万', '4m': '四万', '5m': '五万',
            '6m': '六万', '7m': '七万', '8m': '八万', '9m': '九万',
            # 筒子
            '1p': '一筒', '2p': '二筒', '3p': '三筒', '4p': '四筒', '5p': '五筒',
            '6p': '六筒', '7p': '七筒', '8p': '八筒', '9p': '九筒',
            # 条子
            '1s': '一条', '2s': '二条', '3s': '三条', '4s': '四条', '5s': '五条',
            '6s': '六条', '7s': '七条', '8s': '八条', '9s': '九条',
            # 字牌
            '1z': '东', '2z': '南', '3z': '西', '4z': '北',
            '5z': '白', '6z': '发', '7z': '中',
            # 特殊
            'j': '百搭'
        }
        return tile_names.get(tile_code, tile_code)
    
    def get_tile_image(self, tile_code: str) -> Optional[ImageTk.PhotoImage]:
        """获取指定牌的图片"""
        return self.tile_images.get(tile_code)
    
    def get_back_image(self) -> Optional[ImageTk.PhotoImage]:
        """获取牌背图片"""
        return self.tile_images.get('back')
    
    def download_majsoul_assets(self):
        """下载雀魂官方素材（示例函数）"""
        # 这里可以添加从雀魂官网下载素材的代码
        # 注意：实际使用时需要遵守版权和使用条款
        print("素材下载功能待实现...")
        print("请手动将雀魂素材放置到 assets/tiles/ 目录下")
        
    def reload_assets(self):
        """重新加载所有资源"""
        self.tile_images.clear()
        self.load_all_images()
        print("资源重新加载完成")


# 测试代码
if __name__ == "__main__":
    # 创建测试窗口
    root = tk.Tk()
    root.title("资源管理器测试")
    
    # 初始化资源管理器
    asset_manager = AssetManager()
    
    # 显示一些牌面图片
    test_tiles = ['1m', '5p', '9s', '1z', 'j']
    
    for i, tile_code in enumerate(test_tiles):
        image = asset_manager.get_tile_image(tile_code)
        if image:
            label = tk.Label(root, image=image)
            label.grid(row=0, column=i, padx=5, pady=5)
            
            # 添加标签
            name_label = tk.Label(root, text=asset_manager._get_tile_name(tile_code))
            name_label.grid(row=1, column=i, padx=5, pady=5)
    
    root.mainloop()