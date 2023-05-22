import tkinter
import tkinter.filedialog
import pygame
import sys

from sudoku import ExcaliburSudoku


pygame.init()

# Set size of game and other constants
cell_size = 50
minor_grid_size = 1
major_grid_size = 3
buffer = 5
button_height = 50
button_width = 125
button_border = 2
width = cell_size*9 + minor_grid_size*6 + major_grid_size*4 + buffer*2
height = cell_size*9 + minor_grid_size*6 + \
    major_grid_size*4 + button_height + buffer*3 + button_border*2
size = width, height
white = 255, 255, 255
black = 0, 0, 0
gray = 200, 200, 200
green = 0, 175, 0
red = 200, 0, 0
inactive_btn = 51, 255, 255
active_btn = 51, 153, 255

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Sudoku')


class RectCell(pygame.Rect):
    def __init__(self, left, top, row, col):
        super().__init__(left, top, cell_size, cell_size)
        self.row = row
        self.col = col


def askfile():
    window = tkinter.Tk()
    window.withdraw()
    filename = tkinter.filedialog.askopenfilename(filetypes=(("Json File", "*.json"),),
                                                  title="Choose a file.")
    window.destroy()
    return filename


def create_cells():
    cells = [[] for _ in range(9)]

    # Set attributes for for first RectCell
    row = 0
    col = 0
    left = buffer + major_grid_size
    top = buffer + major_grid_size

    while row < 9:
        while col < 9:
            cells[row].append(RectCell(left, top, row, col))

            # Update attributes for next RectCell
            left += cell_size + minor_grid_size
            if col != 0 and (col + 1) % 3 == 0:
                left = left + major_grid_size - minor_grid_size
            col += 1

        # Update attributes for next RectCell
        top += cell_size + minor_grid_size
        if row != 0 and (row + 1) % 3 == 0:
            top = top + major_grid_size - minor_grid_size
        left = buffer + major_grid_size
        col = 0
        row += 1

    return cells


