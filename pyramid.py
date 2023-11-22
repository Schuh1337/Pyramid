import pygame, sys, math
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pyramid")
background_color = (30, 30, 30)
line_color = (0, 0, 0)
fill_color = (255, 255, 255)
slider_color = (100, 100, 100)
slider_ball_color = (0, 255, 0)
light_direction = (-1, -1, -1)
light_color = (255, 255, 255)
vertices = [
    (0, -2, 0),
    (-2, 2, -2),
    (2, 2, -2),
    (2, 2, 2),
    (-2, 2, 2)]
faces = [
    (0, 1, 2),
    (0, 2, 3),
    (0, 3, 4),
    (0, 4, 1),
    (1, 2, 3, 4)]
edges = [
    (0, 1), (0, 2), (0, 3), (0, 4),
    (1, 2), (2, 3), (3, 4), (4, 1)]
slider_width = 200
slider_height = 10
slider_x = 20
horizontal_slider_y = height - 90
vertical_slider_y = height - 50
slider_ball_radius = 8
clock = pygame.time.Clock()
horizontal_angle = 0
vertical_angle = 0
horizontal_rotation_speed = 0.01
vertical_rotation_speed = 0.005
is_dragging_horizontal = False
is_dragging_vertical = False
is_dragging_zoom = False
font = pygame.font.Font(None, 24)
face_colors = [
    (255, 0, 0, 0),
    (0, 255, 0, 0),
    (0, 0, 255, 0),
    (255, 255, 0, 0),
    (255, 0, 255, 0)]
zoom_slider_width = 10
zoom_slider_height = 150
zoom_slider_x = width - 30
zoom_slider_y = height - zoom_slider_height - 20
zoom_min = 0.5
zoom_max = 2.0
zoom_level = 1.0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(slider_x, horizontal_slider_y, slider_width, slider_height).collidepoint(event.pos):
                is_dragging_horizontal = True
            if pygame.Rect(slider_x, vertical_slider_y, slider_width, slider_height).collidepoint(event.pos):
                is_dragging_vertical = True
            if pygame.Rect(zoom_slider_x, zoom_slider_y, zoom_slider_width, zoom_slider_height).collidepoint(event.pos):
                is_dragging_zoom = True
        elif event.type == pygame.MOUSEBUTTONUP:
            is_dragging_horizontal = False
            is_dragging_vertical = False
            is_dragging_zoom = False
        elif event.type == pygame.MOUSEMOTION:
            if is_dragging_horizontal:
                normalized_x = max(0, min(1, (event.pos[0] - slider_x) / slider_width))
                horizontal_rotation_speed = normalized_x * 0.02
            if is_dragging_vertical:
                normalized_x = max(0, min(1, (event.pos[0] - slider_x) / slider_width))
                vertical_rotation_speed = normalized_x * 0.01
            if is_dragging_zoom:
                normalized_y = max(0, min(1, (event.pos[1] - zoom_slider_y) / zoom_slider_height))
                zoom_level = zoom_min + (zoom_max - zoom_min) * normalized_y
    screen.fill(background_color)
    rotated_vertices = []
    for vertex in vertices:
        x, y, z = vertex
        new_x = x * math.cos(horizontal_angle) - z * math.sin(horizontal_angle)
        new_z = x * math.sin(horizontal_angle) + z * math.cos(horizontal_angle)
        rotated_vertices.append((new_x, y, new_z))
    final_rotated_vertices = []
    for vertex in rotated_vertices:
        x, y, z = vertex
        new_y = y * math.cos(vertical_angle) - z * math.sin(vertical_angle)
        new_z = y * math.sin(vertical_angle) + z * math.cos(vertical_angle)
        final_rotated_vertices.append((x, new_y, new_z))
    projected_vertices = []
    for vertex in final_rotated_vertices:
        x, y, z = vertex
        f = (200 / (z + 4)) * zoom_level
        projected_x = int(x * f + width / 2)
        projected_y = int(-y * f + height / 2)
        projected_vertices.append((projected_x, projected_y))
    for i, face in enumerate(faces):
        vertices_3d = [final_rotated_vertices[vertex_index] for vertex_index in face]
        edge1 = (vertices_3d[1][0] - vertices_3d[0][0], vertices_3d[1][1] - vertices_3d[0][1], vertices_3d[1][2] - vertices_3d[0][2])
        edge2 = (vertices_3d[2][0] - vertices_3d[0][0], vertices_3d[2][1] - vertices_3d[0][1], vertices_3d[2][2] - vertices_3d[0][2])
        normal = (
            edge1[1] * edge2[2] - edge1[2] * edge2[1],
            edge1[2] * edge2[0] - edge1[0] * edge2[2],
            edge1[0] * edge2[1] - edge1[1] * edge2[0])
        length = math.sqrt(normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2)
        normal = (normal[0] / length, normal[1] / length, normal[2] / length)
        dot_product = normal[0] * light_direction[0] + normal[1] * light_direction[1] + normal[2] * light_direction[2]
        intensity = max(0, dot_product)
        shaded_color = (
            min(face_colors[i][0] + intensity * light_color[0], 255),
            min(face_colors[i][1] + intensity * light_color[1], 255),
            min(face_colors[i][2] + intensity * light_color[2], 255),
            face_colors[i][3])
        pygame.draw.polygon(screen, shaded_color, [projected_vertices[vertex_index] for vertex_index in face])
    for edge in edges:
        pygame.draw.line(screen, line_color, projected_vertices[edge[0]], projected_vertices[edge[1]])
    pygame.draw.rect(screen, slider_color, pygame.Rect(slider_x, horizontal_slider_y, slider_width, slider_height))
    pygame.draw.rect(screen, slider_color, pygame.Rect(slider_x, vertical_slider_y, slider_width, slider_height))
    horizontal_ball_x = slider_x + int(horizontal_rotation_speed / 0.02 * slider_width)
    vertical_ball_x = slider_x + int(vertical_rotation_speed / 0.01 * slider_width)
    pygame.draw.circle(screen, slider_ball_color, (horizontal_ball_x, horizontal_slider_y + slider_height // 2), slider_ball_radius)
    pygame.draw.circle(screen, slider_ball_color, (vertical_ball_x, vertical_slider_y + slider_height // 2), slider_ball_radius)
    horizontal_label = font.render("Horizontal Speed", True, (255, 255, 255))
    vertical_label = font.render("Vertical Speed", True, (255, 255, 255))
    screen.blit(horizontal_label, (slider_x, horizontal_slider_y - 30))
    screen.blit(vertical_label, (slider_x, vertical_slider_y - 30))
    pygame.draw.rect(screen, slider_color, pygame.Rect(zoom_slider_x, zoom_slider_y, zoom_slider_width, zoom_slider_height))
    zoom_ball_y = zoom_slider_y + int((zoom_level - zoom_min) / (zoom_max - zoom_min) * zoom_slider_height)
    pygame.draw.circle(screen, slider_ball_color, (zoom_slider_x + zoom_slider_width // 2, zoom_ball_y), slider_ball_radius)
    zoom_label = font.render("Zoom", True, (255, 255, 255))
    screen.blit(zoom_label, (zoom_slider_x - 60, zoom_slider_y - 20))
    pygame.display.flip()
    horizontal_angle += horizontal_rotation_speed
    vertical_angle += vertical_rotation_speed
    clock.tick(60)
pygame.quit()
sys.exit()
