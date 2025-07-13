import json
import os
import re
import time

RULES_PATH = os.path.join('config', 'rules.json')
LOG_PATH = os.path.join(os.sep, 'var', 'log', 'app', 'combined.log')
STATS_PATH = os.path.join('stats', 'server_stats.json')

def load_parsing_rules(path=RULES_PATH):
    """
    Грузим правила парсинга из JSON в словарь
    На вход — путь до rules.json, на выход — dict типа:
    {
        'ERROR': {'pattern': ..., 'groups': [...]},
        ...
    }
    """
    with open(path, 'r', encoding='utf-8') as f:
        rules = json.load(f)
    return rules

def read_log_lines(path=LOG_PATH):
    """
    Читаем лог-файл в список строк
    На вход — путь до лога, на выход — list строк
    """
    lines = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[WARN] Лог-файл не найден: {path}")
    return [line.rstrip('\n') for line in lines]

def parse_log_line(line, rules):
    """
    Парсим строку лога по всем правилам
    На вход — строка и rules, на выход — (event_type, dict с группами) или (None, None)
    """
    for event_type, rule in rules.items():
        pattern = rule['pattern']
        group_names = rule['groups']
        match = re.search(pattern, line)
        if match:
            groups = match.groups()
            groups_dict = dict(zip(group_names, groups))
            return event_type, groups_dict
    return None, None

def collect_stats(log_lines, rules):
    """
    Считаем статистику по серверам
    На вход — список строк и rules, на выход — dict типа:
    {
        'node1': {'errors': 1, 'warnings': 0},
        ...
    }
    """
    stats = {}
    for line in log_lines:
        event_type, groups = parse_log_line(line, rules)

        server = None
        if groups and 'server' in groups:
            server = groups['server']
        if not server:
            continue

        if server not in stats:
            stats[server] = {'errors': 0, 'warnings': 0}

        if event_type == 'ERROR':
            stats[server]['errors'] += 1
        elif event_type == 'WARN':
            stats[server]['warnings'] += 1
    
    return stats

def save_stats(stats, path=STATS_PATH):
    """
    Сохраняем статистику в JSON
    На вход — dict и путь, на выходе — файл.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    while True:
        rules = load_parsing_rules()
        log_lines = read_log_lines()
        stats = collect_stats(log_lines, rules)
        save_stats(stats)
        time.sleep(1)