def draw_grid():
    # Draw minor grid lines
    lines_drawn = 0
    pos = buffer + major_grid_size + cell_size
    # draw white background
    pygame.draw.rect(screen, white, (buffer, buffer,
                     width-buffer*2, height-button_height-buffer*3))
    while lines_drawn < 6:
        pygame.draw.line(screen, black, (pos, buffer),
                         (pos, width-buffer-1), minor_grid_size)
        pygame.draw.line(screen, black, (buffer, pos),
                         (width-buffer-1, pos), minor_grid_size)

        # Update number of lines drawn
        lines_drawn += 1

        # Update pos for next lines
        pos += cell_size + minor_grid_size
        if lines_drawn % 2 == 0:
            pos += cell_size + major_grid_size

    # Draw major grid lines
    for pos in range(buffer+major_grid_size//2, width, cell_size*3 + minor_grid_size*2 + major_grid_size):
        pygame.draw.line(screen, black, (pos, buffer),
                         (pos, width-buffer-1), major_grid_size)
        pygame.draw.line(screen, black, (buffer, pos),
                         (width-buffer-1, pos), major_grid_size)


def minus_from_center(cell, before, now,):
    center = list(cell.center)
    if before[0] == now[0]:
        center[1] -= (now[1] - before[1]) / 3.5
    elif before[1] == now[1]:
        center[0] -= (now[0] - before[0]) / 3.5
    else:
        center[0] -= (now[0] - before[0]) / 5
        center[1] -= (now[1] - before[1]) / 5
    return center


def fill_cells(cells, sudoku: ExcaliburSudoku):
    font = pygame.font.Font(None, 36)

    for head_pos, tails in sudoku.arrows:
        # draw arrow head with circle
        pygame.draw.circle(
            screen, (0, 0, 0, 0), cells[head_pos[0]][head_pos[1]].center, 16, width=1)
        for i, tail in enumerate(tails):
            # draw line
            to_cell = cells[tail[0]][tail[1]]
            if i == 0:
                from_cell = cells[head_pos[0]][head_pos[1]]
            else:
                from_cell = cells[tails[i-1][0]][tails[i-1][1]]
            from_pos = from_cell.center
            to_pos = to_cell.center
            if i == 0:
                from_pos = minus_from_center(
                    from_cell, to_cell.center, from_cell.center)
            elif i == len(tails) - 1:
                to_pos = minus_from_center(
                    to_cell, from_cell.center, to_cell.center)

            pygame.draw.line(screen, black, from_pos, to_pos, width=1)

    # Fill in all cells with correct value
    for row in range(9):
        for col in range(9):
            if not sudoku.is_answered((row, col)):
                continue

            # Fill in given values
            font.bold = False
            text = font.render(f'{sudoku.board[row][col]}', 1, black if (
                row, col) in sudoku.questions else green)

            # Center text in cell
            xpos, ypos = cells[row][col].center
            textbox = text.get_rect(center=(xpos, ypos))
            screen.blit(text, textbox)


def draw_button(left, top, width, height, border, color, border_color, text):
    # Draw the border as outer rect
    pygame.draw.rect(
        screen,
        border_color,
        (left, top, width+border*2, height+border*2),
    )

    # Draw the inner button
    button = pygame.Rect(
        left+border,
        top+border,
        width,
        height
    )
    pygame.draw.rect(screen, color, button)

    # Set the text
    font = pygame.font.Font(None, 26)
    text = font.render(text, 1, black)
    xpos, ypos = button.center
    textbox = text.get_rect(center=(xpos, ypos))
    screen.blit(text, textbox)

    return button


def draw_board(cells, sudoku):
    # Draw grid and cells
    draw_grid()

    # Fill in cell values
    fill_cells(cells, sudoku)


def visual_solve(sudoku: ExcaliburSudoku, cells):
    ExcaliburSudoku.step_count = 0

    def on_update(s):
        draw_board(cells, s)
        pygame.display.flip()
    sudoku.visual_solve(on_update)
    print(ExcaliburSudoku.step_count)


def get_new_sudoku():
    ExcaliburSudoku.step_count = 0
    filename = None
    while not filename:
        filename = askfile()
    sudoku = ExcaliburSudoku.from_json(filename)
    return sudoku


def play():

    sudoku = get_new_sudoku()
    cells = create_cells()
    active_cell = None
    solve_rect = pygame.Rect(
        buffer,
        height-button_height - button_border*2 - buffer,
        button_width + button_border*2,
        button_height + button_border*2
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Handle mouse click
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()

                # Reset button is pressed
                if reset_btn.collidepoint(mouse_pos):
                    sudoku = get_new_sudoku()

                # Solve button is pressed
                if solve_btn.collidepoint(mouse_pos):
                    screen.fill(white)
                    draw_board(cells, sudoku)
                    reset_btn = draw_button(
                        width - buffer - button_border*2 - button_width,
                        height - button_height - button_border*2 - buffer,
                        button_width,
                        button_height,
                        button_border,
                        inactive_btn,
                        black,
                        'Select'
                    )
                    solve_btn = draw_button(
                        width - buffer*2 - button_border*4 - button_width*2,
                        height - button_height - button_border*2 - buffer,
                        button_width,
                        button_height,
                        button_border,
                        inactive_btn,
                        black,
                        'Visual Solve'
                    )
                    pygame.display.flip()
                    visual_solve(sudoku, cells)

        screen.fill(white)

        # Draw board
        draw_board(cells, sudoku)

        # Create buttons
        reset_btn = draw_button(
            width - buffer - button_border*2 - button_width,
            height - button_height - button_border*2 - buffer,
            button_width,
            button_height,
            button_border,
            inactive_btn,
            black,
            'Select'
        )
        solve_btn = draw_button(
            width - buffer*2 - button_border*4 - button_width*2,
            height - button_height - button_border*2 - buffer,
            button_width,
            button_height,
            button_border,
            inactive_btn,
            black,
            'Visual Solve'
        )

        # Check if mouse over either button
        if reset_btn.collidepoint(pygame.mouse.get_pos()):
            reset_btn = draw_button(
                width - buffer - button_border*2 - button_width,
                height - button_height - button_border*2 - buffer,
                button_width,
                button_height,
                button_border,
                active_btn,
                black,
                'Select'
            )
        if solve_btn.collidepoint(pygame.mouse.get_pos()):
            solve_btn = draw_button(
                width - buffer*2 - button_border*4 - button_width*2,
                height - button_height - button_border*2 - buffer,
                button_width,
                button_height,
                button_border,
                active_btn,
                black,
                'Visual Solve'
            )
        if ExcaliburSudoku.step_count != 0:
            font = pygame.font.Font(None, 26)
            font.bold = False
            text = font.render(
                f"Total steps: {ExcaliburSudoku.step_count}", 1, black)
            xpos, ypos = (buffer, height - button_height -
                          button_border*2 - buffer)
            textbox = text.get_rect(topleft=(xpos, ypos))
            screen.blit(text, textbox)

        # Update screen
        pygame.display.flip()


if __name__ == '__main__':
    play()
