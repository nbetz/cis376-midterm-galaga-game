import argparse

import engine
import scene

if __name__ == '__main__':
    # setup command line arguments to accept input for width, height, fps,
    parser = argparse.ArgumentParser()
    parser.add_argument('--fps', nargs='?', type=int, default=10,
                        help='Specify the fps for the game')
    parser.add_argument('--tile_size', nargs='?', type=int, default=30,
                        help='Specify the size of the tiles for the game')
    parser.add_argument('--width', nargs='?', type=int, default=720,
                        help='Specify the width of the screen')
    parser.add_argument('--height', nargs='?', type=int, default=480,
                        help='Specify the height of the screen')
    args = parser.parse_args()

    # grab the arguments and store them in variables
    fps = args.fps
    tile = args.tile_size
    width = args.width
    height = args.height

    # create the engine and scene
    e = engine.Engine(game_fps=fps, screen_width=width, screen_height=height)
    game_scene = scene.MazeScene(tile_size=tile)

    # set the active scene to the game_scene we created, and start the engine loop
    e.add_scene(game_scene)
    e.set_active_scene(game_scene)
    e.loop()
