from random import shuffle
class BlackJack():
  def __init__(self,name,balance,cards):
    self.name=name
    self.balance=balance
    self.cards=cards
    
  def ask_move(self):
    print("{0}! Please choose 0 for STAY or 1 for HIT".format(self.name))
    return int(input("Enter your move:"))
  
  def assign_cards(self,cards_deck):
    self.cards.append(cards_deck.pop())
    print("Now the {} has following cards:".format(self.name))
    for card in self.cards:
      print(card)
    print("\n")
  
  def fixing_cards_value(self):
    for card_index,card in enumerate(self.cards):
      if card[1]==1:
        ace_card_val=int(input("{0}! Please choose either 1 OR 11 for Ace card".format(self.name)))
        print("\n")
        self.cards[card_index][1]=ace_card_val
        
  def compute_sum(self):
    cards_sum=0
    for card in self.cards:
      cards_sum+=card[1]
    return cards_sum
    
  def check_sum(self,card_sum):
    if card_sum>21:
      return 1
    else:
      return 0
    
  def stay_process(self):
    self.fixing_cards_value()
    cards_sum=self.compute_sum()
    result=self.check_sum(cards_sum)
    return result,cards_sum
  
  def hit_process(self,cards_deck):
    self.assign_cards(cards_deck)
    self.fixing_cards_value()
    cards_sum=self.compute_sum()
    result=self.check_sum(cards_sum)
    return result,cards_sum
    
  def credit(self,c_amt):
    self.balance+=c_amt
    print("{0}$ credited successfully into {1}'s account".format(c_amt,self.name))
    print("Available balance: {}$".format(self.balance))
    
  def debit(self,d_amt):
    if self.balance>=d_amt:
      self.balance-=d_amt
      print("{0}$ debited successfully from {1}'s account".format(d_amt,self.name))
    else:
      print("{} has insufficient balance".format(self.name))
    print("Available balance in {1}'s account: {0}$".format(self.balance,self.name))

if __name__=="__main__":
  replay=0
  while 1:
    print("Welcome to BlackJack!\n")
    cards_deck={}
    for card_type in ['H','S','D','C']:
      for x,y in zip(card_type*10,range(1,11)):
        cards_deck[x+str(y)]=y
      cards_deck[card_type+'J']=10
      cards_deck[card_type+'Q']=10
      cards_deck[card_type+'K']=10
    #cards_deck=list(cards_deck.items())
    cards_deck=[list(card) for card in cards_deck.items()]
    shuffle(cards_deck)
    plr_initial_cards=[cards_deck.pop()]+[cards_deck.pop()]
    dlr_initial_cards=[cards_deck.pop()]+[cards_deck.pop()]
    if replay==0:
      plr=BlackJack("Player",1000,plr_initial_cards)
      dlr=BlackJack("Dealer",1000,dlr_initial_cards)
    else:
      plr=BlackJack("Player",plr.balance,plr_initial_cards)
      dlr=BlackJack("Dealer",dlr.balance,dlr_initial_cards)
    def final_result(plr_cards_sum,dlr_cards_sum):
      if plr_cards_sum==dlr_cards_sum:
        win_flg=2
      elif plr_cards_sum>dlr_cards_sum:
        win_flg=1
      else:
        win_flg=0
      return win_flg
  
    print("\nPlayer will take the first move\n")
    bet_amt=int(input("Player! Enter a bet amount between 2$-500$: "))
    if bet_amt<=plr.balance and bet_amt<=dlr.balance:
      print("\n")
      print("Player has following cards:")
      for card in plr.cards:print(card)
      print("\n")
      while 1:
        plr_move=plr.ask_move()
        print("\n")
        if plr_move==0:
          # Code to clear the screen 
          print("Player stays!\n")
          result,plr_cards_sum=plr.stay_process()
          if result==1:
            print("Player busted!\n")
            win_flg=0
            break
          else:
            print("Dealer will take the chance now\n")
            print("Dealer opens his faced down card\n") 
            print("Dealer has following cards:")
            for card in dlr.cards:print(card)
            print("\n")
            while 1:
              dlr_move=dlr.ask_move()
              print("\n")
              if dlr_move==0:
                # Code to clear the screen
                print("Dealer stays!\n")
                result,dlr_cards_sum=dlr.stay_process()
                if result==1:
                  print("Dealer busted!\n")
                  win_flg=1
                  break
                else:
                  win_flg=final_result(plr_cards_sum,dlr_cards_sum)
                  break
              else:
                result,dlr_cards_sum=dlr.hit_process(cards_deck)
                if result==1:
                  print("Dealer busted!\n")
                  win_flg=1
                  break
                else:continue
        else:
          result,plr_cards_sum=plr.hit_process(cards_deck)
          if result==1:
            print("Player busted\n")
            win_flg=0
            break
          else:continue
        if win_flg in (0,1,2):
          break
      if win_flg==1:
        print("Wohoo! Player won\n")
        dlr.debit(bet_amt)
        plr.credit(bet_amt)
        print("\n")
      elif win_flg==0:
        print("Wohoo! Dealer won\n")
        plr.debit(bet_amt)
        dlr.credit(bet_amt)
        print("\n")
      else:
        print("Match is drawn\n")
    else:
      if bet_amt>plr.balance:print("Game could not be played as Player does not have sufficient balance\n")
      else:print("Game could not be played as Dealer does not have sufficient balance\n")
    replay=int(input("Please press 1 for Replay or 0 for Stop:"))
    print("\n")
    if replay==1:continue
    else:break
