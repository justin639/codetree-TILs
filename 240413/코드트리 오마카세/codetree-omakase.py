from collections import deque

SUSHI = 0
CUSTOMER = 1
PICTURE = 2

L, Q = map(int, input().split())
que_l = [[0]*15000 for _ in range(L)]
# print(que_l)
que = deque(que_l)
name_dict = {}
query_list = []
table_list = [[0]*15000 for _ in range(L)]
customer_list = [-1] * 15000
T = 1
sushi_T = 0
custom_T = 0

def name_hash(name):
    if name not in name_dict:
        end = len(name_dict)
        name_dict[name] = end
        return end
    else:
        return name_dict[name]

for _ in range(Q):
    line = list(input().split())
    query_list.append(line)
    if len(line) == 4:
        in_type, t, x, name = line
        name_hash(name)
    elif len(line) == 5:
        in_type, t, x, name, n = line
        name_hash(name)

for k in range(Q):
    line = query_list[k]
    in_type, t, x, name, n = -1, 0, 0, "", 0
    if len(line) == 4:
        in_type, t, x, name = line
        in_type = SUSHI
    elif len(line) == 5:
        in_type, t, x, name, n = line
        in_type = CUSTOMER
    else:
        in_type, t = line
        in_type = PICTURE

    t = int(t)
    x = int(x)
    n = int(n)
    while T < t:
        last = que.pop()
        que.appendleft(last)
        que_l = list(que)
        for j in range(len(name_dict)):
            if customer_list[j] != -1:
                i = customer_list[j]
                if table_list[i][j] > 0 and que_l[i][j] > 0:
                    left = table_list[i][j] - que_l[i][j]
                    # print(name_list[j] + " " + str(left))
                    if left > 0:
                        table_list[i][j] = left
                        sushi_T -= que_l[i][j]
                        que_l[i][j] = 0
                    elif left == 0:
                        custom_T -= 1
                        sushi_T -= table_list[i][j]
                        customer_list[j] = -1
                        table_list[i][j] = 0
                        que_l[i][j] = 0
                    else:
                        custom_T -= 1
                        sushi_T -= table_list[i][j]
                        customer_list[j] = -1
                        table_list[i][j] = 0
                        que_l[i][j] = -left

        que = deque(que_l)
        T += 1

    que_l = list(que)
    if in_type == 0:
        name_n = name_hash(name)
        if table_list[x][name_n] > 0:
            table_list[x][name_n] -= 1
            if table_list[x][name_n] == 0:
                custom_T -= 1
        else:
            que_l[x][name_n] += 1
            sushi_T += 1
            que = deque(que_l)
    elif in_type == 1:
        name_n = name_hash(name)
        left = n - que_l[x][name_n]
        if left > 0:
            table_list[x][name_n] = left
            customer_list[name_n] = x
            custom_T += 1
            sushi_T -= que_l[x][name_n]
            que_l[x][name_n] = 0
        elif left == 0:
            table_list[x][name_n] = 0
            sushi_T -= n
            que_l[x][name_n] = 0
        else:
            table_list[x][name_n] = 0
            que_l[x][name_n] = -left
            sushi_T -= n
        que = deque(que_l)
    elif in_type == 2:
        print(str(custom_T) + " " + str(sushi_T))