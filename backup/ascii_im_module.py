import cv2

def setupAsciiMapping():
    s = ' .-=+*#@'[::-1]
    temp = ''
    for c in s :
        temp += c*(256//8)

    temp += ' '*(280-len(temp))
    for i in range(260) :
        asciiToNum[i] = temp[i]

def ConvertToAscii(img):
    transformedAscii = []

    for i in img:
        temp = []
        
        for j in i:
            temp.append(asciiToNum[j])
            
        transformedAscii.append(temp)
    
    for i in range(len(transformedAscii)):
        transformedAscii[i] = ''.join(transformedAscii[i])

    return transformedAscii

## initialize ####
asciiToNum = {}
setupAsciiMapping()
