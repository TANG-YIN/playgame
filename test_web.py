"""
测试Web应用功能
"""
import sys
import os
import io

# 设置输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("德州扑克Web应用测试")
print("="*60)

# 测试1: 导入核心模块
print("\n[测试1] 导入游戏核心模块...")
try:
    from game_core import Card, Deck, Player, PokerGame, HandEvaluator
    print("✓ 游戏核心模块导入成功")
except Exception as e:
    print(f"✗ 导入失败: {e}")
    sys.exit(1)

# 测试2: 导入Flask应用
print("\n[测试2] 导入Flask应用...")
try:
    from app import app, socketio
    print("✓ Flask应用导入成功")
except Exception as e:
    print(f"✗ 导入失败: {e}")
    sys.exit(1)

# 测试3: 测试游戏核心功能
print("\n[测试3] 测试游戏核心功能...")
try:
    game = PokerGame("test-room")
    
    # 添加玩家
    success, msg = game.add_player("Alice", 1000)
    assert success, "添加玩家Alice失败"
    
    success, msg = game.add_player("Bob", 1000)
    assert success, "添加玩家Bob失败"
    
    print(f"  - 玩家数量: {len(game.players)}")
    
    # 开始游戏
    success, msg = game.start_game()
    assert success, f"开始游戏失败: {msg}"
    print(f"  - 游戏状态: {game.game_state.value}")
    
    # 检查手牌
    for player in game.players:
        assert len(player.hand) == 2, f"{player.name}的手牌数量不对"
        print(f"  - {player.name}的手牌: {[str(c) for c in player.hand]}")
    
    print("✓ 游戏核心功能测试通过")
except Exception as e:
    print(f"✗ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试4: 测试Flask路由
print("\n[测试4] 测试Flask路由...")
try:
    with app.test_client() as client:
        # 测试首页
        response = client.get('/')
        assert response.status_code == 200, "首页访问失败"
        print("  - 首页访问: OK")
        
        # 测试API
        response = client.get('/api/rooms')
        assert response.status_code == 200, "房间列表API失败"
        print("  - 房间列表API: OK")
        
    print("✓ Flask路由测试通过")
except Exception as e:
    print(f"✗ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试5: 测试WebSocket
print("\n[测试5] 测试WebSocket配置...")
try:
    from flask_socketio import SocketIO
    assert socketio is not None, "SocketIO未初始化"
    print("✓ WebSocket配置正确")
except Exception as e:
    print(f"✗ 测试失败: {e}")
    sys.exit(1)

# 测试6: 测试游戏序列化
print("\n[测试6] 测试游戏状态序列化...")
try:
    game = PokerGame("test-room-2")
    game.add_player("Alice")
    game.add_player("Bob")
    
    state = game.get_game_state("player-1")
    
    assert 'game_id' in state, "缺少game_id"
    assert 'players' in state, "缺少players"
    assert 'community_cards' in state, "缺少community_cards"
    assert 'pot' in state, "缺少pot"
    
    print("✓ 游戏状态序列化测试通过")
except Exception as e:
    print(f"✗ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 总结
print("\n" + "="*60)
print("测试完成！所有测试通过 ✓")
print("="*60)
print("\n你可以通过以下命令启动Web服务器:")
print("  python app.py")
print("\n然后在浏览器中访问: http://127.0.0.1:5000")
print("="*60)
