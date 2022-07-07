import xml.etree.ElementTree as ET
import os
import argparse
import cv2
class ModifyXml(object):
    '''
    修改mxl文件内容
    '''
    def __init__(self,xml_path,modify_tags,save_xml_path,rewrite_txt):
        '''
        xml_path：xml地址
        modify_tags：需要修改内容所在的标签
        save_xml_path：新的xml保存地址
        rewrite_txt：新的写入内容
        '''
        self.xml_path = xml_path
        self.modify_tags = modify_tags
        self.save_xml_path = save_xml_path
        self.rewrite_txt = rewrite_txt
    def readxml(self,new_path):
        doc = ET.parse(new_path)
        root = doc.getroot()
        sub1 = root.find(self.modify_tags)  # 找到filename标签，
        #xml文件中图像名 602.jpg
        new_images_name = sub1.text.split('/')[-1]
        #新的替换文本：/home/chenzhenyu/桌面/证件照片检测/my_data/JPEGImages/602.jpg
        replace_text = self.rewrite_txt + '/'+new_images_name
        #标签内容修改
        sub1.text = replace_text
        #最终保存的xml文件名及路径
        finally_save_new_xml_path=str(self.save_xml_path)+'/'+new_images_name.split('.')[0]+'.xml'
        print("当前保存：",finally_save_new_xml_path)
        #保存
        doc.write(finally_save_new_xml_path,'utf-8')  # 保存修改
        return 0
    def save_xml(self):
        if os.path.isdir(self.xml_path):
            for i in os.listdir(self.xml_path):
                new_path = os.path.join(self.xml_path,i)
                print("new_path:",new_path)
                self.readxml(new_path)
            print("..........转化完成..........")
        elif os.path.isfile(self.xml_path):
            self.readxml(self.xml_path)
        return 0
def excute_modify():
    '''
    执行修改xml内容主函数
    '''
    rootpath = os.getcwd()
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml_path', type=str, default=os.path.join(rootpath, 'VOCdevkit/VOC2007/Annotations'), help='xml路径')
    parser.add_argument('--modify_tags', type=str, default='path', help='model path(s)')
    parser.add_argument('--save_xml_path', type=str, default=os.path.join(rootpath, 'VOCdevkit/VOC2007/newAnnotations'), help='新的xml保存地址')
    parser.add_argument('--rewrite_txt',type=str, default=os.path.join(rootpath,'VOCdevkit/VOC2007/JPEGImages'), help='新的写入内容')
    opt = parser.parse_args()

    os.makedirs(opt.save_xml_path,exist_ok=True)
    print(opt)
    ab = ModifyXml(opt.xml_path, opt.modify_tags, opt.save_xml_path, opt.rewrite_txt)
    ab.save_xml()
    return 0

class ReName_file(object):
    '''
    修改图像文件名，使图像后缀保持一致，避免麻烦
    '''
    def __init__(self,file_name):
        self.file_name = file_name
    def re_names_images_name(self):
        file_list = os.listdir(self.file_name)
        os.makedirs(self.file_name.replace('JPEGImages','JPEGImages'),exist_ok=True)
        counter_images_number = 0
        for i in file_list:
            counter_images_number += 1
            img = cv2.imread(self.file_name+'/'+str(i))
            # print(img.shape)
            print(self.file_name.replace('JPEGImages','JPEGImages')+'/'+str(i.split('.')[0])+'.jpg')
            cv2.imwrite(self.file_name.replace('JPEGImages','JPEGImages')+'/'+str(i.split('.')[0])+'.jpg',img)
        print("该目录下总共有图像文件：%s \n读取并重新命名成功的数量为：%s \n新生成的图像保存在：%s"
              %(len(file_list),counter_images_number,self.file_name.replace('JPEGImages','JPEGImages')))
def excute_ReName_file():
    '''
    修改图像名称的运行主函数
    '''
    root_path = os.getcwd()
    filename = os.path.join(root_path,'JPEGImages')
    print(filename)
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, default=filename, help='主路径')
    opt = parser.parse_args()
    abc = ReName_file(opt.filename)
    abc.re_names_images_name()

if __name__=='__main__':
    excute_ReName_file()
    # excute_modify()