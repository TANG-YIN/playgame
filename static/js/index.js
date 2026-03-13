// 首页JavaScript

let selectedRoom = null;
let rooms = [];

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    loadRooms();
});

// 加载房间列表
function loadRooms() {
    const roomList = document.getElementById('roomList');
    roomList.innerHTML = '<div class="loading">加载中...</div>';
    
    fetch('/api/rooms')
        .then(response => response.json())
        .then(data => {
            rooms = data.rooms;
            displayRooms();
        })
        .catch(error => {
            roomList.innerHTML = '<div class="error">加载失败，请重试</div>';
            console.error('Error:', error);
        });
}

// 显示房间列表
function displayRooms() {
    const roomList = document.getElementById('roomList');
    
    if (rooms.length === 0) {
        roomList.innerHTML = '<div class="placeholder">暂无游戏房间</div>';
        return;
    }
    
    roomList.innerHTML = rooms.map(room => `
        <div class="room-item ${room.game_state === 'waiting' ? '' : 'disabled'}" 
             onclick="selectRoom('${room.room_id}')" 
             id="room-${room.room_id}">
            <div class="room-item-header">
                <span class="room-name">${room.room_id}</span>
                <span class="room-status ${room.game_state}">
                    ${room.game_state === 'waiting' ? '等待中' : '游戏中'}
                </span>
            </div>
            <div class="room-item-info">
                玩家: ${room.player_count}/${room.max_players}
                ${room.pot > 0 ? ` | 底池: ${room.pot}` : ''}
            </div>
        </div>
    `).join('');
}

// 选择房间
function selectRoom(roomId) {
    const room = rooms.find(r => r.room_id === roomId);
    
    if (room.game_state !== 'waiting') {
        alert('该房间游戏已开始，无法加入');
        return;
    }
    
    // 移除之前的选择
    document.querySelectorAll('.room-item').forEach(item => {
        item.classList.remove('selected');
    });
    
    // 添加新的选择
    const roomElement = document.getElementById(`room-${roomId}`);
    if (roomElement) {
        roomElement.classList.add('selected');
    }
    
    selectedRoom = roomId;
}

// 加入房间
function joinRoom() {
    const playerName = document.getElementById('playerName').value.trim();
    
    if (!playerName) {
        alert('请输入玩家名称');
        return;
    }
    
    if (!selectedRoom) {
        alert('请选择一个房间');
        return;
    }
    
    // 保存玩家信息
    localStorage.setItem('playerName', playerName);
    
    // 跳转到游戏页面
    window.location.href = `/game/${selectedRoom}`;
}

// 创建新房间
function createRoom() {
    const playerName = document.getElementById('playerName').value.trim();
    
    if (!playerName) {
        alert('请输入玩家名称');
        return;
    }
    
    // 保存玩家信息
    localStorage.setItem('playerName', playerName);
    
    // 请求创建新房间
    fetch('/api/create_room', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // 跳转到新房间
            window.location.href = `/game/${data.room_id}`;
        } else {
            alert('创建房间失败');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('创建房间失败，请重试');
    });
}

// 刷新房间列表
function refreshRooms() {
    loadRooms();
}

// 自动刷新房间列表
setInterval(loadRooms, 30000); // 每30秒刷新一次
