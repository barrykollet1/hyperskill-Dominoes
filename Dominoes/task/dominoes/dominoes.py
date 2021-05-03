import random
import queue


class Domino:

    def __init__(self):
        self.stock_pieces = []
        self.computer_pieces = []
        self.player_pieces = []
        self.domino_snake = queue.deque()

    def distribution(self):
        all_pieces = list()
        next_player = None

        # initialization of dominoes
        for i in range(7):
            for j in range(i, 7):
                all_pieces.append([i, j])
        random.shuffle(all_pieces)

        self.stock_pieces = all_pieces[:14]
        self.computer_pieces = all_pieces[14:21]
        self.player_pieces = all_pieces[21:]
        del all_pieces

        # determination of the next player
        for i in range(6, -1, -1):
            if [i, i] in self.computer_pieces:
                self.computer_pieces.remove([i, i])
                self.domino_snake.append(str([i, i]))
                next_player = 'player'
                break
            elif [i, i] in self.player_pieces:
                self.player_pieces.remove([i, i])
                self.domino_snake.append(str([i, i]))
                next_player = 'computer'
                break

        return next_player

    def snake_display(self):
        snake = list(self.domino_snake)
        if len(snake) <= 6:
            print("".join(snake))
        else:
            print("".join(snake[:3]), "...", "".join(snake[-3:]), sep="")

    def play(self, pieces, position):
        if position < 0:
            piece = pieces.pop(abs(position) - 1)
            if int(self.domino_snake[0][1]) == piece[0]:
                piece.reverse()
            self.domino_snake.appendleft(str(piece))
        elif position > 0:
            piece = pieces.pop(abs(position) - 1)
            if int(self.domino_snake[-1][-2]) == piece[1]:
                piece.reverse()
            self.domino_snake.append(str(piece))
        elif position == 0:
            if len(self.stock_pieces):
                pieces.append(self.stock_pieces.pop(0))

    def legal_move(self, pieces, position):
        snake_queue = None
        piece = pieces[abs(position) - 1]
        if position > 0:
            snake_queue = int(self.domino_snake[-1][-2])
        elif position < 0:
            snake_queue = int(self.domino_snake[0][1])

        if snake_queue in piece or position == 0:
            return True
        else:
            return False

    def computer_ia(self):
        count = []
        for i in range(7):
            nb_snake = "".join(self.domino_snake).count(str(i))
            nb_computer = sum([j.count(i) for j in self.computer_pieces])
            count.append(nb_snake + nb_computer)

        scores = {}
        for i, piece in enumerate(self.computer_pieces):
            # scores[str(piece)] = count[piece[0]] + count[piece[1]]
            scores[i+1] = count[piece[0]] + count[piece[1]]

        scores = sorted(scores.items(), key=lambda t: t[1])
        scores.reverse()

        return scores

    def check_end_game(self):
        first_car = self.domino_snake[0][1]
        last_car = self.domino_snake[-1][-2]
        end = True
        if len(self.player_pieces) == 0:
            print("Status: The game is over. You won!")
        elif len(self.computer_pieces) == 0:
            print("Status: The game is over. The computer won!")
        elif first_car == last_car and str(self.domino_snake).count(first_car) >= 8:
            print("Status: The game is over. It's a draw!")
        else:
            end = False

        return end

    def start(self):
        next_player = self.distribution()
        if next_player:
            while True:
                print(70 * "=")
                print(f"Stock size: {len(self.stock_pieces)}")
                print(f"Computer pieces: {len(self.computer_pieces)}")
                print()
                self.snake_display()
                print()
                print("Your pieces:")
                [print(i + 1, ":", j, sep="") for i, j in enumerate(self.player_pieces)]
                print()
                print("Computer", self.computer_pieces, sep='\n')
                if self.check_end_game():
                    break

                if next_player == 'player':
                    print("Status: It's your turn to make a move. Enter your command.")
                    while True:
                        try:
                            user_choice = int(input())
                        except ValueError:
                            print("Invalid input. Please try again.")
                            continue

                        if abs(user_choice) <= len(self.player_pieces):
                            if not self.legal_move(self.player_pieces, user_choice):
                                print("Illegal move. Please try again.")
                                continue
                            else:
                                self.play(self.player_pieces, user_choice)
                                next_player = 'computer'
                                break
                        else:
                            print("Invalid input. Please try again.")
                            continue
                elif next_player == 'computer':
                    print("Status: Computer is about to make a move. Press Enter to continue...")
                    input()

                    position = 0
                    for position_piecce in [i[0] for i in self.computer_ia()]:
                        if self.legal_move(self.computer_pieces, position_piecce):
                            position = position_piecce
                            break
                        elif self.legal_move(self.computer_pieces, -position_piecce):
                            position = -position_piecce
                            break

                    self.play(self.computer_pieces, position)
                    next_player = 'player'


domino_party = Domino()
domino_party.start()
