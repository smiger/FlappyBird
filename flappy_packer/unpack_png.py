#!python
import os,sys
from xml.etree import ElementTree
from PIL import Image

def tree_to_dict(tree):
    d = {}
    for index, item in enumerate(tree):
        if item.tag == 'key':
            if tree[index+1].tag == 'string':
                d[item.text] = tree[index + 1].text
            elif tree[index + 1].tag == 'true':
                d[item.text] = True
            elif tree[index + 1].tag == 'false':
                d[item.text] = False
            elif tree[index+1].tag == 'dict':
                d[item.text] = tree_to_dict(tree[index+1])
    return d 
    
def gen_png_from_plist(plist_filename, png_filename):
    file_path = plist_filename.replace('.txt', '')
    big_image = Image.open(png_filename)
    file = open(plist_filename)
    for line in file:
        rectlist = line.split()
        width = int(rectlist[1])
        height = int(rectlist[2])
        startX = int(float(rectlist[3]) * 1024)
        startY = int(float(rectlist[4]) * 1024)
        box=( 
            startX,
            startY,
            startX + width,
            startY + height
            )
        print box
        sizelist = [width,height]
        print sizelist
        rect_on_big = big_image.crop(box)
        result_image = Image.new('RGBA', sizelist, (0,0,0,0))
        result_box=(
                0,
                0,
                sizelist[0],
                sizelist[1]
                )
        print result_box
        result_image.paste(rect_on_big, result_box, mask=0)

        if not os.path.isdir(file_path):
            os.mkdir(file_path)
        outfile = (file_path+'/' + rectlist[0])
        #print k
        if outfile.find('.png') == -1:
            outfile = outfile + '.png'
        print outfile, "generated"
        result_image.save(outfile)
    file.close()

if __name__ == '__main__':
    filename = sys.argv[1]
    plist_filename = filename + '.txt'
    png_filename = filename + '.png'
    if (os.path.exists(plist_filename) and os.path.exists(png_filename)):
        gen_png_from_plist( plist_filename, png_filename )
    else:
        print "make sure you have both plist and png files in the same directory"
