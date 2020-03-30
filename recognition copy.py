#!/usr/bin/python3
import os
import face_recognition

# 匹配阈值
TOLERANCE = 0.60
base_image_path="base_image"  #待读取的文件夹

# 基础库读取图片
def get_base_image():   
    path_list=os.listdir(base_image_path)
    path_list.sort() #对读取的路径进行排序
    return [dict(name=filename.split('.jpg')[0], path=os.path.join(base_image_path,filename)) for filename in path_list]

# 图片建模
def face_modeling(image_path):
    image = face_recognition.load_image_file(image_path)
    location = face_recognition.face_locations(image,model="hog")
    face_encodings = face_recognition.face_encodings(image, location)[0]

    return dict(location=location,face_encodings=face_encodings)

# 基础库与陌生人对比
def compare_faces(base_encodings, compare_face):
    results = face_recognition.compare_faces(base_encodings, compare_face, tolerance=TOLERANCE)
    return results

def get_base_modelings():
    base_images = get_base_image()
    base_face_modeling = []
    for img in base_images:
        image_encodings = face_modeling(img.get('path'))
        base_face_modeling.append({
            'name':img.get('name'),
            'path':img.get('path'),
            'location': image_encodings.get('location'),
            'face_encodings': image_encodings.get('face_encodings')
        })

    return base_face_modeling

if __name__ == "__main__":
    base_modelings = get_base_modelings()
    base_encodings = [model.get('face_encodings') for model in base_modelings]
    check_face = "trump2.jpg"
    check_face_modeling = face_modeling(check_face)
    compare_result = compare_faces(base_encodings, check_face_modeling.get('face_encodings'))
    print('compare_result:', compare_result)
    index = compare_result.index(True)
    print('这是:', base_modelings[index].get('name'))
    
 
    