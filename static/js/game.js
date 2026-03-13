// 游戏页面JavaScript

let socket = null;
let myPlayerId = null;
let gameState = null;
let isMyTurn = false;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initSocket();
});

// 初始化WebSocket连接
function initSocket() {
    const playerName = localStorage.getItem('playerName') || 'Guest';
    
    // 连接Socket.IO
    socket = io();
    
    // 监听连接事件
    socket.on('connect', function() {
        console.log('已连接到服务器');
        myPlayerId = socket.id;
        
        // 加入游戏房间
        socket.emit('join_room', {
            room_id: roomId,
            player_name: playerName
        });
    });
    
    // 监听错误事件
    socket.on('error', function(data) {
        addMessage(data.message, 'error');
        console.error('Socket error:', data.message);
    });
    
    // 监听玩家加入事件
    socket.on('player_joined', function(data) {
        addMessage(`${data.player_name} 加入了游戏`, 'info');
        console.log('Player joined:', data);
    });
    
    // 监听玩家离开事件
    socket.on('player_left', function(data) {
        addMessage(`${data.player_name} 离开了游戏`, 'info');
    });
    
    // 监听游戏开始事件
    socket.on('game_started', function(data) {
        addMessage(data.message, 'success');
        closeModal('startModal');
        updateActionButtons(false);
    });
    
    // 监听游戏状态更新
    socket.on('game_state_update', function(state) {
        gameState = state;
        updateGameState(state);
    });
    
    // 监听动作结果
    socket.on('action_result', function(data) {
        addMessage(data.message, 'info');
    });
    
    // 监听可以开始游戏事件
    socket.on('can_start_game', function(data) {
        if (data.can_start) {
            showStartModal();
        }
    });
    
    // 监听断开连接
    socket.on('disconnect', function() {
        addMessage('与服务器断开连接', 'error');
        updateActionButtons(false);
    });
}

// 更新游戏状态显示
function updateGameState(state) {
    // 更新游戏信息
    document.getElementById('gameState').textContent = getGameStageName(state.game_state);
    document.getElementById('pot').textContent = state.pot;
    document.getElementById('currentBet').textContent = state.current_bet;
    
    // 更新公共牌
    updateCommunityCards(state.community_cards);
    
    // 更新玩家列表
    updatePlayersList(state.players, state.current_player, state.dealer_position);
    
    // 更新我的手牌
    updateMyCards(state.players);
    
    // 检查是否轮到我
    checkMyTurn(state.players, state.current_player);
    
    // 检查游戏是否结束
    if (state.game_state === 'game_over') {
        showEndModal(state);
    }
}

// 获取游戏阶段名称
function getGameStageName(stage) {
    const names = {
        'waiting': '等待玩家',
        'preflop': '翻牌前',
        'flop': '翻牌',
        'turn': '转牌',
        'river': '河牌',
        'showdown': '摊牌',
        'game_over': '游戏结束'
    };
    return names[stage] || stage;
}

// 更新公共牌
function updateCommunityCards(cards) {
    const container = document.getElementById('communityCards');
    
    if (!cards || cards.length === 0) {
        container.innerHTML = '<div class="placeholder">等待发牌...</div>';
        return;
    }
    
    container.innerHTML = cards.map(card => createCardHTML(card)).join('');
}

// 创建扑克牌HTML
function createCardHTML(card, hidden = false) {
    if (hidden) {
        return '<div class="card card-back"></div>';
    }
    
    const isRed = card.suit === '♥' || card.suit === '♦';
    return `
        <div class="card ${isRed ? 'red' : 'black'}">
            <div class="card-rank">${card.rank}</div>
            <div class="card-suit">${card.suit}</div>
        </div>
    `;
}

// 更新玩家列表
function updatePlayersList(players, currentPlayerIndex, dealerPosition) {
    const container = document.getElementById('playersArea');
    
    container.innerHTML = players.map((player, index) => {
        const isCurrent = index === currentPlayerIndex;
        const isDealer = index === dealerPosition;
        const isActive = player.is_active && !player.is_folded;
        const isMe = player.id === myPlayerId;
        
        let statusClass = 'active';
        if (player.is_folded) statusClass = 'folded';
        else if (player.is_all_in) statusClass = 'allin';
        
        let statusText = player.last_action || '等待中';
        if (player.is_folded) statusText = '已弃牌';
        else if (player.is_all_in) statusText = '全押';
        
        return `
            <div class="player-card ${isCurrent ? 'current' : ''} ${isActive ? 'active' : ''}">
                <div class="player-header">
                    <span class="player-name">
                        ${player.name}
                        ${isMe ? '(你)' : ''}
                        ${isDealer ? '👑' : ''}
                    </span>
                    <span class="player-status ${statusClass}">${statusText}</span>
                </div>
                <div class="player-info">
                    筹码: ${player.chips} | 下注: ${player.current_bet}
                </div>
                <div class="player-cards">
                    ${player.hand && player.hand.length > 0 
                        ? player.hand.map(card => createCardHTML(card)).join('') 
                        : `<div class="placeholder">${player.hand_count}张牌</div>`
                    }
                </div>
            </div>
        `;
    }).join('');
}

