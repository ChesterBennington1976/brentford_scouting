
# ОТДЕЛ СКАУТИНГА «БРЕНТФОРДА»

# Реализовано 4 функциональных паттерна:
# 1. Декоратор 
# 2. Композиция функций
# 3. Функциональный конвейер
# 4. Частичное применение

import csv
from functools import partial, wraps

# Декоратор для отображения начала и завершения выполнения функции
def LogExecution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\nНачало выполнения: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Завершение выполнения: {func.__name__}")
        return result
    return wrapper

# Функция композиции
def Compose(*functions):
    def composed(value):
        for function in reversed(functions):
            value = function(value)
        return value
    return composed

# Приведение названия лиги к единому формату
def ReplaceLeagueAlias(league):
    aliases = {
        "апл": "epl",
        "premier league": "epl",
        "чемпионшип": "championship",
        "вейккауслига": "veikkausliiga",
        "рпл": "rpl",
        "russian premier league": "rpl"
    }

    return aliases.get(league, league)

# Композиция: очистка названия лиги и приведение к единому формату
NormalizeLeague = Compose(ReplaceLeagueAlias, str.lower, str.strip)

# Функциональный конвейер
def Pipeline(data, *functions):
    for function in functions:
        data = function(data)
    return data

# Авторизация пользователя
def Login():
    while True:
        login = input("Введите логин: ")
        password = input("Введите пароль: ")

        if login == "Кит Эндрюс" and password == "люблю Ирландию":
            return True
        else:
            print("Неверный логин или пароль. Попробуйте ещё раз.")

# Главное меню программы
def ShowMenu():
    print("\nДобро пожаловать в скаутский отдел «Брентфорда!»")

    if Login():
        print("\nВы успешно вошли в систему!")

        while True:
            print("\n" + "=" * 45)
            print("       BRENTFORD FC — SCOUTING DEPARTMENT")
            print("=" * 45)
            print("1. Поиск футболистов")
            print("2. Просмотр базы данных")
            print("3. Статистика базы данных")
            print("4. Информация о программе")
            print("5. Выход")
            print("=" * 45)

            choice = input("Выберите действие: ")

            if choice == "1":
                SearchPlayers()

            elif choice == "2":
                ViewDatabase()

            elif choice == "3":
                ShowDatabaseStatistics()

            elif choice == "4":
                ShowProgramInfo()

            elif choice == "5":
                print("\nРабота программы завершена. До свидания, Кит Эндрюс!")
                break

            else:
                print("\nНеверный пункт меню. Попробуйте ещё раз.")

