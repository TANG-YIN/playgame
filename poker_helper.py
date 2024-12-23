import tkinter as tk
from tkinter import ttk
import itertools
from collections import Counter

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        
    def __str__(self):
        return f"{self.rank}{self.suit}"

class PokerHelper:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("德州扑克助手")
        self.window.geometry("800x600")
        
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.suits = ['♠', '♥', '♣', '♦']
        
        self.setup_gui()
        
    def setup_gui(self):
        # 手牌选择区
        hand_frame = ttk.LabelFrame(self.window, text="你的手牌")
        hand_frame.pack(pady=10, padx=10)
        
        self.hand_cards = []
        for i in range(2):
            card_frame = ttk.Frame(hand_frame)
            card_frame.pack(side=tk.LEFT, padx=5)
            
            rank_var = tk.StringVar()
            suit_var = tk.StringVar()
            
            rank_combo = ttk.Combobox(card_frame, textvariable=rank_var, values=self.ranks, width=5)
            suit_combo = ttk.Combobox(card_frame, textvariable=suit_var, values=self.suits, width=5)
            
            rank_combo.pack(side=tk.LEFT)
            suit_combo.pack(side=tk.LEFT)
            
            self.hand_cards.append((rank_var, suit_var))
            
        # 公共牌选择区
        community_frame = ttk.LabelFrame(self.window, text="公共牌")
        community_frame.pack(pady=10, padx=10)
        
        self.community_cards = []
        for i in range(5):
            card_frame = ttk.Frame(community_frame)
            card_frame.pack(side=tk.LEFT, padx=5)
            
            rank_var = tk.StringVar()
            suit_var = tk.StringVar()
            
            rank_combo = ttk.Combobox(card_frame, textvariable=rank_var, values=self.ranks, width=5)
            suit_combo = ttk.Combobox(card_frame, textvariable=suit_var, values=self.suits, width=5)
            
            rank_combo.pack(side=tk.LEFT)
            suit_combo.pack(side=tk.LEFT)
            
            self.community_cards.append((rank_var, suit_var))
            
        # 计算按钮
        calc_button = ttk.Button(self.window, text="计算胜率", command=self.calculate_odds)
        calc_button.pack(pady=10)
        
        # 结果显示
        self.result_label = ttk.Label(self.window, text="")
        self.result_label.pack(pady=10)
        
    def get_hand_strength(self, cards):
        # 改进牌力计算方法
        ranks = [card.rank for card in cards]
        suits = [card.suit for card in cards]
        
        # 计算点数值
        rank_values = []
        for rank in ranks:
            if rank == 'A':
                rank_values.append(14)
            elif rank == 'K':
                rank_values.append(13)
            elif rank == 'Q':
                rank_values.append(12)
            elif rank == 'J':
                rank_values.append(11)
            else:
                rank_values.append(int(rank))
        
        rank_values.sort(reverse=True)
        rank_counts = Counter(rank_values)
        
        # 检查同花
        suit_counts = Counter(suits)
        flush = max(suit_counts.values()) >= 5
        
        # 检查顺子（考虑A可以作为1的情况）
        straight = False
        if 14 in rank_values:  # 如果有A，添加值1用于A-5顺子判断
            rank_values.append(1)
        
        for i in range(len(rank_values) - 4):
            if rank_values[i] - rank_values[i+4] == 4:
                straight = True
                break
        
        # 返回牌力得分和关键牌值
        if flush and straight:
            return (8, max(rank_values))  # 同花顺
        
        # 检查四条
        if 4 in rank_counts.values():
            four_rank = [r for r, count in rank_counts.items() if count == 4][0]
            kicker = max([r for r in rank_values if r != four_rank])
            return (7, four_rank, kicker)  # 四条
        
        # 检查葫芦
        if 3 in rank_counts.values() and 2 in rank_counts.values():
            three_rank = [r for r, count in rank_counts.items() if count == 3][0]
            pair_rank = max([r for r, count in rank_counts.items() if count == 2])
            return (6, three_rank, pair_rank)  # 葫芦
        
        if flush:
            flush_ranks = sorted([rank_values[i] for i, suit in enumerate(suits) 
                                if suit == max(suit_counts, key=suit_counts.get)], reverse=True)[:5]
            return (5, flush_ranks)  # 同花
        
        if straight:
            straight_high = max(i for i in range(len(rank_values)-4) 
                              if rank_values[i] - rank_values[i+4] == 4)
            return (4, rank_values[straight_high])  # 顺子
        
        if 3 in rank_counts.values():
            three_rank = [r for r, count in rank_counts.items() if count == 3][0]
            kickers = sorted([r for r in rank_values if r != three_rank], reverse=True)[:2]
            return (3, three_rank, kickers)  # 三条
        
        pairs = [r for r, count in rank_counts.items() if count == 2]
        if len(pairs) == 2:
            kicker = max([r for r in rank_values if r not in pairs])
            return (2, sorted(pairs, reverse=True), kicker)  # 两对
        
        if len(pairs) == 1:
            kickers = sorted([r for r in rank_values if r != pairs[0]], reverse=True)[:3]
            return (1, pairs[0], kickers)  # 一对
        
        return (0, rank_values[:5])  # 高牌

    def calculate_odds(self):
        # 获取已知牌
        known_cards = []
        
        # 获取手牌
        for rank_var, suit_var in self.hand_cards:
            if rank_var.get() and suit_var.get():
                known_cards.append(Card(rank_var.get(), suit_var.get()))
                
        # 获取公共牌
        community = []
        for rank_var, suit_var in self.community_cards:
            if rank_var.get() and suit_var.get():
                card = Card(rank_var.get(), suit_var.get())
                known_cards.append(card)
                community.append(card)
                
        if len(known_cards) < 2:
            self.result_label.config(text="请至少选择你的手牌")
            return
            
        # 创建剩余牌堆
        deck = []
        for rank in self.ranks:
            for suit in self.suits:
                card = Card(rank, suit)
                if not any(str(c) == str(card) for c in known_cards):
                    deck.append(card)
                    
        remaining_cards = len(deck)
        remaining_community = 5 - len(community)
        
        # 计算组合数
        def nCr(n, r):
            import math
            return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))
        
        # 计算总的可能性数量
        total_possibilities = 0
        favorable_outcomes = 0
        
        # 对手的手牌组合数
        opponent_combinations = nCr(remaining_cards, 2)
        
        # 如果还有公共牌要发
        if remaining_community > 0:
            # 计算剩余公共牌的组合数
            community_combinations = nCr(remaining_cards - 2, remaining_community)
            total_possibilities = opponent_combinations * community_combinations
            
            # 遍历所有可能的对手手牌
            for opp_cards in itertools.combinations(deck, 2):
                remaining_deck = [card for card in deck if card not in opp_cards]
                
                # 遍历所有可能的公共牌
                for comm_cards in itertools.combinations(remaining_deck, remaining_community):
                    full_community = community + list(comm_cards)
                    
                    # 计算双方的牌力
                    player_strength = self.get_hand_strength(known_cards[:2] + full_community)
                    opponent_strength = self.get_hand_strength(list(opp_cards) + full_community)
                    
                    if player_strength > opponent_strength:
                        favorable_outcomes += 1
                    elif player_strength == opponent_strength:
                        favorable_outcomes += 0.5
        else:
            # 如果公共牌已经全部发出
            total_possibilities = opponent_combinations
            
            # 遍历所有可能的对手手牌
            for opp_cards in itertools.combinations(deck, 2):
                # 计算双方的牌力
                player_strength = self.get_hand_strength(known_cards[:2] + community)
                opponent_strength = self.get_hand_strength(list(opp_cards) + community)
                
                if player_strength > opponent_strength:
                    favorable_outcomes += 1
                elif player_strength == opponent_strength:
                    favorable_outcomes += 0.5
        
        # 计算精确胜率
        win_probability = (favorable_outcomes / total_possibilities) * 100
        
        # 显示结果
        if remaining_community == 0:
            stage = "河牌"
        elif remaining_community == 1:
            stage = "转牌"
        elif remaining_community == 2:
            stage = "翻牌"
        else:
            stage = "发牌前"
            
        self.result_label.config(
            text=f"在{stage}阶段:\n"
                 f"胜率为: {win_probability:.2f}%\n"
                 f"(基于精确数学计算)\n"
                 f"总可能性: {total_possibilities:,}\n"
                 f"有利结果: {favorable_outcomes:,}"
        )
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = PokerHelper()
    app.run() 