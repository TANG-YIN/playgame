"""
测试德州扑克游戏功能
"""
from poker_game import PokerGame, Card, Deck, HandEvaluator
import sys
import io

# 设置输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_card_creation():
    """测试卡牌创建"""
    print("测试卡牌创建...")
    card = Card('A', '♠')
    assert card.rank == 'A'
    assert card.suit == '♠'
    assert str(card) == 'A♠'
    assert card.get_value() == 14
    print("✓ 卡牌创建测试通过")

def test_deck():
    """测试牌堆"""
    print("\n测试牌堆...")
    deck = Deck()
    assert len(deck.cards) == 52  # 标准扑克牌去掉大小王
    print("✓ 牌堆包含52张牌")
    
    # 测试发牌
    card = deck.deal()
    assert card is not None
    assert len(deck.cards) == 51
    print("✓ 发牌功能正常")
    
    # 测试洗牌
    deck.reset()
    assert len(deck.cards) == 52
    print("✓ 牌堆重置功能正常")

def test_hand_evaluation():
    """测试牌力评估"""
    print("\n测试牌力评估...")
    
    # 测试高牌
    cards = [Card('2', '♠'), Card('5', '♥'), Card('7', '♦'), Card('9', '♣'), Card('K', '♠')]
    result = HandEvaluator.evaluate(cards)
    assert result[0] == 0  # 高牌
    print("✓ 高牌识别正确")
    
    # 测试一对
    cards = [Card('2', '♠'), Card('2', '♥'), Card('5', '♦'), Card('7', '♣'), Card('K', '♠')]
    result = HandEvaluator.evaluate(cards)
    assert result[0] == 1  # 一对
    print("✓ 一对识别正确")
    
    # 测试两对
    cards = [Card('2', '♠'), Card('2', '♥'), Card('5', '♦'), Card('5', '♣'), Card('K', '♠')]
    result = HandEvaluator.evaluate(cards)
    assert result[0] == 2  # 两对
    print("✓ 两对识别正确")
    
    # 测试三条
    cards = [Card('2', '♠'), Card('2', '♥'), Card('2', '♦'), Card('7', '♣'), Card('K', '♠')]
    result = HandEvaluator.evaluate(cards)
    assert result[0] == 3  # 三条
    print("✓ 三条识别正确")
    
    # 测试顺子
    cards = [Card('2', '♠'), Card('3', '♥'), Card('4', '♦'), Card('5', '♣'), Card('6', '♠')]
    result = HandEvaluator.evaluate(cards)
    assert result[0] == 4  # 顺子
    print("✓ 顺子识别正确")
    
    # 测试同花
    cards = [Card('2', '♠'), Card('5', '♠'), Card('7', '♠'), Card('9', '♠'), Card('K', '♠')]
    result = HandEvaluator.evaluate(cards)
    assert result[0] == 5  # 同花
    print("✓ 同花识别正确")
    
    # 测试葫芦
    cards = [Card('2', '♠'), Card('2', '♥'), Card('2', '♦'), Card('5', '♣'), Card('5', '♠')]
    result = HandEvaluator.evaluate(cards)
    assert result[0] == 6  # 葫芦
    print("✓ 葫芦识别正确")
    
    # 测试四条
    cards = [Card('2', '♠'), Card('2', '♥'), Card('2', '♦'), Card('2', '♣'), Card('K', '♠')]
    result = HandEvaluator.evaluate(cards)
    assert result[0] == 7  # 四条
    print("✓ 四条识别正确")
    
    # 测试A-5顺子
    cards = [Card('A', '♠'), Card('2', '♥'), Card('3', '♦'), Card('4', '♣'), Card('5', '♠')]
    result = HandEvaluator.evaluate(cards)
    assert result[0] == 4  # 顺子
    print("✓ A-5顺子识别正确")

def test_player_creation():
    """测试玩家创建"""
    print("\n测试玩家创建...")
    from poker_game import Player
    
    player = Player('Test', 1000)
    assert player.name == 'Test'
    assert player.chips == 1000
    assert len(player.hand) == 0
    print("✓ 玩家创建测试通过")
    
    # 测试下注
    player.bet(100)
    assert player.chips == 900
    assert player.current_bet == 100
    print("✓ 下注功能正常")
    
    # 测试跟注
    player.call(50)
    assert player.chips == 850
    assert player.current_bet == 150
    print("✓ 跟注功能正常")
    
    # 测试弃牌
    player.fold()
    assert player.is_folded == True
    print("✓ 弃牌功能正常")

def test_game_initialization():
    """测试游戏初始化"""
    print("\n测试游戏初始化...")
    game = PokerGame()
    
    # 测试添加玩家
    assert game.add_player('Alice', 1000)
    assert game.add_player('Bob', 1000)
    assert len(game.players) == 2
    print("✓ 添加玩家功能正常")
    
    # 测试重复玩家名
    assert not game.add_player('Alice', 1000)
    print("✓ 重复玩家名检测正常")
    
    # 测试玩家数量限制
    game2 = PokerGame()
    for i in range(6):
        game2.add_player(f'Player{i}', 1000)
    assert not game2.add_player('Player6', 1000)
    print("✓ 玩家数量限制正常")

def test_game_flow():
    """测试游戏流程"""
    print("\n测试游戏流程...")
    game = PokerGame()
    game.add_player('Alice', 1000)
    game.add_player('Bob', 1000)
    
    # 开始游戏
    assert game.start_game()
    assert game.game_state.value == "翻牌前"
    print("✓ 游戏启动正常")
    
    # 检查手牌
    for player in game.players:
        assert len(player.hand) == 2
    print("✓ 发手牌功能正常")
    
    # 检查公共牌
    assert len(game.community_cards) == 0
    print("✓ 公共牌初始状态正常")
    
    # 检查盲注
    assert game.pot > 0
    print("✓ 盲注收取正常")

def test_autoplay():
    """测试自动游戏"""
    print("\n测试自动游戏...")
    game = PokerGame()
    game.add_player('Alice', 1000)
    game.add_player('Bob', 1000)
    
    game.start_game()
    
    # 模拟一些动作
    iterations = 0
    max_iterations = 100  # 防止无限循环
    
    while game.game_state.value != "游戏结束" and iterations < max_iterations:
        player = game.players[game.current_player]
        
        # 简单AI：随机选择动作
        import random
        if player.is_folded or player.is_all_in:
            game.next_player()
        else:
            to_call = game.current_bet - player.current_bet
            if to_call == 0:
                # 可以过牌或加注
                if random.random() < 0.7:  # 70%概率过牌
                    game.player_action("check")
                else:
                    game.player_action("allin")
            else:
                # 可以跟注或弃牌
                if random.random() < 0.8:  # 80%概率跟注
                    game.player_action("call")
                else:
                    game.player_action("fold")
        
        iterations += 1
    
    if iterations >= max_iterations:
        print("⚠ 游戏达到最大迭代次数")
    else:
        print(f"✓ 游戏自动完成，共 {iterations} 次操作")

def main():
    """运行所有测试"""
    print("="*50)
    print("德州扑克游戏功能测试")
    print("="*50)
    
    tests = [
        test_card_creation,
        test_deck,
        test_hand_evaluation,
        test_player_creation,
        test_game_initialization,
        test_game_flow,
        test_autoplay
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} 失败: {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"测试完成: 通过 {passed} 个, 失败 {failed} 个")
    print("="*50)
    
    return failed == 0

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
