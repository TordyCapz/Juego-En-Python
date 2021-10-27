import pygame
from enemy import Enemy
from player import Player
from logic import check_collision, check_level
from game import Game   #importamos la clase Game del archivo game


#Inicializador
pygame.init()
clock = pygame.time.Clock()

#Pantalla del juego
screen_width = 800  #Ancho
screen_height = 600 #Alto
screen = pygame.display.set_mode((screen_width, screen_height)) 
carpincho = pygame.image.load("carpincho/izquierda/1.png") #Agrego imagen para la pantalla de game over
background = pygame.transform.scale(pygame.image.load("bg.png"), (screen_width, screen_height)) #Seteo el fondo, escalandolo al tamaño de la pantalla
pygame.display.set_caption("Carpinchometro") 

#Grupos de sprites
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

def main():
    #Parametros basicos
    FPS = 60    #Seteo la velocidad de fotogramas
    #Defino y añado el grupo de enemigos y jugador
    player = Player()
    player_group.add(player)
    enemy = Enemy()
    enemy_group.add(enemy)
    g = Game()  #creamos una variable para inicializar la clase Game

    #Fuentes
    main_font = pygame.font.SysFont("comicsans", 50)    #Fuente Principal
    lost_font = pygame.font.SysFont("comicsans", 60)    #Fuente de Muerte

    #Metodo para refrescar la pantalla
    def redraw_window():
        #Dibujo en pantalla
        screen.blit(background, (0,0))  #Background

        #Defino y dibujo las palabras en pantalla
        lives_label = main_font.render(f"Vidas: {player.lives}", 1, (255,255,255))
        level_label = main_font.render(f"Nivel: {player.level}", 1, (255,255,255))
        screen.blit(lives_label,(10,10)), screen.blit(level_label, (screen_width - lives_label.get_width() - 10, 10))

        #Agrego los enemigos
        enemy_group.update(0.15)
        enemy_group.draw(screen)
        
        #Agrego al jugador
        player_group.update(0.2, screen)
        player_group.draw(screen)

        #Refresco la pantalla
        pygame.display.update()

    def gameover_window():
        #Dibujo en pantalla
        screen.blit(background, (0,0)) #Fijo el fondo

        death_label = lost_font.render("No has podido evitar al carpincho",1,(30,30,30)) #Muestro mensaje de muerte
        score_label = lost_font.render(f"Has llegado al nivel: {player.level+1}",1,(30,30,30)) #Muestro hasta que nivel llego el jugador
        restart_label = lost_font.render("Toca cualquier flecha para reiniciar",1,(30,30,30)) #Muestro instrucciones para reinicio
        screen.blit(carpincho,(300,500))
        screen.blit(death_label,(50,screen_height // 2-100)), screen.blit(score_label,(180,screen_height//2-50)), screen.blit(restart_label,(30,screen_height//2))
        #Refresco la pantalla
        pygame.display.update()

    while g.running:
        clock.tick(FPS)
        g.curr_menu.display_menu()  #despliego el menu

        while g.playing:
            redraw_window()

            #Detecto cuando se presionan las teclas del jugador
            player.get_input()

            #Checkeo las colisiones
            check_collision(player, enemy_group)    #Le paso el jugador y el grupo de enemigos
            check_level(player, enemy_group)    #Compruebo cuando el jugador pasa la pantalla
            
            if(player.lives == 0): #Check si el jugador tiene 0 vidas, si es asi, el if con el juego no va ocurrir
                gameover_window() #Muestro la pantalla de game over
                if event.type == pygame.KEYDOWN: 
                    g.playing = False
                    player.lives = 2
                    player.level = 0
                    player.rect.x = (800 // 2) - 95 #Coloco al jugador en el centro de la pantalla
                    player.rect.y = 600 - 170
                    enemy_group.empty() #Elimino enemigos para evitar que el juego empieze con enemigos ya en el medio de la pantalla
                    new_enemy = Enemy()
                    enemy_group.add(new_enemy) #Agrego nuevos enemigos para que funcione todo correctamente

            #Detecto cuando se cierra la pantalla
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    g.running = False

            
main()