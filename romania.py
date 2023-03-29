from collections import deque
import functools
import time
import math


class State(object):  # 每一个城市的信息
    def __init__(self, name, neighbor_num):
        self.name = name  # 城市名
        self.neighbor_num = neighbor_num  # 相邻的城市个数
        self.nextstate = {
        }  # 相邻城市的信息


state_num = 0  # 城市数量
graph = {}  # 保存罗马尼亚的图：'城市名'：城市信息
cities_name = []  # 保存各城市的名字
daijia = {}  # 存储每种算法的最小代价值
cost = {}  # 存储每个城市的坐标，计算h(n)


def file_input(file1, file2):  # 城市信息文件的读取
    global graph
    global state_num
    with open(file1, 'r', encoding='utf8') as f1:
        for line in f1.readlines():  # 读取每一行城市信息
            state_num += 1  # 计算城市数量(行数)
            line = list(line.split())
            t = State(line[0], int(line[2]))
            line = line[3:]
            for i, j in zip(range(0, len(line), 2), range(0, t.neighbor_num)):
                t.nextstate[j] = {line[i]: int(line[i + 1])}  # 存取该城市所有相邻城市的信息
            graph[t.name] = t  # 添加当前城市
        f1.close()
    with open(file2, 'r', encoding='utf8') as f2:
        for line in f2.readlines():
            line = str(line).split()
            cities_name.extend(line)
        f2.close()


def zuobiao(file3):  # 读取每个城市的坐标信息，放在字典里面
    global cost
    with open(file3, 'r', encoding='utf8') as f3:
        for line in f3.readlines():  # 读取每一行城市信息
            line = list(str(line).split())
            cost[line[0]] = line[1:]  # 存的坐标信息是str型
        f3.close()


def S_route(arr, go):  # 展示搜索路径
    cost = 0  # 总花费
    reached = []  # 存储已经计算过路径值的城市
    for i, j in zip(range(len(arr)), range(len(arr) - 1, -1, -1)):
        if (i == len(arr) - 1):
            print(arr[i])
        else:
            print(arr[i] + "-->", end="")
            for k in range(graph[arr[j]].neighbor_num):
                    for g in graph[arr[j]].nextstate.setdefault(k,'0'):
                        if (g not in reached and g in arr and j != '0'
                            ):  # 判断，如果该城市不在已计算过的列表以及在close表中，则加上路径值，从下往上计算
                            cost += graph[arr[j]].nextstate[k][g]
                            reached.append(g)
    daijia[go] = cost
    print("总代价为：", cost)
    print("经过的节点数为：", len(arr))


def BFS(start, goal):  # 宽度优先搜索
    close = []  # 已拓展的城市，存的是名字
    open = deque()  # 待拓展的城市，存的是名字
    open.append(start)
    while open:
        print("当前open表的状态是:", open, end="")
        print("     当前close表的状态是:", close)
        city = open.popleft()
        if (city not in close):
            if (city == goal):  # 找到目标城市
                close.append(city)
                print("当前open表的状态是:", open, end="")
                print("     当前close表的状态是:", close)
                print("宽度优先搜索的搜索路径是：")
                S_route(close, 'BFS')
                return
            else:
                close.append(city)
                a =(graph[city].neighbor_num)
                for i in range(a):
                        for j in graph[city].nextstate.setdefault(i,'0'):
                            if(j != '0'and j not in open and j not in close):
                                open.append(j)                      
    print("搜索失败")


def DFS(start, goal):
    close = []  # 已拓展的城市，存的是名字
    open = []  # 待拓展的城市，存的是名字,模拟栈
    open.append(start)
    while open:
        print("当前open表的状态是:", open, end="")
        print("     当前close表的状态是:", close)
        city = open.pop()
        if (city not in close):
            if (city == goal):  # 找到目标城市
                close.append(city)
                print("当前open表的状态是:", open, end="")
                print("     当前close表的状态是:", close)
                print("深度优先搜索的搜索路径是：")
                S_route(close, 'DFS')
                return
            else:
                close.append(city)
                for i in range(graph[city].neighbor_num):
                        for j in graph[city].nextstate.setdefault(i,'0'):
                            if(j != '0'and j not in open and j not in close):
                                open.append(j)
    print("搜索失败")


dic = {}  # 存放从起始点到该点的代价值
destination = {}  # 存放当前各点到goal的h(n)


