// 纯前端版德州扑克游戏

class Card {
    constructor(rank, suit) {
        this.rank = rank;
        this.suit = suit;
    }
    
    toString() {
        return `${this.rank}${this.suit}`;
    }
    
    getValue() {
        const values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
            '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
        };
        return values[this.rank];
    }
    
    toHTML() {
        const isRed = this.suit === '♥' || this.suit === '♦';
        return `
            <div class="card ${isRed ? 'red' : 'black'}">
                <div class="card-rank">${this.rank}</div>
                <div class="card-suit">${this.suit}</div>
            </div>
        `;
    }
}

class Deck {
    constructor() {
        this.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];
        this.suits = ['♠', '♥', '♣', '♦'];
        this.reset();
    }
    
    reset() {
        this.cards = [];
        for (let rank of this.ranks) {
            for (let suit of this.suits) {
                this.cards.push(new Card(rank, suit));
            }
        }
        this.shuffle();
    }
    
    shuffle() {
        for (let i = this.cards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]];
        }
    }
    
    deal() {
        return this.cards.pop();
    }
}

class Player {
    constructor(name, chips = 1000, isAI = false) {
        this.name = name;
        this.chips = chips;
        this.hand = [];
        this.currentBet = 0;
        this.isFolded = false;
        this.isAllIn = false;
        this.isAI = isAI;
        this.lastAction = '';
    }
    
    reset() {
        this.hand = [];
        this.currentBet = 0;
        this.isFolded = false;
        this.isAllIn = false;
        this.lastAction = '';
    }
    
    bet(amount) {
        if (amount >= this.chips) {
            const betAmount = this.chips;
            this.currentBet += betAmount;
            this.chips = 0;
            this.isAllIn = true;
            this.lastAction = `全押 ${betAmount}`;
        } else {
            this.chips -= amount;
            this.currentBet += amount;
            this.lastAction = `下注 ${amount}`;
        }
    }
    
    call(amount) {
        const callAmount = Math.min(amount, this.chips);
        this.bet(callAmount);
        if (this.lastAction.startsWith('下注')) {
            this.lastAction = `跟注 ${callAmount}`;
        }
    }
    
    fold() {
        this.isFolded = true;
        this.lastAction = '弃牌';
    }
}

class HandEvaluator {
    static evaluate(cards) {
        if (!cards || cards.length === 0) return (0, []);
        
        const ranks = cards.map(c => c.getValue());
        const suits = cards.map(c => c.suit);
        
        const rankCounts = {};
        ranks.forEach(r => rankCounts[r] = (rankCounts[r] || 0) + 1);
        
        const suitCounts = {};
        suits.forEach(s => suitCounts[s] = (suitCounts[s] || 0) + 1);
        
        const sortedRanks = [...new Set(ranks)].sort((a, b) => b - a);
        
        // 检查顺子
        let straight = false;
        let straightHigh = 0;
        
        // A可以作为1
        if (sortedRanks.includes(14)) {
            sortedRanks.push(1);
            sortedRanks.sort((a, b) => b - a);
        }
        
        for (let i = 0; i <= sortedRanks.length - 5; i++) {
            if (sortedRanks[i] - sortedRanks[i + 4] === 4) {
                straight = true;
                straightHigh = sortedRanks[i];
                break;
            }
        }
        
        // 检查同花
        const flush = Object.values(suitCounts).some(c => c >= 5);
        
        // 同花顺
        if (flush && straight) return (8, straightHigh);
        
        // 四条
        if (Object.values(rankCounts).some(c => c === 4)) {
            const fourRank = parseInt(Object.keys(rankCounts).find(k => rankCounts[k] === 4));
            const kicker = Math.max(...Object.keys(rankCounts).filter(k => parseInt(k) !== fourRank).map(Number));
            return (7, fourRank, kicker);
        }
        
        // 葫芦
        if (Object.values(rankCounts).some(c => c === 3) && Object.values(rankCounts).some(c => c === 2)) {
            const threeRank = Math.max(...Object.keys(rankCounts).filter(k => rankCounts[k] === 3).map(Number));
            const pairRank = Math.max(...Object.keys(rankCounts).filter(k => rankCounts[k] === 2).map(Number));
            return (6, threeRank, pairRank);
        }
        
        // 同花
        if (flush) {
            const flushSuit = Object.keys(suitCounts).find(s => suitCounts[s] >= 5);
            const flushRanks = cards.filter(c => c.suit === flushSuit)
                .map(c => c.getValue())
                .sort((a, b) => b - a)
                .slice(0, 5);
            return (5, flushRanks);
        }
        
        // 顺子
        if (straight) return (4, straightHigh);
        
        // 三条
        if (Object.values(rankCounts).some(c => c === 3)) {
            const threeRank = Math.max(...Object.keys(rankCounts).filter(k => rankCounts[k] === 3).map(Number));
            const kickers = Object.keys(rankCounts)
                .filter(k => parseInt(k) !== threeRank)
                .map(Number)
                .sort((a, b) => b - a)
                .slice(0, 2);
            return (3, threeRank, kickers);
        }
        
        // 两对
        const pairs = Object.keys(rankCounts).filter(k => rankCounts[k] === 2).map(Number).sort((a, b) => b - a);
        if (pairs.length >= 2) {
            const kicker = Math.max(...Object.keys(rankCounts).filter(k => rankCounts[k] !== 2).map(Number), 0);
            return (2, pairs.slice(0, 2), kicker);
        }
        
        // 一对
        if (pairs.length === 1) {
            const kickers = Object.keys(rankCounts)
                .filter(k => parseInt(k) !== pairs[0])
                .map(Number)
                .sort((a, b) => b - a)
                .slice(0, 3);
            return (1, pairs[0], kickers);
        }
        
        // 高牌
        return (0, ranks.sort((a, b) => b - a).slice(0, 5));
    }
    
