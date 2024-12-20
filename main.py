from setup import *
from rectangle import *
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
    def __init__(self,action_class,own_dict):
        self.action = action_class
        self.running = True
        self.my_cards = action.make_list_from_card_dic(own_dict)
        self.cards_in_deck = self.my_cards
        self.deck_rect = Rectangle((245*0.75,324*0.75),(width-100,height-150),(0,0,0),"back_oc.png")
        self.shown_cards = []

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
        self.shown_cards.append(Rectangle((245*0.75,324*0.75),(width-300,height-150),(0,0,0),self.get_image_without_number(self.cards_in_deck[0])))
        del self.cards_in_deck[0]

    def main_loop(self):
        while self.running:
            screen.fill((100,100,125))
            #update things
            self.deck_rect.update(screen)
            for card in self.shown_cards:
                card.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if self.deck_rect.get_point_collide(pygame.mouse.get_pos()):
                            self.draw_card()
                    if event.key == pygame.K_s:
                        self.shuffle_deck()
                        

            pygame.display.update()

my_game = game(action,own_cards_dict)
my_game.main_loop()       