def solution(orders, max_value):
    weight = [orders[item][0] for item in orders]
    value = [orders[item][1] for item in orders]
    n = len(orders)
    table = [[0 for _ in range(max_value + 1)] for __ in range(n + 1)]

    for k in range(n + 1):
        for s in range(max_value + 1):
            if k == 0 or s == 0:
                table[k][s] = 0
            elif weight[k - 1] <= s:
                table[k][s] = max(
                    value[k - 1] + table[k - 1][s - weight[k - 1]], table[k - 1][s]
                )
            else:
                table[k][s] = table[k - 1][s]

    res = table[n][max_value]
    s = max_value
    items_list = []
    for k in range(n, 0, -1):
        if res <= 0:
            break
        if res == table[k - 1][s]:
            continue
        else:
            items_list.append((weight[k - 1], value[k - 1]))
            res -= value[k - 1]
            s -= weight[k - 1]
    selected_stuff = []
    for search in items_list:
        for key, value in orders.items():
            if value == search and key not in selected_stuff:
                selected_stuff.append(key)
                break
    return selected_stuff
