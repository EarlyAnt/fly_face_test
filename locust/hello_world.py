from locust import HttpLocust, HttpUser, TaskSet, task, run_single_user
import json

from requests import Response

class HelloWorld(TaskSet):
    
    def on_start(self):
        print("on start")
        
    def on_stop(self):
        print("on stop")
    
    # @task(1)
    # def test_baidu(self):
    #     self.client.get("/")
    
    @task(1)
    def test_upload_photo(self):
        url = "api/upload/before"
        header = {
            "mid": "MEDDY133310203062506021"
        }
        body = {
            "gender": 1,
            "filename": "Users/gaobo/Desktop/Hair/01/01_020.jpg"
        }
        
        response = self.client.post(url=url, data=json.dumps(body), headers=header)
        print(response)
        
class WebsiteUser(HttpUser):
    tasks = [HelloWorld,]
    # host = "http://www.baidu.com"
    host = "https://mcd.gululu.com/" # web entrance
    host = "https://mcd-api.tst.gululu.com/" # api upload/before
    min_wait = 1000
    max_wait = 5000

if __name__ == "__main__":
    # # 启动方式1
    # run_single_user(WebsiteUser)
    
    # 启动方式2
    import os
    os.system("locust -f locust/hello_world.py")
    
    
    
    
