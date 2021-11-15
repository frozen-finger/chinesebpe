from PIL import Image
import pygame
import os

with open('Data/sgns.target.word-character.char1-1.dynwin5.thr10.neg5.dim300.iter5', encoding='utf-8') as f:
    lines = f.readlines()

dict = {}
for line in lines[60000:]:
    line = line.split(' ')
    char = line[0]
    char = char.strip('\n').strip(' ')
    if all('\u4e00' <= i <= '\u9fff' for i in char):
        for j in char:
            dict[j] = 1

def paste(text,font,area = (16, 16)):
    im = Image.new("RGB", (128, 128), (255, 255, 255))
    rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))
    path = "Data/xihei/"+text+".png"
    pathimage = "Data/xihei/"+text+".png"
    pygame.image.save(rtext, path)
    line = Image.open(path)
    im.paste(line, area)
    #im.show()
    im.save(pathimage)

def pasteWord(word):
    pygame.init()
    font = pygame.font.SysFont('华文细黑', size=96)
    text = word.encode('utf-8').decode('utf-8')
    paste(text, font)

for i in dict:
    if i[0] != ' ':
        pasteWord(i[0])


