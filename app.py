"""
德州扑克Web应用 - Flask后端服务器
提供API接口和WebSocket实时通信
"""
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import uuid
from datetime import datetime
import logging

from game_core import PokerGame, GameState, Player, Card, Deck

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'poker-game-secret-key-2024'

# 配置SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# 全局游戏存储
games = {}  # game_id -> PokerGame
players = {}  # session_id -> player_info

def get_or_create_game(room_id=None):
    """获取或创建游戏"""
    if room_id is None:
        room_id = "default"
    
    if room_id not in games:
        games[room_id] = PokerGame(room_id)
        logger.info(f"创建新游戏房间: {room_id}")
    
    return games[room_id]

def cleanup_inactive_games():
    """清理不活跃的游戏"""
    inactive_rooms = []
    for room_id, game in games.items():
        if len(game.players) == 0 and game.game_state == GameState.WAITING:
            inactive_rooms.append(room_id)
    
    for room_id in inactive_rooms:
        del games[room_id]
        logger.info(f"清理不活跃的游戏房间: {room_id}")

# ==================== Flask路由 ====================

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/game/<room_id>')
def game_room(room_id):
    """游戏房间"""
    return render_template('game.html', room_id=room_id)

@app.route('/api/rooms')
def get_rooms():
    """获取所有游戏房间列表"""
    room_list = []
    for room_id, game in games.items():
        room_info = {
            'room_id': room_id,
            'player_count': len(game.players),
            'game_state': game.game_state.value,
            'pot': game.pot,
            'min_players': game.min_players,
            'max_players': game.max_players
        }
        room_list.append(room_info)
    
    return jsonify({
        'success': True,
        'rooms': room_list
    })

@app.route('/api/game/<room_id>/state')
def get_game_state(room_id):
    """获取游戏状态"""
    game = get_or_create_game(room_id)
    player_id = request.args.get('player_id')
    
    state = game.get_game_state(player_id)
    return jsonify({
        'success': True,
        'state': state
    })

@app.route('/api/create_room', methods=['POST'])
def create_room():
    """创建新房间"""
    room_id = str(uuid.uuid4())[:8]
    games[room_id] = PokerGame(room_id)
    
    logger.info(f"创建房间: {room_id}")
    
    return jsonify({
        'success': True,
        'room_id': room_id
    })

# ==================== WebSocket事件 ====================

@socketio.on('connect')
def handle_connect():
    """客户端连接"""
    logger.info(f"客户端连接: {request.sid}")
    emit('connected', {'session_id': request.sid})

@socketio.on('disconnect')
def handle_disconnect():
    """客户端断开连接"""
    logger.info(f"客户端断开: {request.sid}")
    
    # 从所有房间移除玩家
    if request.sid in players:
        player_info = players[request.sid]
        room_id = player_info.get('room_id')
        
        if room_id and room_id in games:
            game = games[room_id]
            game.remove_player(request.sid)
            
            # 通知房间内所有玩家
            emit('player_left', {
                'player_name': player_info.get('name', '未知'),
                'player_count': len(game.players)
            }, room=room_id)
            
            logger.info(f"玩家 {player_info.get('name')} 离开房间 {room_id}")
    
    if request.sid in players:
        del players[request.sid]
    
    cleanup_inactive_games()

@socketio.on('join_room')
def handle_join_room(data):
    """加入游戏房间"""
    room_id = data.get('room_id', 'default')
    player_name = data.get('player_name', f'Player{len(players)+1}')
    player_id = request.sid
    
    join_room(room_id)
    
    game = get_or_create_game(room_id)
    
    # 检查玩家是否已存在
    existing = [p for p in game.players if p.player_id == player_id]
    if existing:
        emit('error', {'message': '你已经在游戏中了'}, room=room_id)
        return
    
    # 添加玩家
    success, message = game.add_player(player_name)
    
    if success:
        # 保存玩家信息
        players[player_id] = {
            'room_id': room_id,
            'name': player_name,
            'player_id': player_id
        }
        
        # 通知房间内所有玩家
        emit('player_joined', {
            'player_name': player_name,
            'player_count': len(game.players),
            'players': [p.to_dict(show_hand=False) for p in game.players]
        }, room=room_id)
        
        # 发送当前游戏状态
        emit('game_state_update', game.get_game_state(player_id), room=room_id)
        
        logger.info(f"玩家 {player_name} 加入房间 {room_id}")
        
        # 检查是否可以开始游戏
        if len(game.players) >= game.min_players and game.game_state == GameState.WAITING:
            emit('can_start_game', {'can_start': True}, room=room_id)
    else:
        emit('error', {'message': message}, room=room_id)

@socketio.on('start_game')
def handle_start_game(data):
    """开始游戏"""
    room_id = data.get('room_id', 'default')
    
    if room_id not in games:
        emit('error', {'message': '游戏房间不存在'})
        return
    
    game = games[room_id]
    success, message = game.start_game()
    
    if success:
        # 通知所有玩家游戏开始
        emit('game_started', {'message': message}, room=room_id)
        
        # 发送初始游戏状态
        for player in game.players:
            emit('game_state_update', game.get_game_state(player.player_id), room=room_id)
        
        logger.info(f"游戏开始: {room_id}")
    else:
        emit('error', {'message': message}, room=room_id)

@socketio.on('player_action')
def handle_player_action(data):
    """处理玩家动作"""
    room_id = data.get('room_id', 'default')
    action = data.get('action')
    amount = data.get('amount', 0)
    player_id = request.sid
    
    if room_id not in games:
        emit('error', {'message': '游戏房间不存在'})
        return
    
    game = games[room_id]
    success, message = game.player_action(player_id, action, amount)
    
    if success:
        # 通知所有玩家更新游戏状态
        emit('action_result', {
            'action': action,
            'message': message
        }, room=room_id)
        
        # 发送更新后的游戏状态
        for player in game.players:
            emit('game_state_update', game.get_game_state(player.player_id), room=room_id)
        
        logger.info(f"玩家 {player_id} 执行动作: {action}")
    else:
        emit('error', {'message': message})

@socketio.on('get_state')
def handle_get_state(data):
    """获取游戏状态"""
    room_id = data.get('room_id', 'default')
    player_id = request.sid
    
    if room_id in games:
        game = games[room_id]
        emit('game_state_update', game.get_game_state(player_id))

@socketio.on('restart_game')
def handle_restart_game(data):
    """重新开始游戏"""
    room_id = data.get('room_id', 'default')
    
    if room_id not in games:
        emit('error', {'message': '游戏房间不存在'})
        return
    
    game = games[room_id]
    success, message = game.start_game()
    
    if success:
        emit('game_started', {'message': message}, room=room_id)
        
        for player in game.players:
            emit('game_state_update', game.get_game_state(player.player_id), room=room_id)
    else:
        emit('error', {'message': message}, room=room_id)

# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({'success': False, 'message': '页面不存在'}), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    logger.error(f"内部错误: {error}")
    return jsonify({'success': False, 'message': '服务器内部错误'}), 500

# ==================== 启动服务器 ====================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("德州扑克Web服务器")
    print("="*60)
    print(f"服务器地址: http://127.0.0.1:5000")
    print(f"按 Ctrl+C 停止服务器")
    print("="*60 + "\n")
    
    # 启动SocketIO服务器
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
