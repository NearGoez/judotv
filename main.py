from contest_monitor import ContestMonitor
from constants import BASE_API_URL


if __name__ == "__main__":
    monitor = ContestMonitor(api_url=BASE_API_URL, poll_interval=30)
    monitor.run()
