import os
import shutil
import random
import argparse
import cv2
class LabelvocTofasterrcnnvoc(object):
    '''
    创建支持fasterrcnn和ssd数据格式的标准voc格式数据集
    创建如下文件结构：
    --VOCdevkti
    -----VOC2007
    --------Annotations
    --------ImageSets
    ------------train.txt
    ------------valid.txt
    --------JPEGImages
    '''
    def __init__(self,root_path,xml_path, jpg_path, train_val_ratio):
        self.xml_path = xml_path
        self.jpg_path =jpg_path
        self.Annotations = os.path.join(root_path,'VOCdevkit/VOC2007/Annotations')
        self.ImageSets_Main =os.path.join(root_path,'VOCdevkit/VOC2007/ImageSets/Main')
        self.JPEGImages = os.path.join(root_path,'VOCdevkit/VOC2007/JPEGImages')
        self.train_val_ratio = train_val_ratio
        self.make_dir()

    def cp_xml_image_write_txt(self):
        '''
        划分数据集和验证集：创建tran.txt和valid.txt
        train.txt:存放训练数据集图像的路径
        valid.txt: 存放验证数据集图像路径
        '''
        self.copy_file()
        xml_list = os.listdir(self.xml_path)
        random.shuffle(xml_list)
        number_all= len(xml_list)
        train_number = int(self.train_val_ratio * number_all)
        traindata =open(self.ImageSets_Main + '/' + 'train.txt', 'w')
        validata = open(self.ImageSets_Main + '/' + 'valid.txt', 'w')
        print('xml_list:',xml_list)
        for i in range(number_all):
            print("xml_list[i][0]:",str(xml_list[i].split('.')[0]))
            if i<train_number:
                # traindata.write(str(xml_list[i].split('.')[0]) +'\n')
                traindata.write(self.JPEGImages+'/'+str(xml_list[i].replace('xml','jpg')) + '\n')
                #self.JPEGImages
            else:
                validata.write(self.JPEGImages+'/'+str(xml_list[i]).replace('xml','jpg') +'\n')
        return 0
    def make_dir(self):
        '''
        创建数据集的目录结构
        '''
        os.makedirs(self.Annotations,exist_ok=True)
        os.makedirs(self.ImageSets_Main, exist_ok=True)
        os.makedirs(self.JPEGImages, exist_ok=True)
    def copy_file(self):
        for i in os.listdir(self.xml_path):
            shutil.copy(self.xml_path + '/'+str(i), self.Annotations + '/'+str(i))
        for i in os.listdir(self.jpg_path):
            shutil.copy(self.jpg_path + '/'+str(i), self.JPEGImages + '/'+str(i))
        return 0
def excute_main():
    root_path = os.getcwd()
    xmlpath = os.path.join(root_path,'证件照片检测/my_data/newAnnotations')
    jpgpath = os.path.join(root_path,'证件照片检测/my_data/JPEGImages')
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_path', type=str, default=root_path, help='主路径')
    parser.add_argument('--xml_path', type=str, default=xmlpath,help='xml文件路径')
    parser.add_argument('--jpg_path', type=str, default=jpgpath, help='图像文件路径')
    parser.add_argument('--train_val_ratio', type=float, default=0.8, help='训练集所占比例')
    opt = parser.parse_args()
    abc = LabelvocTofasterrcnnvoc(opt.root_path,opt.xml_path,opt.jpg_path,opt.train_val_ratio)
    abc.cp_xml_image_write_txt()
if __name__=='__main__':
    excute_main()
    # ab = ReName_file('/home/goldsun/桌面/数据集创建代码/证件照片检测/my_data/JPEGImages')
    # ab.re_names()

