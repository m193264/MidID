from PIL import Image
from PIL import ExifTags
import numpy as np
import re
import os
import argparse


def exif_open(img_fname):
  try:
      image=Image.open(img_fname)
      for orientation in ExifTags.TAGS.keys():
          if ExifTags.TAGS[orientation]=='Orientation':
              break
      exif=dict(image._getexif().items())

      if exif[orientation] == 3:
          image=image.rotate(180, expand=True)
      elif exif[orientation] == 6:
          image=image.rotate(270, expand=True)
      elif exif[orientation] == 8:
          image=image.rotate(90, expand=True)
  except (AttributeError, KeyError, IndexError):
      # cases: image don't have getexif
      pass
  return image

def format_img_name(name):
    fname = str(name)
    try:
        p = re.compile("[1|2][0-9]{5}")
        fname = p.search(name).group(0)
    except Exception as e:
        print("\n\tException:")
        print("\tError while reformatting name")
        print('\t'+str(e))
    return fname+".jpg"

def resize_imgs(img_folder,img_fnames,resize_w=640,resize_h=960):
    resized_folder = img_folder+'-resized'
    os.makedirs(resized_folder)
    size = (resize_w,resize_h)
    for f_idx in range(len(img_fnames)):
        fullname = os.path.join(img_folder, img_fnames[f_idx])
        print(f_idx+1,' of ',len(img_fnames),end=' ')
        try:
            # Verify image file OK
            im = Image.open(fullname)
            im.verify()
            print(fullname,'OK, Resizing')
			# Must reload image after verify
            im = exif_open(fullname)
            im.thumbnail(size,Image.ANTIALIAS)
            fname = format_img_name(img_fnames[f_idx])
            im.save(resized_folder+'/'+fname,"JPEG",optimize=True)
        except Exception as e:
            print("\n\tException:")
            print('\t'+str(e))

def main():
    parser=argparse.ArgumentParser()
    # First mandatory arg is name of img folder containing imgs to resize
    # if dirname is 'dir', write 'dir' and not 'dir/'
    parser.add_argument("img_folder")

    # optional args to specify max resize dimensions
    parser.add_argument("resized_pixel_width",nargs='?',default=640)
    parser.add_argument("resized_pixel_height",nargs='?',default=960)

    args=parser.parse_args()
    img_folder=args.img_folder
    resize_w = args.resized_pixel_width
    resize_h = args.resized_pixel_height

    print('Resizing to ',resize_w,' x ',resize_h)

    # Load all files in given directory
    img_fnames = []
    print("Loading file names",end="...")
    for (dirpath, dirnames, filenames) in os.walk(img_folder):
    	img_fnames.extend(filenames)
    print("Done")

    # Resize images
    print("Resizing images\n")
    resize_imgs(img_folder,img_fnames)
    print("Done")




if __name__ == "__main__":
    main()
