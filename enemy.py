import pygame
import math
import os
from settings import PATH, PATH2, RED, GREEN

pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))


class Enemy:
    def __init__(self):
        self.width = 40  
        self.height = 50  
        self.image = pygame.transform.scale(ENEMY_IMAGE, (self.width, self.height))
        self.health = 5
        self.max_health = 10
        self.path = PATH
        self.path_index = 0
        self.move_count = 0
        self.stride = 1
        self.x, self.y = self.path[0]  # path中第一個座標

    def draw(self, win):
        # draw enemy
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        # draw enemy health bar
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        Draw health bar on an enemy
        :param win: window
        :return: None
        """
        pygame.draw.rect(win, RED, [(self.x - 15), (self.y - 30), (self.max_health * 3), 4])
        pygame.draw.rect(win, GREEN, [(self.x - 15), (self.y - 30), (self.health * 3), 4])

    def move(self):
        """
        Enemy move toward path points every frame
        :return: None
        """
        now_x, now_y = self.path[self.path_index]  # x,y初始位置
        next_x, next_y = self.path[self.path_index + 1]  # x,y目標位置
        distance = math.sqrt((now_x - next_x)**2 + (now_y - next_y)**2)  #兩點之間距離
        max_count = int(distance / self.stride)  #兩點之間需要的步數
        if self.move_count < max_count:
            unitvector_x = (next_x - now_x) / distance  # x方向單位向量
            unitvector_y = (next_y - now_y) / distance  # y方向單位向量
            delta_x = unitvector_x * self.stride
            delta_y = unitvector_y * self.stride
            
            # 更新 x,y軸座標和 move_count
            self.x += delta_x
            self.y += delta_y 
            self.move_count += 1 
        else:
            self.path_index += 1  #下一個位置
            self.move_count = 0  # move_count重置


class EnemyGroup:
    def __init__(self):
        self.campaign_count = 0
        self.campaign_max_count = 120   # (unit: frame)
        self.reserved_members = []
        self.expedition = [Enemy()]  # don't change this line until you do the EX.3 

    def campaign(self):
        """
        Send an enemy to go on an expedition once 120 frame
        :return: None
        """
        # Hint: self.expedition.append(self.reserved_members.pop())
        if self.campaign_count >= self.campaign_max_count and not self.is_empty():
            self.expedition.append(self.reserved_members.pop())
            self.campaign_count = 0         # reset
        else:
            self.campaign_count += 1

        

    def generate(self, num):
        """
        Generate the enemies in this wave
        :param num: enemy number
        :return: None
        """
        for i in range(num):
            self.reserved_members.append(Enemy())

    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True

    def retreat(self, enemy):
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)