def compute_des(g):  # 计算当前各点到goal的h(n)
    global destination
    for i in cost:
        if (i == g):
            destination[i] = 0
        else:
            destination[i] = math.sqrt((int(cost[i][0]) - int(cost[g][0])) *
                                       (int(cost[i][0]) - int(cost[g][0])) +
                                       (int(cost[i][1]) - int(cost[g][1])) *
                                       (int(cost[i][1]) - int(cost[g][1])))


def sot(C1, C2):
    C1 = graph[C1]
    C2 = graph[C2]
    if (dic[C1.name] + destination[C1.name] <
            dic[C2.name] + destination[C2.name]):  # 总代价小的排前面
        return -1
    if (dic[C1.name] + destination[C1.name] >
            dic[C2.name] + destination[C2.name]):
        return 1
    if (dic[C1.name] + destination[C1.name] == dic[C2.name] +
            destination[C2.name]):  # 总代价相等时，h(n)小的排前面
        if (destination[C1.name] < destination[C2.name]):
            return -1
    return 0


def Astar(start, goal):
    open = deque()  # 待拓展的城市，存的是名字
    close = []  # 已拓展的城市，存的是名字
    open.append(start)
    compute_des(goal)  # 调用函数求h(n)
    while open:
        current = []  # 存每一轮当前城市的邻居城市，每一轮新的循环更新
        print("当前open表的状态是:", open, end="")
        print("     当前close表的状态是:", close)
        city = open.popleft()
        if (city not in close):
            if (city == goal):  # 找到目标城市
                close.append(city)
                print("当前open表的状态是:", open, end="")
                print("     当前close表的状态是:", close)
                print("A*搜索的搜索路径是：")
                S_route(close, 'A*')
                return
            else:
                close.append(city)
                for i in range(graph[city].neighbor_num):
                    if(i<=2):
                        for j in graph[city].nextstate[i]:
                            current.append(j)
                            open.append(j)


# 获取从起点到当前点代价值信息
        for g in range(len(current)):
            for q in range(graph[close[-1]].neighbor_num):
                if(q<=2):
                    if (list(graph[close[-1]].nextstate[q].keys())[0] == current[g]
                        ):
                        if (close[-1] == start):
                            dic[current[g]] = list(
                                graph[close[-1]].nextstate[q].values())[0]
                        else:
                            dic[current[g]] = list(graph[close[-1]].nextstate[q].
                                                values())[0] + dic[close[-1]]
        open = deque(
            sorted(open, key=functools.cmp_to_key(sot))
        )  # f(n) = g(n) + h(n)按综合优先级重新排序open表，g(n)是到达此结点已经花费的代价，h(n)是从该结点到目标结点所花代价.f(n)小的排前面
    print("搜索失败")


def compare():  # 算法时间维度，到达目的地花费代价做对比，可将此可视化
    print("DFS搜索算法时间为：", str((end1 - start1) * 1000) + 'ms')  # 单位为ms
    print("BFS搜索算法时间为：", str((end2 - start2) * 1000) + 'ms')
    print("A*算法时间为：", str((end3 - start3) * 1000) + 'ms')
    print("到达目的地花费代价为：", daijia)



file_input("C:/Users/guan/Desktop/information/cities information.txt","C:/Users/guan/Desktop/information/cities name.txt")
zuobiao("C:/Users/guan/Desktop/information/citie zuobiao.txt")
while (1):
    num = int(input("请选择相关的搜索算法(1.宽度优先搜索/2.深度优先搜素/3.A*搜索/4.退出搜索)："))
    if (num == 4):
        break
    st, go = map(int, input("请选择开始州以及目标州的序号(1-20),以空格分隔：").split())
    if (num == 1 and 1 <= st <= 20 and 1 <= go <= 20):
        start1 = time.time()  
        BFS(cities_name[st - 1], cities_name[go - 1])
        end1 = time.time()  
    elif (num == 2 and 1 <= st <= 20 and 1 <= go <= 20):
        start2 = time.time()  
        DFS(cities_name[st - 1], cities_name[go - 1])
        end2 = time.time()  
    elif (num == 3 and 1 <= st <= 20 and 1 <= go <= 20):
        start3 = time.time()  
        Astar(cities_name[st - 1], cities_name[go - 1])
        end3 = time.time()  
    else:
        print("您的输入有误，请重新输入！")  
compare()
