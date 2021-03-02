from PIL import Image, ImageDraw, ImageFont
import calendar
import datetime


def drawMonth(month,day_list,plugin_path):
    print(day_list)
    WEEK = ('SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT')
    MONTH = ('January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December')

    # create new blank picture
    bg= Image.open(f'{plugin_path}/indexPC.png').convert("RGBA")
    width, height = bg.size
    img = Image.new('RGBA',bg.size, color=(255,255,255,40))
    img.paste(bg,mask=bg)
    # rows = 2 titles + 5or6 rows of days + 2(head + footer)blank
    # cols = 7 cols of week + 1 blank for left + 1 col for right
    if len([day for day in calendar.Calendar(firstweekday=0).itermonthdays(datetime.datetime.now().year, month)])+1>35:
        rows, cols = 10, len(WEEK) + 2
    else:
        rows, cols = 9, len(WEEK) + 2
    colSpace, rowSpace = width // cols, height // rows
    
    white_block=Image.new('RGBA',size=(width-200, height-200), color=(255,255,255,90))
    img.paste(white_block,(100,100),mask=white_block)
    # define font and size
    month_font = f'{plugin_path}/fonts/DancingScript-Bold.ttf'
    title_font = f'{plugin_path}/fonts/DancingScript-Bold.ttf'
    day_font = f'{plugin_path}/fonts/SitkaZ.ttc'
    month_size, title_size, day_size = 80, 60, 70
    ellipse_r=80

    draw = ImageDraw.Draw(img)
    for i in range(len(WEEK) + 1):
        # draw month title
        if i == 0:
            draw.text((colSpace, rowSpace), MONTH[month-1], fill=(0,0,0,), font=ImageFont.truetype(month_font, size=month_size))
            top = rowSpace // 10
            draw.line(xy=[(colSpace, rowSpace*2-top * 2), (colSpace*7.5, rowSpace*2-top * 2)], fill=(255,255,255))
            draw.line(xy=[(colSpace, rowSpace * 2 - top * 1), (colSpace * 7.5, rowSpace * 2 - top * 1)], fill=(255, 255, 255))
            continue
        # draw week title
        draw.text((colSpace*i, rowSpace*2), WEEK[i-1], fill=(0,0,0), font=ImageFont.truetype(title_font, size=title_size))

    # draw days
    cal = calendar.Calendar(firstweekday=0)
    row, col = 3, 2
    mark=Image.open(f'{plugin_path}/200x200.png').convert('RGBA').resize((100, 100), Image.ANTIALIAS)
    for day in cal.itermonthdays(datetime.datetime.now().year, month):
        if day > 0:
            # if weekday, draw with red color
            if col == 1 or col == 7:
                fill = (255, 0, 0)
            else:
                fill = (255, 255, 255)
            # print(day)
            if ('%02d' % day) in day_list:
                img.paste(mark,(colSpace * col , rowSpace * row-20),mask=mark.split()[3])
            if day <10: 
                draw.text((colSpace * col+ellipse_r/2, rowSpace * row), str(day), fill=fill, font=ImageFont.truetype(day_font, size=day_size))
            else:
                draw.text((colSpace * col-day_size/2+ellipse_r/2, rowSpace * row), str(day), fill=fill, font=ImageFont.truetype(day_font, size=day_size))
        col += 1
        # to a new week
        if col == 8:
            col = 1
            row += 1
    img.save(f"{plugin_path}/{MONTH[month-1]}.png")
    return MONTH[month-1] + '.png'
