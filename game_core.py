"""
德州扑克游戏核心逻辑模块
从poker_game.py提取核心类和函数，供Web版本使用
"""
import random
from collections import Counter
from enum import Enum

class GameState(Enum):
    """游戏状态枚举"""
    WAITING = "waiting"
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"
    SHOWDOWN = "showdown"
    GAME_OVER = "game_over"

class Card:
    """扑克牌类"""
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        
    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        """转换为字典格式，便于JSON序列化"""
        return {
            'rank': self.rank,
            'suit': self.suit,
            'value': self.get_value()
        }
    
    def get_value(self):
        """获取牌的数值"""
        rank_values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
            '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }
        return rank_values.get(self.rank, 0)

class Deck:
    """扑克牌堆类"""
    def __init__(self):
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.suits = ['♠', '♥', '♣', '♦']
        self.cards = []
        self.reset()
        
    def reset(self):
        """重置牌堆"""
        self.cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]
        random.shuffle(self.cards)
        
    def deal(self):
        """发一张牌"""
        if self.cards:
            return self.cards.pop()
        return None
    
    def deal_multiple(self, count):
        """发多张牌"""
        return [self.deal() for _ in range(count)]

class Player:
    """玩家类"""
    def __init__(self, name, chips=1000, player_id=None):
        self.name = name
        self.player_id = player_id or name
        self.hand = []
        self.chips = chips
        self.current_bet = 0
        self.is_folded = False
        self.is_all_in = False
        self.is_active = True
        self.last_action = ""
        
    def reset_hand(self):
        """重置玩家手牌状态"""
        self.hand = []
        self.current_bet = 0
        self.is_folded = False
        self.is_all_in = False
        self.last_action = ""
        
    def to_dict(self, show_hand=False):
        """转换为字典格式"""
        return {
            'id': self.player_id,
            'name': self.name,
            'chips': self.chips,
            'current_bet': self.current_bet,
            'is_folded': self.is_folded,
            'is_all_in': self.is_all_in,
            'is_active': self.is_active,
            'last_action': self.last_action,
            'hand': [card.to_dict() for card in self.hand] if show_hand else [],
            'hand_count': len(self.hand)
        }
        
    def fold(self):
        """弃牌"""
        self.is_folded = True
        self.last_action = "弃牌"
        
    def bet(self, amount):
        """下注"""
        if amount >= self.chips:
            # 全押
            self.current_bet += self.chips
            self.chips = 0
            self.is_all_in = True
            self.last_action = f"全押 {self.current_bet}"
        else:
            self.chips -= amount
            self.current_bet += amount
            self.last_action = f"下注 {amount}"
            
    def call(self, amount):
        """跟注"""
        bet_amount = min(amount, self.chips)
        self.bet(bet_amount)
        if self.last_action.startswith("下注"):
            self.last_action = f"跟注 {bet_amount}"

class HandEvaluator:
    """牌力评估器"""
    @staticmethod
    def evaluate(cards):
        """评估手牌强度"""
        if not cards:
            return (0, [])
            
        ranks = [card.get_value() for card in cards]
        suits = [card.suit for card in cards]
        
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)
        
        sorted_ranks = sorted(ranks, reverse=True)
        unique_ranks = sorted(list(set(ranks)), reverse=True)
        if 14 in unique_ranks:
            unique_ranks.append(1)
            
        straight = False
        straight_high = 0
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] - unique_ranks[i+4] == 4:
                straight = True
                straight_high = unique_ranks[i]
                break
        
        flush = max(suit_counts.values()) >= 5
        
        if flush and straight:
            return (8, straight_high)
        
        if 4 in rank_counts.values():
            four_rank = [r for r, count in rank_counts.items() if count == 4][0]
            kicker = max([r for r, count in rank_counts.items() if count != 4])
            return (7, four_rank, kicker)
        
        if 3 in rank_counts.values() and 2 in rank_counts.values():
            three_rank = max([r for r, count in rank_counts.items() if count == 3])
            pair_rank = max([r for r, count in rank_counts.items() if count == 2])
            return (6, three_rank, pair_rank)
        
        if flush:
            flush_suit = max(suit_counts, key=suit_counts.get)
            flush_ranks = sorted([card.get_value() for card in cards if card.suit == flush_suit], reverse=True)[:5]
            return (5, tuple(flush_ranks))
        
        if straight:
            return (4, straight_high)
        
        if 3 in rank_counts.values():
            three_rank = max([r for r, count in rank_counts.items() if count == 3])
            kickers = sorted([r for r, count in rank_counts.items() if count != 3], reverse=True)[:2]
            return (3, three_rank, tuple(kickers))
        
        pairs = sorted([r for r, count in rank_counts.items() if count == 2], reverse=True)
        if len(pairs) >= 2:
            kicker = max([r for r, count in rank_counts.items() if count == 1], default=0)
            return (2, tuple(pairs[:2]), kicker)
        
        if len(pairs) == 1:
            kickers = sorted([r for r, count in rank_counts.items() if count != 2], reverse=True)[:3]
            return (1, pairs[0], tuple(kickers))
        
        return (0, tuple(sorted_ranks[:5]))
    
    @staticmethod
    def get_hand_name(rank):
        """获取牌型名称"""
        names = {
            8: "同花顺",
            7: "四条",
            6: "葫芦",
            5: "同花",
            4: "顺子",
            3: "三条",
            2: "两对",
            1: "一对",
            0: "高牌"
        }
        return names.get(rank, "未知")

