import os
import json
import random
import PySimpleGUI as sg

from locust import HttpLocust, HttpUser, TaskSet, SequentialTaskSet, task, run_single_user

image_folder = "/Users/gaobo/Desktop/Hair/01"
# label_sn = ""
images = []

# 收集图片
def search_images():
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
        print("\033[1;34m ->image: {}\033[0m".format(image))
        return image
    else:
        return None

# 选择图片所在目录的界面
def start_work():
    version = 1.0
    sg.theme('Light Blue 2')
    
    layout = [[sg.Button('压力测试', key="OK"), 
               sg.Button('清理缓存', key="Clean"), 
               sg.Button('退出', key="Exit")],
              [sg.Text('选择目录', auto_size_text=True), sg.Input(size=(40, 1)), 
               sg.FolderBrowse(key='-Folder-', button_text = "浏览", initial_folder=os.path.dirname(__file__))],
              [sg.Text('功能说明：选择测试图片做在的目录，然后进行压力测试', text_color="blue")]
             ]

    window = sg.Window('前端接口压力测试({})'.format(version), layout, resizable=True)

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
                os.system("locust -f {}/api_test.py".format(os.path.dirname(__file__)))
        elif event == "Clean":
            clean_cache()
        elif event in (None, 'Exit'):
            clean_cache()
            break
        print(str(values))
        
    window.close()
    print(f'You clicked {event}')

# 清理缓存
def clean_cache():
    os.system("sh {}/bld_cleanup.sh".format(os.getcwd()))

# 接口压测
class StressTestingTask(SequentialTaskSet):
    label_sn = ""
    
    def on_start(self):
        print("on start")
        search_images()
        
    def on_stop(self):
        print("on stop")
    
    @task(1)
    def test_upload_before(self):
        image_path = get_random_image()
        
        url = "api/upload/before?mock_api=1"
        header = {
            "mid": "MEDDY133310203062506021"
        }
        body = {
            "gender": 1,
            "filename": image_path
            # "filename": "Users/gaobo/Desktop/Hair/01/01_020.jpg"
        }
        
        response = self.client.post(url=url, data=json.dumps(body), headers=header)
        try:
            if response.text is not None:
                result = json.loads(response.text)
                print("upload/before->result: {}".format(result))
                if "data" in result.keys() and "label_sn" in result["data"].keys():
                    global label_sn
                    label_sn = result["data"]["label_sn"]
                    # print("->label_sn: {}".format(label_sn))
        except:
            print("upload/before->response: {}".format(response))
                
    @task(1)
    def test_upload_after(self):
        url = "api/upload/after?mock_api=1"
        header = {
            "mid": "MEDDY133310203062506021"
        }
        body = {
            "label_sn": label_sn
        }
        
        response = self.client.post(url=url, data=json.dumps(body), headers=header)
        try:
            if response.text is not None:
                result = json.loads(response.text)
                print("upload/after->result: {}".format(result))
        except:
            print("upload/after->response: {}".format(response))
            
    @task(1)
    def test_label_desc(self):
        global label_sn
        
        url = "api/label/desc?mock_api=1"
        header = {
            "mid": "MEDDY133310203062506021"
        }
        body = {
            "sn": label_sn
        }
        
        response = self.client.post(url=url, data=json.dumps(body), headers=header)
        try:
            if response.text is not None:
                result = json.loads(response.text)
                print("label/desc->result: {}".format(result))
        except:
            print("label/desc->response: {}".format(response))

# 压测配置
class WebsiteUser(HttpUser):
    tasks = [StressTestingTask,]
    # host = "https://mcd-api.tst.gululu.com/" # test env
    host = "https://mcd-api.gululu.com/" # release env
    min_wait = 1000
    max_wait = 5000

# 入口
if __name__ == "__main__":
    # # 启动方式1
    # run_single_user(WebsiteUser)
    
    # # 启动方式2
    # os.system("locust -f {}/api_test.py".format(os.path.dirname(__file__)))
    
    # 启动方式3
    start_work()
    

    
    
    
    
