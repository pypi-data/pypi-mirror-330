import r3frame as frame
import random

world_size = [
    10_500,
    10_500,
]

clock = frame.app.resource.Clock()
events = frame.app.events.Event_Manager()
assets = frame.app.resource.Asset_Manager()
window = frame.app.resource.Window([800, 600], world_size)
camera = frame.app.resource.Camera(window)
renderer = frame.app.resource.Renderer(camera)

player = frame.objects.game.Game_Object(location=[100, 100], color=[0, 0, 255])

gridmap = frame.objects.gridmap.GridMap(50, 50, 32)
gridmap.cells = [
    frame.objects.game.Game_Object(
        location=[x * 32, y * 32], 
        color=[random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)]
    )
    for x in range(gridmap.width) for y in range(gridmap.height)
]

zoom_factor = 3

while not events.quit:
    clock.update()
    events.update()
    
    if events.key_pressed(frame.app.inputs.Keyboard.Escape): events.quit = 1

    if events.key_pressed(frame.app.inputs.Keyboard.F1): renderer.set_flag(renderer.FLAGS.SHOW_CAMERA)
    if events.key_pressed(frame.app.inputs.Keyboard.F2): renderer.rem_flag(renderer.FLAGS.SHOW_CAMERA)

    if events.key_held(frame.app.inputs.Keyboard.S):       player.set_velocity(vy=200)
    if events.key_held(frame.app.inputs.Keyboard.D):       player.set_velocity(vx=200)
    if events.key_held(frame.app.inputs.Keyboard.A):       player.set_velocity(vx=-200)
    if events.key_held(frame.app.inputs.Keyboard.W):       player.set_velocity(vy=-200)
    
    if events.key_held(frame.app.inputs.Keyboard.Down):    camera.set_velocity(vy=200)
    if events.key_held(frame.app.inputs.Keyboard.Right):   camera.set_velocity(vx=200)
    if events.key_held(frame.app.inputs.Keyboard.Left):    camera.set_velocity(vx=-200)
    if events.key_held(frame.app.inputs.Keyboard.Up):      camera.set_velocity(vy=-200)

    if events.mouse_held(frame.app.inputs.Mouse.LeftClick):
        mouse_location = frame.app.inputs.Mouse.get_location()
        gridmap.cells.append(frame.objects.game.Game_Object(
            location=[
                mouse_location[0] / camera.viewport_scale[0] + camera.location[0],
                mouse_location[1] / camera.viewport_scale[1] + camera.location[1],
            ], color=[random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)]
        ))

    if events.mouse_wheel_up:
        camera.mod_viewport(-zoom_factor)

    if events.mouse_wheel_down:
        camera.mod_viewport(zoom_factor)

    player.update(clock.delta)
    for tile in gridmap.cells:
        tile.update(clock.delta)

    camera.center_on(player.size, player.location)
    camera.update(clock.delta)
    
    [renderer.draw_call(obj.image, obj.location) for obj in [*gridmap.cells, player]]
    renderer.update()
           
    clock.rest()
