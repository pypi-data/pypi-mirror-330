# This code is part of cqlib.
#
# Copyright (C) 2024 China Telecom Quantum Group, QuantumCTek Co., Ltd.,
# Center for Excellence in Quantum Information and Quantum Physics.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from ..exceptions import VisualizationError
import os
import re
from typing import Optional
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Circle, Rectangle
from collections import defaultdict

"""
Quantum circuit visualization
"""
LINE_GATE = {"CZ", "ISWAP", "SWAP", "CCZ", "CCX"}
PARAM_GATE = {"RZ", "RY", "RXY", "RX", "U3", "XY2M", "XY2P"}
MULTIPLE_QUBIT_GATE = {'B', 'M'}


def _processing_circuit(qcis_str):
    """
    Parses and processes circuit strings in preparation for drawing
    """
    draw_data = defaultdict(list)
    qcis_list = qcis_str.upper().split("\n")
    # 双比特门的x坐标集合， 在这个集合里面的x轴坐标除了已添加的双比特门，不能再添加其他门
    c_line_number = []
    for index, qcis in enumerate(qcis_list):
        if c_line_number:
            for key, value in draw_data.items():
                if len(value) - 1 < max(c_line_number):
                    for _ in range(max(c_line_number) - len(value)):
                        value.append(None)
                    value.append("")
        if qcis:
            try:
                qcis_split = qcis.split(" ")
                line_num = validate_and_extract_bit(qcis_split[1])
                bit_gate_name = qcis_split[0]
                # 特殊处理，此类型属于连线类型的门
                if any(
                        substr in bit_gate_name
                        for substr in LINE_GATE
                ):
                    # 此类型属于三个点连线
                    if bit_gate_name in ["CCZ", "CCX"]:
                        line_num = validate_and_extract_bit(qcis_split[3])
                        another_line_number = (
                                ("".join(filter(str.isdigit, qcis_split[1])))
                                + " "
                                + ("".join(filter(str.isdigit, qcis_split[2])))
                        )
                    else:  # 此类型属于两个点连线
                        line_num = validate_and_extract_bit(qcis_split[2])
                        another_line_number = int(
                            "".join(filter(str.isdigit, qcis_split[1]))
                        )
                    bit_gate_name = " ".join([bit_gate_name, str(another_line_number)])
                    _multiple_gate_process(
                        draw_data=draw_data,
                        bit_gate_name=bit_gate_name,
                        line_num=line_num,
                        c_line_number=c_line_number,
                    )
                # 特殊处理 此类型属于带有参数的门
                elif any(
                        substr in bit_gate_name
                        for substr in PARAM_GATE
                ):
                    if "RXY" in bit_gate_name:
                        bit_gate_name = " ".join(
                            [bit_gate_name, qcis_split[2], qcis_split[3]]
                        )
                    elif "U3" in bit_gate_name:
                        bit_gate_name = " ".join(
                            [bit_gate_name, qcis_split[2], qcis_split[3], qcis_split[4]]
                        )
                    else:
                        bit_gate_name = " ".join([bit_gate_name, qcis_split[2]])
                    _normal_gate_process(
                        draw_data=draw_data,
                        bit_gate_name=bit_gate_name,
                        line_num=line_num,
                        c_line_number=c_line_number,
                    )
                elif bit_gate_name in MULTIPLE_QUBIT_GATE:
                    line_num_list = [validate_and_extract_bit(qcis_split[i]) for i in range(1, len(qcis_split))]
                    line_num_gate_index_dict = {}
                    for line_num in line_num_list:
                        gate_line_index = _normal_gate_process(
                            draw_data=draw_data,
                            bit_gate_name=bit_gate_name,
                            line_num=line_num,
                            c_line_number=c_line_number,
                        )
                        line_num_gate_index_dict[line_num] = gate_line_index
                    if bit_gate_name == 'B':
                        _align_barrier(draw_data, line_num_gate_index_dict)
                else:
                    _normal_gate_process(
                        draw_data=draw_data,
                        bit_gate_name=bit_gate_name,
                        line_num=line_num,
                        c_line_number=c_line_number,
                    )
            except Exception as e:
                raise e
                # raise VisualizationError(
                #     f"线路可视化错误---线路第{index}行:'{qcis}' 存在问题"
                # )
    simplify_draw_data(draw_data)
    return draw_data


def validate_and_extract_bit(qcis_bit: Optional[str]):
    """
    Verify qcis_bit string format is correct and extract the number of bit lines
    """
    pattern = r"^Q(\d+)$"
    match = re.match(pattern, qcis_bit)
    if match:
        number = match.group(1)
        return int(number)
    else:
        raise Exception()


