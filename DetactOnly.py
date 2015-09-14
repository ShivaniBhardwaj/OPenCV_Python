import cv2
import csv
import os
import shutil

def path(p):
    #print(p)
    if not os.path.exists(p):
        os.mkdir(p)
    #print(p)
    return p
'''
# Open csv file
'''
def csv_open( path):
    csv_file= list()
    #csv.DictWriter(open('file3.csv','w'), delimiter=',', lineterminator='\n', fieldnames=headers)
    #csv_file.append(csv.DictWriter( open(path, 'a'), delimiter=',', lineterminator='\n'))
    csv_file.append(open(path, 'ab'))
    csv_file.append(csv.writer(csv_file[0], delimiter=','))
    #writer = csv.writer(csv_file, delimiter=',')       
    return csv_file        

'''
# Write data to csv file
'''
def csv_writer( writer, data):
    #print(data)
    writer.writerow(data)

'''
# Close csv file
'''
def csv_close( csv_file):
    csv_file.close()

'''
# read csv file
''' 
def read_csv(filename):
    #print(filename)
    data = []
    with open(filename) as csvfile:
        read = csv.reader(csvfile, delimiter=',', quotechar='|')
        count = 0
        for line in read:
            data.append(line)
    return data



def detect(path):
    img = cv2.imread(path)
    
    cascade = cv2.CascadeClassifier("C:/opencv/build/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml")
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))
    #print('detect',rects)
    if len(rects) == 0:
        #print(path)
        return [], img
    rects[:, 2:] += rects[:, :2]
    return rects, img

def box(rects, img, buf):
    for x1, y1, x2, y2 in rects:
        #cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
        cv2.rectangle(img, (x1-buf, y1-buf), (x2+buf, y2+buf), (127, 255, 0), 2)
    cv2.imwrite('D:/GITRepository/testImg/detected2.jpg', img);

def crop(rects, img, buf, name, dest):
    '''
    first supply the startY and endY coordinates, followed by the startX and endX coordinates to the slice.
    '''
    #print(name)
    datalist = []
    face =1
    height,width,c = img.shape
    
    if (len(rects) <= 1):
        
        imgname = name[name.rfind('\\')+1:]
        
        datalist.append([os.path.join(dest, imgname),0,0,height, width,len(rects)])
        print([os.path.join(dest, imgname), 0,0, width,height,len(rects)])
        #print(os.path.join(dest, imgname))
        shutil.copy(name, os.path.join(dest, imgname))
        
    else:

        for x1, y1, x2, y2 in rects:
            
            x1 = x1-buf
            if x1<0:
                x1 = 0
            y1 = y1-buf
            if y1<0:
                y1 = 0
            y2 = y2+buf
            if y2>height:
                y2 = height
            x2 = x2+buf
            if x2>width:
                x2 = width

            cropped = img[y1:y2, x1:x2]
            iname = name[:name.rfind('.')] + '_'+str(face)+ name[name.rfind('.'):]
            #print(os.path.join(dest, iname[iname.rfind('\\')+1:]))
            cv2.imwrite(os.path.join(dest, iname[iname.rfind('\\')+1:]), cropped)               
            datalist.append([os.path.join(dest, iname[iname.rfind('\\')+1:]), x1,y1,x2,y2,len(rects)])
            print(iname, x1,y1,x2,y2,len(rects))
            face+=1
    print(len(datalist))
    return datalist

def processImg(src, dest):
    clist =[]
    for r,d,f in os.walk(src):
        for di in d:
            dd = path(src.replace(src,dest) )
            src1 = os.path.join(r,di)
            #print(r,src.replace(src,dest))
            #des = path(src.replace('//D//','//CroppedfirstD//'))
            des = path(src1.replace(src,dest))
            #print(des)
        for fi in f:
            if '.txt'not in fi:
                 if ('.csv' and '.xlsx') not in fi:
                    fsrc = os.path.join(r,fi)
                    #print(r,fi)
                    fdes =path(dest+r[r.rfind('/')+1:]+'/')
                    print(fsrc,fdes)
                    if 'DOC' not in fdes:
                        rects, img = detect(fsrc)
                        clist.extend(crop(rects, img, 70, fsrc, fdes))
    return clist
    

if __name__=='__main__':
    
    src = 'D:/ITWICC2/E/'
    dest = path('D:/ITWICC2/CroppedfirstE/')
    #csvRead = 'D:/ChildStarler/test.csv'
    #csvRead = 'D:/ITWICC2/backup/DOC/dataNamed.csv'
    #csvReader = read_csv(csvRead)
    datalist = processImg(src,dest)[:]
    print(len(datalist))
    


    #data = crop(csvReader, src)
    
    #print(data)
    csvWrite = os.path.join(dest,'dataCroppedNamedE.csv')
    #csvWrite = 'D:/ITWICC2/dataCroppedNamed.csv'
    csvWriteHandle = csv_open(csvWrite)

    print('----------------------------------------------------------')
    for line in datalist:
        #print(line)
        csv_writer(csvWriteHandle[1], line)

    csv_close(csvWriteHandle[0])
    print('done')
    
