import cv2

#sudo modprobe bcm2835-v4l2

__camera = cv2.VideoCapture(0)
__scale_division = 2

def deinit() :    
    __camera.release()
    cv2.destroyAllWindows()
    
def capture() :
    ret, image = __camera.read()
    return image

def size_of_image(image) :
    return image.shape[1::-1]

def shrink_image(image) :
    old_size = size_of_image(image)
    new_size = tuple( scale//__scale_division for scale in old_size )
    return cv2.resize(image, new_size, interpolation=cv2.INTER_CUBIC)

def flip_up_down(image) :
    return cv2.flip(image,0)

def flip_left_right(image) :
    return cv2.flip(image,1)

def show_image(image) :
    cv2.imshow('image', image)
