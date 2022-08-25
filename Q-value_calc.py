# %%


f = open("./data/Chen data.csv")
s = f.readline()
columes = s

k = 0 
groups = []
origin_value = []
s = f.readline()

while s:
    line_items = s.strip('\n').split(',')
    groups.append(line_items[0])
    origin_value.append(float(line_items[1]))
    s = f.readline()
    k += 1

f.close()

# %%
# 开始检验
Q_value = 0.90
value = []
abnormal_value = []
num_of_each_group = 3
i = 0
while i < k:
    x = []
    for j in range(num_of_each_group):
        x.append(origin_value[i + j])

    # 组内排序，数多了就改这一部分
    if x[0] > x[1]:
        (x[0], x[1]) = (x[1], x[0])
    if x[0] > x[2]:
        (x[0], x[2]) = (x[2], x[0])
    if x[1] > x[2]:
        (x[1], x[2]) = (x[2], x[1])
    max_range = x[2] - x[0] # 极差

    for j in range(num_of_each_group):
        value.append(x[j])
    i = i + num_of_each_group

    q = [] # Q值
    # 对于最大值或最小值，与他最邻近的元素即为下一个元素
    # 最小值
    q.append((x[1] - x[0]) / max_range)
    # 以下为在三个数的情形下
    # 比较最邻近元素
    if (x[2] - x[1]) > (x[1] - x[0]):
        # x[0]是最邻近
        q.append((x[1] - x[0]) / max_range)
    else:
        # x[2]最邻近
        q.append((x[2] - x[1]) / max_range)
    # 对于最大值
    q.append((x[2] - x[1]) / max_range)

    # 比较Q值
    flag_abnormal = False
    for j in range(3):
        if q[j] < Q_value:
            # 通过检验
            continue
        else:
            flag_abnormal = True
            abnormal_value.append(x[j])
    if flag_abnormal is False:
        abnormal_value.append(-1) # 表示这一组没有异常值


# %%
# 移去异常值
f = open("./data/Data filtered.CSV", 'w')
f.write(columes)
i = 0
while i < k:
    if abnormal_value[int(i / num_of_each_group)] == -1:
        # 该组无异常值
        for j in range(i, i + num_of_each_group):
            f.write(groups[j] + ',')
            f.write(str(origin_value[j]) + '\n')
    else:
        # 存在异常值
        for j in range(i, i + num_of_each_group):
            if origin_value[j] == abnormal_value[int(i / num_of_each_group)]:
                continue
            else:
                f.write(groups[j] + ',')
                f.write(str(origin_value[j]) + '\n')
    i += num_of_each_group
f.close()


# %%