def _align_barrier(draw_data, line_num_gate_index_dict):
    max_gate_index = max(line_num_gate_index_dict.values())
    for line_num, gate_index in line_num_gate_index_dict.items():
        if gate_index < max_gate_index:
            for _ in range(max_gate_index - gate_index):
                draw_data[line_num].insert(gate_index, '')


def simplify_draw_data(draw_data):
    min_len = np.inf
    min_line_num = None
    for line_num, line_data in draw_data.items():
        if len(line_data) < min_len:
            min_len = len(line_data)
            min_line_num = line_num
    for i in range(min_len - 1, -1, -1):
        if all(not (line_data[i]) for line_data in draw_data.values()):
            for line_data in draw_data.values():
                line_data.pop(i)


def _normal_gate_process(draw_data, bit_gate_name, line_num, c_line_number):
    """
    processes bit gates with no special drawing, such as X, Y, M gates....
    """
    line_data = draw_data.get(line_num)
    if line_data:
        for line_data_index, value in enumerate(line_data):
            if value is None and line_data_index not in c_line_number:
                line_data[line_data_index] = bit_gate_name
                return line_data_index
    draw_data[line_num].append(bit_gate_name)
    return len(draw_data[line_num]) - 1


def _multiple_gate_process(draw_data, bit_gate_name, line_num, c_line_number):
    """
    processes bits that need to be wired, e.g. cz, swap,ccz gate.....
    """
    # 目前最长的一条线的长度（连线类型的比特门放到此长度之后）
    line_max_size = 0
    for data in draw_data.values():
        if len(data) > line_max_size:
            line_max_size = len(data)
    line_data = draw_data.get(line_num)
    if line_data:
        if len(line_data) < line_max_size:
            for _ in range(line_max_size - len(line_data)):
                line_data.append("")
    else:
        line_data = []
        for _ in range(line_max_size):
            line_data.append("")
        draw_data[line_num] = line_data

    for index in range(0, len(line_data)):
        if line_data[index] is None:
            line_data[index] = ""
    draw_data[line_num].append(bit_gate_name)

    another_line_number_list = bit_gate_name.split(" ")
    for index in range(1, len(another_line_number_list)):
        another_line_number = int(another_line_number_list[index])
        another_line_data = draw_data.get(another_line_number)
        if another_line_data:
            if len(another_line_data) < line_max_size:
                for _ in range(line_max_size - len(another_line_data)):
                    another_line_data.append("")
        else:
            another_line_data = draw_data[another_line_number] = []
            for _ in range(line_max_size):
                draw_data[another_line_number].append("")
        draw_data[another_line_number].append("")

        for i in range(0, len(another_line_data)):
            if another_line_data[i] is None:
                another_line_data[i] = ""
    c_line_number.append(line_max_size)


