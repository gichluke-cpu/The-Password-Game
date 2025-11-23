from tkinter import *
import pygame
root = Tk()
root.title=('musictest')
root.geometry=("500x400")
pygame.mixer.init()
def play():
    pygame.mixer.music.load("C:\WebScrapingLibrary_NeoM2\REDASH _ grass stage [GODDESS OF VICTORY_ NIKKE OST].mp3")
        #pygame.mixer.music.set_volume(0.7) # Đặt âm lượng (0.0 đến 1.0)
    pygame.mixer.music.play(loops=-1)  # loops=-1 nghĩa là lặp lại vô hạn
myb = Button(root, text='play',command=play)
myb.pack(pady=20)
root.mainloop()