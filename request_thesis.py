
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
from tqdm import tqdm

BASE_URL = "https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dwebmge"


def get_thesis(data: dict):
    def querySelector(query: str, el=None):
        el = el or driver
        return el.find_element(By.CSS_SELECTOR, query)

    def querySelectorAll(query: str, el=None):
        el = el or driver
        return el.find_elements(By.CSS_SELECTOR, query)

    def handleKeyword(kw):
        for i in range(0, 3):
            querySelector(f"input[name=qs{i}]").send_keys(kw)

    def handleYears(years: list | None):
        if (not years or len(years) != 2):
            return
        querySelector("select[name=ltyr]").send_keys(years[0])
        querySelector("select[name=eltyr]").send_keys(years[1])

    def handleDegree(degrees: list | None):
        if (not degrees):
            return
        for degree in degrees:
            querySelector(
                f"input[type=checkbox][name=mtty][value={degree}]").click()

    def handleLang(langs: list | None):
        if (not langs):
            return
        for language in langs:
            querySelector(
                f"input[type=checkbox][name=mtlg][value={language}]").click()

    def toAdvancedSearch():
        '''
        切換到進階搜尋
        '''
        try:
            querySelector("#bodyid > div.etds_mainbd > table > tbody > tr:nth-child(1) > td.etds_mainct > table > tbody > tr:nth-child(2) > td > div.nav > ul.version > li:nth-child(2) > a").click()
        except:
            toAdvancedSearch()

    ACTIVE_TAB_SELECTOR = '#aa[style*="display: block"]'

    def getActiveTab():
        return querySelector(ACTIVE_TAB_SELECTOR)

    def change_page_size():
        select = Select(querySelector("#jpsize"))
        select.select_by_index(4)

    def getCurThesisYear():
        '''分析文章的年份
        '''
        trs = querySelectorAll(
            f"{ACTIVE_TAB_SELECTOR} > table > tbody > tr")
        for tr in trs:
            # print("trText", tr.text)
            th = querySelector("th", tr)
            # print("th text", th.text)
            if (th.text == "論文出版年:"):
                return querySelector("td", tr).text
        return None

        # open browser
    driver = webdriver.Chrome()
    driver.get(BASE_URL)

    toAdvancedSearch()

    # 輸出網頁標題
    print(driver.title)

    # 處理 inputs
    handleKeyword(data["kw"])
    handleYears(data["years"])
    handleDegree(data["degrees"])
    handleLang(data["langs"])

    # 搜尋
    querySelector("#gs32search").click()

    maxCount = int(data["maxCount"])

    f = open("outputs/output.txt", "w", encoding="utf-8")
    df = pd.DataFrame({}, columns=['year', 'title', 'link', 'content'])
    count = 0

    get_thesis_title_progress = tqdm(total=maxCount, desc="取得文章...")

    # change_page_size()

    while (count < maxCount):
        try:

            linkElements = querySelectorAll("a:has(.etd_d)")

            for linkEl in linkElements:
                link = linkEl.get_attribute("href")
                title = querySelector(".etd_d", linkEl).text

                # 更新資料
                df.loc[count] = [0, title, link, ""]
                count += 1

                # 更新進度條
                get_thesis_title_progress.update(1)
                if (count >= maxCount):
                    break

            if (count >= maxCount):
                break

            # 下一頁
            try:
                querySelector("[name=gonext]").click()
            except:
                # 沒有下一頁
                print("沒有下一頁了")
                break
        except Exception as e:
            print(e)
            break

    get_thesis_title_progress.close()

    FOREIGN_SUMMARY_SELECTOR = '#gs32_levelrecord > ul > li > a[title="外文摘要"]'
    FOREIGN_SUMMARY_CONTENT_SELECTOR = '#format0_disparea > tbody > tr > td.stdncl2 > div'

    for i in tqdm(range(0, len(df)), desc="取得文章內容..."):
        s = pd.Series(df.loc[i])

        # 跳轉到文章詳細頁
        driver.get(s["link"])

        year = getCurThesisYear()
        if (year):
            s["year"] = int(year)

        try:
            foreignSummaryEl = querySelector(FOREIGN_SUMMARY_SELECTOR)
        except:
            foreignSummaryEl = None

        # 沒有外文摘要
        if (not foreignSummaryEl):
            # 從 df 中刪除錯誤資料
            df.drop(i, inplace=True)
            continue

        # 跳轉到外文摘要
        foreignSummaryEl.click()

        # 取得文章內容
        text = querySelector(
            FOREIGN_SUMMARY_CONTENT_SELECTOR, getActiveTab()).text

        # 寫入檔案
        f.write(f"{i+1}. {year} {s['title']}\n")
        f.write(text+"\n\n\n")
        s["content"] = text

        # 儲存資料
        df.loc[i] = s

    f.close()
    driver.close()

    print(f"取得文章完成, 已取得 {len(df)} 篇文章\n")
    return df


# print(df["content"].values)
