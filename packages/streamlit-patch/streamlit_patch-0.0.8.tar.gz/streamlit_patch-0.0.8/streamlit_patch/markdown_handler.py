import re

import numpy as np
import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts
from streamlit_float import *
import random
from datetime import datetime, timedelta
import uuid


float_options = {
    "title": {"text": "ECharts Example"},
    "tooltip": {},
    "xAxis": {"data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},
    "yAxis": {},
    "series": [
        {"name": "Sales", "type": "bar", "data": [120, 200, 150, 80, 70, 110, 130]}
    ],
}


def fake_echarts_data():
    data = []
    if len(data) == 0:
        # 设置初始日期
        base = datetime(
            1988, 10, 3
        )  # 注意：Python 中月份是从 1 开始的，所以 10 表示 10 月
        one_day = timedelta(days=1)

        # 初始化 data 数组
        data = [[int(base.timestamp() * 1000), random.random() * 300]]

        # 生成 20000 个数据点
        for i in range(1, 20000):
            base += one_day
            new_value = data[i - 1][1] + random.uniform(-0.5, 0.5) * 20
            data.append([int(base.timestamp() * 1000), round(new_value)])
    return data


def fake_table_data():
    data_table = {
        "基金代码": ["005176", "001510", "161128", "040046"],
        "基金名称": ["富国精准医疗", "富国新动力灵", "易标普信息科", "华安纳斯达克"],
        "成立日期": ["2017-11-16", "2015-08-04", "2016-12-13", "2013-08-02"],
        "今年来": ["19.42%", "18.18%", "19.36%", "19.39%"],
        "近1周": ["6.79%", "4.99%", "0.46%", "0.40%"],
        "近1月": ["-13.04%", "-9.38%", "4.67%", "4.29%"],
        "近3月": ["-6.87%", "-5.80%", "11.04%", "13.17%"],
        "近6月": ["24.10%", "13.31%", "23.96%", "23.36%"],
        "近1年": ["21.29%", "32.03%", "28.70%", None],
        "近2年": ["30.71%", "53.74%", None, None],
        "近3年": ["42.43%", "70.95%", None, None],
        "近5年": ["125.77%", None, None, None],
        "成立来": ["21.56%", "43.00%", "44.38%", "126.00%"],
    }

    # 创建 DataFrame
    df = pd.DataFrame(data_table)
    return df


# 定义一个函数封装组件的逻辑


class EchartsHandlerContainer:
    def __init__(self):
        self.container = st.empty()

    @staticmethod
    def float_init():
        float_init()

    def display_echarts_with_toggle(
        self, options, button_name="Click me", button_key=""
    ):
        def click_button():
            st.session_state[button_key] = not st.session_state[button_key]

        options["title"]["text"] = button_name
        # 初始化float功能
        with self.once_container:
            # 使用 session_state 来保存容器显示状态
            if button_key not in st.session_state:
                st.session_state[button_key] = False  # 默认不显示容器

            # 按钮点击时改变变量的值
            st.button(button_name, key=uuid.uuid4(), on_click=click_button)

            # 根据变量显示或隐藏容器
            if st.session_state[button_key]:
                container = st.container(key=uuid.uuid4())
                with container:
                    chart_data = pd.DataFrame(
                        np.random.randn(20, 3), columns=["a", "b", "c"]
                    )
                    st.line_chart(chart_data)
                container.float(
                    f"background-color: white; transform: translate(calc({len(button_name) + 2} * 10px), -60px); box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); border-radius: 10px;padding: 10px; position: absolute;"
                )

    def display_echarts(self, data: list):
        options = {
            "title": {"left": "center", "text": "Large Ara Chart"},
            "toolbox": {
                "feature": {
                    "dataZoom": {"yAxisIndex": "none"},
                    "restore": {},
                    "saveAsImage": {},
                }
            },
            "xAxis": {"type": "time", "boundaryGap": False},
            "yAxis": {"type": "value", "boundaryGap": [0, "100%"]},
            "dataZoom": [
                {"type": "inside", "start": 0, "end": 20},
                {"start": 0, "end": 20},
            ],
            "series": [
                {
                    "name": "Fake Data",
                    "type": "line",
                    "smooth": True,
                    "symbol": "none",
                    "areaStyle": {},
                    "data": data,
                }
            ],
        }
        with self.once_container:
            st_echarts(options=options)

    def create_interactive_table(self, df):
        with self.once_container:
            st.dataframe(df, key=uuid.uuid4())

    def cus_write(self, text):
        text = re.sub(r"^-\s*", "", text, flags=re.MULTILINE)
        text = re.sub(r"^\d+\.\s*\*\*(《.*?》)\*\*$", r"\1", text, flags=re.MULTILINE)
        # 使用正则表达式按 <link> 分割文本
        parts = re.split(
            r"(《.*?》|/echarts\[[^\]]+\]|/itable\[[^\]]+\])", text, flags=re.MULTILINE
        )  # 现在匹配标签和指令
        button_name = ""

        for part in parts:
            if part.startswith("《") and part.endswith("》"):  # 判断是否为《text》标签
                button_name = part[1:-1]
                # 显示图表
                self.display_echarts_with_toggle(
                    float_options, button_name, f"show_echart_{button_name}"
                )
            elif part.startswith("/echarts[") and part.endswith(
                "]"
            ):  # 判断是否为/echarts[key]
                key = part[9:-1]  # 提取key部分
                # 调用显示图表函数
                self.display_echarts(
                    fake_echarts_data()
                )  # 假设 display_echarts 需要这个key来加载不同的图表
            elif part.startswith("/itable[") and part.endswith(
                "]"
            ):  # 判断是否为/itable[key]
                key = part[8:-1]  # 提取key部分
                # 调用显示交互表格函数
                self.create_interactive_table(
                    fake_table_data()
                )  # 假设 create_interactive_table 需要这个key来加载不同的表格
            else:
                self.once_container.write(part, unsafe_allow_html=True)

    def write(self, text):
        with self.container:
            self.once_container = st.container()
        self.cus_write(text)
        return self.container
