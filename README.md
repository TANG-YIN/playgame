# 🃏 德州扑克在线游戏

一个纯前端实现的德州扑克游戏，支持与AI对手对战。

## 🎮 功能特性

- **纯前端实现**：无需服务器，完全在浏览器中运行
- **AI对手**：支持与3个AI玩家对战
- **完整游戏流程**：翻牌前、翻牌、转牌、河牌、摊牌
- **投注系统**：支持弃牌、过牌、跟注、加注、全押
- **响应式设计**：适配不同屏幕尺寸
- **自动牌力评估**：实时计算最佳牌型

## 🚀 在线访问

### GitHub Pages 部署（推荐）

**重要：需要在GitHub上手动启用GitHub Pages**

#### 启用步骤：

1. **访问仓库设置页面**
   - 打开：https://github.com/TANG-YIN/playgame/settings/pages

2. **配置GitHub Pages**
   - 在 "Build and deployment" 部分
   - **Source** 选择：`Deploy from a branch`
   - **Branch** 选择：`main`
   - **Folder** 选择：`/(root)`
   - 点击 **Save** 按钮

3. **等待部署完成**
   - 保存后，GitHub会自动部署（约1-2分钟）
   - 部署成功后访问：https://tang-yin.github.io/playgame/

4. **开始游戏**
   - 点击"开始新游戏"按钮
   - 与3个AI对手进行德州扑克对战

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

1. **等待开始**：点击"开始新游戏"按钮
2. **翻牌前**：每人发2张手牌，收取盲注
3. **翻牌**：发3张公共牌
4. **转牌**：发第4张公共牌
5. **河牌**：发第5张公共牌
6. **摊牌**：比较牌力，分配筹码

### 操作说明

- **弃牌**：放弃当前回合，失去已下注的筹码
- **过牌**：不增加下注（当不需要跟注时）
- **跟注**：跟随当前最高注额
- **加注**：增加注额（固定为大盲金额）
- **全押**：押上所有筹码

### 游戏参数

- 初始筹码：1000
- 小盲：10
- 大盲：20
- 玩家数量：4人（1人类 + 3AI）

## 💻 本地运行

### 方式一：直接打开

1. 克隆仓库：
```bash
git clone https://github.com/TANG-YIN/playgame.git
cd playgame
```

2. 在浏览器中打开 `index.html` 文件即可运行

### 方式二：使用本地服务器

```bash
# 使用Python启动本地服务器
cd playgame
python -m http.server 8000

# 在浏览器访问 http://localhost:8000
```

## 📁 项目结构

```
playgame/
├── index.html           # 游戏主页面（包含所有HTML、CSS、JS）
├── app.py               # Flask后端（用于多人在线版本）
├── game_core.py         # 游戏核心逻辑
├── poker_game.py        # 命令行版本
├── poker_helper.py      # 胜率计算器
├── requirements.txt     # Python依赖
├── templates/           # HTML模板（Flask版本）
├── static/             # 静态资源（Flask版本）
└── README.md           # 本文档
```

## 🔧 技术栈

### 纯前端版本（index.html）

- **HTML5/CSS3**：页面结构和样式
- **JavaScript (ES6+)**：游戏逻辑
- **面向对象编程**：Card、Deck、Player、HandEvaluator、PokerGame类

### Flask后端版本

- **Python 3.6+**
- **Flask**：Web框架
- **Flask-SocketIO**：WebSocket支持（用于多人在线）

## 🌐 部署说明

### GitHub Pages 部署

1. 按照上述"启用步骤"配置GitHub Pages
2. 代码会自动部署到 https://tang-yin.github.io/playgame/
3. 无需任何额外配置

### 其他静态托管服务

也可以部署到：
- Vercel
- Netlify
- Cloudflare Pages

只需将 `index.html` 上传即可。

## 🎨 游戏界面

### 主要组件

- **顶部栏**：游戏标题和"新游戏"按钮
- **信息面板**：显示游戏阶段、底池、当前注额、你的筹码
- **公共牌区域**：显示5张公共牌
- **玩家卡片**：显示每个玩家的手牌、筹码、状态
- **你的区域**：显示你的手牌和操作按钮
- **消息区域**：显示游戏日志

## 📝 游戏特点

### AI行为

- AI玩家会根据当前情况做出决策
- 70%概率过牌（当可以过牌时）
- 80%概率跟注
- 有一定概率加注或全押
- 有一定概率弃牌

### 胜负判定

- 自动计算每个玩家的最佳5张牌组合
- 根据牌型等级和关键牌进行排名
- 多个玩家牌型相同时，比较关键牌的大小
- 自动分配底池给获胜者

## 🧪 测试

### 本地测试

```bash
# 在浏览器中打开 index.html
# 或使用本地服务器
python -m http.server 8000
```

### 测试要点

- 游戏流程是否完整
- AI行为是否合理
- 牌力评估是否准确
- 按钮状态是否正确

## 📄 许可证

MIT License

## 👥 贡献

欢迎提交Issue和Pull Request！

## 🔗 相关链接

- GitHub仓库：https://github.com/TANG-YIN/playgame
- 问题反馈：https://github.com/TANG-YIN/playgame/issues

## 📮 联系方式

如有问题或建议，欢迎通过GitHub Issues联系。

---

**享受游戏！** 🎉
