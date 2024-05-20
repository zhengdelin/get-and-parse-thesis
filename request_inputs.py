import pandas as pd


DEGREES_PROMPT = """請輸入要搜尋的學位(以空格隔開)：
    1. 博士
    2. 碩士
"""
DEGREES_MAP = {
    "1": "博士",
    "2": "碩士",
}

LANGS_PROMPT = """請輸入要搜尋的語言(以空格隔開)：
    1. 中文
    2. 英文
    3. 日文
    4. 其他語言
"""
LANGS_MAP = {
    "1": "中文",
    "2": "英文",
    "3": "日文",
    "4": "其他語言"
}


def transform_input_degree(degree):
    if (degree in DEGREES_MAP):
        return DEGREES_MAP[degree]
    return degree


def transform_degrees(degrees):
    return list(map(transform_input_degree, degrees.split(" ")))


def transform_input_lang(lang):
    # print(lang, LANGS_MAP)
    if (lang in LANGS_MAP):
        return LANGS_MAP[lang]
    return lang


def transform_langs(langs):
    return list(map(transform_input_lang, langs.split(" ")))


def request_inputs():

    print("直接按 Enter 即可使用 inputs/inputs.txt 的輸入")

    # file inputs
    fileInputs = pd.read_csv("./inputs/inputs.txt", sep="|",
                             dtype=str).loc[0].to_dict()

    kw = input("請輸入要搜尋的字詞：") or fileInputs["kw"]
    if (not kw):
        raise ValueError("請輸入要搜尋的字詞")

    years = input("請輸入畢業學年度(民國)(以空格隔開)：") or fileInputs["years"]
    if (years != "" and len(years.split(" ")) != 2):
        raise ValueError("請輸入正確的畢業學年度")

    degrees = input(DEGREES_PROMPT) or fileInputs["degrees"]

    langs = input(LANGS_PROMPT) or fileInputs["langs"]

    maxCount = eval(input("請輸入要搜尋的最大筆數(預設100)：")
                    or str(fileInputs["maxCount"]) or "100")

    return {
        "kw": kw,
        "years": years.split(" ") if years else None,
        "degrees": transform_degrees(degrees) if degrees else None,
        "langs": transform_langs(langs) if langs else None,
        "maxCount": maxCount
    }
