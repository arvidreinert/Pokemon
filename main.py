from setup import *
from rectangle import *
from online_stuff import *
import os

images = os.listdir()
info_text = False
#looking if Deckinfos exist
for file in images:
    if "Deck_info_" in file:
        info_text = True
        break

imgs = []
#sorting images:
for im in images:
    if "png" in im and not "back_oc" in im:
        imgs.append(im)

#creating a Deck_file if none is existing:

if info_text == False:
    font = pygame.font.Font('freesansbold.ttf', 40)
    #we need every card to be in a dict of the form Imagename:amount
    card_images_dict = {}
    for im in imgs:
        x = 1.75
        rect = Rectangle((245*x,324*x),(width/2,height/2),(0,0,0),im)
        acepted = False
        card_counter = 0
        text = font.render('GeeksForGeeks', True,(0,0,0))
        textRect = text.get_rect()
        textRect.center = (width/2+400, height/2)
        while not acepted:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        card_counter -= 1

                    if event.key == pygame.K_c:
                        card_images_dict[im] = str(card_counter)
                        acepted = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    card_counter += 1

            text = font.render(str(card_counter), True,(0,0,0))

            screen.fill((100,100,120))
            rect.update(screen)
            screen.blit(text, textRect)
            pygame.display.update()

    #saving the dict in a file
    #Has to be edited!
    name = input("name des Decks?(Idealerweise gleich wie bei den Bildern)")
    f = open(f"Deck_info_{name}.txt", "a")
    f.write(f"card_images={card_images_dict}")
    f.close()

#now here the real code starts:
class actions():
    def __init__(self,own_card_dic):
        self.my_cards = own_cards_dict
        #print(self.my_cards,type(self.my_cards))

    def make_list_from_card_dic(self,card_dic):
        card_list = []
        listed_dic = list(card_dic)
        for key in listed_dic:
            if card_dic[key] == 1:
                card_list.append(f"{key}1")
            else:
                for i in range(0,int(card_dic[key])):
                    card_list.append(f"{key}{i}")
        return card_list

    def shuffle_deck():
        pass

def get_dict_from_deck_info(name):
    deck_info_own = name
    file = open(deck_info_own, "r")
    card_dict,content = file.readline().split("=")

    deck_info_own = content
    test_dic = {}
    x = deck_info_own.split(",")
    x[0] = list(x[0])
    del x[0][0]
    t = ""
    for i in x[0]:
        t += i
    x[0] = t

    x[-1] = list(x[-1])
    del x[-1][-1]
    t = ""
    for i in x[-1]:
        t += i
    x[-1] = t

    for element in x:
        key,value = element.split(":")
        key = key.replace("'","")
        key = key.replace(" ","")
        value = value.replace("'","")
        value = value.replace(" ","")

        test_dic[key] = value
    return test_dic

#getting how the own safe file is called:
deck_info_own = ""
files = os.listdir()
for file in files:
    if "Deck_info_" in file and "opponent" not in file:
        deck_info_own = file
#getting the dict from it:
own_cards_dict = get_dict_from_deck_info(deck_info_own)
action = actions(own_cards_dict)
#print(action.make_list_from_card_dic(own_cards_dict))