// 更新我的手牌
function updateMyCards(players) {
    const myPlayer = players.find(p => p.id === myPlayerId);
    const container = document.getElementById('myCards');
    
    if (!myPlayer || !myPlayer.hand || myPlayer.hand.length === 0) {
        container.innerHTML = '<div class="placeholder">等待发牌...</div>';
        return;
    }
    
    container.innerHTML = myPlayer.hand.map(card => createCardHTML(card)).join('');
}

// 检查是否轮到我
function checkMyTurn(players, currentPlayerIndex) {
    const myPlayer = players.find(p => p.id === myPlayerId);
    const currentPlayer = players[currentPlayerIndex];
    
    isMyTurn = myPlayer && currentPlayer && myPlayer.id === currentPlayer.id;
    
    updateActionButtons(isMyTurn);
}

// 更新操作按钮状态
function updateActionButtons(enable) {
    const buttons = document.querySelectorAll('.btn-action');
    buttons.forEach(btn => {
        btn.disabled = !enable;
    });
    
    // 根据当前状态更新按钮显示
    if (gameState && myPlayerId) {
        const myPlayer = gameState.players.find(p => p.id === myPlayerId);
        if (myPlayer) {
            const toCall = gameState.current_bet - myPlayer.current_bet;
            
            // 跟注/过牌按钮
            const callBtn = document.getElementById('callBtn');
            const checkBtn = document.getElementById('checkBtn');
            
            if (toCall > 0) {
                callBtn.textContent = `跟注 ${toCall}`;
                callBtn.style.display = 'inline-block';
                checkBtn.style.display = 'none';
            } else {
                callBtn.style.display = 'none';
                checkBtn.style.display = 'inline-block';
            }
            
            // 全押按钮
            const allinBtn = document.getElementById('allinBtn');
            allinBtn.textContent = `全押 (${myPlayer.chips})`;
        }
    }
}

// 玩家执行操作
function playerAction(action, amount = 0) {
    if (!isMyTurn) {
        addMessage('不是你的回合', 'error');
        return;
    }
    
    socket.emit('player_action', {
        room_id: roomId,
        action: action,
        amount: amount
    });
}

// 加注
function raiseBet() {
    const raiseInput = document.getElementById('raiseInput');
    const raiseAmount = document.getElementById('raiseAmount');
    
    raiseInput.style.display = 'flex';
    raiseAmount.focus();
    
    // 设置最小加注金额
    if (gameState && myPlayerId) {
        const myPlayer = gameState.players.find(p => p.id === myPlayerId);
        if (myPlayer) {
            const minRaise = gameState.current_bet + 20;
            raiseAmount.min = minRaise;
            raiseAmount.value = minRaise;
        }
    }
}

// 确认加注
function confirmRaise() {
    const raiseAmount = document.getElementById('raiseAmount').value;
    const amount = parseInt(raiseAmount);
    
    if (isNaN(amount) || amount <= 0) {
        addMessage('请输入有效的加注金额', 'error');
        return;
    }
    
    if (gameState && myPlayerId) {
        const myPlayer = gameState.players.find(p => p.id === myPlayerId);
        if (amount > myPlayer.chips) {
            addMessage('筹码不足', 'error');
            return;
        }
    }
    
    playerAction('raise', amount);
    cancelRaise();
}

// 取消加注
function cancelRaise() {
    document.getElementById('raiseInput').style.display = 'none';
}

// 添加消息
function addMessage(message, type = 'info') {
    const container = document.getElementById('gameMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
    
    // 限制消息数量
    while (container.children.length > 50) {
        container.removeChild(container.firstChild);
    }
}

// 显示开始游戏模态框
function showStartModal() {
    const modal = document.getElementById('startModal');
    const playerCount = document.getElementById('playerCount');
    
    if (gameState) {
        playerCount.textContent = gameState.player_count;
    }
    
    modal.style.display = 'flex';
}

// 开始游戏
function startGame() {
    socket.emit('start_game', {
        room_id: roomId
    });
}

// 显示游戏结束模态框
function showEndModal(state) {
    const modal = document.getElementById('endModal');
    const winnerInfo = document.getElementById('winnerInfo');
    
    // 找出获胜者
    const winners = state.players.filter(p => !p.is_folded).sort((a, b) => b.chips - a.chips);
    
    if (winners.length > 0) {
        winnerInfo.innerHTML = `
            <p>🎉 游戏结束！</p>
            <p style="font-size: 1.2em; margin-top: 15px;">
                <strong>${winners[0].name}</strong> 以 ${winners[0].chips} 筹码获胜！
            </p>
        `;
    } else {
        winnerInfo.textContent = '游戏结束';
    }
    
    modal.style.display = 'flex';
}

// 重新开始游戏
function restartGame() {
    closeModal('endModal');
    closeModal('startModal');
    
    socket.emit('restart_game', {
        room_id: roomId
    });
}

// 离开房间
function leaveRoom() {
    if (confirm('确定要离开房间吗？')) {
        window.location.href = '/';
    }
}

// 关闭模态框
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// 处理回车键
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const raiseInput = document.getElementById('raiseInput');
        if (raiseInput.style.display === 'flex') {
            confirmRaise();
        }
    }
});
