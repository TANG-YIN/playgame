"""
德州扑克游戏主程序
支持2-6人玩家，包含完整的游戏逻辑
"""
import random
from collections import Counter
from enum import Enum

class GameState(Enum):
    """游戏状态枚举"""
    WAITING = "等待玩家加入"
    PREFLOP = "翻牌前"
    FLOP = "翻牌"
    TURN = "转牌"
    RIVER = "河牌"
    SHOWDOWN = "摊牌"
    GAME_OVER = "游戏结束"

class Card:
    """扑克牌类"""
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        
    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    def __repr__(self):
        return self.__str__()
    
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
    def __init__(self, name, chips=1000):
        self.name = name
        self.hand = []
        self.chips = chips
        self.current_bet = 0
        self.is_folded = False
        self.is_all_in = False
        self.is_active = True  # 是否在游戏中
        self.last_action = ""
        
    def reset_hand(self):
        """重置玩家手牌状态"""
        self.hand = []
        self.current_bet = 0
        self.is_folded = False
        self.is_all_in = False
        self.last_action = ""
        
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
            
    def __str__(self):
        status = ""
        if self.is_folded:
            status = " [已弃牌]"
        elif self.is_all_in:
            status = " [全押]"
        return f"{self.name}{status} - 筹码: {self.chips}"

