import pygame
import random
import os
import json

# Inicialização
pygame.init()
pygame.mixer.init()

# Configurações da tela
LARGURA = 640
ALTURA = 480
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pong de 8 bits")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Raquetes
RAQUETE_LARGURA = 15
RAQUETE_ALTURA = 90
raquete_jogador1 = pygame.Rect(50, ALTURA // 2 - RAQUETE_ALTURA // 2, RAQUETE_LARGURA, RAQUETE_ALTURA)
raquete_jogador2 = pygame.Rect(LARGURA - 50 - RAQUETE_LARGURA, ALTURA // 2 - RAQUETE_ALTURA // 2, RAQUETE_LARGURA,
                               RAQUETE_ALTURA)

# Bola
QUADRADO_TAMANHO = 15
quadrado = pygame.Rect(LARGURA // 2 - QUADRADO_TAMANHO // 2, ALTURA // 2 - QUADRADO_TAMANHO // 2, QUADRADO_TAMANHO, QUADRADO_TAMANHO)
quadrado_dx = 7 * random.choice((1, -1))
quadrado_dy = 7 * random.choice((1, -1))

# Placar
placar_jogador1 = 0
placar_jogador2 = 0
PLACAR_MAXIMO = 11

# Fonte estilo retro
fonte = pygame.font.Font(os.path.join("fontes", "PressStart2P-Regular.ttf"), 16)
fonte_grande = pygame.font.Font(os.path.join("fontes", "PressStart2P-Regular.ttf"), 32)

# Sons
som_raquete = pygame.mixer.Sound(os.path.join("sons", "pong.mp3"))
som_ponto = pygame.mixer.Sound(os.path.join("sons", "score.mp3"))
som_menu = pygame.mixer.Sound(os.path.join("sons", "menu.mp3"))
som_gameover = pygame.mixer.Sound(os.path.join("sons", "gameover.mp3"))
som_win = pygame.mixer.Sound(os.path.join("sons", "win.mp3"))


# Estados do jogo
MENU = 0
JOGANDO = 1
GAME_OVER = 2
PAUSADO = 3
estado_jogo = MENU

# Modo de jogo
modo_um_jogador = True


def salvar_jogo():
    dados = {
        "placar_jogador1": placar_jogador1,
        "placar_jogador2": placar_jogador2,
        "raquete_jogador1_y": raquete_jogador1.y,
        "raquete_jogador2_y": raquete_jogador2.y,
        "quadrado_x": quadrado.x,
        "quadrado_y": quadrado.y,
        "quadrado_dx": quadrado_dx,
        "quadrado_dy": quadrado_dy,
        "modo_um_jogador": modo_um_jogador
    }
    with open("pong_save.json", "w") as arquivo:
        json.dump(dados, arquivo)


def carregar_jogo():
    global placar_jogador1, placar_jogador2, raquete_jogador1, raquete_jogador2, quadrado, quadrado_dx, quadrado_dy, modo_um_jogador
    try:
        with open("pong_save.json", "r") as arquivo:
            dados = json.load(arquivo)
        placar_jogador1 = dados["placar_jogador1"]
        placar_jogador2 = dados["placar_jogador2"]
        raquete_jogador1.y = dados["raquete_jogador1_y"]
        raquete_jogador2.y = dados["raquete_jogador2_y"]
        quadrado.x = dados["quadrado_x"]
        quadrado.y = dados["quadrado_y"]
        quadrado_dx = dados["quadrado_dx"]
        quadrado_dy = dados["quadrado_dy"]
        modo_um_jogador = dados["modo_um_jogador"]
        return True
    except FileNotFoundError:
        return False


def desenhar_menu():
    global quadrado_dx, quadrado_dy, quadrado_dx, quadrado_dy
    tela.fill(PRETO)
    titulo = fonte_grande.render("PONG", True, BRANCO)
    subtitulo1 = fonte.render("1 - Um Jogador", True, BRANCO)
    subtitulo2 = fonte.render("2 - Dois Jogadores", True, BRANCO)
    subtitulo3 = fonte.render("C - Continuar jogo salvo", True, BRANCO)
    subtitulo4 = fonte.render("Q - Sair", True, BRANCO)
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 2 - 150))
    tela.blit(subtitulo1, (LARGURA // 2 - subtitulo1.get_width() // 2, ALTURA // 2))
    tela.blit(subtitulo2, (LARGURA // 2 - subtitulo2.get_width() // 2, ALTURA // 2 + 50))
    tela.blit(subtitulo3, (LARGURA // 2 - subtitulo3.get_width() // 2, ALTURA // 2 + 100))
    tela.blit(subtitulo4, (LARGURA // 2 - subtitulo4.get_width() // 2, ALTURA // 2 + 150))

    # Animação da bola no menu
    pygame.draw.rect(tela, BRANCO, quadrado)
    quadrado.x += quadrado_dx
    quadrado.y += quadrado_dy
    if quadrado.left <= 0 or quadrado.right >= LARGURA:
        quadrado_dx *= -1
    if quadrado.top <= 0 or quadrado.bottom >= ALTURA:
        quadrado_dy *= -1


def desenhar_game_over():
    tela.fill(PRETO)
    if modo_um_jogador:
        if placar_jogador1 > placar_jogador2:
            mensagem = "VOCÊ VENCEU!"
            som_win.play()
        else:
            mensagem = "VOCÊ PERDEU!"
            som_gameover.play()

    else:
        if placar_jogador1 > placar_jogador2:
            mensagem = "JOGADOR 1 VENCEU!"
            som_win.play()
        else:
            mensagem = "JOGADOR 2 VENCEU!"
            som_win.play()

    texto_game_over = fonte_grande.render(mensagem, True, BRANCO)
    texto_reiniciar = fonte.render("ESPAÇO - Reiniciar", True, BRANCO)
    texto_menu = fonte.render("M - Menu principal", True, BRANCO)
    texto_sair = fonte.render("Q - Sair", True, BRANCO)

    tela.blit(texto_game_over, (LARGURA // 2 - texto_game_over.get_width() // 2, ALTURA // 2 - 100))
    tela.blit(texto_reiniciar, (LARGURA // 2 - texto_reiniciar.get_width() // 2, ALTURA // 2 + 50))
    tela.blit(texto_menu, (LARGURA // 2 - texto_menu.get_width() // 2, ALTURA // 2 + 100))
    tela.blit(texto_sair, (LARGURA // 2 - texto_sair.get_width() // 2, ALTURA // 2 + 150))


def desenhar_jogo_pausado():
    tela.fill(PRETO)
    texto_pausado = fonte_grande.render("JOGO PAUSADO", True, BRANCO)
    texto_continuar = fonte.render("ESPAÇO - Continuar", True, BRANCO)
    texto_salvar = fonte.render("S - Salvar e sair", True, BRANCO)
    texto_menu = fonte.render("M - Menu principal", True, BRANCO)

    tela.blit(texto_pausado, (LARGURA // 2 - texto_pausado.get_width() // 2, ALTURA // 2 - 100))
    tela.blit(texto_continuar, (LARGURA // 2 - texto_continuar.get_width() // 2, ALTURA // 2 + 50))
    tela.blit(texto_salvar, (LARGURA // 2 - texto_salvar.get_width() // 2, ALTURA // 2 + 100))
    tela.blit(texto_menu, (LARGURA // 2 - texto_menu.get_width() // 2, ALTURA // 2 + 150))


def reiniciar_jogo():
    global placar_jogador1, placar_jogador2, quadrado, quadrado_dx, quadrado_dy
    placar_jogador1 = 0
    placar_jogador2 = 0
    quadrado.center = (LARGURA // 2, ALTURA // 2)
    quadrado_dx = 7 * random.choice((1, -1))
    quadrado_dy = 7 * random.choice((1, -1))
    raquete_jogador1.centery = ALTURA // 2
    raquete_jogador2.centery = ALTURA // 2


# Loop principal do jogo
rodando = True
clock = pygame.time.Clock()

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if estado_jogo == MENU:
                if evento.key == pygame.K_1:
                    modo_um_jogador = True
                    estado_jogo = JOGANDO
                    reiniciar_jogo()
                elif evento.key == pygame.K_2:
                    modo_um_jogador = False
                    estado_jogo = JOGANDO
                    reiniciar_jogo()
                elif evento.key == pygame.K_c:
                    if carregar_jogo():
                        estado_jogo = JOGANDO
                    else:
                        print("Nenhum jogo salvo encontrado.")
                elif evento.key == pygame.K_q:
                    rodando = False
            elif estado_jogo == JOGANDO:
                if evento.key == pygame.K_ESCAPE:
                    estado_jogo = PAUSADO
            elif estado_jogo == GAME_OVER:
                if evento.key == pygame.K_SPACE:
                    estado_jogo = JOGANDO
                    reiniciar_jogo()
                elif evento.key == pygame.K_m:
                    estado_jogo = MENU
                elif evento.key == pygame.K_q:
                    rodando = False
            elif estado_jogo == PAUSADO:
                if evento.key == pygame.K_SPACE:
                    estado_jogo = JOGANDO
                elif evento.key == pygame.K_s:
                    salvar_jogo()
                    rodando = False
                elif evento.key == pygame.K_m:
                    estado_jogo = MENU

    if estado_jogo == MENU:
        desenhar_menu()
        som_menu.play()

    elif estado_jogo == JOGANDO:
        # Movimento do jogador 1
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w] and raquete_jogador1.top > 0:
            raquete_jogador1.y -= 7
        if teclas[pygame.K_s] and raquete_jogador1.bottom < ALTURA:
            raquete_jogador1.y += 7

        # Movimento do jogador 2 ou CPU
        if modo_um_jogador:
            if raquete_jogador2.centery < quadrado.centery and raquete_jogador2.bottom < ALTURA:
                raquete_jogador2.y += 7
            elif raquete_jogador2.centery > quadrado.centery and raquete_jogador2.top > 0:
                raquete_jogador2.y -= 7
        else:
            if teclas[pygame.K_UP] and raquete_jogador2.top > 0:
                raquete_jogador2.y -= 7
            if teclas[pygame.K_DOWN] and raquete_jogador2.bottom < ALTURA:
                raquete_jogador2.y += 7

        # Movimento da bola
        quadrado.x += quadrado_dx
        quadrado.y += quadrado_dy

        # Colisão com as bordas
        if quadrado.top <= 0 or quadrado.bottom >= ALTURA:
            quadrado_dy *= -1
            som_raquete.play()

        # Colisão com as raquetes
        if quadrado.colliderect(raquete_jogador1) or quadrado.colliderect(raquete_jogador2):
            quadrado_dx *= -1
            som_raquete.play()

        # Pontuação
        if quadrado.left <= 0:
            placar_jogador2 += 1
            som_ponto.play()
            quadrado.center = (LARGURA // 2, ALTURA // 2)
            bola_dx = 7 * random.choice((1, -1))
            bola_dy = 7 * random.choice((1, -1))
        elif quadrado.right >= LARGURA:
            placar_jogador1 += 1
            som_ponto.play()
            quadrado.center = (LARGURA // 2, ALTURA // 2)
            bola_dx = 7 * random.choice((1, -1))
            bola_dy = 7 * random.choice((1, -1))

        # Verifica se alguém ganhou
        if placar_jogador1 >= PLACAR_MAXIMO or placar_jogador2 >= PLACAR_MAXIMO:
            estado_jogo = GAME_OVER
            som_gameover.play()

        # Desenho
        tela.fill(PRETO)
        pygame.draw.rect(tela, BRANCO, raquete_jogador1)
        pygame.draw.rect(tela, BRANCO, raquete_jogador2)
        pygame.draw.rect(tela, BRANCO, quadrado)
        pygame.draw.aaline(tela, BRANCO, (LARGURA // 2, 0), (LARGURA // 2, ALTURA))

        # Placar
        texto_placar = fonte.render(f"{placar_jogador1}   {placar_jogador2}", True, BRANCO)
        tela.blit(texto_placar, (LARGURA // 2 - texto_placar.get_width() // 2, 10))

    elif estado_jogo == GAME_OVER:
        desenhar_game_over()
    elif estado_jogo == PAUSADO:
        desenhar_jogo_pausado()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()