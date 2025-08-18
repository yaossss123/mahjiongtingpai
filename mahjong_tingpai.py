#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麻将听牌判断程序（支持百搭牌）
输入13张牌，计算出哪些牌可以胡牌

牌型表示：
- 123456789s: 条子（索子）
- 123456789m: 万子
- 123456789p: 筒子（饼子）
- 1234567z: 东南西北白发中
- j: 百搭牌（可以替代任何牌）
"""

import re
from collections import Counter
from typing import List, Set, Tuple
from itertools import product

class MahjongTingpaiWithJoker:
    def __init__(self):
        # 定义所有可能的牌（不包括百搭牌）
        self.normal_tiles = (
            [f"{i}s" for i in range(1, 10)] +  # 条子
            [f"{i}m" for i in range(1, 10)] +  # 万子
            [f"{i}p" for i in range(1, 10)] +  # 筒子
            [f"{i}z" for i in range(1, 8)]    # 字牌：东南西北白发中
        )
        
        # 包括百搭牌的所有牌
        self.all_tiles = self.normal_tiles + ['j']
        
        # 字牌名称映射
        self.honor_names = {
            '1z': '东', '2z': '南', '3z': '西', '4z': '北',
            '5z': '白', '6z': '发', '7z': '中', 'j': '百搭'
        }
        
        # 国士无双的幺九牌
        self.terminal_honor_tiles = [
            '1s', '9s',  # 一九条
            '1m', '9m',  # 一九万
            '1p', '9p',  # 一九筒
            '1z', '2z', '3z', '4z', '5z', '6z', '7z'  # 东南西北白发中
        ]
    
    def parse_hand(self, hand_str: str) -> List[str]:
        """
        解析手牌字符串，支持百搭牌j
        例如: "123456789s1234m12pj" -> ['1s', '2s', '3s', ..., 'j']
        """
        tiles = []
        
        # 处理百搭牌
        joker_count = hand_str.count('j')
        hand_str_no_joker = hand_str.replace('j', '')
        
        # 处理普通牌
        pattern = r'(\d+)([smpz])'
        matches = re.findall(pattern, hand_str_no_joker)
        
        for numbers, suit in matches:
            for num in numbers:
                tiles.append(f"{num}{suit}")
        
        # 添加百搭牌
        tiles.extend(['j'] * joker_count)
        
        return sorted(tiles)
    
    def generate_joker_combinations(self, hand: List[str]) -> List[List[str]]:
        """
        生成所有可能的百搭牌替换组合
        """
        joker_count = hand.count('j')
        if joker_count == 0:
            return [hand]
        
        # 移除百搭牌，获得基础手牌
        base_hand = [tile for tile in hand if tile != 'j']
        
        # 如果百搭牌太多，限制组合数量以避免性能问题
        if joker_count > 4:
            joker_count = 4
        
        # 生成所有可能的替换组合
        combinations = []
        for replacement in product(self.normal_tiles, repeat=joker_count):
            new_hand = base_hand + list(replacement)
            combinations.append(sorted(new_hand))
        
        # 去重
        unique_combinations = []
        seen = set()
        for combo in combinations:
            combo_tuple = tuple(combo)
            if combo_tuple not in seen:
                seen.add(combo_tuple)
                unique_combinations.append(combo)
        
        return unique_combinations
    
    def is_valid_sequence(self, tiles: List[str]) -> bool:
        """
        检查是否为有效顺子（3张连续的同花色牌）
        """
        if len(tiles) != 3:
            return False
        
        # 字牌不能组成顺子
        if any(tile.endswith('z') for tile in tiles):
            return False
        
        # 检查花色是否相同
        suits = [tile[-1] for tile in tiles]
        if len(set(suits)) != 1:
            return False
        
        # 检查数字是否连续
        numbers = sorted([int(tile[0]) for tile in tiles])
        return numbers == [numbers[0], numbers[0]+1, numbers[0]+2]
    
    def is_valid_triplet(self, tiles: List[str]) -> bool:
        """
        检查是否为有效刻子（3张相同的牌）
        """
        return len(tiles) == 3 and len(set(tiles)) == 1
    
    def is_valid_pair(self, tiles: List[str]) -> bool:
        """
        检查是否为有效对子（2张相同的牌）
        """
        return len(tiles) == 2 and tiles[0] == tiles[1]
    
    def can_form_meld(self, tiles: List[str]) -> bool:
        """
        检查牌组是否能组成面子或对子
        """
        if len(tiles) == 2:
            return self.is_valid_pair(tiles)
        elif len(tiles) == 3:
            return self.is_valid_sequence(tiles) or self.is_valid_triplet(tiles)
        return False
    
    def _check_thirteen_orphans(self, tiles: List[str]) -> bool:
        """
        检查是否为国士无双（十三幺）
        需要13种幺九牌各一张，其中一种成对
        """
        if len(tiles) != 14:
            return False
            
        tile_count = Counter(tiles)
        
        # 检查是否只包含幺九牌
        for tile in tiles:
            if tile not in self.terminal_honor_tiles:
                return False
        
        # 检查是否有且仅有一个对子，其余都是单张
        pair_count = 0
        single_count = 0
        
        for tile in self.terminal_honor_tiles:
            count = tile_count.get(tile, 0)
            if count == 2:
                pair_count += 1
            elif count == 1:
                single_count += 1
            elif count > 2 or count == 0:
                return False
        
        # 必须有12种单张 + 1种对子
        return pair_count == 1 and single_count == 12
    
    def _check_seven_pairs(self, tiles: List[str]) -> bool:
        """
        检查是否为七对子
        """
        if len(tiles) != 14:
            return False
            
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
    
    def is_winning_hand(self, tiles: List[str]) -> bool:
        """
        判断14张牌是否为胡牌牌型（支持百搭牌）
        """
        if len(tiles) != 14:
            return False
        
        # 如果没有百搭牌，直接检查
        if 'j' not in tiles:
            return (self._check_standard_win(tiles) or 
                    self._check_seven_pairs(tiles) or 
                    self._check_thirteen_orphans(tiles))
        
        # 有百搭牌时，尝试所有可能的替换组合
        combinations = self.generate_joker_combinations(tiles)
        
        for combo in combinations:
            if (self._check_standard_win(combo) or 
                self._check_seven_pairs(combo) or 
                self._check_thirteen_orphans(combo)):
                return True
        
        return False
    
    def get_winning_type(self, tiles: List[str]) -> str:
        """
        获取胡牌类型（支持百搭牌）
        """
        if len(tiles) != 14:
            return "非胡牌"
        
        # 如果没有百搭牌，直接检查
        if 'j' not in tiles:
            if self._check_thirteen_orphans(tiles):
                return "国士无双"
            elif self._check_seven_pairs(tiles):
                return "七对子"
            elif self._check_standard_win(tiles):
                return "标准胡牌"
            else:
                return "非胡牌"
        
        # 有百搭牌时，尝试所有可能的替换组合
        combinations = self.generate_joker_combinations(tiles)
        
        for combo in combinations:
            if self._check_thirteen_orphans(combo):
                return "国士无双（含百搭）"
            elif self._check_seven_pairs(combo):
                return "七对子（含百搭）"
            elif self._check_standard_win(combo):
                return "标准胡牌（含百搭）"
        
        return "非胡牌"
    
    def find_winning_tiles(self, hand: List[str]) -> Set[str]:
        """
        找出所有可以胡牌的牌（支持百搭牌）
        """
        if len(hand) != 13:
            raise ValueError("手牌必须是13张")
        
        winning_tiles = set()
        hand_counter = Counter(hand)
        
        for tile in self.all_tiles:
            # 检查加入这张牌是否会超过4张限制（百搭牌除外）
            if tile != 'j' and hand_counter[tile] >= 4:
                continue
            
            test_hand = hand + [tile]
            if self.is_winning_hand(test_hand):
                winning_tiles.add(tile)
        
        return winning_tiles
    
    def analyze_hand(self, hand_str: str) -> dict:
        """
        分析手牌，返回详细信息（支持百搭牌）
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
            
            # 检查每种牌是否超过4张（百搭牌除外）
            tile_count = Counter(hand)
            over_limit = [tile for tile, count in tile_count.items() 
                         if tile != 'j' and count > 4]
            if over_limit:
                return {
                    'error': f'以下牌超过4张限制：{over_limit}',
                    'hand': hand
                }
            
            winning_tiles = self.find_winning_tiles(hand)
            
            # 分析可能的胡牌类型
            winning_types = set()
            for tile in winning_tiles:
                test_hand = hand + [tile]
                win_type = self.get_winning_type(test_hand)
                if win_type != "非胡牌":
                    winning_types.add(win_type)
            
            # 统计手牌信息
            suits_count = {
                's': len([t for t in hand if t.endswith('s')]),
                'm': len([t for t in hand if t.endswith('m')]),
                'p': len([t for t in hand if t.endswith('p')]),
                'z': len([t for t in hand if t.endswith('z')]),
                'j': hand.count('j')
            }
            
            return {
                'hand': hand,
                'hand_str': hand_str,
                'tile_count': len(hand),
                'suits_distribution': suits_count,
                'winning_tiles': sorted(list(winning_tiles)),
                'winning_count': len(winning_tiles),
                'winning_types': list(winning_types),
                'is_tingpai': len(winning_tiles) > 0,
                'tile_frequency': dict(tile_count),
                'joker_count': hand.count('j')
            }
            
        except Exception as e:
            return {
                'error': f'解析错误：{str(e)}',
                'hand_str': hand_str
            }
    
    def format_tile_name(self, tile: str) -> str:
        """
        格式化牌名显示（支持百搭牌）
        """
        if tile == 'j':
            return '百搭'
        elif tile.endswith('z'):
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
        打印分析结果（支持百搭牌）
        """
        print("=" * 60)
        print("麻将听牌分析结果（支持百搭牌）")
        print("=" * 60)
        
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
        print(f"花色分布：条{suits['s']}张，万{suits['m']}张，筒{suits['p']}张，字牌{suits['z']}张，百搭{suits['j']}张")
        
        # 显示牌频统计
        print("\n牌频统计：")
        for tile, count in sorted(result['tile_frequency'].items()):
            print(f"  {self.format_tile_name(tile)}: {count}张")
        
        # 显示百搭牌信息
        if result.get('joker_count', 0) > 0:
            print(f"\n🃏 包含{result['joker_count']}张百搭牌")
        
        # 显示听牌结果
        if result['is_tingpai']:
            print(f"\n🎉 听牌！可胡{result['winning_count']}种牌：")
            winning_names = [self.format_tile_name(tile) for tile in result['winning_tiles']]
            print(f"  {' '.join(result['winning_tiles'])}")
            print(f"  ({' '.join(winning_names)})")
            
            # 显示可能的胡牌类型
            if 'winning_types' in result and result['winning_types']:
                print(f"\n可能的胡牌类型：{', '.join(result['winning_types'])}")
        else:
            print("\n❌ 未听牌")
        
        print("=" * 60)

def main():
    """
    主函数
    """
    analyzer = MahjongTingpaiWithJoker()
    
    print("麻将听牌判断程序（支持百搭牌）")
    print("输入格式：123456789s代表条子，123456789m代表万子，123456789p代表筒子，1234567z代表东南西北白发中")
    print("百搭牌用j表示，可以替代任何牌")
    print("示例：123456789s123mj (13张牌，包含1张百搭牌)")
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