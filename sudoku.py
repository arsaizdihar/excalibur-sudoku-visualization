import time
from typing import List, Tuple, Set, Dict, Optional
from copy import deepcopy, copy
import json


class ExcaliburSudoku:
    VISUAL_DELAY = 0.025
    step_count = 0

    def __init__(self, board: List[List[int]], arrows: List[Tuple[Tuple[int, int], List[Tuple[int, int]]]]):
        self.board = board
        self.arrows = arrows
        self.possible_vals: List[List[Set[int]]] = [
            [set() for _ in range(9)] for _ in range(9)]
        self.unanswered_count = 0
        self.questions: Set[Tuple[int, int]] = set()
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    self.unanswered_count += 1
                    self.possible_vals[i][j] = set(range(1, 10))
        self.possible_sums: Dict[Tuple[int, int], List[List[int]]] = {}
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    self.questions.add((i, j))
                    self.update_possible_vals(self.board[i][j], i, j)
        self.update_arrows()

    def solve(self):
        if self.unanswered_count == 0:
            return True
        for i in range(9):
            for j in range(9):
                if not self.is_answered((i, j)) and len(self.possible_vals[i][j]) == 0:
                    return False

        ExcaliburSudoku.step_count += 1

        start = time.process_time()
        # check only one possibility in row, column, and block
        to_run = None
        for k in range(9):
            for l in range(1, 10):
                if l in self.board[k]:
                    continue
                count = 0
                last_idx = 0
                for m in range(9):
                    if l in self.possible_vals[k][m]:
                        last_idx = m
                        count += 1
                if count == 1:
                    to_run = (l, (k, last_idx))

        if not to_run:
            for k in range(9):
                for l in range(1, 10):
                    if l in [self.board[m][k] for m in range(9)]:
                        continue
                    count = 0
                    last_idx = 0
                    for m in range(9):
                        if l in self.possible_vals[m][k]:
                            last_idx = m
                            count += 1
                    if count == 1:
                        to_run = (l, (last_idx, k))
        if not to_run:
            for k in range(3):
                for l in range(3):
                    for m in range(1, 10):
                        if m in [self.board[3*k+i][3*l+j] for i in range(3) for j in range(3)]:
                            continue
                        count = 0
                        last_idx = (0, 0)
                        for i in range(3):
                            for j in range(3):
                                if m in self.possible_vals[3*k+i][3*l+j]:
                                    last_idx = (3*k+i, 3*l+j)
                                    count += 1
                        if count == 1:
                            to_run = (m, last_idx)

        if to_run:
            num, (i, j) = to_run
            self.unanswered_count -= 1
            self.board[i][j] = num
            self.possible_vals[i][j] = set()
            self.update_possible_vals(self.board[i][j], i, j)
            self.update_arrows()
            return self.solve()

        # search for only one possible value
        for i in range(9):
            for j in range(9):
                if len(self.possible_vals[i][j]) == 1:
                    self.unanswered_count -= 1
                    self.board[i][j] = self.possible_vals[i][j].pop()
                    self.update_possible_vals(self.board[i][j], i, j)
                    self.update_arrows()
                    return self.solve()

        # search for two and more
        for i in range(2, 10):
            for j in range(9):
                for k in range(9):
                    if self.is_answered((j, k)):
                        continue
                    poss = self.possible_vals[j][k]
                    if len(poss) == 0:
                        return False
                    if len(poss) == i:
                        for p in poss:
                            copy = self.get_copy()
                            copy.board[j][k] = p
                            copy.possible_vals[j][k] = set()
                            copy.unanswered_count -= 1
                            copy.update_possible_vals(p, j, k)
                            copy.update_arrows()
                            if copy.solve():
                                self.board = copy.board
                                self.possible_vals = copy.possible_vals
                                return True
                        return False
        return False

    def visual_solve(self, on_update):
        if self.unanswered_count == 0:
            return True
        for i in range(9):
            for j in range(9):
                if not self.is_answered((i, j)) and len(self.possible_vals[i][j]) == 0:
                    return False

        ExcaliburSudoku.step_count += 1
        # check only one possibility in row, column, and block
        to_run = None
        for k in range(9):
            for l in range(1, 10):
                if l in self.board[k]:
                    continue
                count = 0
                last_idx = 0
                for m in range(9):
                    if l in self.possible_vals[k][m]:
                        last_idx = m
                        count += 1
                if count == 1:
                    to_run = (l, (k, last_idx))

        if not to_run:
            for k in range(9):
                for l in range(1, 10):
                    if l in [self.board[m][k] for m in range(9)]:
                        continue
                    count = 0
                    last_idx = 0
                    for m in range(9):
                        if l in self.possible_vals[m][k]:
                            last_idx = m
                            count += 1
                    if count == 1:
                        to_run = (l, (last_idx, k))
        if not to_run:
            for k in range(3):
                for l in range(3):
                    for m in range(1, 10):
                        if m in [self.board[3*k+i][3*l+j] for i in range(3) for j in range(3)]:
                            continue
                        count = 0
                        last_idx = (0, 0)
                        for i in range(3):
                            for j in range(3):
                                if m in self.possible_vals[3*k+i][3*l+j]:
                                    last_idx = (3*k+i, 3*l+j)
                                    count += 1
                        if count == 1:
                            to_run = (m, last_idx)

        if to_run:
            num, (i, j) = to_run
            self.unanswered_count -= 1
            self.board[i][j] = num
            self.possible_vals[i][j] = set()
            self.update_possible_vals(self.board[i][j], i, j)
            self.update_arrows()
            time.sleep(self.VISUAL_DELAY)
            on_update(self)
            return self.visual_solve(on_update)

        # search for only one possible value
        for i in range(9):
            for j in range(9):
                if len(self.possible_vals[i][j]) == 1:
                    self.unanswered_count -= 1
                    self.board[i][j] = self.possible_vals[i][j].pop()
                    self.update_possible_vals(self.board[i][j], i, j)
                    self.update_arrows()
                    time.sleep(self.VISUAL_DELAY)
                    on_update(self)
                    return self.visual_solve(on_update)

        # search for two and more
        for i in range(2, 10):
            for j in range(9):
                for k in range(9):
                    if self.is_answered((j, k)):
                        continue
                    poss = self.possible_vals[j][k]
                    if len(poss) == i:
                        for p in poss:
                            copy = self.get_copy()
                            copy.board[j][k] = p
                            copy.unanswered_count -= 1
                            copy.possible_vals[j][k] = set()
                            copy.update_possible_vals(p, j, k)
                            copy.update_arrows()
                            time.sleep(self.VISUAL_DELAY)
                            on_update(copy)
                            if copy.visual_solve(on_update):
                                self.board = copy.board
                                self.possible_vals = copy.possible_vals
                                return True
                        return False
        return False

    def update_possible_vals(self, input: int, i: int, j: int):
        # same row and column
        for k in range(9):
            self.possible_vals[i][k].discard(input)
            self.possible_vals[k][j].discard(input)

        # same block
        block_i = i // 3
        block_j = j // 3
        for k in range(3):
            for l in range(3):
                self.possible_vals[block_i * 3 +
                                   k][block_j * 3 + l].discard(input)

    def update_arrows(self):
        for sum_pos, all_num_poss in self.arrows:
            safe_numbers = [set() for _ in range(len(all_num_poss) + 1)]
            sum_answered = self.is_answered(sum_pos)
            if sum_answered and all([self.is_answered(pos) for pos in all_num_poss]):
                continue
            sum_possibilities = [self.board[sum_pos[0]][sum_pos[1]]
                                 ] if sum_answered else self.possible_vals[sum_pos[0]][sum_pos[1]]
            for n in sum_possibilities:
                possible_values = self.get_possible_sums(n, len(all_num_poss))
                for poss in possible_values:
                    this_possible = True
                    for i, p in enumerate(poss):
                        pos = all_num_poss[i]
                        if self.is_answered(pos):
                            if self.board[pos[0]][pos[1]] != p:
                                this_possible = False
                                break
                            continue
                        if p not in self.possible_vals[pos[0]][pos[1]]:
                            this_possible = False
                            break
                        for j in range(i):
                            if p == poss[j] and not self.can_be_same(pos, all_num_poss[j]):
                                this_possible = False
                                break
                    if this_possible:
                        safe_numbers[len(poss)].add(n)
                        for i, p in enumerate(poss):
                            pos = all_num_poss[i]
                            safe_numbers[i].add(p)
            for i in range(len(all_num_poss)):
                if not self.is_answered(all_num_poss[i]):
                    self.possible_vals[all_num_poss[i][0]
                                       ][all_num_poss[i][1]] = safe_numbers[i]
            if not sum_answered:
                self.possible_vals[sum_pos[0]][sum_pos[1]] = safe_numbers[-1]

    def get_possible_sums(self, total: int, num: int):
        if (total, num) in self.possible_sums:
            return self.possible_sums[(total, num)]
        res = []
        if num == 1:
            if total in range(1, 10):
                res.append([total])
            self.possible_sums[(total, num)] = res
            return res

        for i in range(1, 10):
            if total - i in range(1, 10):
                for j in self.get_possible_sums(total - i, num - 1):
                    res.append([i] + j)

        self.possible_sums[(total, num)] = res
        return res

    def can_be_same(self, pos1: Tuple[int, int], pos2: Tuple[int, int]):
        if pos1[0] == pos2[0]:
            return False
        if pos1[1] == pos2[1]:
            return False

        block_i1 = pos1[0] // 3
        block_j1 = pos1[1] // 3
        block_i2 = pos2[0] // 3
        block_j2 = pos2[1] // 3
        if block_i1 == block_i2 and block_j1 == block_j2:
            return False

        return True

    def is_answered(self, pos: Tuple[int, int]):
        return self.board[pos[0]][pos[1]] != 0

    def get_copy(self):
        scopy = copy(self)
        scopy.board = deepcopy(self.board)
        scopy.possible_vals = deepcopy(self.possible_vals)
        return scopy

    def print_board(self):
        for i in range(9):
            for j in range(9):
                print(self.board[i][j], end=' ')
            print()

    @staticmethod
    def from_json(filename: str):
        with open(filename, 'r') as f:
            data = json.load(f)
            return ExcaliburSudoku(data['board'], data['arrows'])
