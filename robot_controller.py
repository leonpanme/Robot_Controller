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
barriers_in_row1 = 0
for data in env_data[0]:
    if data == 2:
        barriers_in_row1 += 1

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
    """
    判断机器人在当前位置是否可以移动，将移动限制到环境边界内.

    参数:
    loc -- 元组，机器人的当前坐标
    act -- 字符串, 机器人的下一步移动方向
    """
    # 将loc的行列信息解析
    current_row, current_column = loc
    # move_valid 来判断是否可以移动，True即可以，False为不可以
    move_valid = True

    if act == 'u':
        current_row -= 1
    elif act == 'd':
        current_row += 1
    elif act == 'l':
        current_column -= 1
    elif act == 'r':
        current_column += 1

    if current_row < 0 or current_column < 0 or current_row >= rows or current_column >= columns:
        move_valid = False
        return move_valid

    elif env_data[current_row][current_column] == 0:
        move_valid = True
        return move_valid

    elif env_data[current_row][current_column] == 3:
        move_valid = True
        return move_valid


def is_move_valid(env, loc, act):
    """
    判断机器人在当前位置是否可以移动.

    参数:
    env -- 列表, 迷宫的环境数据
    loc -- 元组，机器人的当前坐标
    act -- 字符串, 机器人的下一步移动方向
    """
    # 将loc的行列信息解析
    current_row, current_column = loc
    # move_valid 来判断是否可以移动，True即可以，False为不可以
    move_valid = True

    if act == 'u':
        current_row -= 1
    elif act == 'd':
        current_row += 1
    elif act == 'l':
        current_column -= 1
    elif act == 'r':
        current_column += 1

    if current_row < 0 or current_column < 0 or current_row >= rows or current_column >= columns:
        move_valid = False
        return move_valid

    elif env[current_row][current_column] == 2:
        move_valid = False
        return move_valid

    elif env[current_row][current_column] == 0:
        move_valid = True
        return move_valid

    elif env[current_row][current_column] == 3:
        move_valid = True
        return move_valid

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
    # 将loc的行列信息解析
    current_row, current_column = loc
    move_valid = is_move_valid(env_data, loc, act)
    if move_valid:
        if act == 'u':
            current_row -= 1
        elif act == 'd':
            current_row += 1
        elif act == 'l':
            current_column -= 1
        elif act == 'r':
            current_column += 1

        # 将移动后的新位置保存到 new_loc
        new_loc = (current_row, current_column)
        return new_loc

    else:
        print("Invalid move, try again!")


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
            print("没有找到宝藏，请重新运行或者增大循环次数。")
            break

# 运行
random_choose_actions(env_data, robot_current_loc)
