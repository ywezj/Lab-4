LENGTH = 4
WIDTH = 2
MAX_VOLUME = LENGTH * WIDTH
start_points = 15

items = {
    'r': {'points': 25, 'volume': 3},
    'p': {'points': 15, 'volume': 2},
    'a': {'points': 15, 'volume': 2},
    'm': {'points': 20, 'volume': 2},
    'i': {'points': 5, 'volume': 1},
    'k': {'points': 15, 'volume': 1},
    'x': {'points': 20, 'volume': 3},
    't': {'points': 25, 'volume': 1},
    'f': {'points': 15, 'volume': 1},
    'd': {'points': 10, 'volume': 1},
    's': {'points': 20, 'volume': 2},
    'c': {'points': 20, 'volume': 2},
}

items_list = list(items.items())


def calculate_optimal_items(items, max_volume=MAX_VOLUME):
    dp = [(0, [])] * (max_volume + 1)
    
    for name, value in items:
        points, volume = value['points'], value['volume']
        
        for v in range(max_volume, volume - 1, -1):
            current_points, current_items = dp[v - volume]
            new_points = current_points + points
            if new_points > dp[v][0]:
                dp[v] = (new_points, current_items + [(name, volume)])
    
    max_points, selected_items = max(dp)
    return selected_items, max_points


def calculate_score(selected_items):
    all_points = sum(item['points'] for item in items.values())
    points = sum(items[name]['points'] for name, _ in selected_items)
    score = start_points + points - (all_points - points)
    return score


def pack_items(selected_items, length=LENGTH, width=WIDTH):
    grid = [[0] * length for _ in range(width)]
    item_placement = {
        1: [],
        2: [],
        3: [],
        4: [],
    }

    for name, vol in selected_items:
        item_placement[vol].append(f'[{name}]')
    
    def place_items(volume, positions):
        while item_placement[volume]:
            item = item_placement[volume].pop(0)
            for pos in positions:
                x, y = pos
                if grid[x][y] == 0:
                    grid[x][y] = item
                else:
                    break

    place_items(3, [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)])
    place_items(2, [(0, 0), (0, 2), (0, 3), (1, 0), (1, 2), (1, 3)])
    
    for l in range(length):
        for w in range(width):
            if grid[w][l] == 0 and item_placement[1]:
                grid[w][l] = item_placement[1].pop(0)
    
    return grid


if __name__ == '__main__':
    selected_items, max_points = calculate_optimal_items(items_list)
    final_score = calculate_score(selected_items)
    backpack = pack_items(selected_items)
    
    for line in backpack:
        print(*line, sep=',')
    print('Результат:', final_score)


#Решение для допзадания

import itertools

LENGTH = 7
WIDTH = 1
MAX_VOLUME = LENGTH * WIDTH
start_points = 15

items = {
    'r': {'points': 25, 'volume': 3},
    'p': {'points': 15, 'volume': 2},
    'a': {'points': 15, 'volume': 2},
    'm': {'points': 20, 'volume': 2},
    'i': {'points': 5, 'volume': 1},
    'k': {'points': 15, 'volume': 1},
    'x': {'points': 20, 'volume': 3},
    't': {'points': 25, 'volume': 1},
    'f': {'points': 15, 'volume': 1},
    'd': {'points': 10, 'volume': 1},
    's': {'points': 20, 'volume': 2},
    'c': {'points': 20, 'volume': 2},
}

def calculate_optimal_items_all_combinations(items, max_volume=MAX_VOLUME):
    all_combinations = []
    for r in range(len(items) + 1):
        for combination in itertools.combinations(items.keys(), r):
            selected_items = list(combination)
            total_volume = sum(items[item]['volume'] for item in selected_items)
            if total_volume <= max_volume:
                valid_combination = True
                if 'i' not in selected_items and 'd' not in selected_items:
                    valid_combination = False
                if valid_combination:
                    all_combinations.append(selected_items)
    return all_combinations

def calculate_score(selected_items):
    all_points = sum(items[name]['points'] for name in items)
    points = sum(items[name]['points'] for name in selected_items)
    score = start_points + points - (all_points - points)
    return score

def pack_items(selected_items, length=LENGTH, width=WIDTH):
    grid = [0] * length
    i = 0
    for item in selected_items:
        for j in range(items[item]['volume']):
            grid[i] = f'[{item}]'
            i += 1
    return grid


if __name__ == "__main__":
    all_combinations = calculate_optimal_items_all_combinations(items)
    positive_score_combinations = []

    for combination in all_combinations:
        score = calculate_score(combination)
        if score > 0:
            positive_score_combinations.append((combination, score))

    if positive_score_combinations:
        print("Комбинации с положительным счетом:")
        for combination, score in positive_score_combinations:
            backpack = pack_items(combination)
            print(*backpack, sep=", ")
            print(f"Score: {score}")
    else:
        print("Отсутствие доказанно")
