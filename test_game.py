import pytest
import pygame
from game import Game
from players import Player
from meteorite import Meteorite

# Inicializa Pygame
@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def game():
    return Game()

@pytest.fixture
def player():
    return Player()

@pytest.fixture
def meteorite():
    return Meteorite()

def test_player_initial_position(player):
    assert player.rect.bottom == 600 #Verfica que el cohete inicie en la posicion baja del mapa
    assert player.rect.x>0 and player.rect.x<=800 #Verifica si la posicion inicial de la nave se encuentra dentro de los limites
    assert player.rect.y>0 and player.rect.y<=800

def test_player_movement(player):
    initial_x = player.rect.x
    player.move(5, 0)  # Mover a la derecha
    assert player.rect.x == initial_x + 5

    player.move(-10, 0)  # Mover a la izquierda
    assert player.rect.x == initial_x - 5  # Debería estar dentro de los límites

    player.move(-800, 0)  # Intentar moverse más allá de la izquierda
    assert player.rect.left == 0

    player.move(810, 0)  # Intentar moverse más allá de la derecha
    assert player.rect.right == 800

def test_meteorite_initial_position(meteorite):
    assert meteorite.rect.x >= 0 and meteorite.rect.x <= 800 #Verifica que la posicion inicial de cada meteorito en la posicion x este dentro de los limites de la interfaz
    assert meteorite.rect.y >= -100 and meteorite.rect.y <= -40 #Verifique que la creacion de los meteoritos sea unos cuantos pixeles antes del inicio de la interfaz, para asi simular la caida de estos

def test_meteorite_update(meteorite): #Verifica que en cada actualizacion el meteorito se mueve en la direccion 'y' un valor igual a meteorite.speed
    initial_y = meteorite.rect.y
    meteorite.update()
    assert meteorite.rect.y == initial_y + meteorite.speed

def test_meteorite_reset_position(meteorite): #Verificar que cuando un meteorito se salga de la pantalla, esta resetee su posicion
    meteorite.rect.y = 700  # Simular que el meteorito ha salido de la pantalla
    meteorite.reset_position()
    assert meteorite.rect.y >= -100 and meteorite.rect.y <= -40
    assert meteorite.rect.x >= 0 and meteorite.rect.x <= 800

def test_collision(player, meteorite):
    meteorite.rect.x = player.rect.x
    meteorite.rect.y = player.rect.y
    assert meteorite.check_collision(player) is True

    meteorite.rect.y = -50  # Cambiamos la posición para no colisionar
    assert meteorite.check_collision(player) is False
