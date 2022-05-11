from locust import TaskSet, HttpUser, task, run_single_user


class BaiduTaskSet(TaskSet):
    """
    任务集
    """
    @task
    def search_by_key(self):
        self.client.get('/')

class BaiduUser(HttpUser):
    """
    - 会产生并发用户实例
    - 产生的用户实例会依据规则去执行任务集

    """
    # 定义的任务集
    tasks = [BaiduTaskSet,]
    host = 'http://www.baidu.com'


if __name__ == '__main__':
    # debug：调试任务是否可以跑通
    run_single_user(BaiduUser)
