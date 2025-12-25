import pygame
import queue

class TFTPVisualizer:
    def __init__(self, animation_queue):
        pygame.init()
        self.animation_queue = animation_queue
        self.screen = pygame.display.set_mode((800, 450))
        pygame.display.set_caption("Client-Proxy-Server Analyzer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 14, bold=True)
        self.nodes = {"Client": (150, 225), "Proxy": (400, 225), "Server": (650, 225)}
        self.packets = []

    def draw_ui(self):
        self.screen.fill((25, 25, 35))
        pygame.draw.line(self.screen, (60, 60, 80), self.nodes["Client"], self.nodes["Server"], 3)
        for name, pos in self.nodes.items():
            color = (0, 180, 255) if name == "Proxy" else (200, 200, 200)
            pygame.draw.circle(self.screen, color, pos, 30)
            label = self.font.render(name, True, (255, 255, 255))
            self.screen.blit(label, (pos[0]-25, pos[1]+40))

    def update_packets(self):
        for p in self.packets[:]:
            dx = p["target"][0] - p["pos"][0]
            dy = p["target"][1] - p["pos"][1]
            dist = (dx**2 + dy**2)**0.5
            if dist < 5:
                self.packets.remove(p)
            else:
                movement_speed = 6
                p["pos"][0] += (dx/dist) * movement_speed
                p["pos"][1] += (dy/dist) * movement_speed
                pygame.draw.rect(self.screen, p["color"], (p["pos"][0]-10, p["pos"][1]-8, 20, 16))
                txt = self.font.render(p["label"], True, (255, 255, 255))
                self.screen.blit(txt, (p["pos"][0]-15, p["pos"][1]-30))

    def run(self):
        running = True
        while running:
            self.draw_ui()
            try:
                while not self.animation_queue.empty():
                    cmd = self.animation_queue.get_nowait()
                    self.packets.append({
                        "pos": list(self.nodes[cmd['f']]),
                        "target": self.nodes[cmd['t']],
                        "label": cmd['l'],
                        "color": cmd['c']
                    })
            except: pass
            self.update_packets()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
            pygame.display.flip()
            # SLOW MOTION: Frame rate lowered to 15 FPS
            self.clock.tick(60)
        pygame.quit()