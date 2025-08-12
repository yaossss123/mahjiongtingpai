#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麻将听牌判断程序
输入13张牌，计算出哪些牌可以胡牌

牌型表示：
- 123456789s: 条子（索子）
- 123456789m: 万子
- 123456789p: 筒子（饼子）
- 1234567z: 东南西北白发中
"""

import re
from collections import Counter
from typing import List, Set, Tuple

class MahjongTingpai:
    def __init__(self):
        # 定义所有可能的牌
        self.all_tiles = (
            [f"{i}s" for i in range(1, 10)] +  # 条子
            [f"{i}m" for i in range(1, 10)] +  # 万子
            [f"{i}p" for i in range(1, 10)] +  # 筒子
            [f"{i}z" for i in range(1, 8)]    # 字牌：东南西北白发中
        )
        
        # 字牌名称映射
        self.honor_names = {
            '1z': '东', '2z': '南', '3z': '西', '4z': '北',
            '5z': '白', '6z': '发', '7z': '中'
        }
    
    def parse_hand(self, hand_str: str) -> List[str]:
        """
        解析手牌字符串
        例如: "123456789s1234m12p" -> ['1s', '2s', '3s', ...]
        """
        tiles = []
        pattern = r'(\d+)([smpz])'
        matches = re.findall(pattern, hand_str)
        
        for numbers, suit in matches:
            for num in numbers:
                tiles.append(f"{num}{suit}")
        
        return sorted(tiles)
    
    def is_valid_sequence(self, tiles: List[str]) -> bool:
        """
        判断是否为有效顺子（同花色连续3张）
        """
        if len(tiles) != 3:
            return False
        
        # 字牌不能组成顺子
        if any(tile.endswith('z') for tile in tiles):
            return False
        
        # 检查是否同花色
        suits = [tile[-1] for tile in tiles]
        if len(set(suits)) != 1:
            return False
        
        # 检查是否连续
        numbers = sorted([int(tile[0]) for tile in tiles])
        return numbers == [numbers[0], numbers[0]+1, numbers[0]+2]
    
    def is_valid_triplet(self, tiles: List[str]) -> bool:
        """
        判断是否为有效刻子（3张相同牌）
        """
        return len(tiles) == 3 and len(set(tiles)) == 1
    
    def is_valid_pair(self, tiles: List[str]) -> bool:
        """
        判断是否为有效对子（2张相同牌）
        """
        return len(tiles) == 2 and len(set(tiles)) == 1
    
    def can_form_meld(self, tiles: List[str]) -> bool:
        """
        判断牌组是否能组成面子（顺子或刻子）或对子
        """
        if len(tiles) == 2:
            return self.is_valid_pair(tiles)
        elif len(tiles) == 3:
            return self.is_valid_sequence(tiles) or self.is_valid_triplet(tiles)
        return False
    
    def is_winning_hand(self, tiles: List[str]) -> bool:
        """
        判断14张牌是否为胡牌牌型
        标准胡牌：4个面子 + 1个对子
        """
        if len(tiles) != 14:
            return False
        
        return self._check_standard_win(tiles) or self._check_seven_pairs(tiles)
    
    def _check_seven_pairs(self, tiles: List[str]) -> bool:
        """
        检查是否为七对子
        """
        counter = Counter(tiles)
        pairs = [count for count in counter.values() if count == 2]
        return len(pairs) == 7 and sum(counter.values()) == 14
    
    def _check_standard_win(self, tiles: List[str]) -> bool:
        """
        检查是否为标准胡牌（4面子+1对子）
        """
        return self._try_combinations(tiles, [], 0)
    
    def _try_combinations(self, remaining: List[str], groups: List[List[str]], pair_count: int) -> bool:
        """
        递归尝试所有可能的组合
        """
        if not remaining:
            # 检查是否有4个面子和1个对子
            melds = [g for g in groups if len(g) == 3]
            pairs = [g for g in groups if len(g) == 2]
            return len(melds) == 4 and len(pairs) == 1
        
        if len(groups) > 5:  # 最多5组（4面子+1对子）
            return False
        
        # 对剩余牌进行排序，确保处理顺序一致
        remaining_sorted = sorted(remaining)
        
        # 取第一张牌，避免重复计算
        first_tile = remaining_sorted[0]
        
        # 尝试组成对子（只有当还没有对子时）
        if pair_count == 0 and remaining_sorted.count(first_tile) >= 2:
            new_remaining = remaining_sorted.copy()
            new_remaining.remove(first_tile)
            new_remaining.remove(first_tile)
            new_groups = groups + [[first_tile, first_tile]]
            if self._try_combinations(new_remaining, new_groups, 1):
                return True
        
        # 尝试组成刻子
        if remaining_sorted.count(first_tile) >= 3:
            new_remaining = remaining_sorted.copy()
            new_remaining.remove(first_tile)
            new_remaining.remove(first_tile)
            new_remaining.remove(first_tile)
            new_groups = groups + [[first_tile, first_tile, first_tile]]
            if self._try_combinations(new_remaining, new_groups, pair_count):
                return True
        
        # 尝试组成顺子（非字牌）
        if not first_tile.endswith('z'):
            suit = first_tile[-1]
            num = int(first_tile[0])
            if num <= 7:  # 确保能组成顺子
                tile2 = f"{num+1}{suit}"
                tile3 = f"{num+2}{suit}"
                if tile2 in remaining_sorted and tile3 in remaining_sorted:
                    new_remaining = remaining_sorted.copy()
                    new_remaining.remove(first_tile)
                    new_remaining.remove(tile2)
                    new_remaining.remove(tile3)
                    new_groups = groups + [[first_tile, tile2, tile3]]
                    if self._try_combinations(new_remaining, new_groups, pair_count):
                        return True
        
        return False
    
    def find_winning_tiles(self, hand: List[str]) -> Set[str]:
        """
        找出所有可以胡牌的牌
        """
        if len(hand) != 13:
            raise ValueError("手牌必须是13张")
        
        winning_tiles = set()
        hand_counter = Counter(hand)
        
        for tile in self.all_tiles:
            # 检查加入这张牌是否会超过4张限制
            if hand_counter[tile] >= 4:
                continue
                
            test_hand = hand + [tile]
            if self.is_winning_hand(test_hand):
                winning_tiles.add(tile)
        
        return winning_tiles
    
    def analyze_hand(self, hand_str: str) -> dict:
        """
        分析手牌，返回详细信息
        """
        try:
            hand = self.parse_hand(hand_str)
            
            if len(hand) != 13:
                return {
                    'error': f'手牌数量错误：{len(hand)}张，应该是13张',
                    'hand': hand
                }
            
            # 检查牌的有效性
            invalid_tiles = [tile for tile in hand if tile not in self.all_tiles]
            if invalid_tiles:
                return {
                    'error': f'无效的牌：{invalid_tiles}',
                    'hand': hand
                }
            
            # 检查每种牌是否超过4张
            tile_count = Counter(hand)
            over_limit = [tile for tile, count in tile_count.items() if count > 4]
            if over_limit:
                return {
                    'error': f'以下牌超过4张限制：{over_limit}',
                    'hand': hand
                }
            
            winning_tiles = self.find_winning_tiles(hand)
            
            # 统计手牌信息
            suits_count = {
                's': len([t for t in hand if t.endswith('s')]),
                'm': len([t for t in hand if t.endswith('m')]),
                'p': len([t for t in hand if t.endswith('p')]),
                'z': len([t for t in hand if t.endswith('z')])
            }
            
            return {
                'hand': hand,
                'hand_str': hand_str,
                'tile_count': len(hand),
                'suits_distribution': suits_count,
                'winning_tiles': sorted(list(winning_tiles)),
                'winning_count': len(winning_tiles),
                'is_tingpai': len(winning_tiles) > 0,
                'tile_frequency': dict(tile_count)
            }
            
        except Exception as e:
            return {
                'error': f'解析错误：{str(e)}',
                'hand_str': hand_str
            }
    
    def format_tile_name(self, tile: str) -> str:
        """
        格式化牌名显示
        """
        if tile.endswith('z'):
            return self.honor_names.get(tile, tile)
        elif tile.endswith('s'):
            return f"{tile[0]}条"
        elif tile.endswith('m'):
            return f"{tile[0]}万"
        elif tile.endswith('p'):
            return f"{tile[0]}筒"
        return tile
    
    def print_analysis(self, result: dict):
        """
        打印分析结果
        """
        print("=" * 50)
        print("麻将听牌分析结果")
        print("=" * 50)
        
        if 'error' in result:
            print(f"❌ 错误：{result['error']}")
            if 'hand' in result:
                print(f"解析的手牌：{result['hand']}")
            return
        
        print(f"输入：{result['hand_str']}")
        print(f"手牌：{' '.join(result['hand'])}")
        print(f"牌数：{result['tile_count']}张")
        
        # 显示花色分布
        suits = result['suits_distribution']
        print(f"花色分布：条{suits['s']}张，万{suits['m']}张，筒{suits['p']}张，字牌{suits['z']}张")
        
        # 显示牌频统计
        print("\n牌频统计：")
        for tile, count in sorted(result['tile_frequency'].items()):
            print(f"  {self.format_tile_name(tile)}: {count}张")
        
        # 显示听牌结果
        if result['is_tingpai']:
            print(f"\n🎉 听牌！可胡{result['winning_count']}种牌：")
            winning_names = [self.format_tile_name(tile) for tile in result['winning_tiles']]
            print(f"  {' '.join(result['winning_tiles'])}")
            print(f"  ({' '.join(winning_names)})")
        else:
            print("\n❌ 未听牌")
        
        print("=" * 50)

def main():
    """
    主函数
    """
    analyzer = MahjongTingpai()
    
    print("麻将听牌判断程序")
    print("输入格式：123456789s代表条子，123456789m代表万子，123456789p代表筒子，1234567z代表东南西北白发中")
    print("示例：123456789s1234m (13张牌)")
    print("输入 'quit' 退出程序\n")
    
    while True:
        try:
            hand_input = input("请输入13张手牌: ").strip()
            
            if hand_input.lower() in ['quit', 'exit', 'q']:
                print("程序退出")
                break
            
            if not hand_input:
                continue
            
            result = analyzer.analyze_hand(hand_input)
            analyzer.print_analysis(result)
            print()
            
        except KeyboardInterrupt:
            print("\n程序退出")
            break
        except Exception as e:
            print(f"程序错误：{e}")

if __name__ == '__main__':
    main()