def draw_circuit(
        qcis_str: Optional[str],
        file_name: Optional[str] = None,
        scale: Optional[float] = 1.0,
        interactive: Optional[bool] = False,
):
    """Draw a quantum circuit based on matplotlib.

    Args:
        qcis_str: A visual qcis string is required
        file_name: The address to save the image.Default to 'None'
        scale: Scale of image to draw .The value must be greater than 0,if it is greater than 1.0, it is enlarged, and if it is less than 1.0, it is shrunk. Default to '1.0'
        interactive:Displays the created image.Default to 'False'

    Returns:
        matplotlib.figure.Figure: a matplotlib figure object for the qcis circuit diagram

    Raises:
        VisualizationError: There is a problem with the line format
        ValueError: 'scale' parameter range error
    """
    draw_data = _processing_circuit(qcis_str)
    if not draw_data:
        raise VisualizationError("解析qcis线路失败")
    if scale <= 0:
        raise ValueError("scale参数值不能小于等于0")
    total_num_line = len(draw_data)
    x_len = max([len(value) for value in draw_data.values()])
    y_len = total_num_line + 2
    # 设置画布大小
    plt.figure(figsize=((x_len + 1), y_len), dpi=150 * scale)
    plt.xlim(0, (x_len + 1))
    plt.ylim(0, y_len)
    y_values = range(1, total_num_line + 1)
    qubit_index_list = sorted([key for key in draw_data])
    line_num_list = range(0, total_num_line)
    map_q2line = dict(zip(qubit_index_list, line_num_list))
    for y, line_num in zip(reversed(y_values), line_num_list):
        q_index = qubit_index_list[line_num]
        line_data = draw_data.get(q_index)
        # 画一个水平线
        plt.axhline(y=y, color="black", linestyle="-", zorder=0, linewidth=3.5)
        # 在水平线左边添加文字信息
        rect = Rectangle(
            (0, (y - 0.25)), 0.6, 0.505, edgecolor="none", facecolor="white"
        )
        plt.gca().add_patch(rect)
        plt.annotate(
            f"q[{q_index}]",
            (0.1 - (q_index // 10) * 0.1, y),
            color="black",
            fontsize=13,
            fontweight="bold",
            ha="left",
            va="center",
        )
        if line_data:
            for index, data in enumerate(line_data):
                index = index + 0.75
                if not data or "two_gate" in data:
                    continue
                image_name = data

                # 特殊处理-cz iswap swap
                if any(
                        substr in data for substr in LINE_GATE
                ):
                    data_split = data.split(" ")
                    another_line = map_q2line[int(data_split[1])]
                    image_name = data_split[0]
                    another_line1 = None
                    color = "#D6271D"
                    if image_name in ["CCZ", "CCX"]:
                        another_line1 = map_q2line[int(data_split[2])]
                        color = "#1A4DF2"
                    # 画一条竖线
                    plt.axvline(
                        x=(index + 0.3),
                        ymin=(y - (another_line - line_num)) / y_len,
                        ymax=y / y_len,
                        color=color,
                        linewidth=3.5,
                    )
                    if another_line1 is not None:
                        plt.axvline(
                            x=(index + 0.3),
                            ymin=(y - (another_line1 - line_num)) / y_len,
                            ymax=y / y_len,
                            color=color,
                            linewidth=3.5,
                        )
                    ##读取图片
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    image_folder = "image"
                    image_path = os.path.join(
                        current_dir, image_folder, f"{image_name}.png"
                    )
                    img = mpimg.imread(image_path)
                    ##将图片置于水平线上
                    plt.imshow(
                        img,
                        extent=[index, (index + 0.6), (y - 0.3), (y + 0.3)],
                        aspect="auto",
                        zorder=3,
                        alpha=1,
                    )
                    # iswap和swap每个比特都是图片
                    if image_name in ["ISWAP", "SWAP"]:

                        plt.imshow(
                            img,
                            extent=[
                                index,
                                (index + 0.6),
                                ((y - (another_line - line_num)) - 0.3),
                                ((y - (another_line - line_num)) + 0.3),
                            ],
                            aspect="auto",
                            zorder=3,
                            alpha=1,
                        )
                    else:
                        # 画一个圆
                        circle = Circle(
                            ((index + 0.3), (y - (another_line - line_num))),
                            0.12,
                            color=color,
                        )
                        plt.gca().add_patch(circle)
                        if another_line1 is not None:
                            circle = Circle(
                                ((index + 0.3), (y - (another_line1 - line_num))),
                                0.12,
                                color=color,
                            )
                            plt.gca().add_patch(circle)

                # 特殊处理-rx ry rxy rz u3
                elif any(substr in data for substr in PARAM_GATE):
                    bit_gate_name = data.split(" ")[0]
                    if "RXY" in data:
                        angle1 = str(round(float(data.split(" ")[1]), 4))
                        angle2 = str(round(float(data.split(" ")[2]), 4))
                        angle = angle1 + "_" + angle2
                    elif "U3" in data:
                        angle1 = str(round(float(data.split(" ")[1]), 4))
                        angle2 = str(round(float(data.split(" ")[2]), 4))
                        angle3 = str(round(float(data.split(" ")[3]), 4))
                        angle = angle1 + "_" + angle2 + "\n" + "_" + angle3
                    else:
                        angle = str(round(float(data.split(" ")[1]), 4))
                    if bit_gate_name == "RZ":
                        color = "#D6271D"
                    else:
                        color = "#1A4DF2"
                    rect = Rectangle(
                        ((index - 0.1), (y - 0.3)),
                        0.8,
                        0.6,
                        linewidth=1,
                        edgecolor="none",
                        facecolor=color,
                    )
                    plt.gca().add_patch(rect)
                    plt.annotate(
                        bit_gate_name,
                        ((index + 0.3), (y + 0.1)),
                        color="white",
                        fontsize=18,
                        ha="center",
                        va="center",
                    )
                    if len(angle) > 12:
                        fontsize = 8
                    elif 8 < len(angle) <= 12:
                        fontsize = 10
                    else:
                        fontsize = 12

                    plt.annotate(
                        angle,
                        ((index + 0.3), (y - 0.15)),
                        color="white",
                        fontsize=fontsize,
                        ha="center",
                        va="center",
                    )

                else:
                    # 读取图片
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    image_folder = "image"
                    image_path = os.path.join(
                        current_dir, image_folder, f"{image_name}.png"
                    )
                    img = mpimg.imread(image_path)
                    # 将图片置于水平线上
                    plt.imshow(
                        img,
                        extent=[index, (index + 0.6), (y - 0.3), (y + 0.3)],
                        aspect="auto",
                        zorder=3,
                        alpha=1,
                    )
    plt.axis("off")

    plt.subplots_adjust(top=1, bottom=0, left=0, right=1)
    if file_name is not None:
        plt.savefig(f"{file_name}.png")
    fig = plt.gcf()
    if interactive:
        plt.show()
    return fig
