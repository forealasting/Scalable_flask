import requests
from concurrent.futures import ThreadPoolExecutor
import time
import docker
import os
import pymongo
import threading

# cloud mongodb
'''
client = pymongo.MongoClient("mongodb+srv://ncku_gwhsu:123@cluster0.wtz5pwg.mongodb.net/?retryWrites=true&w=majority")
db_cpu = client['state']['cpu_u1']
'''
r = 'tm1'
simulation_time = 300

# request setting
f = open('request/request5.txt')
request_num = []
request_n = simulation_time
for line in f:
    if len(request_num) < request_n:

        request_num.append(int(float(line)))

# print(len(request_num))
# print(request_num)

# request_num = [1, 5, 10, 15, 50, 50, 100, 100, 500, 500, 1000, 1000, 5000, 5000]
# request_num = request_num[:1800]
# request_num = [500]*8

# request_num = [r]*simulation_time

# request_num = request_num[:60]

# url settings
# url1 = "http://127.0.0.1:5000/ping"
url1 = "http://172.17.0.2:5000/ping"
# url2 = "http://127.0.0.1:5000/ping"
url2 = "http://172.17.0.3:5000/ping"
url3 = "http://172.17.0.4:5000/ping"
url4 = "http://172.17.0.5:5000/ping"

url_type = [url1, url2]

type = 1


def cal_cpu_percent(d):
    # cpu_count = len(d["cpu_stats"]["cpu_usage"]["percpu_usage"])
    # cpu_count fix
    cpu_count = 16
    cpu_percent = 0.0
    cpu_delta = float(d["cpu_stats"]["cpu_usage"]["total_usage"]) - \
                float(d["precpu_stats"]["cpu_usage"]["total_usage"])
    system_delta = float(d["cpu_stats"]["system_cpu_usage"]) - \
                   float(d["precpu_stats"]["system_cpu_usage"])
    if system_delta > 0.0:
        cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
    return cpu_percent


def get_url(url):
    myobj = {'num': 123}
    x = requests.post(url, data=myobj)

    # get_data = requests.get(url)
    final_time = time.time()
    alltime = final_time - start_time

    return x


def store_cpu(start_time, service):
    ## store_cpu
    for i in range(10000):
        # time.sleep(0.1) // moniter period

        client = docker.from_env()
        container = client.containers.get(service)
        d = container.stats(stream=False)
        state_u = cal_cpu_percent(d)
        # print(state_u)
        path = "output_cpu" + str(r) + ".txt"
        final_time = time.time()
        t = final_time - start_time
        f = open(path, 'a')
        data = str(t) + ' ' + str(state_u) + '\n'
        f.write(data)
        f.close()
        # mydict = {'cpu_u': state_u}
        # db_cpu.insert_one(mydict)


def con_send_request(url_type, type, start_time):

    for i in request_num:
        time.sleep(5)  # send requests every 1s
        if type == 2:
            list_of_urls = [url_type[0]] * int(i / 2) + [url_type[1]] * int(i / 2)
        else:
            list_of_urls = [url_type[0]] * i

        with ThreadPoolExecutor(max_workers=20) as pool:
            response_list = list(pool.map(get_url, list_of_urls))
            print(len(response_list))

        for response in response_list:
            # print(response)
            continue


def send_request(url_type, type, start_time):
    simulation_t = 1
    for i in request_num:
        # print(i)
        for j in range(i):

            get_url(url_type[0])
            time.sleep(1/i)  # send requests every 1s
        time.sleep(2)

    final_time = time.time()
    alltime = final_time - start_time
    print('time:: ', alltime)


start_time = time.time()
t1 = threading.Thread(target=send_request, args=(url_type, type, start_time, ))
t2 = threading.Thread(target=store_cpu, args=(start_time, 'service_1', ))

t1.start()
t2.start()
t1.join()
t2.join()




