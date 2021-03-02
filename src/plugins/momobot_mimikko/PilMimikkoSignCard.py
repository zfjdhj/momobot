import os
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


plugin_path = os.path.dirname(os.path.abspath(__file__))
# plugin_path='./'

description_font = os.path.join(plugin_path, "fonts/思源黑体SourceHanSansCN-Medium.otf")
description_font_size = 32


NotLoadImUrlTxtPath = os.path.join(plugin_path, "NotLoadImUrls.txt")
LogTxtPath = os.path.join(plugin_path, "Log.txt")
ImSetDir = os.path.join(plugin_path, "ImSet")
if not os.path.isdir(ImSetDir):
    os.makedirs(ImSetDir)


def drawSigncard(sign_data):
    if sign_data["code"] == "0":
        ImUrl = sign_data["body"]["PictureUrl"]
        ImDescription = sign_data["body"]["Description"]
        ImPictureName = sign_data["body"]["Name"]
        with open(NotLoadImUrlTxtPath, "w") as FId, open(LogTxtPath, "w") as FId2:
            _, ImName = os.path.split(ImUrl.strip())
            SaveImPath = os.path.join(ImSetDir, ImName)
            try:
                r = requests.get(ImUrl.strip())
            except Exception as error:
                FId.writelines(ImUrl)
                MsgTxt = "not download {} Connection refused\n".format(ImName)
                print(MsgTxt)
                FId2.writelines(MsgTxt)
                return error
            StatCode = r.status_code
            if StatCode == 403 or StatCode == 404:
                FId.writelines(ImUrl)
                MsgTxt = "not download {} {} error\n".format(ImName, StatCode)
                print(MsgTxt)
                FId2.writelines(MsgTxt)
            try:
                Im = Image.open(BytesIO(r.content))
                # print(Im.size) # 900,540
                # 保存原图
                Im.save(SaveImPath)
                # 绘制背景
                bg = Image.new(mode="RGB", size=(964, 833), color="white")
                im_border = int((bg.size[0] - Im.size[0]) / 2)
                bg.paste(Im, (im_border, im_border))

                # 绘制Description文字
                draw = ImageDraw.Draw(bg)
                font = ImageFont.truetype(description_font, size=description_font_size)

                # 文字分割换行
                strList = []
                newStr = ""
                index = 0
                for item in ImDescription:
                    newStr += item
                    if len(newStr) > 26 or index == len(ImDescription) - 1:
                        strList.append(newStr)
                        newStr = ""
                    index += 1
                index = 0
                for item in strList:
                    if len(strList) <= 4:
                        text_y = Im.size[1] + 60 + int(index * 1.2 * description_font_size)
                    else:
                        text_y = Im.size[1] + description_font_size + int(index * 1.2 * description_font_size)
                    draw.text(
                        (2 * description_font_size, text_y),
                        item,
                        fill=(
                            129,
                            129,
                            129,
                        ),
                        font=font,
                    )
                    index += 1

                # 绘制pictureName
                font_width, font_height = draw.textsize(ImPictureName, font)
                x = bg.size[0] - font_width - 80
                if bg.size[1] - font_height - 60 < Im.size[1] + 60 + int((index + 1) * description_font_size):
                    y = bg.size[1] - font_height - 60
                else:
                    y = Im.size[1] + 60 + int((index + 1) * description_font_size)
                draw.text(
                    (x, y),
                    ImPictureName,
                    fill=(
                        168,
                        168,
                        168,
                    ),
                    font=font,
                )

                # 绘制pluginName
                text = "MimikkoAutoSign"
                font_width, font_height = draw.textsize(text, font)
                draw.text(
                    ((bg.size[0] - font_width) / 2, bg.size[1] - font_height - 12),
                    text=text,
                    fill=(
                        135,
                        135,
                        135,
                    ),
                    font=font,
                )
                date = time.strftime("%Y%m%d", time.localtime())
                bg.save(os.path.join(ImSetDir, f"SignCard{date}.jpg"))
                MsgTxt = "download {} with requests.get({})\n".format(ImName, ImUrl)
                FId2.writelines(MsgTxt)
                return os.path.join(ImSetDir, f"SignCard{date}.jpg")
            except Exception as error:
                FId.writelines(ImUrl)
                MsgTxt = "not download {} with ERROR: {}\n".format(ImName, error)
                FId2.writelines(MsgTxt)
                return error
    else:
        return "sign_data error"