    static getHandName(rank) {
        const names = {
            8: '同花顺',
            7: '四条',
            6: '葫芦',
            5: '同花',
            4: '顺子',
            3: '三条',
            2: '两对',
            1: '一对',
            0: '高牌'
        };
        return names[rank] || '未知';
    }
    
    static compareHands(hand1, hand2) {
        const result1 = HandEvaluator.evaluate(hand1);
        const result2 = HandEvaluator.evaluate(hand2);
        
        for (let i = 0; i < Math.min(result1.length, result2.length); i++) {
            const val1 = Array.isArray(result1[i]) ? 
                (Array.isArray(result2[i]) ? JSON.stringify(result1[i]) : result1[i]) : result1[i];
            const val2 = Array.isArray(result2[i]) ? 
                (Array.isArray(result1[i]) ? JSON.stringify(result2[i]) : result2[i]) : result2[i];
            
            if (val1 > val2) return 1;
            if (val1 < val2) return -1;
        }
        return 0;
    }
}

class PokerGame {
    constructor(playerCount = 4) {
        this.deck = new Deck();
        this.players = [];
        this.communityCards = [];
        this.pot = 0;
        this.currentBet = 0;
        this.dealerPosition = 0;
        this.currentPlayerIndex = 0;
        this.gameStage = 'waiting';
        this.smallBlind = 10;
        this.bigBlind = 20;
        
        this.initPlayers(playerCount);
    }
    
    initPlayers(count) {
        this.players = [];
        
        // 添加人类玩家
        this.players.push(new Player('你', 1000, false));
        
        // 添加AI玩家
        const aiNames = ['小明', '小红', '小刚', '小丽', '小华'];
        for (let i = 1; i < count; i++) {
            this.players.push(new Player(aiNames[i - 1], 1000, true));
        }
    }
    
    startNewGame() {
        this.deck.reset();
        this.communityCards = [];
        this.pot = 0;
        this.currentBet = 0;
        this.gameStage = 'preflop';
        
        // 重置玩家
        this.players.forEach(p => p.reset());
        
        // 移除没有筹码的玩家
        this.players = this.players.filter(p => p.chips > 0);
        
        if (this.players.length < 2) {
            addMessage('游戏结束！你赢了！', 'success');
            return;
        }
        
        // 发手牌
        for (let i = 0; i < 2; i++) {
            this.players.forEach(p => p.hand.push(this.deck.deal()));
        }
        
        // 收取盲注
        this.collectBlinds();
        
        this.updateUI();
        addMessage('游戏开始！', 'info');
        
        // 如果当前玩家是AI，让AI行动
        if (this.players[this.currentPlayerIndex].isAI) {
            setTimeout(() => this.aiTurn(), 1000);
        }
    }
    
    collectBlinds() {
        const sbPlayer = this.players[(this.dealerPosition + 1) % this.players.length];
        const bbPlayer = this.players[(this.dealerPosition + 2) % this.players.length];
        
        sbPlayer.bet(this.smallBlind);
        bbPlayer.bet(this.bigBlind);
        
        this.pot += this.smallBlind + this.bigBlind;
        this.currentBet = this.bigBlind;
        
        this.currentPlayerIndex = (this.dealerPosition + 3) % this.players.length;
    }
    
