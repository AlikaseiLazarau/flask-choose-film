class FilmSelection:
    def __init__(self, user_id: int, room_id: str, selected_films_ids):
        self.userId = user_id
        self.roomId = room_id
        self.selectedFilmsIds = selected_films_ids

    def __repr__(self):
        return f"FilmSelection(userId={self.userId}, roomId={self.roomId}, selectedFilmsIds={self.selectedFilmsIds})"
