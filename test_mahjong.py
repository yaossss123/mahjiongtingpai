#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麻将听牌判断程序测试文件
包含各种典型的听牌情况测试
"""

from mahjong_tingpai import MahjongTingpai

def test_cases():
    """
    测试各种听牌情况
    """
    analyzer = MahjongTingpai()
    
    test_hands = [
        # 基本听牌情况
        {
            'name': '单钓听牌',
            'hand': '111222333444m5',  # 听5万
            'expected_wins': ['5m']
        },
        {
            'name': '边张听牌',
            'hand': '12345678m1122p7',  # 听7筒
            'expected_wins': ['7p']
        },
        {
            'name': '坎张听牌',
            'hand': '12345678m1133p2',  # 听2筒
            'expected_wins': ['2p']
        },
        {
            'name': '两面听牌',
            'hand': '12345678m112p34p',  # 听2筒或5筒
            'expected_wins': ['2p', '5p']
        },
        {
            'name': '多面听牌',
            'hand': '123789m11223p456s',  # 复杂听牌
        },
        {
            'name': '七对子听牌',
            'hand': '1122334455667m8',  # 听8万（七对子）
            'expected_wins': ['8m']
        },
        {
            'name': '字牌听牌',
            'hand': '12345678m111z22z',  # 听2z（南）
            'expected_wins': ['2z']
        },
        {
            'name': '混合花色听牌',
            'hand': '123m456p789s111z2z',  # 听2z
            'expected_wins': ['2z']
        },
        # 特殊情况
        {
            'name': '无效手牌（12张）',
            'hand': '12345678m112p',  # 只有12张牌
        },
        {
            'name': '无效手牌（超过4张同牌）',
            'hand': '11111m2345678m12p',  # 1万超过4张
        },
        {
            'name': '无听牌情况',
            'hand': '147m258p369s1234z',  # 散牌无法听牌
        }
    ]
    
    print("=" * 60)
    print("麻将听牌判断程序 - 测试用例")
    print("=" * 60)
    
    for i, test in enumerate(test_hands, 1):
        print(f"\n测试 {i}: {test['name']}")
        print(f"手牌: {test['hand']}")
        
        result = analyzer.analyze_hand(test['hand'])
        
        if 'error' in result:
            print(f"❌ 错误: {result['error']}")
        else:
            if result.get('is_tingpai', False):
                print(f"✅ 听牌! 可胡: {result['winning_tiles']}")
                winning_names = [analyzer.format_tile_name(tile) for tile in result['winning_tiles']]
                print(f"   中文: {winning_names}")
                
                # 检查预期结果
                if 'expected_wins' in test:
                    expected = set(test['expected_wins'])
                    actual = set(result['winning_tiles'])
                    if expected.issubset(actual):
                        print(f"   ✓ 包含预期结果: {test['expected_wins']}")
                    else:
                        print(f"   ⚠ 预期: {test['expected_wins']}, 实际: {result['winning_tiles']}")
            else:
                print("❌ 未听牌")
        
        print("-" * 40)

def interactive_test():
    """
    交互式测试
    """
    analyzer = MahjongTingpai()
    
    print("\n" + "=" * 60)
    print("交互式测试模式")
    print("输入格式示例:")
    print("  123456789s1234m - 条子1-9 + 万子1-4")
    print("  111222333m444p5p - 万子三组刻子 + 筒子4,4,4,5")
    print("  1122334455667m8m - 七对子型")
    print("输入 'back' 返回菜单")
    print("=" * 60)
    
    while True:
        try:
            hand_input = input("\n请输入13张手牌: ").strip()
            
            if hand_input.lower() == 'back':
                break
            
            if not hand_input:
                continue
            
            result = analyzer.analyze_hand(hand_input)
            analyzer.print_analysis(result)
            
        except KeyboardInterrupt:
            print("\n返回菜单")
            break
        except Exception as e:
            print(f"错误: {e}")

def demo_examples():
    """
    演示典型例子
    """
    analyzer = MahjongTingpai()
    
    examples = [
        {
            'name': '经典听牌 - 两面听',
            'hand': '12345678m112p34p',
            'description': '万子1-8 + 筒子1,1,2,3,4，听2筒或5筒'
        },
        {
            'name': '七对子听牌',
            'hand': '1122334455667m8',
            'description': '万子七对子型，听8万'
        },
        {
            'name': '字牌混合听牌',
            'hand': '123m456p789s111z2z',
            'description': '各花色顺子 + 东风刻子，听南风'
        },
        {
            'name': '复杂多面听',
            'hand': '234567m23456p11s',
            'description': '万筒各一个顺子，条子对子，多种听牌可能'
        }
    ]
    
    print("\n" + "=" * 60)
    print("典型听牌示例演示")
    print("=" * 60)
    
    for i, example in enumerate(examples, 1):
        print(f"\n示例 {i}: {example['name']}")
        print(f"说明: {example['description']}")
        print(f"手牌: {example['hand']}")
        
        result = analyzer.analyze_hand(example['hand'])
        
        if 'error' in result:
            print(f"❌ 错误: {result['error']}")
        elif result.get('is_tingpai', False):
            print(f"✅ 听牌结果: {result['winning_tiles']}")
            winning_names = [analyzer.format_tile_name(tile) for tile in result['winning_tiles']]
            print(f"   可胡: {' '.join(winning_names)}")
            print(f"   听牌数: {result['winning_count']}种")
        else:
            print("❌ 未听牌")
        
        print("-" * 40)

def main():
    """
    主菜单
    """
    while True:
        print("\n" + "=" * 50)
        print("麻将听牌判断程序 - 测试菜单")
        print("=" * 50)
        print("1. 运行预设测试用例")
        print("2. 典型示例演示")
        print("3. 交互式测试")
        print("4. 启动主程序")
        print("5. 退出")
        
        choice = input("\n请选择 (1-5): ").strip()
        
        if choice == '1':
            test_cases()
        elif choice == '2':
            demo_examples()
        elif choice == '3':
            interactive_test()
        elif choice == '4':
            print("\n启动主程序...")
            from mahjong_tingpai import main as main_program
            main_program()
        elif choice == '5':
            print("退出程序")
            break
        else:
            print("无效选择，请重新输入")

if __name__ == '__main__':
    main()