    dealCommunityCards(count) {
        for (let i = 0; i < count; i++) {
            this.communityCards.push(this.deck.deal());
        }
    }
    
    nextStage() {
        this.currentBet = 0;
        this.players.forEach(p => p.currentBet = 0);
        
        if (this.gameStage === 'preflop') {
            this.dealCommunityCards(3);
            this.gameStage = 'flop';
        } else if (this.gameStage === 'flop') {
            this.dealCommunityCards(1);
            this.gameStage = 'turn';
        } else if (this.gameStage === 'turn') {
            this.dealCommunityCards(1);
            this.gameStage = 'river';
        } else if (this.gameStage === 'river') {
            this.showdown();
            return;
        }
        
        this.currentPlayerIndex = (this.dealerPosition + 1) % this.players.length;
        this.updateUI();
        
        // 检查当前玩家是否是AI
        if (this.players[this.currentPlayerIndex].isAI) {
            setTimeout(() => this.aiTurn(), 1000);
        }
    }
    
    showdown() {
        this.gameStage = 'showdown';
        
        const activePlayers = this.players.filter(p => !p.isFolded);
        
        if (activePlayers.length === 1) {
            const winner = activePlayers[0];
            winner.chips += this.pot;
            addMessage(`${winner.name} 赢得 ${this.pot} 筹码！`, 'success');
        } else {
            let bestPlayer = null;
            let bestHand = null;
            
            activePlayers.forEach(player => {
                const allCards = player.hand.concat(this.communityCards);
                const hand = HandEvaluator.evaluate(allCards);
                
                if (!bestHand || this.compareHands(allCards, bestPlayer.hand.concat(this.communityCards)) > 0) {
                    bestHand = allCards;
                    bestPlayer = player;
                }
            });
            
            bestPlayer.chips += this.pot;
            const handName = HandEvaluator.getHandName(HandEvaluator.evaluate(bestPlayer.hand.concat(this.communityCards))[0]);
            addMessage(`${bestPlayer.name} 赢得 ${this.pot} 筹码！牌型：${handName}`, 'success');
        }
        
        this.updateUI();
    }
    
    playerAction(action, amount = 0) {
        const player = this.players[this.currentPlayerIndex];
        
        if (player.isFolded || player.isAllIn) {
            this.nextPlayer();
            return;
        }
        
        switch(action) {
            case 'fold':
                player.fold();
                break;
            case 'check':
                if (player.currentBet >= this.currentBet) {
                    player.lastAction = '过牌';
                } else {
                    addMessage('无法过牌，需要跟注', 'error');
                    return;
                }
                break;
            case 'call':
                const callAmount = this.currentBet - player.currentBet;
                if (callAmount > 0) {
                    player.call(callAmount);
                    this.pot += callAmount;
                }
                break;
            case 'raise':
                if (amount > this.currentBet) {
                    const raiseAmount = amount - this.currentBet;
                    player.bet(raiseAmount);
                    this.pot += raiseAmount;
                    this.currentBet = amount;
                } else {
                    addMessage(`加注必须大于当前注额 ${this.currentBet}`, 'error');
                    return;
                }
                break;
            case 'allin':
                const allinAmount = player.chips;
                player.bet(allinAmount);
                this.pot += allinAmount;
                if (player.currentBet > this.currentBet) {
                    this.currentBet = player.currentBet;
                }
                break;
        }
        
        addMessage(`${player.name}: ${player.lastAction}`, 'info');
        
        if (this.checkRoundComplete()) {
            this.nextStage();
        } else {
            this.nextPlayer();
        }
    }
    
    nextPlayer() {
        do {
            this.currentPlayerIndex = (this.currentPlayerIndex + 1) % this.players.length;
        } while (this.players[this.currentPlayerIndex].isFolded || this.players[this.currentPlayerIndex].isAllIn);
        
        this.updateUI();
        
        // 如果当前玩家是AI
        if (this.players[this.currentPlayerIndex].isAI) {
            setTimeout(() => this.aiTurn(), 1000);
        }
    }
    
    checkRoundComplete() {
        const activePlayers = this.players.filter(p => !p.isFolded && !p.isAllIn);
        
        if (activePlayers.length <= 1) return true;
        
        const allMatched = activePlayers.every(p => p.currentBet === this.currentBet);
        const allActed = activePlayers.every(p => p.lastAction !== '');
        
        return allMatched && allActed;
    }
    