# Загрузка футболистов из CSV-файла
@LogExecution
def LoadPlayers(league):
    filename = ""
    league = NormalizeLeague(league)

    if league == "epl":
        filename = "epl.csv"
    elif league == "championship":
        filename = "championship.csv"
    elif league == "veikkausliiga":
        filename = "veikkausliiga.csv"
    elif league == "rpl":
        filename = "rpl.csv"

    players = []

    try:
        with open(filename, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for player in reader:
                players.append(player)

    except FileNotFoundError:
        print("Файл с данными выбранной лиги не найден!")
        return []

    if not players:
        print("В выбранной лиге нет данных о футболистах!")

    return players

# Получение критериев поиска
def GetCriteria():
    position = input("Введите позицию футболиста: ")
    league = input("Введите лигу: ")

    league = NormalizeLeague(league)

    age = int(input("Максимальный возраст футболиста: "))
    price = float(input("Максимальная стоимость футболиста: "))

    while True:
        goals = int(input("Минимальное количество голов: "))

        if goals > 0:
            break
        else:
            print("Количество голов должно быть больше нуля!")

    while True:
        assists = int(input("Минимальное количество голевых передач: "))

        if assists > 0:
            break
        else:
            print("Количество передач должно быть больше нуля!")

    while True:
        passAccuracy = float(input("Минимальная точность передач (в %): "))

        if 0 < passAccuracy <= 100:
            break
        else:
            print("Точность передач должна быть больше 0 и не превышать 100!")

    return {
        "position": position,
        "league": league,
        "age": age,
        "price": price,
        "goals": goals,
        "assists": assists,
        "passAccuracy": passAccuracy
    }

# Вывод информации о футболисте
def ShowInfo(player):
    for key, value in player.items():
        print(f"{key}: {value}")

# Фильтрация футболистов по основным критериям
def FilterPlayers(players, criteria):
    filteredPlayers = []

    for player in players:
        if (
            player["position"].strip().upper() == criteria["position"].strip().upper()
            and NormalizeLeague(player["league"]) == criteria["league"]
            and int(player["age"].strip()) <= criteria["age"]
            and float(player["price"].strip()) <= criteria["price"]
        ):
            filteredPlayers.append(player)
    return filteredPlayers

# Анализ игровых показателей
@LogExecution
def Analytics(players, criteria):
    candidates = FilterPlayers(players, criteria)

    print(f"Найдено кандидатов: {len(candidates)}")

    correctCandidates = []

    for player in candidates:
        if (
            int(player["goals"]) >= criteria["goals"]
            and int(player["assists"]) >= criteria["assists"]
            and float(player["passAccuracy"]) >= criteria["passAccuracy"]
        ):
            correctCandidates.append(player)

    print(f"Подходящих кандидатов: {len(correctCandidates)}")

    # Отмечаем выполнение дополнительных требований
    for player in candidates:
        if player in correctCandidates:
            player["criteria_match"] = "Да"
        else:
            player["criteria_match"] = "Нет"
    return candidates

# Расчёт рейтинга футболистов
@LogExecution
def CalculateRating(candidates, criteria):
    for player in candidates:
        goalsScore = int(player["goals"]) / criteria["goals"]
        assistsScore = int(player["assists"]) / criteria["assists"]
        passAccuracyScore = float(player["passAccuracy"]) / criteria["passAccuracy"]

        rating = (
            goalsScore * 0.4
            + assistsScore * 0.3
            + passAccuracyScore * 0.3
        )

        player["rating"] = rating * 100
    return candidates

# Сортировка футболистов по рейтингу
@LogExecution
def RankPlayers(candidates):
    sortedCandidates = sorted(
        candidates,
        key=lambda player: player["rating"],
        reverse=True
    )
    return sortedCandidates

# Вывод результатов поиска
def ShowResults(sortedCandidates, criteria):
    if not sortedCandidates:
        print("\nК сожалению, подходящих футболистов не найдено!")
        return

    print("\nРЕЗУЛЬТАТЫ ПОИСКА")
    print("=" * 45)

    for number, player in enumerate(sortedCandidates, start=1):
        print(f"\nМесто в рейтинге: {number}")

        ShowInfo(player)

        print(
            f"\nФутболист забил {player['goals']} голов "
            f"(минимум по запросу: {criteria['goals']})."
        )

        print(
            f"Футболист отдал {player['assists']} голевых передач "
            f"(минимум по запросу: {criteria['assists']})."
        )

        print(
            f"Точность передач составляет {player['passAccuracy']}% "
            f"(минимум по запросу: {criteria['passAccuracy']}%)."
        )

        print(f"Индекс соответствия: {player['rating']:.2f}\n")
        print("-" * 40)

# Поиск футболистов
def SearchPlayers():
    criteria = GetCriteria()
    players = LoadPlayers(criteria["league"])

    if not players:
        return

    # Частичное применение: заранее передаём критерии поиска функциям
    analyticsWithCriteria = partial(Analytics, criteria=criteria)
    ratingWithCriteria = partial(CalculateRating, criteria=criteria)

    # ПАТТЕРН Функциональный конвейер: результат каждой функции передаётся следующей
    sortedCandidates = Pipeline(
        players,
        analyticsWithCriteria,
        ratingWithCriteria,
        RankPlayers
    )
    ShowResults(sortedCandidates, criteria)

# Просмотр базы данных по конкретной лиге
def ViewDatabase():
    league = input("\nВведите лигу: ")

    players = LoadPlayers(league)

    if not players:
        return

    print(f"\nВсего футболистов в базе: {len(players)}")
    print("=" * 40)

    for number, player in enumerate(players, start=1):
        print(f"\nФутболист №{number}")
        ShowInfo(player)
        print("-" * 40)

# Статистика базы данных
def ShowDatabaseStatistics():
    league = input("\nВведите лигу: ")

    players = LoadPlayers(league)

    if not players:
        return

    clubs = set()
    positions = {}

    for player in players:
        clubs.add(player["club"])

        position = player["position"]
        positions[position] = positions.get(position, 0) + 1

    print("\nСТАТИСТИКА БАЗЫ ДАННЫХ")
    print("=" * 40)
    print(f"Количество футболистов: {len(players)}")
    print(f"Количество клубов: {len(clubs)}")

    print("\nРаспределение по позициям:")

    for position, count in positions.items():
        print(f"{position}: {count}")

    print("-" * 40)

# Информация о программе
def ShowProgramInfo():
    print("\nBRENTFORD FC — SCOUTING DEPARTMENT")
    print("=" * 40)

    print("Программа предназначена для поиска и анализа футболистов.")

    print("\nОсновные возможности:")
    print("1. Поиск игроков по заданным критериям.")
    print("2. Фильтрация по лиге, позиции, возрасту и стоимости.")
    print("3. Анализ игровых показателей.")
    print("4. Расчёт индивидуального рейтинга.")
    print("5. Сортировка футболистов по рейтингу.")
    print("6. Просмотр базы данных и статистики.")

    print("\nИспользуемые паттерны функционального программирования:")
    print("1. Functional Pipeline")
    print("2. Decorator")
    print("3. Function Composition")
    print("4. Partial Application")

    print("=" * 40)

# Запуск программы
if __name__ == "__main__":
    ShowMenu()
