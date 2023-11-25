import subprocess
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Proyecto 3")

pygame.mixer.music.load("Christmas.mp3")
pygame.mixer.music.play(-1)



# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)

# Define the menu state
class Menu:
    def __init__(self):
        
        self.click_sound = pygame.mixer.Sound("Jingle.mp3")

        self.background_image = pygame.image.load("bg.png").convert()

        self.title_text = title_font.render("Proyecto 3", True, white)
        self.title_rect = self.title_text.get_rect(center=(width // 2, height // 4))

        self.start_button = pygame.Rect(width // 2 - 100, height // 2, 200, 50)
        self.start_text = font.render("Comenzar", True, white)
        self.start_rect = self.start_text.get_rect(center=self.start_button.center)
        
        self.info_button = pygame.Rect(width // 2 - 100, height - height // 3, 200, 50)
        self.info_text = font.render("Info", True, white)
        self.info_rect = self.info_text.get_rect(center=self.info_button.center)

    def draw(self):
        
        screen.blit(self.background_image, (0, 0))

        screen.blit(self.title_text, self.title_rect)
        pygame.draw.rect(screen, white, self.start_button, 2)
        screen.blit(self.start_text, self.start_rect)
        pygame.draw.rect(screen, white, self.info_button, 2)
        screen.blit(self.info_text, self.info_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if the Start button is clicked
            if self.start_button.collidepoint(event.pos):
                self.click_sound.play()
                return Main()
            if self.info_button.collidepoint(event.pos):
                self.click_sound.play()
                return Info()
        return self  # If no state change, return the current instance

class Info:
    def __init__(self):
        screen.fill(black)
        self.click_sound = pygame.mixer.Sound("Jingle.mp3")

        self.game_text = title_font.render("Creado por Renatto Guzmán", True, white)
        self.game_rect = self.game_text.get_rect(center=(width // 2, height // 2 - 10))

        self.desc_text =  font.render("Presiona 3 veces para regresar", True, white)
        self.desc_rect =  self.desc_text.get_rect(center=(width // 2, height // 2 + 50))
        
        self.click_count = 0

    def draw(self):
        screen.blit(self.game_text, self.game_rect)
        screen.blit(self.desc_text, self.desc_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.click_count += 1
            self.click_sound.play()
            if self.click_count == 3:
                return Menu()

        return self  # If no state change, return the current instance


class Main:
    def __init__(self):
        self.background_image = pygame.image.load("bg.png").convert()

        self.game_text = title_font.render("Proyecto 3", True, white)
        self.game_rect = self.game_text.get_rect(center=(width // 2, height // 2))

    def draw(self):        
        screen.blit(self.background_image, (0, 0))

        screen.blit(self.game_text, self.game_rect)

    def handle_event(self, event):
        script_path = "RendererGL.py"  # Replace with the actual path
        self.count = 0
        

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Transition back to the menu when the mouse is clicked
            if self.count == 0:
                subprocess.Popen(["python", script_path])
                self.count += 1
            
            return Menu()

        return self  # If no state change, return the current instance

# Set initial state to the menu
current_state = Menu()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle events in the current state
        current_state = current_state.handle_event(event)

    current_state.draw()

    pygame.display.flip()
    pygame.time.Clock().tick(30)
