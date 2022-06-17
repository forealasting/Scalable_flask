import requests
from concurrent.futures import ThreadPoolExecutor
import time

f = open('request.txt')
request_num = []
request_n = 3600
for line in f:
    if len(request_num) < request_n:
        request_num.append(int(line))

# print(len(request_num))

# print(request_num)
request_num = [1000]*100
request_num = request_num[:100]
print(len(request_num))

req_inx = 0


def get_url(url):
    global req_inx
    # print(req_inx)
    myobj = {'num': '123'}

    x = requests.post(url, data=myobj)

    # get_data = requests.get(url)

    return x


url = "http://127.0.0.1:5000/ping"
start_time = time.time()
for i in request_num:
    # time.sleep(5)  # send requests every 1s
    list_of_urls = [url]*i

    with ThreadPoolExecutor(max_workers=20) as pool:
        response_list = list(pool.map(get_url, list_of_urls))

    for response in response_list:
        # print(response)
        continue
    req_inx += 1
    print(len(response_list))
final_time = time.time()
alltime = final_time - start_time
print('time:: ', alltime)
