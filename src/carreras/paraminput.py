class ParamInputMixin:
    def ask_player_count(self) -> int:
        raise NotImplementedError

    def ask_player_names(self, count: int) -> list[str]:
        raise NotImplementedError

    def ask_race_length(self) -> int:
        raise NotImplementedError

    def get_game_params(self) -> tuple[int, int, list[str]]:
        players = self.ask_player_count()
        names = self.ask_player_names(players)
        length = self.ask_race_length()
        return players, length, names