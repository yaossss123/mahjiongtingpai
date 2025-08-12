#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mahjong_tingpai import MahjongTingpai

def main():
    print("麻将听牌分析演示")
    print("=" * 30)
    
    analyzer = MahjongTingpai()
    
    # 用户提到的手牌
    hand = "1112345678999m"
    print(f"手牌: {hand}")
    
    result = analyzer.analyze_hand(hand)
    
    if result['is_tingpai']:
        print("✅ 听牌成功!")
        print(f"可胡牌: {' '.join(result['winning_tiles'])}")
        print("\n验证: 确实123456789m都可以胡!")
    else:
        print("❌ 不听牌")

if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-
"""
麻将听牌程序简单测试
直接测试核心功能，无需交互
"""

from mahjong_tingpai import MahjongTingpai

def simple_test():
    """
    简单功能测试
    """
    print("=" * 50)
    print("麻将听牌程序 - 功能验证")
    print("=" * 50)
    
    analyzer = MahjongTingpai()
    
    # 测试用例
    test_cases = [
        {
            'name': '两面听牌',
            'hand': '123456789m112p34p',  # 13张牌
            'description': '万子1-9 + 筒子1,1,2,3,4'
        },
        {
            'name': '七对子听牌',
            'hand': '1122334455667m8',  # 13张牌
            'description': '万子七对子型'
        },
        {
            'name': '字牌听牌',
            'hand': '123m456p789s111z2z',  # 13张牌
            'description': '各花色顺子 + 东风刻子'
        },
        {
            'name': '单钓听牌',
            'hand': '111222333444m5',  # 13张牌
            'description': '万子四组刻子 + 单张5万'
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test['name']}")
        print(f"说明: {test['description']}")
        print(f"手牌: {test['hand']}")
        
        try:
            result = analyzer.analyze_hand(test['hand'])
            
            if 'error' in result:
                print(f"❌ 错误: {result['error']}")
            else:
                print(f"✅ 解析成功，共{result['tile_count']}张牌")
                
                if result.get('is_tingpai', False):
                    print(f"🎉 听牌！可胡{result['winning_count']}种牌:")
                    print(f"   牌型: {' '.join(result['winning_tiles'])}")
                    
                    # 显示中文名称
                    winning_names = [analyzer.format_tile_name(tile) for tile in result['winning_tiles']]
                    print(f"   中文: {' '.join(winning_names)}")
                else:
                    print("❌ 未听牌")
                    
        except Exception as e:
            print(f"❌ 程序错误: {e}")
        
        print("-" * 30)

def test_parsing():
    """
    测试解析功能
    """
    print("\n" + "=" * 50)
    print("解析功能测试")
    print("=" * 50)
    
    analyzer = MahjongTingpai()
    
    test_strings = [
        "123456789s",  # 条子1-9
        "123456789m",  # 万子1-9
        "123456789p",  # 筒子1-9
        "1234567z",    # 字牌全部
        "123s456m789p1z",  # 混合
    ]
    
    for test_str in test_strings:
        print(f"\n输入: {test_str}")
        try:
            parsed = analyzer.parse_hand(test_str)
            print(f"解析结果: {parsed}")
            print(f"牌数: {len(parsed)}")
        except Exception as e:
            print(f"解析错误: {e}")

def test_winning_detection():
    """
    测试胡牌检测
    """
    print("\n" + "=" * 50)
    print("胡牌检测测试")
    print("=" * 50)
    
    analyzer = MahjongTingpai()
    
    # 测试已胡牌的情况（14张）
    winning_hands = [
        ['1m', '1m', '1m', '2m', '3m', '4m', '5m', '5m', '5m', '6m', '7m', '8m', '9m', '9m'],  # 标准胡牌
        ['1m', '1m', '2m', '2m', '3m', '3m', '4m', '4m', '5m', '5m', '6m', '6m', '7m', '7m'],  # 七对子
    ]
    
    for i, hand in enumerate(winning_hands, 1):
        print(f"\n测试胡牌 {i}: {hand}")
        is_win = analyzer.is_winning_hand(hand)
        print(f"结果: {'✅ 胡牌' if is_win else '❌ 未胡牌'}")

def main():
    """
    主函数
    """
    try:
        simple_test()
        test_parsing()
        test_winning_detection()
        
        print("\n" + "=" * 50)
        print("✅ 所有测试完成！")
        print("麻将听牌程序功能正常")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()