from board import Board


def test_board():
    """test the list of list created by board size"""
    n = Board(6, 6, 100)
    assert n.all_disks == [[-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1],
                           [-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1],
                           [-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1]]
    assert n.available == [0, 0, 0, 0, 0, 0]
    m = Board(2, 2, 100)
    assert m.all_disks == [[-1, -1], [-1, -1]]
    assert m.available == [0, 0]


def test_board_full():
    n = Board(2, 2, 100)
    n.all_disks = [[0, 1], [1, 0]]
    assert n.board_full(n.all_disks) is True
    m = Board(1, 1, 100)
    m.all_disks = [[-1]]
    assert m.board_full(m.all_disks) is False


def test_win_game():
    i = 0
    j = 0
    n = Board(4, 4, 100)
    # vertical four
    n.all_disks = [[1, 1, 1, 1], [-1, -1, -1, -1], [-1, -1, -1, -1],
                   [-1, -1, -1, -1]]
    assert n.win_game(n.all_disks, 1, i, j) == 1

    m = Board(4, 4, 100)
    # horizon four
    m.all_disks = [[0, -1, -1, -1], [0, -1, -1, -1], [0, -1, -1, -1],
                   [0, -1, -1, -1]]
    assert m.win_game(m.all_disks, 0, i, j) == 0

    a = Board(4, 4, 100)
    # slope down
    a.all_disks = [[0, -1, -1, -1], [-1, 0, -1, -1], [-1, -1, 0, -1],
                   [-1, -1, -1, 0]]
    assert m.win_game(a.all_disks, 0, i, j) == 0

    b = Board(4, 4, 100)
    # slope up
    b.all_disks = [[-1, -1, -1, 1], [-1, -1, 1, -1], [-1, 1, -1, -1],
                   [1, -1, -1, -1]]
    assert m.win_game(b.all_disks, 1, 3, 0) == 1
