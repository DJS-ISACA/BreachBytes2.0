from PIL import Image

flag = ''

raw_img = Image.open(r'image0.png')
raw_pix = list(raw_img.getdata())
for i in range(1,217):
    #print("trying image",i)
    embed_img = Image.open(f'image{i}.png')
    embed_pix = list(embed_img.getdata())
    if raw_pix != embed_pix:
        flag += "1"
        continue
    flag += "0"
    embed_img.close()
raw_img.close()

print(flag)
flag = ''.join([chr(int(flag[i:i+8], 2)) for i in range(0, len(flag), 8)])
print(flag)