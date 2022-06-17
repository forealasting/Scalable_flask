import plotly.express as px
import pandas as pd


# delay modify = average every x delay (x = 10, 50, 100)
# request rate r
r = 'tm1'
simulation_time = 300  # 300 s
if_store = 0

path = "output_cpu" + str(r) + ".txt"
f = open(path, "r")
cpu = []
time = []

for line in f:
    s = line.split(' ')
    if float(s[1]) > 5:
        time.append(float(s[0]))
        cpu.append(float(s[1]))

f.close()

# calculate  cpu (ms) ---------------

print(len(cpu))
avg = sum(cpu) / len(cpu)
max_d = max(cpu)
min_d = min(cpu)
print(avg, max_d, min_d)

# calculate  cpu (ms) ---------------

#
x = 10
cpu_m = []
time_m = []

for i, j in zip(time, cpu):

    if i <= 900:

        time_m.append(i)
        cpu_m.append(j)

print(len(cpu_m))
print(len(time_m))

# Plot --------------------------------------
x = time_m
y = cpu_m
d = {'timestamp(s)': x, 'Cpu utilization(%)': y}
df = pd.DataFrame(d)


fig = px.line(df, x='timestamp(s)', y='Cpu utilization(%)')

fig.update_layout(
    # title="Set request rate = " + str(r) + " requests/s",
    title="Set request rate = workload4 ",
    # legend_title="Legend Title",
    font=dict(
        # family="Courier New, monospace",
        size=18,
        # color="RebeccaPurple"
    )
)
fig.update_xaxes(range=[0, 300])
fig.update_yaxes(range=[0, 50])

fig.show()

# Plot --------------------------------------



# store if need
if if_store:

    path = 'output_cpu_u_m_' + str(r) + '.txt'
    f = open(path, 'a')
    for d in cpu_m:
        data = str(d) + '\n'
        f.write(data)
    f.close()


