"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

The program build the backend of a brick breaking game. After create the window, all the bricks, and the paddle,
once the user clicks the mouse, the ball will start to move and check whether it hit anything each time it move.
The ball will break the brick when hit it, and will bounce when hit the paddle or
the top, left, and right borders of the window. The game will reset when the ball drop out of the bottom of the window.
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.window.add(self.paddle, x=(self.window.width-self.paddle.width)/2,
                        y=self.window.height-paddle_offset-self.paddle.height)

        # Center a filled ball in the graphical window
        self.ball_radius = ball_radius
        self.ball = GOval(ball_radius*2, ball_radius*2)
        self.ball.filled = True
        self.window.add(self.ball, x=self.window.width/2-self.ball_radius, y=self.window.height/2-self.ball_radius)

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0
        self.switch = True

        # Calculate the bricks remained and the score
        self.brick_cols = brick_cols
        self.brick_rows = brick_rows
        self.original_bricks = self.brick_rows * self.brick_cols
        self.total_bricks = self.original_bricks

        # Score board
        self.score = 0
        self.score_board = GLabel(f'Score: {self.score}')
        self.score_board.font = '-20'
        self.window.add(self.score_board, x=5, y=self.window.height - self.score_board.height)

        # Lives remain
        self.lives = 3
        self.lives_remain = GLabel(f'Lives: {self.lives}')
        self.lives_remain.font = '-20'
        self.window.add(self.lives_remain, x=self.window.width - self.lives_remain.width,
                        y=self.window.height - self.lives_remain.height)

        # Initialize our mouse listeners
        onmouseclicked(self.reset_ball_speed)
        onmousemoved(self.move_paddle)

        # Draw bricks
        for i in range(brick_rows):
            for j in range(brick_cols):
                self.brick = GRect(brick_width, brick_height)
                self.brick.filled = True
                if 0 < j + 1 <= brick_cols / 5 * 1:
                    self.brick.fill_color = 'red'
                elif brick_cols / 5 * 1 < j + 1 <= brick_cols / 5 * 2:
                    self.brick.fill_color = 'orange'
                elif brick_cols / 5 * 2 < j + 1 <= brick_cols / 5 * 3:
                    self.brick.fill_color = 'yellow'
                elif brick_cols / 5 * 3 < j + 1 <= brick_cols / 5 * 4:
                    self.brick.fill_color = 'green'
                elif brick_cols / 5 * 4 < j + 1 <= brick_cols / 5 * 5:
                    self.brick.fill_color = 'blue'
                self.window.add(self.brick, x=(brick_spacing + brick_width)*i,
                                y=brick_offset + (brick_spacing + brick_height)*j)

    def move_paddle(self, mouse):
        if 0 <= self.paddle.x <= self.window.width - self.paddle.width:
            self.paddle.x = mouse.x - self.paddle.width/2
        while 0 > self.paddle.x:
            self.paddle.x = 0
        while self.paddle.x > self.window.width - self.paddle.width:
            self.paddle.x = self.window.width - self.paddle.width

    def ball_move(self):
        self.ball.move(self.__dx, self.__dy)
        # the ball hit the left or right border of the window.
        if 0 > self.ball.x or self.ball.x >= self.window.width - self.ball.width:
            self.__dx = - self.__dx
        # the ball hit the ceiling of the window.
        if 0 > self.ball.y:
            self.__dy = - self.__dy
        # the ball drop out of the bottom of the window.
        if self.ball.y > self.window.height - self.ball.height:
            self.lives -= 1
        # check whether the ball hit anything inside the window.
        upper_left = self.window.get_object_at(self.ball.x, self.ball.y)
        lower_left = self.window.get_object_at(self.ball.x, self.ball.y + 2*self.ball_radius)
        upper_right = self.window.get_object_at(self.ball.x + 2*self.ball_radius, self.ball.y)
        lower_right = self.window.get_object_at(self.ball.x + 2*self.ball_radius, self.ball.y + 2*self.ball_radius)
        if upper_left is None:
            if lower_left is None:
                if upper_right is None:
                    if lower_right is None:
                        pass
                    else:
                        if lower_right is self.paddle:
                            self.__dy = - self.__dy
                        elif lower_right is self.score_board:
                            self.__dy = self.__dy
                        elif lower_right is self.lives_remain:
                            self.__dy = self.__dy
                        else:  # hit brick
                            self.window.remove(lower_right)
                            self.total_bricks -= 1
                            self.__dy = - self.__dy
                else:
                    if upper_right is self.paddle:
                        self.__dx = - self.__dx  # When the upper side hit the paddle, it's too late to save the ball.
                    elif upper_right is self.score_board:
                        self.__dy = self.__dy
                    elif upper_right is self.lives_remain:
                        self.__dy = self.__dy
                    else:  # hit brick
                        self.window.remove(upper_right)
                        self.total_bricks -= 1
                        self.__dy = - self.__dy
            else:
                if lower_left is self.paddle:
                    self.__dy = - self.__dy
                elif lower_left is self.score_board:
                    self.__dy = self.__dy
                elif lower_left is self.lives_remain:
                    self.__dy = self.__dy
                else:  # hit brick
                    self.window.remove(lower_left)
                    self.total_bricks -= 1
                    self.__dy = - self.__dy
        else:
            if upper_left is self.paddle:
                self.__dx = - self.__dx
            elif upper_left is self.score_board:
                self.__dy = self.__dy
            elif upper_left is self.lives_remain:
                self.__dy = self.__dy
            else:  # hit brick
                self.window.remove(upper_left)
                self.total_bricks -= 1
                self.__dy = - self.__dy
        self.score = self.original_bricks - self.total_bricks  # count score
        self.score_board.text = f'Score: {self.score}'
        self.lives_remain.text = f'Lives: {self.lives}'

    def reset_ball_speed(self, mouse):
        """
        When the user click the mouse, the ball would be given a random speed, and the switch would be turned to False,
        so that any mouseclick won't affect the ball speed again.
        """
        if self.switch is True:
            self.__dx = random.randint(1, MAX_X_SPEED)
            if random.random() > 0.5:
                self.__dx = - self.__dx
            self.__dy = INITIAL_Y_SPEED
        self.switch = False

    def get_ball_x_speed(self):
        return self.__dx

    def get_ball_y_speed(self):
        return self.__dy

    def reset_ball_position(self):
        """
        When the ball drop out of the window, it would be back to the middle of the window, and the switch would be
        turned on again to wait the user click again to start the 2nd round of the game.
        """
        self.window.add(self.ball, x=self.window.width/2-self.ball_radius, y=self.window.height/2-self.ball_radius)
        self.switch = True
        self.__dx = 0
        self.__dy = 0

    def get_total_bricks(self):
        return self.total_bricks
