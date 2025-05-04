import re
import json
import csv
import uuid


def parse_entry(text, source_id=None):
    """
    从输入文本中解析出所有的问答对。

    参数:
        text (str): 含有多个"Yes"或"No"答案的问答文本。
        source_id (str|int): 来源标识，可选，用于生成唯一id。

    返回:
        List[dict]: 问答对列表，每项包含id、Question、Answer、source_id。
    """
    # 匹配以问号结尾的问题，后接Yes或No答案
    pattern = re.compile(r'([^?？]+[?？])\s*(Yes|No)', flags=re.IGNORECASE)
    pairs = []
    for idx, match in enumerate(pattern.finditer(text), 1):
        question = match.group(1).strip()
        answer = match.group(2).strip().capitalize()
        # 生成唯一id：可选拼接来源和索引，也可使用uuid
        if source_id is not None:
            unique_id = f"{source_id}_{idx}"
        else:
            unique_id = str(uuid.uuid4())
        pairs.append({
            "id": unique_id,
            "Question": question,
            "Answer": answer,
            "source_id": source_id
        })
    return pairs


def process_csv(input_path, output_path, col_name='input'):
    """
    读取CSV文件，对指定列的每一行调用parse_entry处理，
    并将所有问答对写入JSON文件，每行一个JSON对象。

    参数:
        input_path (str): 输入CSV文件路径
        output_path (str): 输出JSON文件路径（JSON Lines格式）
        col_name (str): 需解析的列名，默认 'input'
    """
    all_pairs = []
    with open(input_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row_idx, row in enumerate(reader, 1):
            text = row.get(col_name, '')
            source_id = row.get('id') if 'id' in row else row_idx
            pairs = parse_entry(text, source_id)
            all_pairs.extend(pairs)

    # 写入 JSON Lines 格式
    with open(output_path, 'w', encoding='utf-8') as jsonfile:
        for item in all_pairs:
            jsonfile.write(json.dumps(item, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='解析问答对并输出为JSON Lines格式')
    parser.add_argument('--input', '-i', required=True, help='输入CSV文件路径')
    parser.add_argument('--output', '-o', required=True, help='输出JSON文件路径')
    parser.add_argument('--col', '-c', default='input', help='需解析的列名，默认为 input')
    args = parser.parse_args()

    process_csv(args.input, args.output, args.col)
    print(f"解析完成，结果已保存至 {args.output}")
