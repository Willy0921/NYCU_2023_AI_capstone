import sys
from game_control import MinesweeperGame
from player_control import *


def add_global_info(game, KB, m, n):
    """
    Add global information to KB

    Args:
        game: MinesweeperGame object
        KB: KnowledgeBase object
        m: number of safe cells
        n: number of mines

    Return: list of new literals
    """

    new_literals = []
    unmarked_cells = game.get_unmarked_cells()
    if m > n:
        clauses1 = generate_clauses(unmarked_cells, m - n + 1, 1)
        clauses2 = generate_clauses(unmarked_cells, n + 1, 0)
        clauses = clauses1 + clauses2
        for clauses in clauses:
            KB.add_clause(list(clauses))
    elif n == 0:
        for cell in unmarked_cells:
            new_literals.append((cell, 0))
    elif m == n:
        for cell in unmarked_cells:
            new_literals.append((cell, 1))

    return new_literals


def query_safe_cells(game, KB):
    """
    Query safe cells

    Args:
        game: MinesweeperGame object
        KB: KnowledgeBase object

    Returns:
        list of new literals
    """
    new_literals = []
    for literal in KB.literals:
        cell, mark = literal

        if mark == 0:
            unmarked_neighbors = game.get_unmarked_neighbor(cell)
            n = len(unmarked_neighbors)

            if n == 0:
                KB.remove_literal(literal)
                continue

            hint = game.get_hint(cell)

            if hint == 0:
                for neighbor_cell in unmarked_neighbors:
                    new_literals.append((neighbor_cell, 0))
            elif hint > 0:
                if n == hint:
                    for neighbor_cell in unmarked_neighbors:
                        new_literals.append((neighbor_cell, 1))
                elif n > hint:
                    clauses1 = generate_clauses(unmarked_neighbors, n - hint + 1, 1)
                    clauses2 = generate_clauses(unmarked_neighbors, hint + 1, 0)

                    clauses = clauses1 + clauses2
                    for clauses in clauses:
                        KB.add_clause(list(clauses))

    valid_literals = [
        literal
        for literal in new_literals
        if literal not in KB.literals and literal not in KB.useless_literals
    ]
    return valid_literals


def process_new_literal(new_literals, game, KB):
    """
    Process new literals

    Args:
        new_literals: list of new literals
        game: MinesweeperGame object
        KB: KnowledgeBase object

    Returns:
        None
    """
    while len(new_literals) > 0:
        new_literal = new_literals.pop()
        if new_literal not in KB.literals:
            cell, mark = new_literal

            game.is_marked[cell] = 1
            if mark == 1:
                game.update_hint(cell)

            KB.add_literal(new_literal)
    new_literals += KB.remove_single_length_clause()
    new_literals += query_safe_cells(game, KB)


def play(KB, game):
    """
    Play game with logic inference

    Args:
        KB: KnowledgeBase object
        game: MinesweeperGame object
    """
    stuck_time = 0
    new_literals = [(cell, 0) for cell in game.init_safe_cells]
    m = game.get_num_unmarked_cells()

    while m > 0 and stuck_time < 10:
        game.display()

        process_new_literal(new_literals, game, KB)
        while len(new_literals) > 0:
            process_new_literal(new_literals, game, KB)
            game.display()
    
        KB.check_subset_clauses()
        new_literals += KB.matching_clauses_pair()
        KB.check_subset_clauses()

        if not KB.has_new_literal:
            stuck_time += 1
        else:
            KB.has_new_literal = False
            stuck_time = 0

        m = game.get_num_unmarked_cells()
        if m < 15:
            n = game.get_num_unmarked_mines()
            new_literals += add_global_info(game, KB, m, n)

    game.display()


if __name__ == "__main__":
    args = sys.argv
    level = args[1]

    game = MinesweeperGame(level)

    KB = KnowledgeBase()
    play(KB, game)

    print(f"succussful mark rate: {game.get_mark_rate()}")
    print(f"remaining unmark cells: {game.get_num_unmarked_cells()}")
    print(f"remaining mines: {game.get_num_unmarked_mines()}")
