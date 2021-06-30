import math
import random as rnd
import copy


class Board:
    """a board that can store all the disks and drawing functions"""

    def __init__(self, row, col, cell_size):
        """a board with row * col size,
        use list of list to represent disk data"""
        self.row = row
        self.col = col
        # cell_size = boarder size + single internal cell size
        self.cell_size = cell_size
        self.boarder_size = self.cell_size/5
        self.text_x = self.cell_size * self.col/5
        self.text_y = self.cell_size * self.row/2
        # if row 0 , column 0, generate a disk
        # x = (cell size - boarder size)/2 + boarder size, simplified as blow
        self.DISK_CENTER = self.cell_size/2 + self.boarder_size/2

        self.EMPTY = -1
        self.RED = 0
        self.YELLOW = 1
        # default red starts first
        self.cur_player = self.RED
        # list of list to represent the board coordinate (row, column)
        # all_disks[0][0] is the upper left corner
        # store -1 as empty cell, 0 is red disk, 1 is yellow disk
        self.all_disks = [[self.EMPTY for j in range(self.col)]
                          for i in range(self.row)]
        # another data: only track number of disks droped in each column
        self.available = [0 for i in range(self.col)]

        # initial checking variables
        self.drop_y = 0
        self.adding_col = 0          # players move -> add col
        self.ai_m = 0                # ai move -> add col
        self.dropping = False
        self.is_full = False         # board full return variable
        self.win_check = self.EMPTY  # win_check default to not red or yellow

# -------------------------Draw Part-------------------------------------------

    def draw_board(self):
        "draw a board with rows and columns"
        # draw row
        row_length = self.col*self.cell_size + self.boarder_size
        for i in range(1, self.row + 2):
            fill(0, 0, 255)
            noStroke()
            x = 0
            y = i*self.cell_size
            rect(x, y, row_length, self.boarder_size)
        # draw colomn
        column_length = self.row*self.cell_size + self.boarder_size
        for i in range(0, self.col + 1):
            fill(0, 0, 255)
            noStroke()
            x = i*self.cell_size
            y = self.cell_size
            rect(x, y, self.boarder_size, column_length)

    def draw_disk(self, color, x, y):
        """draw disks with red or yellow controlled by players turn"""
        if color == self.RED:
            fill(255, 0, 0)
        elif color == self.YELLOW:
            fill(255, 255, 0)
        noStroke()
        circle(x, y, self.cell_size)

    def mouse_column(self, mouse_x, mouse_y):
        """locate mouse position to identify which column the mose at"""
        if (mouse_x > 0 and mouse_x < self.col * self.cell_size
            and mouse_y > 0 and mouse_y < self.cell_size
                and not self.dropping):
            # adding_col refer to the list of list index, starts from 0
            self.adding_col = int(math.floor(mouse_x/self.cell_size))
            return True
        else:
            return False

    def generate_disk(self, mouse_x, mouse_y):
        """draw a disk at the top of the board"""
        if self.mouse_column(mouse_x, mouse_y):
            # if the column is full with disks, no more disk need to generate
            if (self.all_disks[0][self.adding_col] != self.EMPTY):
                return
            # if the column is not full, keep generating disks
            x = self.adding_col * self.cell_size + self.DISK_CENTER
            y = self.cell_size/2
            self.draw_disk(self.cur_player, x, y)

    def draw_drop_disk(self):
        if self.cur_player == self.RED:
            col = self.adding_col
        elif self.cur_player == self.YELLOW:
            col = self.ai_m
        target_y = self.cell_size/2
        # search for the first empty cell to put disk in the board
        i = self.row - 1 - self.available[col]
        target_y = (i + 1) * self.cell_size + self.cell_size/2
        if self.drop_y < target_y and self.dropping:
            x = col * self.cell_size + self.DISK_CENTER
            self.draw_disk(self.cur_player, x, self.drop_y)
            self.drop_y += 25
        if self.drop_y >= target_y:
            # even number is red, odd number is yellow
            self.dropping = False
            self.drop_y = 0
            # switch player after the dropping animation is finish
            self.cur_player = (self.cur_player + 1) % 2

    def update_board(self):
        """constantly draw circle disks in board, after the disk movement
        updated according to the data changed by add_disk function"""
        for i in range(0, self.row):
            for j in range(self.col):
                x = j * self.cell_size + self.DISK_CENTER
                y = (i + 1) * self.cell_size + self.DISK_CENTER
                # while = 0, draw a red disk
                if self.all_disks[i][j] == self.RED:
                    fill(255, 0, 0)
                    noStroke()
                    circle(x, y, self.cell_size)
                # while = 1, draw a yellow disk
                elif self.all_disks[i][j] == self.YELLOW:
                    fill(255, 255, 0)
                    noStroke()
                    circle(x, y, self.cell_size)

    def draw_text(self):
        textSize(85)
        fill(0, 0, 0)
        if self.win_check != self.EMPTY:
            if self.cur_player == self.RED:
                text("Red  Win", self.text_x, self.text_y)
            elif self.cur_player == self.YELLOW:
                text("Yellow  Win", self.text_x, self.text_y)
        elif self.is_full is True:
            text("Tie  Game", self.text_x, self.text_y)

