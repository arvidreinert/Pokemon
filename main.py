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
    def __init__(self):
        self.my_cards = {}
        #print(self.my_cards,type(self.my_cards))

                

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
v = {'arvid_charzard_deck0.png': '3', 'arvid_charzard_deck1.png': '1', 'arvid_charzard_deck10.png': '1', 'arvid_charzard_deck11.png': '2', 'arvid_charzard_deck12.png': '4', 'arvid_charzard_deck13.png': '2', 'arvid_charzard_deck14.png': '1', 'arvid_charzard_deck15.png': '1', 'arvid_charzard_deck16.png': '1', 'arvid_charzard_deck17.png': '3', 'arvid_charzard_deck18.png': '2', 'arvid_charzard_deck19.png': '3', 'arvid_charzard_deck2.png': '1', 'arvid_charzard_deck20.png': '4', 'arvid_charzard_deck21.png': '1', 'arvid_charzard_deck22.png': '10', 'arvid_charzard_deck23.png': '1', 'arvid_charzard_deck24.png': '1', 'arvid_charzard_deck25.png': '1', 'arvid_charzard_deck3.png': '4', 'arvid_charzard_deck4.png': '1', 'arvid_charzard_deck5.png': '2', 'arvid_charzard_deck6.png': '3', 'arvid_charzard_deck7.png': '1', 'arvid_charzard_deck8.png': '4', 'arvid_charzard_deck9.png': '2'}
print(own_cards_dict==v)
action = actions()