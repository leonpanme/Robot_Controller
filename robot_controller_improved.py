"""
导入 helper 模块来生成模拟环境数据
导入 random 模块的 choice 函数来随机选择
"""
import helper
from random import choice

env_data = helper.fetch_maze()

# 模拟环境的行数
rows = len(env_data[0:])
# 模拟环境的列数
columns = len(env_data[0])
# 模拟环境第三行第六列的元素
row_3_col_6 = env_data[2][5]

print("迷宫共有{}行, {}列，第三行第六列的元素是{}。".format(rows, columns, row_3_col_6))

# 计算模拟环境中，第一行的的障碍物个数。
# 列表解析
barriers_in_row1 = len([x for x in env_data[0] if x==2])

# 计算模拟环境中，第三列的的障碍物个数。
barriers_in_column3 = 0
row = 0
while row < rows:
    if env_data[row][2] == 2:
        barriers_in_column3 += 1
    row += 1
row = 0

print("迷宫中，第一行共有{}个障碍物，第三列共有{}个障碍物。".format(barriers_in_row1, barriers_in_column3))

"""
创建一个名为 loc_map 的字典，它有两个键值，分别为 start 和 destination，对应的值分别为起点和目标点的坐标.
从字典中取出 start 对应的值，保存在 robot_current_loc 对应的变量中，这个变量表示小车现在的位置。
"""
loc_map = {}
while row < rows:
    for data in env_data[row]:
        if data == 1:
            start_row = row
        if data == 3:
            destination_row = row
    row += 1
row = 0

for column in range(len(env_data[start_row])):
    if env_data[start_row][column] == 1:
        start_column = column

for column in range(len(env_data[destination_row])):
    if env_data[destination_row][column] == 3:
        destination_column = column

loc_map['start'] = (start_row,start_column)
loc_map['destination'] = (destination_row,destination_column)
print(loc_map)

robot_current_loc = loc_map['start']
print(robot_current_loc)


def is_move_valid_sepcial(loc, act):

    x, y = loc
    if act == 'u':
        x -= 1
    elif act == 'd':
        x += 1
    elif act == 'l':
        y -= 1
    elif act == 'r':
        y += 1

    return (0 <= y <= columns - 1) and (0 <= x <= rows - 1) and (env_data[x][y] != 2)


def is_move_valid(env, loc, act):
    """
    判断机器人在当前位置是否可以移动.

    参数:
    env -- 列表, 迷宫的环境数据
    loc -- 元组，机器人的当前坐标
    act -- 字符串, 机器人的下一步移动方向
    """
    x, y = loc
    if act == 'u':
        x -= 1
    elif act == 'd':
        x += 1
    elif act == 'l':
        y -= 1
    elif act == 'r':
        y += 1

    return (0 <= y <= columns - 1) and (0 <= x <= rows - 1) and (env[x][y] != 2)

"""
定义 valid_actions 的函数，输出机器人在这个位置所有的可行动作到列表 available_actions。

参数：
env：列表，虚拟环境的数据
loc：元祖，机器人所在的位置
"""
def valid_actions(env, loc):
    available_actions = []

    if is_move_valid(env, loc, 'u'):
        available_actions.append('u')
    if is_move_valid(env, loc, 'd'):
        available_actions.append('d')
    if is_move_valid(env, loc, 'l'):
        available_actions.append('l')
    if is_move_valid(env, loc, 'r'):
        available_actions.append('r')

    return available_actions

"""
定义名为 move_robot 的函数，返回机器人执行动作之后的新位置 new_loc。
参数：
loc: 元祖，机器人当前所在的位置
act: 字符串，即将执行的动作
"""
def move_robot(loc, act):

    move_dict = {
        'u': (-1,0),
        'd': (1,0),
        'l': (0,-1),
        'r': (0,1),
    }

    return loc[0] + move_dict[act][0], loc[1] + move_dict[act][1]


"""
定义名为 random_choose_actions 的函数，它有两个输入，分别为虚拟环境的数据 env_data，以及机器人所在的位置 loc。机器人会执行一个300次的循环，每次循环，他会执行以下任务：

利用上方定义的 valid_actions 函数，找出当前位置下，机器人可行的动作；
利用 random 库中的 choice 函数，从机器人可行的动作中，随机挑选出一个动作；
接着根据这个动作，利用上方定义的 move_robot 函数，来移动机器人，并更新机器人的位置；
当机器人走到终点时，输出“在第n个回合找到宝藏！”。
"""
def random_choose_actions(env, current_loc):
    # 回合计数
    round_count = 0
    loop_limit = 300
    for i in range(300):
        round_count += 1
        actions = valid_actions(env, current_loc)
        action = choice(actions)
        current_loc = move_robot(current_loc, action)

        if current_loc == loc_map['destination']:
            print("在第{}个回合找到宝藏!".format(round_count))
            break
        elif round_count >= loop_limit:
            print("没有找到宝藏，请重试或者增大循环次数。")
            break

# 运行
random_choose_actions(env_data, robot_current_loc)
