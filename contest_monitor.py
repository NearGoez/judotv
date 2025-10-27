import time
import requests
from typing import Any

from streaming_session import StreamingSession

class ContestMonitor:
    def __init__(self, api_url: str, poll_interval: int = 30) -> None:
        self.api_url = api_url

        self.poll_interval = poll_interval
        self.last_contest_id = None

        self._competition_schedule: list[tuple[int, str]] = []
        self.active_streaming_sessions: list[StreamingSession] = []

    def run(self) -> None:

        self.fetch_competition_schedule()

        self.find_active_contest()
        pass

    def fetch_competition_schedule(self) -> None:

        if not self._competition_schedule:
            competitions_fetched = self.fetch_competitions()

            self._competition_schedule = [
                (int(comp['idCompetition']), comp['dateFrom'])
                for comp in competitions_fetched
            ]

            self._competition_schedule.sort(
                key=lambda x: x[1], reverse=True
            )
        print(self._competition_schedule[0])


    def fetch_competitions(self) -> list[dict[str, Any]]:

        response = requests.get(self.api_url + 'competitions')
        response.raise_for_status()

        return response.json().get('list', [])

    def find_active_contest(self) -> None:

        while True:
            time.sleep(self.poll_interval)
            pass