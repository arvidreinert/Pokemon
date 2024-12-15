import os
images = os.listdir()
imgs = []
#sorting images:
for im in images:
    if "png" in im and not "back_oc" in im:
        imgs.append(im)

counter = 0
for im in imgs:
    name = "arvid_charzard_deck"
    os.rename(im,f"{name}{counter}.png")
    counter += 1