class PokerGame:
    """德州扑克游戏类"""
    def __init__(self, game_id=None):
        self.game_id = game_id or str(random.randint(100000, 999999))
        self.players = []
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.dealer_position = 0
        self.current_player = 0
        self.game_state = GameState.WAITING
        self.small_blind = 10
        self.big_blind = 20
        self.round_bets = []
        self.min_players = 2
        self.max_players = 6
        
    def add_player(self, name, chips=1000):
        """添加玩家"""
        if len(self.players) >= self.max_players:
            return False, "游戏已满"
            
        if any(p.name == name for p in self.players):
            return False, "玩家名已存在"
            
        player = Player(name, chips)
        self.players.append(player)
        return True, f"玩家 {name} 已加入游戏"
    
    def remove_player(self, player_id):
        """移除玩家"""
        for i, player in enumerate(self.players):
            if player.player_id == player_id:
                self.players.pop(i)
                return True
        return False
    
    def get_game_state(self, player_id=None):
        """获取游戏状态"""
        show_hand = player_id is not None
        return {
            'game_id': self.game_id,
            'game_state': self.game_state.value,
            'pot': self.pot,
            'current_bet': self.current_bet,
            'community_cards': [card.to_dict() for card in self.community_cards],
            'players': [p.to_dict(show_hand=(p.player_id == player_id)) for p in self.players],
            'current_player': self.current_player,
            'dealer_position': self.dealer_position,
            'player_count': len(self.players),
            'min_players': self.min_players,
            'max_players': self.max_players
        }
    
    def start_game(self):
        """开始游戏"""
        if len(self.players) < self.min_players:
            return False, f"至少需要{self.min_players}名玩家"
            
        self.players = [p for p in self.players if p.chips > 0]
        
        if len(self.players) < self.min_players:
            return False, f"至少需要{self.min_players}名有筹码的玩家"
            
        self.game_state = GameState.PREFLOP
        self.start_new_round()
        return True, "游戏开始"
    
    def start_new_round(self):
        """开始新一回合"""
        self.deck.reset()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.round_bets = []
        
        for player in self.players:
            player.reset_hand()
            
        self.deal_hole_cards()
        self.collect_blinds()
        
    def deal_hole_cards(self):
        """发手牌"""
        for _ in range(2):
            for player in self.players:
                if player.chips > 0:
                    player.hand.append(self.deck.deal())
    
    def collect_blinds(self):
        """收取盲注"""
        if not self.players:
            return
            
        num_players = len(self.players)
        sb_position = (self.dealer_position + 1) % num_players
        bb_position = (self.dealer_position + 2) % num_players
        
        sb_player = self.players[sb_position]
        sb_amount = min(self.small_blind, sb_player.chips)
        sb_player.bet(sb_amount)
        self.pot += sb_amount
        
        bb_player = self.players[bb_position]
        bb_amount = min(self.big_blind, bb_player.chips)
        bb_player.bet(bb_amount)
        self.pot += bb_amount
        
        self.current_bet = self.big_blind
        self.current_player = (bb_position + 1) % num_players
    
    def deal_community_cards(self, count):
        """发公共牌"""
        cards = self.deck.deal_multiple(count)
        self.community_cards.extend(cards)
        return cards
    
    def next_stage(self):
        """进入下一阶段"""
        self.current_bet = 0
        for player in self.players:
            player.current_bet = 0
        self.round_bets = []
        
        if len(self.players) == 0:
            return False, "没有玩家"
            
        self.current_player = (self.dealer_position + 1) % len(self.players)
        
        if self.game_state == GameState.PREFLOP:
            self.deal_community_cards(3)
            self.game_state = GameState.FLOP
        elif self.game_state == GameState.FLOP:
            self.deal_community_cards(1)
            self.game_state = GameState.TURN
        elif self.game_state == GameState.TURN:
            self.deal_community_cards(1)
            self.game_state = GameState.RIVER
        elif self.game_state == GameState.RIVER:
            self.game_state = GameState.SHOWDOWN
            return self.showdown()
            
        return True, "进入下一阶段"
    
    def showdown(self):
        """摊牌"""
        active_players = [p for p in self.players if not p.is_folded]
        
        if len(active_players) == 1:
            winner = active_players[0]
            winner.chips += self.pot
            self.game_state = GameState.GAME_OVER
            return True, f"{winner.name} 赢得 {self.pot} 筹码"
        
        best_hands = []
        for player in active_players:
            all_cards = player.hand + self.community_cards
            hand_result = HandEvaluator.evaluate(all_cards)
            best_hands.append((player, hand_result))
        
        best_hands.sort(key=lambda x: x[1], reverse=True)
        best_hand = best_hands[0]
        best_players = [p for p, h in best_hands if h == best_hand[1]]
        
        win_amount = self.pot // len(best_players)
        winners = []
        for player in best_players:
            player.chips += win_amount
            hand_name = HandEvaluator.get_hand_name(best_hand[1][0])
            winners.append(f"{player.name} ({hand_name})")
        
        self.game_state = GameState.GAME_OVER
        self.dealer_position = (self.dealer_position + 1) % len(self.players)
        
        return True, f"获胜者: {', '.join(winners)}"
    
    def player_action(self, player_id, action, amount=0):
        """玩家执行动作"""
        player = None
        for p in self.players:
            if p.player_id == player_id:
                player = p
                break
                
        if not player:
            return False, "玩家不存在"
            
        if player.player_id != self.players[self.current_player].player_id:
            return False, "不是你的回合"
            
        if player.is_folded or player.is_all_in:
            self.next_player()
            return True, "自动跳过"
        
        try:
            if action == "fold":
                player.fold()
            elif action == "check":
                if player.current_bet >= self.current_bet:
                    player.last_action = "过牌"
                else:
                    return False, "无法过牌，需要跟注"
            elif action == "call":
                call_amount = self.current_bet - player.current_bet
                if call_amount > 0:
                    player.call(call_amount)
                    self.pot += call_amount
            elif action == "raise":
                if amount > self.current_bet:
                    raise_amount = amount - self.current_bet
                    total_bet = raise_amount - (self.current_bet - player.current_bet)
                    if total_bet <= player.chips:
                        player.bet(total_bet)
                        self.pot += total_bet
                        self.current_bet = amount
                    else:
                        return False, f"筹码不足，最大可下注: {player.chips + player.current_bet}"
                else:
                    return False, f"加注金额必须大于当前注额: {self.current_bet}"
            elif action == "allin":
                allin_amount = player.chips
                total_bet = allin_amount + player.current_bet
                player.bet(allin_amount)
                self.pot += allin_amount
                if total_bet > self.current_bet:
                    self.current_bet = total_bet
            else:
                return False, "未知操作"
                
            if self.check_round_complete():
                return self.next_stage()
            else:
                self.next_player()
                return True, "操作成功"
                
        except Exception as e:
            return False, str(e)
    
    def next_player(self):
        """下一个玩家"""
        num_players = len(self.players)
        if num_players == 0:
            return
            
        for _ in range(num_players):
            self.current_player = (self.current_player + 1) % num_players
            player = self.players[self.current_player]
            
            if not player.is_folded and not player.is_all_in:
                active_players = [p for p in self.players if not p.is_folded and not p.is_all_in]
                if len(active_players) <= 1:
                    self.next_stage()
                    return
                
                all_matched = all(p.current_bet == self.current_bet for p in active_players)
                if all_matched:
                    if self.current_player == (self.dealer_position + 1) % num_players:
                        self.next_stage()
                        return
                return
        
        self.next_stage()
    
    def check_round_complete(self):
        """检查回合是否完成"""
        active_players = [p for p in self.players if not p.is_folded and not p.is_all_in]
        
        if not active_players:
            return True
            
        if all(p.current_bet == self.current_bet for p in active_players):
            all_acted = all(p.last_action != "" for p in active_players)
            if all_acted:
                return True
                
        return False
