import requests
from concurrent.futures import ThreadPoolExecutor
import time
import docker
import os
import threading
import pandas as pd


# delay modify = average every x delay (x = 10, 50, 100)
# request rate r
r = 1
use_tm = 1
T_max = 0.01  # 𝐓_𝒎𝒂𝒙  𝒗𝒊𝒐𝒍𝒂𝒕𝒊𝒐𝒏
cpus = 0.3  # initial cpus
simulation_time = 300  # 300 s
type = 1  # the nuber of containers
violation = []
request_num = []
request_n = simulation_time
change = 0
if use_tm:
    f = open('request/request5.txt')

    for line in f:
        if len(request_num) < request_n:

            request_num.append(int(float(line)))
else:
    request_num = [r for i in range(simulation_time)]
print('lennnnn:: ', len(request_num))


def update_type(type1, type_c):
    myquery = {'type': type1}
    newvalues = {"$set": {'type': type_c}}
    db_type.update_many(myquery, newvalues)


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

    if alltime > 300:
        print('time:: ', alltime)
        exit()
    return x

# store cpu utilization and cpus
def store_cpu(start_time):
    ## store_cpu
    global cpus
    for i in range(100000):
        time.sleep(0.1)
        client = docker.from_env()
        container1 = client.containers.get('service_1')
        d = container1.stats(stream=False)
        state_u = cal_cpu_percent(d)
        path = "output_cpu.txt"
        final_time = time.time()
        t = final_time - start_time
        f = open(path, 'a')
        data = str(t) + ' ' + str(state_u) + ' ' + str(cpus) + '\n'
        f.write(data)
        f.close()


def send_con_request(url_type, start_time):
    global type

    for i in request_num:
        time.sleep(5)  # send requests every 5s
        list_of_urls = [url_type[0]] * i
        if type == '1':
            list_of_urls = [url_type[0]] * i
        if type == '2':
            list_of_urls = [url_type[0]] * int(i / 2) + [url_type[1]] * int(i / 2)
        if type == '3':
            list_of_urls = [url_type[0]] * int(i / 3) + [url_type[1]] * int(i / 3) + [url_type[2]] * int(i / 3)
        if type == '4':
            list_of_urls = [url_type[0]] * int(i / 4) + [url_type[1]] * int(i / 4) + [url_type[2]] * int(i / 4) + [url_type[3]] * int(i / 4)

        with ThreadPoolExecutor(max_workers=20) as pool:
            response_list = list(pool.map(get_url, list_of_urls))
            print(len(response_list))

        for response in response_list:
            # print(response)
            continue


def send_request(url_type, request_num, start_time):
    global change


    for i in request_num:
        print(i)
        for j in range(i):

            get_url(url_type[0])
            time.sleep(1/i)  # send requests every 1s
        time.sleep(2)
        if change == 1:
            time.sleep(2)
            change = 0

    final_time = time.time()
    alltime = final_time - start_time
    print('time:: ', alltime)



def get_delay():
    global type

    path = path = 'output_1.txt'
    try:
        f = open(path, "r")
        delay = []
        for line in f:
            delay.append(float(line.rstrip('\n')))
        # f.close()
        print('delay :: ', max(delay))
        return max(delay)
    except:
        tmp_delay = 0
        print('cant open')
        return tmp_delay
    # print(delay[-1])

# add container
def take_action():
    global type

    for i in range(100000):
        if type == '1':
            if get_delay() > 0.025:
                cmd = "sudo docker run --rm --cpus 0.3  --cpuset-cpus 13 --name service_2 f2"
                os.system(cmd)
                time.sleep(1)
        if type == '2':
            if get_delay() > 0.025:
                cmd = "sudo docker run --rm --cpus 0.3  --cpuset-cpus 13 --name service_2 f2"
                os.system(cmd)
                time.sleep(1)
        if type == '3':
            if get_delay() > 0.025:
                cmd = "sudo docker run --rm --cpus 0.3  --cpuset-cpus 13 --name service_2 f2"
                os.system(cmd)
                time.sleep(1)


# add cpu resource
def take_action1():
    global cpus, T_max, type, change
    for i in range(100000):
        if type == 1:
            tmp_delay = get_delay()

            if tmp_delay > T_max:
                cpus += 0.1
                cpus = round(cpus, 1)
                print('cps ::: ', cpus)
                cmd = "sudo docker update --cpus " + str(cpus) + " service_1"
                os.system(cmd)
                change = 1
                print('change!!!!')
                time.sleep(5)

# sudo docker update --cpus 0.3 service_1
url1 = "http://172.17.0.2:5000/ping"
url2 = "http://172.17.0.3:5000/ping"
url3 = "http://172.17.0.4:5000/ping"
url4 = "http://172.17.0.5:5000/ping"

url_type = [url1, url2, url3, url4]
start_time = time.time()

t1 = threading.Thread(target=send_request, args=(url_type, request_num, start_time, ))
t2 = threading.Thread(target=store_cpu, args=(start_time, ))
t3 = threading.Thread(target=take_action1)
# t4 = threading.Thread(target=get_delay)
t1.start()
t2.start()
t3.start()
# t4.start()

t1.join()
t2.join()
t3.join()
# t4.join()


