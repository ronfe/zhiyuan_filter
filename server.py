from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd
import util
import pickle

app = Flask(__name__, template_folder='templates')

with open('data.pkl', 'rb') as f:
    d = pickle.load(f)

@app.route('/score/<keywords>/<mins>/<maxs>', methods=("POST", "GET"))
def html_table(keywords, mins, maxs):
    kw = keywords.split('-')
    dk = [t for t in d if t[6] >= int(mins) and t[6] <= int(maxs)]
    result = list()

    for row in dk:
        for k in kw:
            if k in row[3] or (row[8] is not None and k in row[8]):
                result.append(row)
                break

    dk = pd.DataFrame(result)
    dk.columns =  ['院校代号', '院校名称', '专业代号', '专业名称', '计划人数', '已报人数', '最低分数', '学费', '备注']
    dk = dk.sort_values('最低分数', ascending=False)

    return render_template('sample.html',  tables=[dk.to_html(classes='data')], titles=dk.columns.values)



if __name__ == '__main__':
    app.run(host='0.0.0.0')