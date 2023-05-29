import os
import sys
import time
import eyed3
from rich.console import Console
from rich.table import Table
from rich import box
from pygame import mixer


def get_mp3_files(folder_path):
    mp3_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".mp3"):
            mp3_files.append(file)
    return mp3_files


def get_track_info(track_path):
    audiofile = eyed3.load(track_path)
    artist = audiofile.tag.artist if audiofile.tag and audiofile.tag.artist else "Unknown"
    album = audiofile.tag.album if audiofile.tag and audiofile.tag.album else "Unknown"
    year = str(audiofile.tag.getBestDate()) if audiofile.tag and audiofile.tag.getBestDate() else "Unknown"
    genre = audiofile.tag.genre.name if audiofile.tag and audiofile.tag.genre else "Unknown"
    return artist, album, year, genre
    
def change_track_info(track_path):
    audiofile = eyed3.load(track_path)
    artist = input("Введите нового артиста (оставьте пустым для пропуска): ")
    if artist:
        audiofile.tag.artist = artist

    album = input("Введите новый альбом (оставьте пустым для пропуска): ")
    if album:
        audiofile.tag.album = album

    year = input("Введите новый год (оставьте пустым для пропуска): ")
    if year:
        audiofile.tag.year = year

    genre = input("Введите новый жанр (оставьте пустым для пропуска): ")
    if genre:
        audiofile.tag.genre = genre

    audiofile.tag.save()
    print("Информация о треке успешно изменена.")


def set_track_info(track_path, artist, album, year, genre):
    audiofile = eyed3.load(track_path)
    if audiofile.tag is None:
        audiofile.initTag()
    audiofile.tag.artist = artist
    audiofile.tag.album = album
    audiofile.tag.year = year
    audiofile.tag.genre = genre
    audiofile.tag.save()


def play_track(track_path):
    mixer.music.load(track_path)
    mixer.music.play()


def set_volume(volume):
    if 0 <= volume <= 100:
        new_volume = volume / 100.0
        mixer.music.set_volume(new_volume)
        print(f"Громкость установлена: {volume}%")


def increase_volume():
    current_volume = mixer.music.get_volume()
    if current_volume < 1.0:
        new_volume = min(current_volume + 0.1, 1.0)
        mixer.music.set_volume(new_volume)
        print(f"Громкость увеличена: {int(new_volume * 100)}%")


def decrease_volume():
    current_volume = mixer.music.get_volume()
    if current_volume > 0.0:
        new_volume = max(current_volume - 0.1, 0.0)
        mixer.music.set_volume(new_volume)
        print(f"Громкость уменьшена: {int(new_volume * 100)}%")


def change_volume(volume):
    if 0 <= volume <= 100:
        new_volume = volume / 100.0
        mixer.music.set_volume(new_volume)
        print(f"Громкость установлена: {volume}%")


def display_help():
    console = Console()
    console.clear()

    # Создаем таблицу для отображения меню помощи
    table = Table(box=box.SIMPLE)
    table.add_column("Команда", style="bold green")
    table.add_column("Описание", style="italic red")

    # Добавляем строки с командами и их описаниями
    table.add_row("next", "перейти к следующему треку")
    table.add_row("prev", "перейти к предыдущему треку")
    table.add_row("next_page", "перейти к следующей странице треков")
    table.add_row("prev_page", "перейти к предыдущей странице треков")
    table.add_row("stop", "остановить воспроизведение")
    table.add_row("less", "уменьшить громкость")
    table.add_row("more", "увеличить громкость")
    table.add_row("volume <уровень>", "установить уровень громкости (от 0 до 100)")
    table.add_row("change_info <индекс>", "изменить информацию о треке")
    table.add_row("play <индекс песни>", "воспроизвести трек по индексу")
    table.add_row("help", "отобразить это меню")
    table.add_row("exit", "выйти из программы")

    # Очищаем консоль и выводим таблицу меню помощи в центре экрана
    console.print("\n")
    console.print(table, justify="center")