# ---------------------------Game Controller Part------------------------------

    def player_move(self, mouse_x, mouse_y):
        """player move, add disks regarding on the mouse move"""
        if self.mouse_column(mouse_x, mouse_y) and not self.dropping:
            # search for the first empty cell to put disk in the board
            i = self.row - 1 - self.available[self.adding_col]
            self.all_disks[i][self.adding_col] = self.cur_player
            self.available[self.adding_col] += 1
            if self.win_game(self.all_disks, self.cur_player,
                             i, self.adding_col) == self.cur_player:
                self.win_check = self.cur_player
                return self.cur_player
            elif self.board_full(self.all_disks) is True:
                self.is_full = True
                return self.is_full
            self.dropping = True

    def ai_move(self):
        """AI move, add disks on the test run result of monte carlo"""
        if (self.cur_player == self.YELLOW and not self.dropping):
            self.ai_m = self.ai(self.cur_player)
            # search for the first empty cell to put disk in the board
            i = self.row - 1 - self.available[self.ai_m]
            self.all_disks[i][self.ai_m] = self.cur_player
            self.available[self.ai_m] += 1
            if self.win_game(self.all_disks, self.cur_player,
                             i, self.ai_m) == self.cur_player:
                self.win_check = self.cur_player
                return self.cur_player
            elif self.board_full(self.all_disks) is True:
                self.is_full = True
                return self.is_full
            self.dropping = True

    def board_full(self, data):
        """check the first row to see if the board is full"""
        for j in range(self.col):
            if data[0][j] == self.EMPTY:
                return False
        return True

    def win_game(self, data, color, i, j):
        """four directions to check if there is four disks connected"""
        if (self.horizon_four(data, color, i, j) or
            self.vertical_four(data, color, i, j) or
            self.slope_down_four(data, color, i, j) or
                self.slope_up_four(data, color, i, j)):
            return color
        return self.EMPTY

    def horizon_four(self, data, color, i, j):
        """check if four connect in horizon direction"""
        connect = 0
        for n in range(self.col):
            if abs(j-n) <= 3:
                if data[i][n] == color:
                    connect += 1
                    if connect == 4:
                        return True
                else:
                    connect = 0
        return False

    def vertical_four(self, data, color, i, j):
        """check if four connect in veritical direction"""
        connect = 0
        for n in range(self.row):
            if abs(i-n) <= 3:
                if data[n][j] == color:
                    connect += 1
                    if connect == 4:
                        return True
                else:
                    connect = 0
        return False

    def slope_down_four(self, data, color, i, j):
        """check if four connect in down slope direction"""
        connect = 0
        count = 3
        while (i > 0 and j > 0 and count > 0):
            i = i - 1
            j = j - 1
            count = count - 1
        count = self.row
        while (i < self.row and j < self.col and count > 0):
            if data[i][j] == color:
                connect += 1
                if connect == 4:
                    return True
            else:
                connect = 0
            i = i + 1
            j = j + 1
            count = count - 1
        return False

    def slope_up_four(self, data, color, i, j):
        """check if four connect in up slope direction"""
        connect = 0
        count = 3
        while (i < self.row - 1 and j > 0 and count > 0):
            i = i + 1
            j = j - 1
            count = count - 1
        count = self.row
        while (i >= 0 and j < self.col and count > 0):
            if data[i][j] == color:
                connect += 1
                if connect == 4:
                    return True
            else:
                connect = 0
            i = i - 1
            j = j + 1
            count = count - 1
        return False

# --------------------------AI Part--------------------------------------------

    def ai(self, cur_player):
        """call monte carlo for 500 test_runs,
        add up all the win, lose or tie result from the monte carlo
        select the highest score to take that first move.
        return an adding column"""
        TEST_RUN = 500
        ai_move = 0
        max_score = 0
        for i in range(self.col):
            if self.available[i] < 6:
                data = copy.deepcopy(self.all_disks)
                available = copy.deepcopy(self.available)
                n = self.row - 1 - available[i]
                m = i
                data[n][m] = self.YELLOW
                available[i] += 1
                current_score = 0
                # check if this step is direct take AI win
                if (self.win_game(data, self.YELLOW, n, m) == self.YELLOW):
                    return i
                # if not win, theck this step makes player win
                # if so take this step as yellow
                data[n][m] = self.RED
                if (self.win_game(data, self.RED, n, m) == self.RED):
                    return i
                data[n][m] = self.YELLOW
                for _ in range(TEST_RUN):
                    current_score += self.monte_carlo(data, available, 0)
                if (current_score > max_score):
                    max_score = current_score
                    ai_move = i
        return ai_move

    def monte_carlo(self, data, available, cur_player):
        """assume the first step is give, and randomly play all the rest
        till game is over. record the result"""
        test_cur_player = 0
        monte_ai_win = 0
        test_disks = copy.deepcopy(data)
        test_available = copy.deepcopy(available)
        game_over = False
        while not game_over:
            if self.board_full(test_disks) is True:
                monte_ai_win = 0.2
                game_over = True
            r = rnd.randint(0, 6)
            if test_available[r] < 6:
                i = self.row - 1 - test_available[r]
                test_available[r] += 1
                j = r
                test_disks[i][j] = test_cur_player
                win_player = self.win_game(test_disks, test_cur_player, i, j)
                if win_player == self.RED:
                    game_over = True
                if win_player == self.YELLOW:
                    game_over = True
                    monte_ai_win = 1
                test_cur_player = (test_cur_player + 1) % 2
        return monte_ai_win
