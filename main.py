# pip install -r requirements.txt

from request_inputs import request_inputs
from request_thesis import get_thesis
from language_parser import get_errors_in_texts
from tqdm import tqdm
# import pandas as pd

data = request_inputs()
# print(data)
df = get_thesis(data)


def fn(x):
    errors = get_errors_in_texts(x)
    # return pd.Series([errors, len(errors)])
    return len(errors)


tqdm.pandas(desc="分析錯誤中...")
# df[["errors", "error_count"]] = df["content"].progress_apply(fn)
df["error_count"] = df["content"].progress_apply(fn)


print("結果輸出中...")
df.to_excel("outputs/output.xlsx", index=None,
            columns=df.columns.drop(["link"]))
print("結果已輸出至 output.xlsx")

input("分析結束，按下任意鍵結束程式")
