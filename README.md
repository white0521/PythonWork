一个轻量级的 Python 工具，用于从 CSV文件中提取 “Question? Yes/No” 格式的问答对，并将结果保存为 JSON Lines（`.jsonl`）格式。

## 功能特点
- **灵活的列名**：可通过 `--col` 参数指定字段名称，默认读取 `input` 列。  
- **自动 ID**：为每个问答对生成唯一 `id`（可指定来源 `source_id` 或随机 UUID）。  
- **性能统计**：脚本会在运行结束时打印提取总数和耗时，方便性能评估。  

## 环境依赖
- Python ≥ 3.7  
- 用到的模块如 `re`、`json`、`csv`、`uuid`、`argparse` 等均为 Python 标准库，无需额外安装。
