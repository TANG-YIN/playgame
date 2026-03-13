# 德州扑克Web在线游戏

一个支持2-6人在线对战的德州扑克Web应用，具有实时通信和精美界面。

## 🎮 功能特性

- **多人在线对战**: 支持2-6人同时游戏
- **实时通信**: 基于WebSocket的实时游戏更新
- **完整游戏流程**: 翻牌前、翻牌、转牌、河牌、摊牌
- **自动牌力评估**: 支持所有德州扑克牌型识别
- **直观界面**: 现代化的游戏界面设计
- **房间系统**: 创建和加入游戏房间

## 🚀 快速开始

### 方式一：本地运行

#### 1. 安装依赖

```bash
cd d:/depu/texasHelper
pip install -r requirements.txt
```

#### 2. 启动服务器

```bash
python app.py
```

服务器将在 `http://127.0.0.1:5000` 启动

#### 3. 开始游戏

1. 在浏览器中打开 `http://127.0.0.1:5000`
2. 输入玩家名称
3. 选择房间或创建新房间
4. 等待其他玩家加入
5. 开始游戏！

### 方式二：GitHub Pages（静态演示）

项目包含一个静态演示页面，可以部署到GitHub Pages。

## 📁 项目结构

```
texasHelper/
├── app.py                 # Flask应用主文件
├── game_core.py           # 游戏核心逻辑
├── poker_game.py          # 命令行版本游戏
├── poker_helper.py        # 德州扑克胜率计算器
├── test_poker.py          # 自动化测试
├── requirements.txt       # Python依赖
├── templates/             # HTML模板
│   ├── index.html         # 首页
│   └── game.html          # 游戏页面
├── static/                # 静态资源
│   ├── css/
│   │   └── style.css      # 样式文件
│   └── js/
│       ├── index.js       # 首页脚本
│       └── game.js        # 游戏脚本
└── README.md              # 本文档
```

## 🎯 游戏规则

### 牌型等级（从高到低）

1. **同花顺** (Straight Flush)
2. **四条** (Four of a Kind)
3. **葫芦** (Full House)
4. **同花** (Flush)
5. **顺子** (Straight)
6. **三条** (Three of a Kind)
7. **两对** (Two Pair)
8. **一对** (One Pair)
9. **高牌** (High Card)

### 游戏流程

1. **等待玩家**: 2-6名玩家加入房间
2. **翻牌前**: 发2张手牌，收取盲注
3. **翻牌**: 发3张公共牌
4. **转牌**: 发第4张公共牌
5. **河牌**: 发第5张公共牌
6. **摊牌**: 比较牌力，分配筹码

### 操作说明

- **过牌**: 不增加下注（当不需要跟注时）
- **跟注**: 跟随当前最高注额
- **加注**: 增加注额
- **全押**: 押上所有筹码
- **弃牌**: 放弃当前回合

### 游戏参数

- 初始筹码: 1000
- 小盲: 10
- 大盲: 20

## 🔧 技术栈

### 后端

- **Python 3.6+**
- **Flask**: Web框架
- **Flask-SocketIO**: WebSocket支持
- **Socket.IO**: 实时双向通信

### 前端

- **HTML5/CSS3**
- **JavaScript (ES6+)**
- **Socket.IO Client**: 实时通信

## 🌐 部署说明

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
python app.py

# 访问 http://127.0.0.1:5000
```

### 生产部署

使用 Gunicorn + Eventlet:

```bash
# 安装Gunicorn
pip install gunicorn eventlet

# 运行生产服务器
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
```

### Heroku部署

1. 创建 `Procfile`:
```
web: gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app:app
```

2. 部署到Heroku:
```bash
heroku create
git push heroku main
```

### 云服务器部署

支持部署到各种云平台：
- 阿里云
- 腾讯云
- AWS
- DigitalOcean

## 📝 API文档

### REST API

#### 获取房间列表
```
GET /api/rooms
```

#### 获取游戏状态
```
GET /api/game/<room_id>/state?player_id=<player_id>
```

#### 创建房间
```
POST /api/create_room
```

### WebSocket事件

#### 客户端事件

- `join_room`: 加入游戏房间
- `start_game`: 开始游戏
- `player_action`: 执行玩家动作
- `get_state`: 获取游戏状态
- `restart_game`: 重新开始游戏

#### 服务器事件

- `connected`: 连接成功
- `player_joined`: 玩家加入
- `player_left`: 玩家离开
- `game_started`: 游戏开始
- `game_state_update`: 游戏状态更新
- `action_result`: 动作结果
- `error`: 错误消息

## 🧪 测试

运行自动化测试:

```bash
python test_poker.py
```

测试覆盖：
- 卡牌创建和操作
- 牌堆洗牌和发牌
- 所有牌型识别
- 玩家状态管理
- 游戏流程
- 自动游戏模拟

## 🎨 界面预览

### 首页
- 输入玩家名称
- 查看和选择房间
- 创建新房间

### 游戏页面
- 实时显示公共牌
- 玩家状态和筹码
- 手牌展示
- 操作按钮
- 游戏消息

## 📄 许可证

MIT License

## 👥 贡献

欢迎提交Issue和Pull Request！

## 🔗 相关链接

- GitHub仓库: https://github.com/Wenzhi-dog/texasHelper
- 问题反馈: https://github.com/Wenzhi-dog/texasHelper/issues

## 📮 联系方式

如有问题或建议，欢迎通过GitHub Issues联系。

---

**享受游戏！** 🎉
