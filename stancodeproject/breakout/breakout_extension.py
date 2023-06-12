"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

This program build a brick breaking game. The ball will start to move right after the user click the mouse.
The game will over after the ball drop out of the window for 3 times, which means lose, or all the bricks were broken,
 which means win!
"""

from campy.gui.events.timer import pause
from campy.graphics.gobjects import GLabel
from breakoutgraphics_extension import BreakoutGraphics

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    graphics = BreakoutGraphics()
    lives = NUM_LIVES
    fail = GLabel('FAIL !!')
    fail.font = '-100'
    fail.color = 'red'
    win = GLabel('WIN !!')
    win.font = '-100'
    win.color = 'green'
    while True:
        graphics.ball_move()
        brick_count = graphics.get_total_bricks()
        if graphics.ball.y > graphics.window.height - graphics.ball.height:
            graphics.reset_ball_position()
            lives -= 1
        if lives == 0:
            graphics.window.add(fail, x=(graphics.window.width-fail.width)/2, y=graphics.window.height/2)
            break
        if brick_count == 0:
            graphics.window.add(win, x=(graphics.window.width - win.width)/2, y=graphics.window.height/2)
            break
        pause(FRAME_RATE)


if __name__ == '__main__':
    main()
