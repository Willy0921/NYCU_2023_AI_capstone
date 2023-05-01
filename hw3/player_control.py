import itertools
import copy


class KnowledgeBase:
    def __init__(self):
        """
        Initialize KB
        """
        self.literals = []
        self.clauses = []
        self.useless_literals = []
        self.has_new_literal = False

    def add_literal(self, literal):
        """
        Adds a literal to KB

        Args:
            literal: tuple of (cell, mark)
            game: MinesweeperGame object
        Return:
            None
        """
        self.literals.append(literal)
        self.single_resolution(literal)
        self.has_new_literal = True

    def remove_literal(self, literal):
        """
        Removes a literal from KB

        Args:
            literal: tuple of (cell, mark)
        Return:
            None
        """
        self.single_resolution(literal)
        self.literals.remove(literal)
        self.useless_literals.append(literal)

    def add_clause(self, clause):
        """
        Adds a clause to KB

        Args:
            clause: list of literals
        Return:
            None
        """
        if clause not in self.clauses:
            self.clauses.append(clause)

    def remove_clause(self, clause):
        """
        Removes a clause from KB

        Args:
            clause: list of literals
        Return:
            None
        """
        self.clauses.remove(clause)

    def single_resolution(self, literal):
        """
        Single resolution

        Args:
            literal: tuple of (cell, mark)
        Return:
            None
        """
        negation_literal = (literal[0], 1 - literal[1])
        for clause in self.clauses:
            if negation_literal in clause:
                clause.remove(negation_literal)
        self.remove_duplicated_clauses()

    def remove_single_length_clause(self):
        """
        Removes single length clause

        Args:
            None

        Return:
            new_literals: list of literals
        """
        new_literals = []
        clauses = copy.deepcopy(self.clauses)
        for clause in clauses:
            if len(clause) == 1:
                new_literals.append(clause[0])
                self.remove_clause(clause)
            elif len(clause) == 0:
                self.remove_clause(clause)

        valid_literals = [
            literal
            for literal in new_literals
            if literal not in self.literals and literal not in self.useless_literals
        ]
        return valid_literals

    def remove_duplicated_clauses(self):
        """
        Removes duplicated clauses
        """
        self.clauses = [list(x) for x in set(tuple(x) for x in self.clauses)]

    def check_subset_clauses(self):
        """
        Checks subset clauses
        """
        clauses_copy = copy.deepcopy(self.clauses)
        n = len(clauses_copy)
        for clause in self.clauses:
            for i in range(n):
                set1 = set(clauses_copy[i])
                set2 = set(clause)

                if set1.issubset(set2):
                    self.clauses.remove(clause)
                    break

    def matching_clauses_pair(self):
        """
        Matching clauses pair

        Args:
            None

        Return:
            list of new literals
        """

        copy_clauses = copy.deepcopy(self.clauses)

        new_literals = []

        n = len(copy_clauses)
        for i in range(n):
            if len(copy_clauses[i]) > 2:
                continue
            for j in range(i + 1, n):
                ref_clause = copy.deepcopy(copy_clauses[i])
                neg_clause = []

                for literal in ref_clause:
                    neg_clause.append((literal[0], 1 - literal[1]))
                clause = copy.deepcopy(copy_clauses[j])

                set1 = set(neg_clause)
                set2 = set(clause)
                common_literals = list(set1 & set2)

                if len(common_literals) == 1:
                    ref_clause.remove(
                        (common_literals[0][0], 1 - common_literals[0][1])
                    )
                    clause.remove(common_literals[0])
                    new_clause = clauses_merge(ref_clause, clause)
                    if len(new_clause) == 1:
                        new_literals.append(new_clause[0])
                    else:
                        self.add_clause(new_clause)

        valid_literals = [
            literal
            for literal in new_literals
            if literal not in self.literals and literal not in self.useless_literals
        ]
        return valid_literals


def generate_clauses(cells, n, mark):
    """
    Generate clauses

    Args:
        cells: list of cells
        n: number of cells
        mark: 0 or 1

    Return:
        list of clauses
    """

    literals = [(cell, mark) for cell in cells]
    combinations = list(itertools.combinations(literals, n))
    return combinations


def clauses_merge(clause1, clause2):
    """
    Merges two clauses

    Args:
        clause1: list of literals
        clause2: list of literals

    Return:
        new clause: list of literals
    """
    return list(set(clause1 + clause2))