    aiTurn() {
        const player = this.players[this.currentPlayerIndex];
        const toCall = this.currentBet - player.currentBet;
        
        // 简单AI逻辑
        const random = Math.random();
        
        if (toCall === 0) {
            // 可以过牌或加注
            if (random < 0.7) {
                this.playerAction('check');
            } else {
                const raiseAmount = Math.min(this.currentBet + this.bigBlind, player.chips);
                this.playerAction('raise', raiseAmount);
            }
        } else {
            // 需要跟注或弃牌
            if (random < 0.8) {
                this.playerAction('call');
            } else if (random < 0.95) {
                this.playerAction('allin');
            } else {
                this.playerAction('fold');
            }
        }
    }
    
    updateUI() {
        // 更新游戏信息
        document.getElementById('gameStage').textContent = this.getStageName();
        document.getElementById('pot').textContent = this.pot;
        document.getElementById('currentBet').textContent = this.currentBet;
        
        // 更新公共牌
        const communityCardsDiv = document.getElementById('communityCards');
        if (this.communityCards.length === 0) {
            communityCardsDiv.innerHTML = '<div style="color: #9ca3af;">等待发牌...</div>';
        } else {
            communityCardsDiv.innerHTML = this.communityCards.map(c => c.toHTML()).join('');
        }
        
        // 更新玩家列表
        const playersSection = document.getElementById('playersSection');
        playersSection.innerHTML = this.players.map((player, index) => {
            const isActive = index === this.currentPlayerIndex;
            const statusClass = player.isFolded ? 'folded' : (player.isAllIn ? 'allin' : '');
            
            return `
                <div class="player-card ${isActive ? 'current' : ''}">
                    <div class="player-header">
                        <span class="player-name">${player.name} ${!player.isAI ? '(你)' : ''}</span>
                        <span class="player-status ${statusClass}">${player.lastAction || '等待中'}</span>
                    </div>
                    <div class="player-stats">
                        筹码: ${player.chips} | 下注: ${player.currentBet}
                    </div>
                    <div class="my-cards" style="margin-top: 10px;">
                        ${player.hand.map(c => c.toHTML()).join('')}
                    </div>
                </div>
            `;
        }).join('');
        
        // 更新我的区域
        const myPlayer = this.players[0];
        if (this.gameStage !== 'waiting') {
            document.getElementById('mySection').style.display = 'block';
            document.getElementById('myChips').textContent = myPlayer.chips;
            
            const myCardsDiv = document.getElementById('myCards');
            myCardsDiv.innerHTML = myPlayer.hand.map(c => c.toHTML()).join('');
            
            // 更新按钮状态
            const toCall = this.currentBet - myPlayer.currentBet;
            const isMyTurn = this.currentPlayerIndex === 0;
            
            document.getElementById('btnFold').disabled = !isMyTurn;
            document.getElementById('btnCheck').disabled = !isMyTurn || toCall > 0;
            document.getElementById('btnCall').disabled = !isMyTurn || toCall === 0;
            document.getElementById('btnRaise').disabled = !isMyTurn;
            document.getElementById('btnAllin').disabled = !isMyTurn;
            
            if (toCall > 0) {
                document.getElementById('btnCall').textContent = `跟注 ${toCall}`;
                document.getElementById('btnCheck').style.display = 'none';
                document.getElementById('btnCall').style.display = 'inline-block';
            } else {
                document.getElementById('btnCheck').style.display = 'inline-block';
                document.getElementById('btnCall').style.display = 'none';
            }
        }
    }
    
    getStageName() {
        const names = {
            'waiting': '等待开始',
            'preflop': '翻牌前',
            'flop': '翻牌',
            'turn': '转牌',
            'river': '河牌',
            'showdown': '摊牌'
        };
        return names[this.gameStage] || this.gameStage;
    }
}

// 全局游戏实例
let game = null;

// 添加消息
function addMessage(message, type = 'info') {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// 开始新游戏
function startNewGame() {
    game = new PokerGame(4); // 4名玩家（1人类 + 3AI）
    game.startNewGame();
}

// 玩家行动
function playerAction(action, amount = 0) {
    if (!game || game.currentPlayerIndex !== 0) {
        addMessage('不是你的回合', 'error');
        return;
    }
    
    if (action === 'raise') {
        const raiseAmount = game.currentBet + game.bigBlind;
        game.playerAction('raise', raiseAmount);
    } else {
        game.playerAction(action, amount);
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 不自动开始，等待用户点击
});
