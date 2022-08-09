import imp
from Decode_QR import *
from server_detection import *
from preprocessing import *
from app import *
from PIL import Image
import glob
def decode_pyzbar_thuan(img):
    """
    Check scanQR code by Pyzbar with no detect
    """
    item = []
    barcodes = pyzbar.decode(img, symbols=[pyzbar.ZBarSymbol.QRCODE])
    for barcode in barcodes:
        content = ""
        barcodeData = barcode.data.decode("utf-8")
        content = "{}".format(barcodeData)
        if content != "" and content not in item:
            item.append(content)
    return img, item

def scan_qrcode(image):
    """
    Scan test qr
    """
    img, item = decode_image(image)
    #img, item = decode_pyzbar_thuan(image)
    return img, len(item)

a = 0
sum = 0
for filename in glob.glob('/run/user/1000/gvfs/google-drive:host=gm.uit.edu.vn,user=18521655/0AFBvObI2Dya1Uk9PVA/1-1b83NknWhvPOMW5v8a1Z1vCFBJ2R3I1/1IVLLT7gSsa427FOc_t8eXKGqm4d0E5bI/1TDigqmU8egBclzXrgpqqWvr1ViInJ7SC/*.JPG'): #assuming gif
    a +=1
    im=Image.open(filename)
    newImage = np.array(im.convert('RGB'))
    img2, total = scan_qrcode(newImage)
    sum += total
    cv2.imwrite("/home/vinh/ProjectEDU/qr_detection_gpu/scr/test_qr_thuan/{}_{}.JPG"    .format(a,total), img2)
    print(total)
print(sum)  