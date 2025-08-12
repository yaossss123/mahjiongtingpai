#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麻将听牌程序使用示例
演示如何使用麻将听牌判断功能
"""

from mahjong_tingpai import MahjongTingpai

def demo_basic_usage():
    """
    基本使用演示
    """
    print("=" * 60)
    print("麻将听牌程序 - 使用演示")
    print("=" * 60)
    
    # 创建分析器
    analyzer = MahjongTingpai()
    
    # 演示各种听牌情况
    examples = [
        {
            'name': '两面听牌示例',
            'hand': '12345678m112p34p',  # 13张牌：万子1-8 + 筒子1,1,2,3,4
            'explanation': '万子1-8连续，筒子有1,1,2,3,4，缺2筒或5筒可胡牌'
        },
        {
            'name': '七对子听牌',
            'hand': '1122334455667m8',  # 13张牌：万子七对子型
            'explanation': '已有6个对子，再来一张8万就是七对子胡牌'
        },
        {
            'name': '字牌听牌',
            'hand': '123m456p789s111z2z',  # 13张牌：各花色顺子+东风刻子
            'explanation': '三个顺子加东风刻子，再来一张南风(2z)组成对子即可胡牌'
        },
        {
            'name': '单钓听牌',
            'hand': '111222333m444p5p',  # 13张牌：三个刻子+一个对子+单张
            'explanation': '已有三个刻子和一个对子，单钓5筒胡牌'
        },
        {
            'name': '边张听牌',
            'hand': '12345678m111p12p',  # 13张牌：万子1-8+筒子刻子+12
            'explanation': '筒子1,2需要3筒组成顺子，边张听牌'
        },
        {
            'name': '坎张听牌',
            'hand': '12345678m111p13p',  # 13张牌：万子1-8+筒子刻子+13
            'explanation': '筒子1,3需要2筒组成顺子，坎张听牌'
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n示例 {i}: {example['name']}")
        print(f"手牌输入: {example['hand']}")
        print(f"说明: {example['explanation']}")
        
        # 分析手牌
        result = analyzer.analyze_hand(example['hand'])
        
        if 'error' in result:
            print(f"❌ 错误: {result['error']}")
        else:
            # 显示手牌信息
            print(f"解析手牌: {' '.join(result['hand'])}")
            
            # 显示花色分布
            suits = result['suits_distribution']
            print(f"花色分布: 条{suits['s']}张 万{suits['m']}张 筒{suits['p']}张 字牌{suits['z']}张")
            
            # 显示听牌结果
            if result['is_tingpai']:
                print(f"🎉 听牌成功！可胡{result['winning_count']}种牌:")
                print(f"   可胡牌型: {' '.join(result['winning_tiles'])}")
                
                # 显示中文名称
                winning_names = [analyzer.format_tile_name(tile) for tile in result['winning_tiles']]
                print(f"   中文名称: {' '.join(winning_names)}")
            else:
                print("❌ 未听牌")
        
        print("-" * 50)

def demo_input_formats():
    """
    演示不同的输入格式
    """
    print("\n" + "=" * 60)
    print("输入格式演示")
    print("=" * 60)
    
    analyzer = MahjongTingpai()
    
    format_examples = [
        {
            'input': '123456789s1234m',
            'description': '条子1-9 + 万子1-4 (连续数字写法)'
        },
        {
            'input': '1s2s3s4s5s6s7s8s9s1m2m3m4m',
            'description': '条子1-9 + 万子1-4 (单个数字写法)'
        },
        {
            'input': '111222333m444p5p',
            'description': '万子三个刻子 + 筒子4,4,4,5 (重复数字写法)'
        },
        {
            'input': '1234567z123456s',
            'description': '所有字牌 + 条子1-6'
        }
    ]
    
    for example in format_examples:
        print(f"\n输入: {example['input']}")
        print(f"说明: {example['description']}")
        
        try:
            parsed = analyzer.parse_hand(example['input'])
            print(f"解析结果: {' '.join(parsed)}")
            print(f"牌数: {len(parsed)}张")
            
            if len(parsed) == 13:
                result = analyzer.analyze_hand(example['input'])
                if result['is_tingpai']:
                    winning_names = [analyzer.format_tile_name(tile) for tile in result['winning_tiles']]
                    print(f"听牌: {' '.join(winning_names)}")
                else:
                    print("未听牌")
        except Exception as e:
            print(f"错误: {e}")
        
        print("-" * 40)

def demo_tile_names():
    """
    演示牌名对照
    """
    print("\n" + "=" * 60)
    print("牌名对照表")
    print("=" * 60)
    
    analyzer = MahjongTingpai()
    
    print("条子(索子): ", end="")
    for i in range(1, 10):
        tile = f"{i}s"
        name = analyzer.format_tile_name(tile)
        print(f"{tile}={name}", end=" ")
    
    print("\n万子: ", end="")
    for i in range(1, 10):
        tile = f"{i}m"
        name = analyzer.format_tile_name(tile)
        print(f"{tile}={name}", end=" ")
    
    print("\n筒子(饼子): ", end="")
    for i in range(1, 10):
        tile = f"{i}p"
        name = analyzer.format_tile_name(tile)
        print(f"{tile}={name}", end=" ")
    
    print("\n字牌: ", end="")
    for i in range(1, 8):
        tile = f"{i}z"
        name = analyzer.format_tile_name(tile)
        print(f"{tile}={name}", end=" ")
    
    print("\n")

def demo_interactive():
    """
    简单交互演示
    """
    print("\n" + "=" * 60)
    print("交互式演示 (输入 'quit' 退出)")
    print("=" * 60)
    
    analyzer = MahjongTingpai()
    
    print("请输入13张麻将牌，格式示例:")
    print("  123456789s1234m  (条子1-9 + 万子1-4)")
    print("  111222333m444p5p (万子三刻子 + 筒子4,4,4,5)")
    print("  1122334455667m8  (七对子型)")
    
    while True:
        try:
            user_input = input("\n请输入手牌: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q', '']:
                print("退出演示")
                break
            
            result = analyzer.analyze_hand(user_input)
            
            if 'error' in result:
                print(f"❌ {result['error']}")
            else:
                print(f"✅ 解析成功: {' '.join(result['hand'])}")
                
                if result['is_tingpai']:
                    winning_names = [analyzer.format_tile_name(tile) for tile in result['winning_tiles']]
                    print(f"🎉 听牌！可胡: {' '.join(winning_names)}")
                else:
                    print("❌ 未听牌")
                    
        except KeyboardInterrupt:
            print("\n退出演示")
            break
        except Exception as e:
            print(f"程序错误: {e}")

def main():
    """
    主演示函数
    """
    try:
        demo_basic_usage()
        demo_input_formats()
        demo_tile_names()
        
        # 询问是否进行交互演示
        print("\n是否进行交互式演示？(y/n): ", end="")
        choice = input().strip().lower()
        if choice in ['y', 'yes', '是']:
            demo_interactive()
        
        print("\n" + "=" * 60)
        print("✅ 演示完成！")
        print("现在您可以使用 python mahjong_tingpai.py 启动完整程序")
        print("=" * 60)
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()