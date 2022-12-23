from AES import AES128_EBC
from PIL import Image
import numpy as np
key = "sajid ekta bolod"
aes = AES128_EBC(key)
'''
image = Image.open('sajid.jpg')

resizedimage = image.resize((256, 256))
print(resizedimage.size)
#resizedimage.show()
a = np.asarray(resizedimage)
flat_a = a.flatten()
encrypted_image = aes.encrypt_image(flat_a.tolist())
b = np.array(encrypted_image).reshape(256,256,3)
new = Image.fromarray(b)
new.show()'''



