import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle 

base_url = 'https://www.nm.zsks.cn'

def get_row(table_soup, is_tbody=False):
    data = list()
    if is_tbody == False:
        table_body = table_soup.find('tbody')
    else:
        table_body = table_soup

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    
    return data


def org_data(each, major):
    tmp = [each[3], each[4], major[0], major[1], int(major[2]), int(major[4]), int(major[3])]
    try:
        tmp.append(int(major[5]))
    except:
        tmp.append(-1)
    
    if len(major) == 8:
        tmp.append(major[7])
    else:
        tmp.append(None)
    
    return tmp


def calc_pd(kw_list, category='L', batch=2, year=2018, sort_by='name', min_score=0, max_score=750):
    pattern = '/zy_33_41_2018/B_14.html'
    if category == 'L' and batch == 2 and year == 2018:
        pattern = '/zy_33_41_2018/B_14.html'
    
    r = requests.get(base_url+pattern)
    r.encoding='gb2312'

    soup = BeautifulSoup(r.text, 'lxml')
    college_table = soup.find('table')
    t = get_row(college_table, True)[2:][1:-1]

    major_pattern = '/zy_33_41_2018/4_B_{}_14.html'
    computer_list = list()

    for each in t:
        code = each[3]
        c_major_pattern = major_pattern.format(code)
        res = requests.get(base_url+c_major_pattern)
        res.encoding = 'gb2312'
        soup = BeautifulSoup(res.text, 'lxml')
        major_table = soup.find('table')
        b = get_row(major_table, True)[3:-2]
        for major in b:
            name = major[1]
            flag = True
            # for kw in kw_list:
            #     if kw in major[1]:
            #         flag = True
            #         # break
            #     if len(major) == 8 and kw in major[7]:
            #         flag = True
            #         # break
            if flag: 
                tmp = org_data(each, major)
                computer_list.append(tmp)
    
    df = pd.DataFrame(computer_list)

    with open('data.pkl', 'wb+') as f:
        pickle.dump(computer_list, f)

    if len(df) >0:
        df = df[df[6] >= min_score] 
        df = df[df[6] <= max_score]

        df.columns = ['院校代号', '院校名称', '专业代号', '专业名称', '计划人数', '已报人数', '最低分数', '学费', '备注']

        if sort_by == 'name':
            df = df.sort_values('院校名称')
        if sort_by == 'score':
            df = df.sort_values('最低分数', reversed=True)
    
    return df[:10]


if __name__ == '__main__':
    calc_pd([])