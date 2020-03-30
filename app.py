#!/usr/bin/python3

from sanic import Sanic
from sanic.response import json as sanic_json
import os,json
from recognition import Recognition
from util.util import base64_to_image

app = Sanic(name='my_face_app')

app.static('/static', './view')

@app.route("/")
async def index(request):
    return sanic_json({"hello": "world"})

 
@app.route("/favicon.ico")
async def favicon(request):
    return sanic_json({"hello": "world"})

@app.post("/api/save-face")
async def checkFace(request):
    name = request.json.get('name')
    base_modelings = app.rec.base_modelings

    check_model = None
    for m in base_modelings:
        if name == m.get('name'):
            check_model = m
            break

    if check_model:
        return sanic_json({
            "type": '-1',
            "msg": f"基础库已有{name}",
            "data": None
        })

    image = request.json.get('image')
    image_type = image.split(';base64,')[0].split('data:image/')[1]
    base64_code = image.split(';base64,')[1]

    save_face_path = f'base_image/{name}.{image_type}'
    base64_to_image(save_face_path, base64_code)
    
    save_res = app.rec.save_base_modelings(name, save_face_path)
    if not save_res:
        return sanic_json({"type":-1, "data": None, "msg":"没有检测到人脸请重新上传!"})

    return sanic_json({
        "type": 0,
        "msg":"建模成功!",
        "data": dict(
            name=name,
            path=save_face_path,
            location=save_res.get('location')
        )
    })

@app.websocket('/socket/check-face')
async def feed(request, ws):
    while True:
        rec_data = await ws.recv()
        rec_data = json.loads(rec_data)
        rec_type = rec_data.get('type')
        
        if rec_type == 'connect':
            print(rec_data.get('data'))
        elif rec_type == 'check_face':
            image = rec_data.get('data')
            image_type = image.split(';base64,')[0].split('data:image/')[1]
            base64_code = image.split(';base64,')[1]

            check_face = f'temp.{image_type}'
            base64_to_image(check_face,base64_code)

            check_face_modeling = app.rec.face_modeling(check_face)
            if not check_face_modeling:
                await ws.send(json.dumps({
                    "type": "data",
                    "data": None,
                    "msg":"没有检测到人"
                }))
            else:
                compare_result = app.rec.get_compare_result(check_face_modeling.get('face_encodings'))
                if not compare_result:
                    await ws.send(json.dumps({
                        "type": "data",
                        "data": None,
                        "msg":"没有匹配到底库数据"
                    }))
                else:
                    await ws.send(json.dumps({
                        "type": "data",
                        "msg":"",
                        "data": dict(
                            name=compare_result.get('name'),
                            path=compare_result.get('path'),
                            location=check_face_modeling.get('location'),
                            match=compare_result.get('match')
                        )
                    }))
        

@app.listener('before_server_start')
def before_server_start(app, loop):
    app.rec = Recognition()  #创建对比对象

@app.listener('after_server_start')
async def notify_server_started(app, loop):
    
    print('Server is start: 127.0.0.1:8000')

# @app.listener('before_server_stop')
# async def notify_server_stopping(app, loop):
#     print('Server shutting down!')

# @app.listener('after_server_stop')
# async def close_db(app, loop):
#     await app.db.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    