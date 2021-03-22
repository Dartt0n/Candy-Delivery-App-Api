def solution(orders, max):
    A = max
    n = len(orders)
    weight = [i[0] for i in orders.values()]
    value = [i[1] for i in orders.values()]

    V = [[0 for i in range(A + 1)] for i in range(n + 1)]

    for i in range(n + 1):
        for a in range(A + 1):
            if weight[i - 1] <= a:
                V[i][a] = max(value[i - 1] + V[i - 1][a - weight[i - 1]], V[i - 1][a])
            else:
                V[i][a] = V[i - 1][a]

    res = V[n][A]
    a = A
    items_list = []
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == V[i- 1][a]:
            continue
        else:
            items_list.append((weight[i-1], value[i-1]))
            res -= value[i - 1]
            a -= weight[i - 1]

    selected = []

    for search in items_list:
        for key, value in orders.items():
            if value == search:
                selected.append(key)

    return selected