import xml.etree.ElementTree as ET
import os
import argparse
import random
import shutil
rootpath = os.getcwd()
classes = ["0", "1"]
class VocToYolo(object):
    '''
    labelimg贴的标签voc文件转化为yolo支持的格式
    '''
    def __init__(self,xml_path,save_txt_path):
        self.xml_path =xml_path
        self.save_txt_path = save_txt_path
        self.roots = self.readxmls()
    def readxmls(self):
        f = open(self.xml_path)
        xml_text = f.read()
        root = ET.fromstring(xml_text)
        f.close()
        return root
    def get_image_path(self):
        root = self.readxmls()
        images_path = root.find('path')
        img_name = images_path.text.split('/')[-1].split('.')[0]
        print(img_name)
        return images_path.text,img_name
    def get_hw(self):
        size = self.roots.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        return (w,h)
    def convert_size(self,size, box):
        dw = 1.0 / size[0]
        dh = 1.0 / size[1]
        x = (box[0] + box[1]) / 2.0
        y = (box[2] + box[3]) / 2.0
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh
        return (x, y, w, h)
    def get_xyxy_label(self):
        _,a = self.get_image_path()
        os.makedirs(self.save_txt_path,exist_ok=True)
        out_file = open(self.save_txt_path+'/' + str(a) + '.txt', 'w')
        for obj in self.roots.iter('object'):
            cls = obj.find('name').text
            if cls not in classes:
                print(cls)
                continue
            print("标签：",cls)
            label_now = classes.index(cls)
            print("标签索引:", label_now)
            xmlbox = obj.find('bndbox')
            xmin = int(float(xmlbox.find('xmin').text))
            ymin = int(float(xmlbox.find('ymin').text))
            xmax = int(float(xmlbox.find('xmax').text))
            ymax = int(float(xmlbox.find('ymax').text))
            size = self.get_hw()
            xyhw = self.convert_size(size, (xmin, ymin, xmax, ymax))

            out_file.write(str(label_now) + " " + " ".join([str(xyhw) for xyhw in xyhw]) + '\n')
            print(xmin, ymin, xmax, ymax)
        return 0
def excute_voc_to_yolo():
    '''
    转化为yolo格式主函数
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml_path', type=str, default='./Annotations', help='xml路径')
    parser.add_argument('--save_txt', type=str, default='./labels', help='txt保存路径')
    opt = parser.parse_args()
    for i in os.listdir(opt.xml_path):
        xml_path = opt.xml_path + '/' + str(i)
        ab = VocToYolo(xml_path, opt.save_txt)
        ab.get_xyxy_label()

class SplitValTrain(object):
    '''
    划分验证集和训练集
    '''
    def __init__(self,rootpath,label_path,images_path,ratios):
        self.rootpath = rootpath
        self.label_path = label_path
        self.images_path = images_path
        self.ratios = ratios
        self.train_images_path = rootpath + '/mydata/train/images'
        self.train_labels_path = rootpath + '/mydata/train/labels'
        self.val_images_path = rootpath + '/mydata/val/images'
        self.val_labels_path = rootpath + '/mydata/val/labels'
    def make_data_dir(self):
        os.makedirs(self.train_images_path,exist_ok=True)
        os.makedirs(self.train_labels_path,exist_ok=True)
        os.makedirs(self.val_images_path, exist_ok=True)
        os.makedirs(self.val_labels_path, exist_ok=True)
    def split_val_train(self):
        self.make_data_dir()
        filename = os.listdir(self.images_path)
        # print(filename)
        random.shuffle(filename)

        go_to = int(self.ratios*len(filename))
        print(go_to,len(filename))
        for i in range(len(filename)):
            name_num = filename[i].split('.')[0]
            print(filename[i])
            if i<go_to:
                shutil.copy(self.images_path+'/'+str(filename[i]), self.train_images_path)
                shutil.copy(self.label_path + '/' + str(name_num) + '.txt', self.train_labels_path)
            else:
                shutil.copy(self.images_path + '/' + str(filename[i]), self.val_images_path)
                shutil.copy(self.label_path + '/' + str(name_num) + '.txt', self.val_labels_path)
        return 0
def excute_split_val_train():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rootpath', type=str, default=rootpath, help='当前目录')
    parser.add_argument('--label_path', type=str, default='./labels', help='txt文件路径')
    parser.add_argument('--images_path', type=str, default='./JPEGImages', help='图像路径')
    parser.add_argument('--ratios', type=float, default=0.8, help='训练集划分比例')
    opt = parser.parse_args()
    ab = SplitValTrain(opt.rootpath, opt.rootpath, opt.label_path, opt.images_path, opt.ratios)
    ab.split_val_train()
if __name__ == '__main__':
    excute_split_val_train()