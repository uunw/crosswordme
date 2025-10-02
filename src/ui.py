import pygame

class Button:
    """Create a button, define its properties."""
    def __init__(self, x, y, width, height, text, color, hover_color, click_color=(200, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.click_color = click_color
        self.is_hovered = False
        self.is_clicked_state = False

    def draw(self, screen, font):
        """Draw the button on the screen."""
        current_color = self.color
        if self.is_clicked_state:
            current_color = self.click_color
        elif self.is_hovered:
            current_color = self.hover_color
        
        pygame.draw.rect(screen, current_color, self.rect)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        """Check if the mouse is hovering over the button."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        """Check if the button is clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            self.is_clicked_state = True
            return True
        if event.type == pygame.MOUSEBUTTONUP:
            self.is_clicked_state = False
        return False

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (200, 200, 200)
        self.error_color = (255, 0, 0)
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.is_error = False
        self.error_timer = 0
        self.error_duration = 30  # frames

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, (0,0,0))
        return None

    def trigger_error(self):
        self.is_error = True
        self.error_timer = self.error_duration

    def update(self):
        # Blinking cursor
        self.cursor_timer += 1
        if self.cursor_timer >= 60: # Blink every 60 frames
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible
        
        # Error timer
        if self.is_error:
            self.error_timer -= 1
            if self.error_timer <= 0:
                self.is_error = False

    def draw(self, screen):
        border_color = self.error_color if self.is_error else self.color
        pygame.draw.rect(screen, border_color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        if self.active and self.cursor_visible:
            cursor_pos = self.rect.x + 5 + self.txt_surface.get_width()
            pygame.draw.line(screen, (0,0,0), (cursor_pos, self.rect.y + 5), (cursor_pos, self.rect.y + self.rect.height - 5))