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

deck_info_own = ""
files = os.listdir()
for file in files:
    if "Deck_info_" in file and "opponent" not in file:
        deck_info_own = file

file = open(deck_info_own, "r")
card_dict,content = file.readline().split("=")

deck_info_own = content
test_dic = {}
x = deck_info_own.split(",")
x[0] = list(x[0])
print(x[0])
del x[0][0]
print(x[0])
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

action = actions()