class HandEvaluator:
    """牌力评估器"""
    @staticmethod
    def evaluate(cards):
        """
        评估手牌强度
        返回元组 (牌型等级, 关键牌值)
        牌型等级:
        0: 高牌
        1: 一对
        2: 两对
        3: 三条
        4: 顺子
        5: 同花
        6: 葫芦
        7: 四条
        8: 同花顺
        """
        if not cards:
            return (0, [])
            
        ranks = [card.get_value() for card in cards]
        suits = [card.suit for card in cards]
        
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)
        
        # 排序点数
        sorted_ranks = sorted(ranks, reverse=True)
        
        # 检查同花
        flush = max(suit_counts.values()) >= 5
        
        # 检查顺子（考虑A可以作为1）
        unique_ranks = sorted(list(set(ranks)), reverse=True)
        if 14 in unique_ranks:
            unique_ranks.append(1)  # A作为1
            
        straight = False
        straight_high = 0
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] - unique_ranks[i+4] == 4:
                straight = True
                straight_high = unique_ranks[i]
                break
        
        # 同花顺
        if flush and straight:
            return (8, straight_high)
        
        # 四条
        if 4 in rank_counts.values():
            four_rank = [r for r, count in rank_counts.items() if count == 4][0]
            kicker = max([r for r, count in rank_counts.items() if count != 4])
            return (7, four_rank, kicker)
        
        # 葫芦
        if 3 in rank_counts.values() and 2 in rank_counts.values():
            three_rank = max([r for r, count in rank_counts.items() if count == 3])
            pair_rank = max([r for r, count in rank_counts.items() if count == 2])
            return (6, three_rank, pair_rank)
        
        # 同花
        if flush:
            flush_suit = max(suit_counts, key=suit_counts.get)
            flush_ranks = sorted([card.get_value() for card in cards if card.suit == flush_suit], reverse=True)[:5]
            return (5, tuple(flush_ranks))
        
        # 顺子
        if straight:
            return (4, straight_high)
        
        # 三条
        if 3 in rank_counts.values():
            three_rank = max([r for r, count in rank_counts.items() if count == 3])
            kickers = sorted([r for r, count in rank_counts.items() if count != 3], reverse=True)[:2]
            return (3, three_rank, tuple(kickers))
        
        # 两对
        pairs = sorted([r for r, count in rank_counts.items() if count == 2], reverse=True)
        if len(pairs) >= 2:
            kicker = max([r for r, count in rank_counts.items() if count == 1], default=0)
            return (2, tuple(pairs[:2]), kicker)
        
        # 一对
        if len(pairs) == 1:
            kickers = sorted([r for r, count in rank_counts.items() if count != 2], reverse=True)[:3]
            return (1, pairs[0], tuple(kickers))
        
        # 高牌
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
    def __init__(self):
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
        self.round_bets = []  # 当前回合的投注历史
        
    def add_player(self, name, chips=1000):
        """添加玩家"""
        if len(self.players) >= 6:
            print("游戏最多支持6名玩家")
            return False
            
        if any(p.name == name for p in self.players):
            print(f"玩家 {name} 已存在")
            return False
            
        player = Player(name, chips)
        self.players.append(player)
        print(f"玩家 {name} 已加入游戏，初始筹码: {chips}")
        return True
    
    def start_game(self):
        """开始游戏"""
        if len(self.players) < 2:
            print("至少需要2名玩家才能开始游戏")
            return False
            
        # 只保留有筹码的玩家
        self.players = [p for p in self.players if p.chips > 0]
        
        if len(self.players) < 2:
            print("至少需要2名有筹码的玩家才能开始游戏")
            return False
            
        self.game_state = GameState.PREFLOP
        self.start_new_round()
        return True
    
    def start_new_round(self):
        """开始新一回合"""
        self.deck.reset()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.round_bets = []
        
        # 重置所有玩家状态
        for player in self.players:
            player.reset_hand()
            
        # 发手牌
        self.deal_hole_cards()
        
        # 收取盲注
        self.collect_blinds()
        
        print("\n" + "="*50)
        print("新一回合开始！")
        print(f"庄家位置: {self.players[self.dealer_position].name}")
        print(f"小盲: {self.small_blind}, 大盲: {self.big_blind}")
        print("="*50 + "\n")
        
        self.show_game_state()
        
    def deal_hole_cards(self):
        """发手牌"""
        for _ in range(2):
            for player in self.players:
                if player.chips > 0:
                    player.hand.append(self.deck.deal())
                    
        # 显示每个玩家的手牌
        for player in self.players:
            if player.chips > 0:
                hand_str = " ".join(str(card) for card in player.hand)
                print(f"{player.name} 的手牌: {hand_str}")
    
    def collect_blinds(self):
        """收取盲注"""
        num_players = len(self.players)
        
        # 小盲位置 (庄家下一位)
        sb_position = (self.dealer_position + 1) % num_players
        # 大盲位置 (小盲下一位)
        bb_position = (self.dealer_position + 2) % num_players
        
        # 收取小盲
        sb_player = self.players[sb_position]
        sb_amount = min(self.small_blind, sb_player.chips)
        sb_player.bet(sb_amount)
        self.pot += sb_amount
        
        # 收取大盲
        bb_player = self.players[bb_position]
        bb_amount = min(self.big_blind, bb_player.chips)
        bb_player.bet(bb_amount)
        self.pot += bb_amount
        
        self.current_bet = self.big_blind
        
        print(f"{sb_player.name} 支付小盲: {sb_amount}")
        print(f"{bb_player.name} 支付大盲: {bb_amount}")
        
        # 设置当前玩家（大盲下一位）
        self.current_player = (bb_position + 1) % num_players
    
    def deal_community_cards(self, count):
        """发公共牌"""
        cards = self.deck.deal_multiple(count)
        self.community_cards.extend(cards)
        return cards
    
    def next_stage(self):
        """进入下一阶段"""
        # 重置当前回合投注
        self.current_bet = 0
        for player in self.players:
            player.current_bet = 0
        self.round_bets = []
        
        # 设置当前玩家为庄家下一位
        self.current_player = (self.dealer_position + 1) % len(self.players)
        
        if self.game_state == GameState.PREFLOP:
            # 翻牌：发3张公共牌
            self.deal_community_cards(3)
            self.game_state = GameState.FLOP
        elif self.game_state == GameState.FLOP:
            # 转牌：发1张公共牌
            self.deal_community_cards(1)
            self.game_state = GameState.TURN
        elif self.game_state == GameState.TURN:
            # 河牌：发1张公共牌
            self.deal_community_cards(1)
            self.game_state = GameState.RIVER
        elif self.game_state == GameState.RIVER:
            # 摊牌
            self.game_state = GameState.SHOWDOWN
            self.showdown()
            return
            
        print(f"\n进入{self.game_state.value}阶段")
        if self.community_cards:
            comm_str = " ".join(str(card) for card in self.community_cards)
            print(f"公共牌: {comm_str}")
        print(f"底池: {self.pot}\n")
        
        self.show_game_state()
    
    def showdown(self):
        """摊牌阶段"""
        print("\n" + "="*50)
        print("摊牌！")
        print("="*50)
        
        # 找出未弃牌的玩家
        active_players = [p for p in self.players if not p.is_folded]
        
        if len(active_players) == 1:
            # 只剩一个玩家
            winner = active_players[0]
            winner.chips += self.pot
            print(f"其他玩家都已弃牌，{winner.name} 赢得 {self.pot} 筹码！")
        else:
            # 比较牌力
            best_hands = []
            for player in active_players:
                all_cards = player.hand + self.community_cards
                hand_result = HandEvaluator.evaluate(all_cards)
                hand_name = HandEvaluator.get_hand_name(hand_result[0])
                
                print(f"{player.name}: {hand_name}")
                print(f"  手牌: {' '.join(str(c) for c in player.hand)}")
                
                best_hands.append((player, hand_result))
            
            # 找出最大的牌
            best_hands.sort(key=lambda x: x[1], reverse=True)
            best_hand = best_hands[0]
            best_players = [p for p, h in best_hands if h == best_hand[1]]
            
            # 分配筹码
            win_amount = self.pot // len(best_players)
            for player in best_players:
                player.chips += win_amount
                hand_name = HandEvaluator.get_hand_name(best_hand[1][0])
                print(f"\n{player.name} 赢得 {win_amount} 筹码！")
                print(f"牌型: {hand_name}")
        
        print("="*50 + "\n")
        
        # 移动庄家位置
        self.dealer_position = (self.dealer_position + 1) % len(self.players)
        self.game_state = GameState.GAME_OVER
    
    def player_action(self, action, amount=0):
        """玩家执行动作"""
        player = self.players[self.current_player]
        
        if player.is_folded or player.is_all_in:
            self.next_player()
            return
            
        print(f"{player.name} 执行动作: {action}")
        
        if action == "fold":
            player.fold()
        elif action == "check":
            if player.current_bet >= self.current_bet:
                player.last_action = "过牌"
            else:
                print("无法过牌，需要跟注")
                return
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
                    print(f"筹码不足，最大可下注: {player.chips + player.current_bet}")
                    return
            else:
                print(f"加注金额必须大于当前注额: {self.current_bet}")
                return
        elif action == "allin":
            allin_amount = player.chips
            total_bet = allin_amount + player.current_bet
            player.bet(allin_amount)
            self.pot += allin_amount
            if total_bet > self.current_bet:
                self.current_bet = total_bet
        
        # 检查是否所有人行动完毕
        if self.check_round_complete():
            self.next_stage()
        else:
            self.next_player()
    
    def next_player(self):
        """下一个玩家"""
        num_players = len(self.players)
        
        # 找下一个未弃牌、未全押的玩家
        for _ in range(num_players):
            self.current_player = (self.current_player + 1) % num_players
            player = self.players[self.current_player]
            
            if not player.is_folded and not player.is_all_in:
                # 检查是否所有玩家都已经跟注
                active_players = [p for p in self.players if not p.is_folded and not p.is_all_in]
                all_matched = all(p.current_bet == self.current_bet for p in active_players)
                
                if all_matched:
                    if self.current_player == (self.dealer_position + 1) % num_players:
                        # 回到第一个行动玩家，回合结束
                        self.next_stage()
                        return
                
                return
        
        # 所有活跃玩家都全押了
        self.next_stage()
    
    def check_round_complete(self):
        """检查回合是否完成"""
        active_players = [p for p in self.players if not p.is_folded and not p.is_all_in]
        
        if not active_players:
            # 所有人都全押了或弃牌了
            return True
            
        if all(p.current_bet == self.current_bet for p in active_players):
            # 所有人都已跟注
            # 检查是否所有活跃玩家都至少行动过一次
            all_acted = all(p.last_action != "" for p in active_players)
            if all_acted:
                return True
                
        return False
    
    def show_game_state(self):
        """显示游戏状态"""
        print(f"底池: {self.pot}")
        print(f"当前注额: {self.current_bet}")
        print("\n玩家状态:")
        
        for i, player in enumerate(self.players):
            marker = " <- 庄家" if i == self.dealer_position else ""
            marker += " <- 当前" if i == self.current_player else ""
            print(f"  {player}{marker}")
            
            if player.current_bet > 0:
                print(f"    本轮下注: {player.current_bet}")
            if player.last_action:
                print(f"    动作: {player.last_action}")
        
        print()
    
    def play_round(self):
        """进行一回合游戏（命令行交互）"""
        if self.game_state == GameState.GAME_OVER:
            if not self.start_game():
                return
        
        while self.game_state != GameState.GAME_OVER:
            print("\n" + "="*50)
            print(f"当前阶段: {self.game_state.value}")
            print("="*50)
            
            player = self.players[self.current_player]
            
            if player.is_folded:
                print(f"{player.name} 已弃牌")
                self.next_player()
                continue
                
            if player.is_all_in:
                print(f"{player.name} 已全押")
                self.next_player()
                continue
            
            print(f"\n当前玩家: {player.name}")
            print(f"筹码: {player.chips}")
            print(f"手牌: {' '.join(str(c) for c in player.hand)}")
            print(f"当前下注: {player.current_bet}, 底池注额: {self.current_bet}")
            
            # 显示操作选项
            to_call = self.current_bet - player.current_bet
            print(f"\n需要跟注: {to_call}")
            print("可用操作:")
            if to_call == 0:
                print("  1. 过牌 (check)")
                print("  2. 加注 (raise)")
                print("  3. 弃牌 (fold)")
                print("  4. 全押 (allin)")
            else:
                print("  1. 跟注 (call)")
                print("  2. 加注 (raise)")
                print("  3. 弃牌 (fold)")
                print("  4. 全押 (allin)")
            
            # 获取用户输入
            choice = input("\n请选择操作 (1-4): ").strip()
            
            if choice == "1":
                if to_call == 0:
                    self.player_action("check")
                else:
                    self.player_action("call")
            elif choice == "2":
                try:
                    min_raise = self.current_bet + self.big_blind
                    amount = int(input(f"加注金额 (最小 {min_raise}): "))
                    if amount >= min_raise:
                        self.player_action("raise", amount)
                    else:
                        print(f"加注金额不能小于 {min_raise}")
                except ValueError:
                    print("请输入有效的数字")
            elif choice == "3":
                self.player_action("fold")
            elif choice == "4":
                self.player_action("allin")
            else:
                print("无效的选择")
            
            self.show_game_state()
            
            # 自动进入下一阶段
            if self.check_round_complete():
                input("按回车键继续...")
                self.next_stage()

def main():
    """主函数"""
    print("="*50)
    print("德州扑克游戏")
    print("="*50)
    
    game = PokerGame()
    
    # 添加玩家
    while len(game.players) < 2:
        name = input(f"输入第 {len(game.players)+1} 位玩家名称: ").strip()
        if name:
            game.add_player(name)
    
    while True:
        more = input(f"已添加 {len(game.players)} 名玩家，是否继续添加？(y/n): ").strip().lower()
        if more != 'y':
            break
        
        if len(game.players) >= 6:
            print("游戏最多支持6名玩家")
            break
            
        name = input("输入玩家名称: ").strip()
        if name:
            game.add_player(name)
    
    # 开始游戏
    print("\n游戏开始！")
    game.start_game()
    
    # 游戏循环
    while True:
        game.play_round()
        
        # 检查是否有足够玩家继续
        active_players = [p for p in game.players if p.chips > 0]
        if len(active_players) < 2:
            print("\n游戏结束！")
            print(f"获胜者: {active_players[0].name}")
            break
        
        # 询问是否继续
        cont = input("\n是否开始新一回合？(y/n): ").strip().lower()
        if cont != 'y':
            break
        
        game.start_game()
    
    print("\n感谢游戏！")

if __name__ == "__main__":
    main()
