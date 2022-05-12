import json
import random
import PySimpleGUI as sg

from cProfile import label
from locust import HttpLocust, HttpUser, TaskSet, SequentialTaskSet, task, run_single_user

image_folder = "/Users/gaobo/Desktop/Hair/01"
# label_sn = ""
images = []

# 收集图片
def search_images():
    import os
    
    if len(images) == 0:
        file_list = sorted(os.listdir(image_folder))
        for file in file_list:
            if (file.startswith(".")):
                continue
            images.append("{}/{}".format(image_folder, file))

# 随机获取图片
def get_random_image():
    image_count = len(images)
    if image_count > 0:
        index = random.randint(0, image_count - 1)
        image = images[index]
        # print("->image: {}".format(image))
        print("\033[1;34m ->image: {}\033[0m".format(image))
        return image
    else:
        return None

# 选择图片所在目录的界面
def start_work():
    import os
    
    version = 1.0
    sg.theme('Light Blue 2')
    
    layout = [[sg.Text('功能说明：选择测试图片做在的目录，然后进行压力测试', text_color="blue")],
              [sg.Button('OK'), sg.Button('Exit')],
              [sg.Text('选择目录', auto_size_text=True), sg.Input(size=(40, 1)), 
               sg.FolderBrowse(key='-Folder-', initial_folder=os.path.dirname(__file__))]
             ]

    window = sg.Window('压力测试工具({})'.format(version), layout, resizable=True)

    while True:
        event, values = window.read()
        print(f'Event: {event}')
        
        if event == 'OK':
            if (values[0] == ""):
                sg.popup("请选择目录")
            elif (not os.path.exists(values[0])):
                sg.popup("目录不存在，请重新选择")
            else:
                global image_folder
                image_folder = values[0]

                # result = sg.popup_yes_no("现在开始压力测试吗？", title="确认")
                # if str(result).lower() == "yes":
                os.system("locust -f locust/hello_world.py")
        elif event in (None, 'Exit'):
            break
        print(str(values))
        
    window.close()
    print(f'You clicked {event}')

# 接口压测
class HelloWorld(SequentialTaskSet):
    label_sn = ""
    
    def on_start(self):
        print("on start")
        search_images()
        
    def on_stop(self):
        print("on stop")
    
    @task(1)
    def test_upload_before(self):
        image_path = get_random_image()
        
        url = "api/upload/before"
        header = {
            "mid": "MEDDY133310203062506021"
        }
        body = {
            "gender": 1,
            "filename": image_path
            # "filename": "Users/gaobo/Desktop/Hair/01/01_020.jpg"
        }
        
        response = self.client.post(url=url, data=json.dumps(body), headers=header)
        # print("upload/before->response: {}".format(response))
        
        if response.text is not None:
            result = json.loads(response.text)
            print("upload/before->result: {}".format(result))
            if "data" in result.keys() and "label_sn" in result["data"].keys():
                global label_sn
                label_sn = result["data"]["label_sn"]
                # print("->label_sn: {}".format(label_sn))
                
    @task(1)
    def test_upload_after(self):
        url = "api/upload/after"
        header = {
            "mid": "MEDDY133310203062506021"
        }
        body = {
            "label_sn": label_sn
        }
        
        response = self.client.post(url=url, data=json.dumps(body), headers=header)
        # print("upload/after->response: {}".format(response))
        
        if response.text is not None:
            result = json.loads(response.text)
            print("upload/after->result: {}".format(result))
            
    @task(1)
    def test_label_desc(self):
        global label_sn
        
        url = "api/label/desc"
        header = {
            "mid": "MEDDY133310203062506021"
        }
        body = {
            "sn": label_sn
        }
        
        response = self.client.post(url=url, data=json.dumps(body), headers=header)
        # print("label/desc->response: {}".format(response))
        
        if response.text is not None:
            result = json.loads(response.text)
            print("label/desc->result: {}".format(result))

# 压测配置
class WebsiteUser(HttpUser):
    tasks = [HelloWorld,]
    # host = "https://mcd.gululu.com/" # web entrance
    # host = "https://mcd-api.tst.gululu.com/" # api test
    host = "https://mcd-api.gululu.com/" # api release
    min_wait = 1000
    max_wait = 5000
    
# 入口
if __name__ == "__main__":
    # # 启动方式1
    # run_single_user(WebsiteUser)
    
    # # 启动方式2
    # import os
    # os.system("locust -f locust/hello_world.py")
    
    # 启动方式3
    start_work()
    
    
    
    
