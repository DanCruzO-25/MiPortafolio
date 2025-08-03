import pygame
import random
import math

# === CONFIGURACIÓN GENERAL ===
_ANCHO = 1000
_ALTO = 700
_LIVESPLAYER = 3
enemigos = 7
_LEVEL = 0

# === INICIALIZACIÓN ===
pygame.init()
window = pygame.display.set_mode((_ANCHO, _ALTO))
pygame.display.set_caption("Space Shooter")

# === CARGA Y ESCALADO DE IMÁGENES ===
backgroundImage = pygame.transform.scale(pygame.image.load("background.jpg"), (_ANCHO, _ALTO))
shipImage = pygame.transform.scale(pygame.image.load("ship.png"), (48, 48))
enemyImage = pygame.transform.scale(pygame.image.load("enemy.webp"), (40, 40))
loseImage = pygame.transform.scale(pygame.image.load("lose.jpg"), (_ANCHO, _ALTO))
bala = pygame.transform.scale(pygame.image.load("bullet.png"), (4, 12))

# === NAVE ===
ship = {
    "pos": [_ANCHO // 2, _ALTO - 60],
    "tamaño": list(shipImage.get_size()),
    "vel": 5,
    "cooldown": 15,
    "firewait": 0,
    "respawncooldown": 180,
    "respawnwait": 0,
    "lives": _LIVESPLAYER,
    "image": shipImage
}

def shipDraw(window, ship):
    x = ship["pos"][0] - ship["tamaño"][0] // 2
    y = ship["pos"][1] - ship["tamaño"][1] // 2
    window.blit(ship["image"], (x, y))

def shipMoveRight(ship):
    if ship["respawnwait"] == 0:
        ship["pos"][0] = min(ship["pos"][0] + ship["vel"], _ANCHO - ship["tamaño"][0] // 2)

def shipMoveLeft(ship):
    if ship["respawnwait"] == 0:
        ship["pos"][0] = max(ship["pos"][0] - ship["vel"], ship["tamaño"][0] // 2)

def shipFire(ship):
    if ship["firewait"] <= 0 and ship["respawnwait"] == 0:
        bullet = {
            "pos": [ship["pos"][0], ship["pos"][1] - ship["tamaño"][1] // 2],
            "vel": -20,
            "color": bala,
            "radio": 2
        }
        bullets.append(bullet)
        ship["firewait"] = ship["cooldown"]

def shipUpdate(ship):
    ship["firewait"] -= 1
    if ship["respawnwait"] > 0:
        ship["pos"][0] = -100
        ship["respawnwait"] -= 1
        if ship["respawnwait"] == 0:
            ship["pos"][0] = _ANCHO // 2

def shipDeath(ship):
    ship["lives"] -= 1
    ship["respawnwait"] = ship["respawncooldown"]

# === BALAS ===
bullets = []
enemyBullets = []

def bulletUpdate(bullet):
    bullet["pos"][1] += bullet["vel"]

def bulletDraw(window, bullet):
    window.blit(bala, bullet["pos"])

def bulletsDraw(window, bullets):
    for b in bullets:
        bulletDraw(window, b)

def bulletsUpdate(bullets):
    for b in bullets[:]:
        if b["pos"][1] < 0 or b["pos"][1] > _ALTO:
            bullets.remove(b)
        else:
            bulletUpdate(b)

# === ENEMIGOS ===
enemies = []

def enemyCreate(pos, w, h):
    enemy = {
        "pos": pos[:],
        "tamaño": [w, h],
        "vel": random.choice([3, -3]),
        "dirchangeprob": 2,
        "time": random.uniform(0, math.pi * 2),
        "timeinc": 0.05,
        "firerate": 120,
        "firewait": random.randint(60, 120),
        "image": enemyImage
    }
    enemies.append(enemy)

def enemiesCreate(n):
    for _ in range(n):
        pos = [random.randint(40, _ANCHO - 40), random.randint(40, _ALTO // 2)]
        enemyCreate(pos, 40, 40)

def enemyDraw(window, enemy):
    x = enemy["pos"][0] - enemy["tamaño"][0] // 2
    y = enemy["pos"][1] - enemy["tamaño"][1] // 2
    window.blit(enemy["image"], (x, y))

def enemiesDraw(window, enemies):
    for e in enemies:
        enemyDraw(window, e)

def enemyUpdate(enemy):
    if enemy["pos"][0] <= enemy["tamaño"][0] // 2 or enemy["pos"][0] >= _ANCHO - enemy["tamaño"][0] // 2:
        enemy["vel"] *= -1
    if random.randrange(100) < enemy["dirchangeprob"]:
        enemy["vel"] *= -1

    enemy["pos"][0] += enemy["vel"]
    enemy["pos"][1] = max(enemy["tamaño"][1] // 2, enemy["pos"][1] + math.sin(enemy["time"]))
    enemy["time"] += enemy["timeinc"]

    if enemy["firewait"] <= 0:
        enemyFire(enemy)
        enemy["firewait"] = enemy["firerate"]
    else:
        enemy["firewait"] -= 1

def enemiesUpdate(enemies):
    for e in enemies:
        enemyUpdate(e)

def enemyFire(enemy):
    bullet = {
        "pos": [enemy["pos"][0], enemy["pos"][1] + enemy["tamaño"][1] // 2],
        "vel": 5,
        "radio": 3,
        "color": (0, 255, 0)
    }
    enemyBullets.append(bullet)

# === COLISIONES ===
def enemyIsHit(obj, bullet):
    x1 = obj["pos"][0] - obj["tamaño"][0] // 2 + bullet["radio"]
    x2 = obj["pos"][0] + obj["tamaño"][0] // 2 + bullet["radio"]
    y1 = obj["pos"][1] - obj["tamaño"][1] // 2 + bullet["radio"]
    y2 = obj["pos"][1] + obj["tamaño"][1] // 2 + bullet["radio"]
    return x1 <= bullet["pos"][0] <= x2 and y1 <= bullet["pos"][1] <= y2

def checkEnemyCollisions(enemies, bullets):
    for e in enemies[:]:
        for b in bullets[:]:
            if enemyIsHit(e, b):
                enemies.remove(e)
                bullets.remove(b)

def checkShipCollisions(ship, enemyBullets):
    for b in enemyBullets[:]:
        if enemyIsHit(ship, b):
            enemyBullets.remove(b)
            shipDeath(ship)

# === MAIN LOOP ===
def main():
    global enemigos, enemies, _LEVEL
    clock = pygame.time.Clock()
    enemiesCreate(enemigos)
    paused = False

    loop = True
    while loop:
        clock.tick(60)  # 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused  # Alternar pausa

        keys = pygame.key.get_pressed()
        if not paused:
            if keys[pygame.K_LEFT]:
                shipMoveLeft(ship)
            if keys[pygame.K_RIGHT]:
                shipMoveRight(ship)
            if keys[pygame.K_SPACE]:
                shipFire(ship)

            if not enemies:
                _LEVEL += 1
                enemigos += 2
                enemiesCreate(enemigos)
                ship["lives"] = _LIVESPLAYER

            checkEnemyCollisions(enemies, bullets)
            checkShipCollisions(ship, enemyBullets)

            bulletsUpdate(bullets)
            bulletsUpdate(enemyBullets)

            shipUpdate(ship)
            enemiesUpdate(enemies)

        # Dibujado
        window.blit(backgroundImage, (0, 0))

        bulletsDraw(window, bullets)
        bulletsDraw(window, enemyBullets)

        if ship["lives"] > 0:
            shipDraw(window, ship)
            enemiesDraw(window, enemies)
        else:
            window.blit(loseImage, (0, 0))
            if keys[pygame.K_RETURN]:
                enemigos = max(7, enemigos - _LEVEL * 2)
                enemies.clear()
                enemiesCreate(enemigos)
                ship["lives"] = _LIVESPLAYER
                ship["respawnwait"] = 0
                ship["pos"] = [_ANCHO // 2, _ALTO - 60]

        # Texto de PAUSA
        if paused:
            font = pygame.font.SysFont(None, 72)
            pause_text = font.render("PAUSA", True, (255, 255, 255))
            rect = pause_text.get_rect(center=(_ANCHO // 2, _ALTO // 2))
            window.blit(pause_text, rect)

        pygame.display.update()

    pygame.quit()

main()
    
