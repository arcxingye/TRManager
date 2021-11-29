from PIL import Image, ImageDraw, ImageFont

# 合成背包
IMAGE_SIZE = 50  # 每个格子的大小
font1 = ImageFont.truetype('C:/windows/fonts/simhei.ttf', 25)
font2 = ImageFont.truetype('C:/windows/fonts/simhei.ttf', 18)
async def synInv(img_list: list, number: list, name: str):
    try:
        to_image = Image.open("./data/images/inv/InvFrame.png")
        # 横向渲染5行10列
        for y in range(1, 6):
            for x in range(1, 11):
                img_xy_index=(10 * (y - 1) + x - 1)
                if img_list[img_xy_index]:
                    from_image = Image.open(img_list[img_xy_index]).convert('RGBA')
                    to_image.paste(from_image, ((x - 1) * IMAGE_SIZE+(x*54)-22, (y - 1) * IMAGE_SIZE+(y*55)+13), from_image)
                    if number[img_xy_index]!='1':
                        ImageDraw.Draw(to_image).text(((x - 1) * IMAGE_SIZE+(x*54)-22, (y - 1) * IMAGE_SIZE+(y*55)+52), number[img_xy_index], font=font1)
        # 竖向渲染4行2列(钱币弹药)
        for x in range(1, 3):
            for y in range(1, 5):
                img_yx_index=(50 + (4 * (x - 1) + y - 1))
                if img_list[img_yx_index]:
                    from_image = Image.open(img_list[img_yx_index]).convert('RGBA')
                    to_image.paste(from_image, ((x - 1) * IMAGE_SIZE+(x*31)+1050, (y - 1) * IMAGE_SIZE+(y*25)+230), from_image)
                    if number[img_yx_index]!='1':
                        ImageDraw.Draw(to_image).text(((x - 1) * IMAGE_SIZE+(x*31)+1050, (y - 1) * IMAGE_SIZE+(y*25)+250), number[img_yx_index], font=font2)
        # 鼠标操作着的物品
        if img_list[58]:
            from_image = Image.open(img_list[58]).convert('RGBA')
            to_image.paste(from_image, (1100, 80), from_image)
            ImageDraw.Draw(to_image).text((1100, 120), number[58], font=font1)
        save_url="./data/images/inv/inv.jpg"
        to_image.save(save_url)
    except:
        return ''
    else:
        return save_url

# 合成饰品