class game():
    def __init__(self,action_class,own_dict,server):
        self.server = server
        self.action = action_class
        self.running = True
        self.my_cards = action.make_list_from_card_dic(own_dict)
        self.cards_in_deck = self.my_cards
        self.deck_rect = Rectangle((245*0.75,324*0.75),(width-100,height-350),(0,0,0),"back_oc.png")
        self.deck_opponent_rect = Rectangle((245*0.75,324*0.75),(100,350),(0,0,0),"back_oc.png")
        self.your_turn_rect = Rectangle((100,100),(150,height/2),(0,0,255))
        self.your_turn = None
        self.deck_opponent_rect.is_updating = False
        self.shown_cards = {}
        self.defeated_cards = []
        self.actions = []

    def shuffle_deck(self):
        random.shuffle(self.cards_in_deck)

    def get_image_without_number(self,image):
        l_image = list(image)
        l_image[-1] = ""
        image = ""
        for i in l_image:
            image += i
        return image

    def draw_card(self):
        l = len(list(self.shown_cards))
        self.shown_cards[f"card{l}"] = Rectangle((245*0.65,324*0.65),(width-300,height-400),(0,0,0),self.get_image_without_number(self.cards_in_deck[0]),cards_full_name=self.cards_in_deck[0])
        self.flip_card(f"card{l}")
        #the command to make a card with the attributes name,original image,the cards full name
        self.actions.append(f"create:card{l},{self.get_image_without_number(self.cards_in_deck[0])},{self.cards_in_deck[0]}")
        del self.cards_in_deck[0]

    def flip_card(self,card_name):
        if not self.shown_cards[str(card_name)].flipped:
            self.shown_cards[str(card_name)].set_image(self.shown_cards[str(card_name)].unloaded_image,False)
            self.shown_cards[str(card_name)].flipped = True
        else:
            self.shown_cards[str(card_name)].set_image("back_oc.png",False)
            self.shown_cards[str(card_name)].flipped = False
    def transform_the_position(self,pos=(width-300,height-400)):
        #a function to place the opponents cards on the right place:
        new_pos = (width-pos[0],height-pos[1])
        return new_pos
    
    def decode(self,data_string=""):
        #this function can decode the information that was sent by the server into the games actions:
        splitted = data_string.split(":")
        action_name = splitted[0]
        action_info_string = splitted[1]
        action_info_list = action_info_string.split(",")
        print(action_info_list,action_name)
        if action_name == "create":
            self.shown_cards[action_info_list[0]] = Rectangle((245*0.65,324*0.65),self.transform_the_position((width-300,height-400)),(0,0,0),action_info_list[1],cards_full_name=action_info_list[2])
            self.flip_card(action_info_list[0])
        self.your_turn = "True"

    def main_loop(self):
        players_count = 0
        selected_card = False
        while self.running:
            #turn managing
            if self.your_turn == "False":
                answ = server.send_and_listen("req:actio")
                if not answ == "False":
                    l_answ = list(answ)
                    del l_answ[0],l_answ[-1]
                    answ = ""
                    for b in l_answ:
                        answ += b
                    l_answ = list(answ)
                    del l_answ[0],l_answ[-1]
                    answ = ""
                    for b in l_answ:
                        answ += b
                    self.decode(answ)

            if players_count <= 1:
                players_count = self.server.send_and_listen("req peer online")
                players_count = int(players_count)

            if players_count >= 2 and self.your_turn == None:
                self.deck_opponent_rect.is_updating = True
                mt = self.server.send_and_listen("req clients turn")
                self.your_turn = mt
                print(self.your_turn)


            screen.fill((100,100,125))
            #update things
            self.deck_rect.update(screen)
            self.deck_opponent_rect.update(screen)
            if self.your_turn == "True":
                self.your_turn_rect.fill_rect_with_color((0,255,0))
            if self.your_turn == "False":
                self.your_turn_rect.fill_rect_with_color((255,0,0))

            #moving the selected card:
            if selected_card != False:
                m_pos = pygame.mouse.get_pos()
                self.shown_cards[selected_card].set_position(m_pos[0],m_pos[1])
                if self.shown_cards[selected_card].get_point_collide((width-10,height-10)):
                    self.shown_cards[selected_card].kill()
                    #the defeated card must be updated:
                    self.defeated_cards.append(self.shown_cards[selected_card].cardsfn)
                    #how to get the exact name of the card print(self.shown_cards[selected_card].cardsfn)

            self.your_turn_rect.update(screen)
            listed_s_c = list(self.shown_cards)
            for card in listed_s_c:
                self.shown_cards[card].update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if self.deck_rect.get_point_collide(pygame.mouse.get_pos()):
                            self.draw_card()
                    if event.key == pygame.K_s:
                        self.shuffle_deck()
                    if event.key == pygame.K_ESCAPE:
                        self.server.send("break")
                    if event.key == pygame.K_z:
                        if selected_card != False:
                            listed_s_c = list(self.shown_cards)
                            self.shown_cards[listed_s_c[-1]], self.shown_cards[selected_card] = self.shown_cards[selected_card],self.shown_cards[listed_s_c[-1]]
                            listed_s_c = list(self.shown_cards)
                            selected_card = listed_s_c[-1]
                            if self.shown_cards[selected_card].size == (245*0.65,324*0.65):
                                self.shown_cards[selected_card] = Rectangle((245*1.1,324*1.1),(width-300,height-400),(0,0,0),self.shown_cards[selected_card].unloaded_image,cards_full_name=self.shown_cards[selected_card].cardsfn)
                            else:
                                self.shown_cards[selected_card] = Rectangle((245*0.65,324*0.65),(width-300,height-400),(0,0,0),self.shown_cards[selected_card].unloaded_image,cards_full_name=self.shown_cards[selected_card].cardsfn)
                    if event.key == pygame.K_RIGHT:
                        if selected_card != False:
                            self.shown_cards[selected_card].change_rotation(-90)
                    if event.key == pygame.K_LEFT:
                        if selected_card != False:
                            self.shown_cards[selected_card].change_rotation(90)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        listed_s_c = list(self.shown_cards)
                        for card in listed_s_c:
                            if self.shown_cards[card].get_point_collide(pygame.mouse.get_pos()):
                                self.flip_card(card)

                    if event.button == 1:
                        listed_s_c = list(self.shown_cards)
                        pre_sel = selected_card
                        if selected_card != False:
                            selected_card = False
                        #complicated way of handling selecting and unselecting cards
                        for card in listed_s_c:
                            if self.shown_cards[card].get_point_collide(pygame.mouse.get_pos()):
                                    if selected_card == False and not pre_sel == card:
                                        selected_card = card
                        if self.your_turn_rect.get_point_collide(pygame.mouse.get_pos()) and self.your_turn == "True":
                            server.send(f"actio;{self.actions}")
                            self.your_turn = "False"

            pygame.display.update()

server = server_manager()
my_game = game(action,own_cards_dict,server)
my_game.main_loop()       