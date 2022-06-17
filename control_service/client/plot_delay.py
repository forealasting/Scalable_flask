import plotly.express as px
import pandas as pd


# delay modify = average every x delay (x = 10, 50, 100)
# request rate r
r = 10
use_tm = 0
# data_name = '_tm1'
data_name = '10'
simulation_time = 300  # 300 s
path = "result1/result_cpu0.3/output" + str(data_name) + ".txt"

f = open(path, "r")
delay = []
for line in f:
    delay.append(float(line.rstrip('\n'))*1000)
f.close()


# calculate  delay (ms)
print(len(delay))
all_time = sum(delay)
avg = sum(delay) / len(delay)
max_d = max(delay)
min_d = min(delay)
print(all_time, avg, max_d, min_d)
# max_d = 80.82


request_num = []
request_n = simulation_time
if use_tm:
    f = open('request/request5.txt')

    for line in f:
        if len(request_num) < request_n:

            request_num.append(int(float(line)))
else:
    request_num = [r for i in range(simulation_time)]
print(request_num)
print(sum(request_num))
for r in request_num:
    r = int(r)
    r_ = int(r/1.3)
    delay_m = []
    count = 0
    for i in range(simulation_time):
        tmp = delay[count:count+r]
        tmp = sorted(tmp, reverse=True)

        avg = sum(tmp[:r_]) / r_
        # max_ = max(tmp)
        if len(tmp) != 0:
            if tmp[0] > max_d-20:
                if tmp[0] > 100:
                    delay_m.append(max_d)
                else:
                    delay_m.append(tmp[0])
            else:
                delay_m.append(avg)

        count += r

print(delay_m)
# print(len(delay_m))
'''
x = []
d = 1/r
count = 0
j = 300*r
for i in range(j):
    x.append(count)
    count += d
'''

x = [i for i in range(300)]
y = delay_m
print(len(x))
print(len(y))
d = {'timestamp(s)': x, 'Response time(ms)': y}
df = pd.DataFrame(d)


fig = px.line(df, x='timestamp(s)', y='Response time(ms)')

fig.update_layout(
    # title="Set request rate = " + str(r) + " requests/s",
    # title="Set request rate = workload4 ",
    # legend_title="Legend Title",
    font=dict(
        size=18,
        # color="RebeccaPurple"
    )
)

fig.update_xaxes(range=[0, 300])
fig.update_yaxes(range=[0, 100])
fig.show()

