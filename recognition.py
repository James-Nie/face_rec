#!/usr/bin/python3
import os
import face_recognition
from PIL import Image

class Recognition:

    def __init__(self, tolerance=0.60,base_image_path='base_image'):
        self.tolerance = tolerance # 匹配阈值
        self.base_image_path = base_image_path # 基础库路径
        self.base_modelings = []
        self.init_base_modelings()

    # 基础库读取图片
    def get_base_image(self):   
        path_list=os.listdir(self.base_image_path)
        path_list.sort() #对读取的路径进行排序
        return [dict(name=filename.split('.jpg')[0], path=os.path.join(self.base_image_path,filename)) for filename in path_list]

    # 图片建模
    def face_modeling(self, image_path):
        img= Image.open(image_path)#返回一个Image对象
        width = img.size[0]
        height = img.size[1]

        image = face_recognition.load_image_file(image_path)
        location = face_recognition.face_locations(image, model="hog")
        if not location:
            return None

        face_encodings = face_recognition.face_encodings(image, location)[0]

        top, right, bottom, left = location[0]
        perc_location=dict(
            top=round(top/height, 2),
            left=round(left/width, 2),
            width=round((right-left)/width, 2),
            height=round((bottom-top)/height, 2)
        )

        return dict(location=perc_location,face_encodings=face_encodings)

    # 基础库与陌生人对比
    def compare_faces(self, base_encodings, compare_face):
        results = face_recognition.compare_faces(base_encodings, compare_face, tolerance=self.tolerance)
        return results
    
    def save_base_modelings(self, name, img_path):
        image_model = self.face_modeling(img_path)
        if image_model:
            model = {
                'name': name,
                'path': img_path,
                'location': image_model.get('location'),
                'face_encodings': image_model.get('face_encodings')
            }
            self.base_modelings.append(model)
            return model
        else:
            return False

    def init_base_modelings(self):
        base_images = self.get_base_image()
        for img in base_images:
            self.save_base_modelings(img.get('name'), img.get('path'))
    
    def get_compare_result(self, check_face_encodings):
        base_encodings = [model.get('face_encodings') for model in self.base_modelings]
        if not base_encodings:
            return None
        face_distances = face_recognition.face_distance(base_encodings, check_face_encodings)
        index_match = None
        dis_match = 1
        for index,dis in enumerate(face_distances):
            if dis_match > dis and dis <= self.tolerance:
                dis_match = dis
                index_match = index
        
        if index_match is None:
            return None
        else:
            model = self.base_modelings[index_match]
            model.update({'match': dis_match})
            return model