def main():
    # Указываем путь к папке с MP3 файлами
    folder_path = "/Users/daniiltesluk/Documents/MUSIC/NEW ERA"

    # Инициализируем mixer
    mixer.init()

    # Получаем список MP3 файлов в папке
    mp3_files = get_mp3_files(folder_path)

    if len(mp3_files) == 0:
        print("Нет MP3 файлов в указанной папке.")
        return

    # Создаем консоль Rich
    console = Console()

    # Прослушивание треков
    current_index = 0
    total_tracks = len(mp3_files)
    tracks_per_page = 10

    while True:
        # Создаем таблицу для отображения треков
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Имя файла", style="dim")
        table.add_column("Индекс", justify="right")
        table.add_column("Артист", justify="left")
        table.add_column("Год", justify="left")
        table.add_column("Альбом", justify="left")
        table.add_column("Жанр", justify="left")

        # Определяем индексы треков для текущей страницы
        start_index = current_index
        end_index = min(current_index + tracks_per_page, total_tracks)
        current_page_tracks = mp3_files[start_index:end_index]

        # Заполняем таблицу треками текущей страницы
        for index, mp3_file in enumerate(current_page_tracks):
            track_path = os.path.join(folder_path, mp3_file)
            artist, album, year, genre = get_track_info(track_path)
            table.add_row(mp3_file, str(start_index + index + 1), artist, year, album, genre)

        # Очищаем консоль и отображаем таблицу треков
        console.clear()
        console.print(table)

        # Выводим информацию о текущей странице
        console.print(f"\nТекущая страница: {start_index + 1} - {end_index} из {total_tracks}")

        # Выводим информацию о текущем треке
        console.print(f"\nСейчас играет: [bold cyan]{mp3_files[current_index]}[/bold cyan]\n")

        command = input("Введите команду: ")

        if command == "exit":
            mixer.music.stop()
            mixer.quit()
            break
        elif command == "next":
            current_index = (current_index + 1) % total_tracks
        elif command == "prev":
            current_index = (current_index - 1) % total_tracks
        elif command == "next_page":
            current_index = (current_index + tracks_per_page) % total_tracks
        elif command == "prev_page":
            current_index = (current_index - tracks_per_page) % total_tracks
        elif command == "stop":
            mixer.music.stop()
            continue
        elif command == "less":
            decrease_volume()
        elif command == "more":
            increase_volume()
        elif command.startswith("volume"):
            try:
                volume = int(command.split()[1])
                change_volume(volume)
            except (ValueError, IndexError):
                print("Неверный формат команды volume. Используйте: volume <уровень>")
        elif command.startswith("change_info"):
            try:
                track_index = int(command.split()[1]) - 1
                if 0 <= track_index < total_tracks:
                    track_path = os.path.join(folder_path, mp3_files[track_index])
                    change_track_info(track_path)
                else:
                    print("Неверный индекс трека.")
            except (ValueError, IndexError):
                print("Неверный формат команды change_info. Используйте: change_info <индекс>")
        elif command.startswith("play"):
            try:
                track_index = int(command.split()[1]) - 1
                if 0 <= track_index < total_tracks:
                    track_path = os.path.join(folder_path, mp3_files[track_index])
                    play_track(track_path)
                    current_index = track_index
                else:
                    print("Неверный индекс трека.")
            except (ValueError, IndexError):
                print("Неверный формат команды play. Используйте: play <индекс песни>")
        elif command == "help":
            display_help()
            input("Нажмите Enter, чтобы продолжить...")
        else:
            continue

        track_path = os.path.join(folder_path, mp3_files[current_index])
        console.clear()
        console.print(table)
        console.print(f"\nСейчас играет: [bold cyan]{mp3_files[current_index]}[/bold cyan]\n")

        play_track(track_path)


if __name__ == "__main__":
    main()
