#  ____       _____           _
# |  _ \ _   |_   _|__   ___ | |___ ____
# | |_) | | | || |/ _ \ / _ \| / __|_  /
# |  __/| |_| || | (_) | (_) | \__ \/ /
# |_|    \__, ||_|\___/ \___/|_|___/___|
#        |___/

# Copyright (c) 2024 Sidney Zhang <zly@lyzhang.me>
# PyToolsz is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

from pathlib import Path

import pdfplumber
import sys


def checkFolders(folders:str|Path|list[str|Path], 
                 mkdir:bool = True, output:bool = False) -> bool|list[bool]|None :
    """
    检查多个文件夹路径是否存在
    mkdir - 是否创建不存在的文件夹（默认创建）
    output - 是否输出检查结果（默认不输出）
    """
    if isinstance(folders, (str, Path)) :
        givefolders = [folders]
    else :
        givefolders = folders
    givefolders = [Path(x) for x in givefolders]
    res = [x.exists() for x in givefolders]
    if mkdir :
        for i in range(len(givefolders)) :
            if not res[i] :
                if givefolders[i] != Path("No Path") :
                    givefolders[i].mkdir(parents=True, exist_ok=True)
    if output :
        if len(res) == 1 :
            return res[0]
        else :
            return res

def lastFile(folder:str|Path, filename:str,
             last_:str = "mtime", mode:str = "desc") -> Path :
    """
    获取指定文件夹下的最后一个文件
    filename - 文件名或查找匹配的字符
    last_ - 排序方式，可选值为 : 
            "mtime"（修改时间）
            "createtime"（创建时间）
            "atime"（访问时间）
            "size"（文件大小）
    mode - 排序方式，可选值为 :
            "desc"（降序）
            "asc"（升序）
    """
    if mode not in ["desc", "asc"] :
        raise ValueError("mode must be one of {}".format(["desc", "asc"]))
    kfolder = Path(folder)
    findedfile = sorted(kfolder.glob(filename))
    if sys.version_info >= (3, 12) :
        fixlast = "birthtime" if last_ == "createtime" else last_
    else :
        fixlast = "ctime" if last_ == "createtime" else last_
    attname = "st_{}".format(fixlast)
    if len(findedfile) == 0 :
        return Path("No Path")
    checkList = [getattr(x.stat(), attname) for x in findedfile]
    if mode == "desc" :
        cKdata = checkList.index(max(checkList))
    else: 
        cKdata = checkList.index(min(checkList))
    return findedfile[cKdata]

def read_pdf_text(pdfPath:str|Path) -> list[str] :
    """
    以文本形式读取PDF内容
    """
    data = []
    with pdfplumber.open(Path(pdfPath)) as pdf :
        for page in pdf.pages:
                    txt = page.extract_text()
                    txt = txt.split('\n')
                    data.extend(txt)
    return data