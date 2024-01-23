import itertools
import csv
import re

from pyecharts import options as opts
from pyecharts.charts import Tree


def build_tree_data(tree):
    if tree[1]:
        result = {"name": tree[0], "children": []}
        for child in tree[1]:
            result["children"].append(build_tree_data(child))
        return result
    else:
        result = {"name": tree[0], "value": 0}
        return result


def draw_tree(tree, tree_name):
    tree_data = build_tree_data(tree)
    c = (
        Tree(init_opts=opts.InitOpts(width="1000px", height="600px"))
        .add("", [tree_data], collapse_interval=2, orient="TB")
    )

    html_code = c.render("temp.html")
    with open("temp.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    html_code_with_title = re.sub(r"<body\b[^>]*>", f"<body><h1>{tree_name}</h1>", html_content)
    return html_code_with_title


def read_csv(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data


def find_combinations(items, data):
    """
    :param items: 有哪些输入
    :param data:  配种的数据 a+b->c
    :return:  返回具体的配种情况，元祖嵌套树
    """
    combinations = {}
    next_item_tree_list = [(item, ()) for item in items]
    iter_time = 0
    while True:
        add_class_time = 0
        item_tree_list = [item for item in next_item_tree_list]
        for combination in itertools.permutations(item_tree_list, 2):
            # 排序去重复
            a, b = sorted(combination, key=lambda x: x[0])
            for row in data:
                if (a[0] == row[0] and b[0] == row[1]) or (a[0] == row[1] and b[0] == row[0]):
                    # 新元素
                    new_item = (row[2], (a, b))
                    if new_item[0] not in combinations:
                        # 没有新物种增加就停止
                        add_class_time += 1
                        next_item_tree_list.append(new_item)
                        combinations[new_item[0]] = new_item[1]
        print(f"第{iter_time}次迭代,添加种类：{add_class_time}")
        if add_class_time == 0:
            break
        iter_time += 1
    return combinations


def main():
    file_path = 'combinations.csv'
    input_items = ['棉悠悠', '幻悦蝶', '波霸牛']
    data = read_csv(file_path)
    combinations = find_combinations(input_items, data)
    # 初始化一个字符串，用于保存所有图表的 HTML 代码
    all_html_code = ""
    # 遍历 combinations 字典
    for key, value in combinations.items():
        html_code_with_title = draw_tree((key, value), key)
        all_html_code += html_code_with_title
    # 拼接整个 HTML 代码，包括必要的头部信息
    final_html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
        {all_html_code}
    </body>
    </html>
    """
    # 将整个 HTML 代码保存到文件中
    file_name = "_".join(input_items)
    with open(f"{file_name}.html", "w", encoding="utf-8") as file:
        file.write(final_html_code)


if __name__ == "__main__":
    main()
