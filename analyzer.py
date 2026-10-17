
from datetime import datetime


def parse_commit_line(line):
    """Перетворює один рядок логу на словник."""
    parts = line.strip().split("|", 3)

    # Перевіряємо, чи є всі 4 поля
    if len(parts) != 4:
        return None

    commit_hash, author, date_text, message = parts

    try:
        commit_date = datetime.strptime(
            date_text, "%Y-%m-%d %H:%M:%S %z"
        )
    except ValueError:
        return None

    # Перевіряємо, чи заповнені обов'язкові поля
    if not commit_hash or not author or not message:
        return None

    return {
        "hash": commit_hash,
        "author": author,
        "date": commit_date,
        "message": message,
    }


def load_log(filename):
    """Читає файл і повертає список комітів."""
    commits = []

    try:
        with open(filename, "r", encoding="utf-8-sig") as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue

                commit = parse_commit_line(line)

                if commit is None:
                    print(
                        f"Попередження: неправильний формат "
                        f"у рядку {line_number} файлу {filename}"
                    )
                    continue

                commits.append(commit)

    except FileNotFoundError:
        print(f"Помилка: файл '{filename}' не знайдено.")
        return None

    return commits


def analyze_commits(commits):
    """Обчислює статистику комітів."""
    if not commits:
        return None

    # Сортуємо коміти від найстарішого до найновішого
    sorted_commits = sorted(
        commits, key=lambda commit: commit["date"]
    )

    authors = {commit["author"] for commit in commits}

    return {
        "count": len(commits),
        "authors": len(authors),
        "first": sorted_commits[0],
        "last": sorted_commits[-1],
    }


def format_report(branch, stats):
    """Формує текстовий звіт для гілки."""
    if stats is None:
        return f"=== Звіт по гілці: {branch} ===\nНемає коректних комітів."

    first = stats["first"]
    last = stats["last"]

    return (
        f"=== Звіт по гілці: {branch} ===\n\n"
        f"Комітів: {stats['count']}\n"
        f"Авторів: {stats['authors']}\n\n"
        f"Перший коміт: {first['date']:%Y-%m-%d} — "
        f'"{first["message"]}"\n'
        f"Останній коміт: {last['date']:%Y-%m-%d} — "
        f'"{last["message"]}"'
    )


def analyze_branch(branch, filename):
    """Читає лог, аналізує його та друкує звіт."""
    commits = load_log(filename)

    if commits is None:
        return

    stats = analyze_commits(commits)
    print(format_report(branch, stats))
    print()


def main():
    """Запускає аналіз обох гілок."""
    analyze_branch("main", "main.log")
    analyze_branch("feature/stats", "feature_stats.log")


if __name__ == "__main__":
    main()

