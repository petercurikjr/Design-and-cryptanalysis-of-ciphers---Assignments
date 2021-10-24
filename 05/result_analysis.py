import plotly.graph_objects as go

f = open('keytableoutput.txt')
data = []
bias = []
keys = []

idx = 0
for line in f:
    data.append(
        (hex(idx), float(line.strip('\n')))
    )
    idx += 1

data.sort(key=lambda y:y[1])

for i in range(len(data)):
    keys.append(data[i][0])
    bias.append(data[i][1])

fig = go.Figure()
fig.add_trace(go.Bar(x=keys, y=bias, marker_color='rgb(55, 83, 109)'))

fig.update_layout(
    title='Results of linear cryptanalysis on the SPN',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Bias',
        titlefont_size=16,
        tickfont_size=14,
    ),
    xaxis=dict(
        title='Keys'
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1
)
fig.show()

chosen_keys = keys[:3]
chosen_keys.append('0x81')
chosen_keys += keys[-3:]

chosen_biases = bias[:3]
chosen_biases.append(0.001953)
chosen_biases += bias[-3:]

fig2 = go.Figure()
fig2.add_trace(go.Bar(x = chosen_keys, y = chosen_biases, marker_color='rgb(55, 83, 109)'))
fig2.update_layout(
    title='Results of linear cryptanalysis on the SPN',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Bias',
        titlefont_size=16,
        tickfont_size=14,
    ),
    xaxis=dict(
        title='Keys'
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1
)
fig2.show()
