import time
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from yt_dlp import YoutubeDL, DownloadError
from rich import print, get_console
from rich.live import Live
from rich.console import Group
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
    MofNCompleteColumn,
    TaskID,
)

from .error_handeling import YDL_log_filter, reaction_to
from ..episode import Episode
from ..langs import Lang


logger = logging.getLogger(__name__)
logger.addFilter(YDL_log_filter)

console = get_console()
download_progress = Progress(
    TextColumn("[bold blue]{task.fields[episode_name]}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    DownloadColumn(),
    "•",
    TransferSpeedColumn(),
    "•",
    TimeRemainingColumn(),
    console=console,
)
total_progress = Progress(
    TextColumn("[bold cyan]{task.description}"),
    BarColumn(bar_width=None),
    MofNCompleteColumn(),
    TimeRemainingColumn(),
    console=console,
)
progress = Group(total_progress, download_progress)


def download(
    episode: Episode,
    path: Path,
    prefer_languages: list[Lang] = ["VO"],
    concurrent_fragment_downloads=3,
):
    if not any(episode.languages.values()):
        print("[red]No player available")
        return

    me = download_progress.add_task("download", episode_name=episode.name, total=None)
    task = download_progress.tasks[me]

    full_path = (
        path / episode.serie_name / episode.season_name / episode.name
    ).expanduser()

    def hook(data: dict):
        if data.get("status") != "downloading":
            return

        task.total = data.get("total_bytes") or data.get("total_bytes_estimate")
        download_progress.update(me, completed=data.get("downloaded_bytes", 0))

    option = {
        "outtmpl": {"default": f"{full_path}.%(ext)s"},
        "concurrent_fragment_downloads": concurrent_fragment_downloads,
        "progress_hooks": [hook],
        "logger": logger,
    }

    for player in episode.consume_player(prefer_languages):
        retry_time = 1
        sucess = False

        while True:
            try:
                with YoutubeDL(option) as ydl:  # type: ignore
                    error_code: int = ydl.download([player])  # type: ignore

                    if not error_code:
                        sucess = True
                    else:
                        logger.fatal(
                            "The download error with the code %s. Please report this to the developper.",
                            error_code,
                        )

                    break

            except DownloadError as execption:
                match reaction_to(execption.msg):
                    case "continue":
                        break

                    case "retry":
                        logger.warning(
                            "Download interrupted. Retrying in %ss.", retry_time
                        )
                        time.sleep(retry_time)
                        retry_time *= 2

                    case "crash":
                        raise execption

                    case "":
                        logger.fatal(
                            "The above error wasn't handle. Please report it to the developper."
                        )
                        break

        if sucess:
            break

    download_progress.update(me, visible=False)
    if total_progress.tasks:
        total_progress.update(TaskID(0), advance=1)


def multi_download(
    episodes: list[Episode],
    path: Path,
    concurrent_downloads={},
    prefer_languages: list[Lang] = ["VO"],
):
    """
    Not sure if you can use this function multiple times
    """
    total_progress.add_task("Downloaded", total=len(episodes))
    with Live(progress, console=console):
        with ThreadPoolExecutor(
            max_workers=concurrent_downloads.get("video", 1)
        ) as executor:
            for episode in episodes:
                executor.submit(
                    download,
                    episode,
                    path,
                    prefer_languages,
                    concurrent_downloads.get("fragment", 1),
                )
