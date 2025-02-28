import nbformat as nbf

all_scripts = dict() #nested dictionary; contains dates (key), points to 2nd dictionary (value) containing collection of scripts from that date

all_scripts['1/30/2025'] = {'nb': True,
                            'filename': 'advanced_data_visualization.ipynb',
                            1: [
        nbf.v4.new_code_cell("""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import uconndatascienceclub as ucdsc
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
"""),
        
        nbf.v4.new_code_cell("""
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.tan(x)
y4 = np.exp(-x)

plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1) 
plt.plot(x, y1, label='sin(x)')
plt.title('sin(x)')
plt.legend()

plt.subplot(2, 2, 2)  
plt.plot(x, y2, label='cos(x)', color='orange')
plt.title('cos(x)')
plt.legend()

plt.subplot(2, 2, 3) 
plt.plot(x, y3, label='tan(x)', color='orange')
plt.title('tan(x)')
plt.legend(['test'])

plt.subplot(2, 2, 4)  
plt.plot(x, y4, label='exp(-x)', color='red')
plt.title('exp(-x)')
plt.legend()

plt.tight_layout()
plt.show()
"""),
        
        nbf.v4.new_code_cell("""
fig, ax = plt.subplots(1, 1)
x = np.linspace(0, 10, 100)
line, = ax.plot(x, np.sin(x), color='blue')

ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)
ax.set_title("Animating a Sine Wave")
ax.set_xlabel("X")
ax.set_ylabel("Amplitude")

def update(frame):
    line.set_ydata(np.sin(x + frame * 0.1)) 
    return line,

ani = animation.FuncAnimation(fig, update, frames=100, interval=50, blit=True)
ani.save("sine_wave.gif", writer=animation.PillowWriter(fps=20))

plt.show()
"""),
        
        nbf.v4.new_code_cell("""
df = ucdsc.Data('fires').dataframe()
category_counts = df['day'].value_counts()

categories = category_counts.index.tolist()
final_heights = category_counts.values

fig, ax = plt.subplots(figsize=(8, 6))
x = np.arange(len(categories))  
current_heights = np.zeros(len(categories))  
growth_rates = final_heights / 50 
bars = ax.bar(x, current_heights, tick_label=categories, color="royalblue")

ax.set_ylim(0, max(final_heights) * 1.1)
ax.set_title("Wildfire Counts by Day of Week", fontsize=14)
ax.set_xlabel("DOW")
ax.set_ylabel("Count")

def update(frame):
    for i, bar in enumerate(bars):
        if current_heights[i] < final_heights[i]:  # Grow until target
            current_heights[i] += growth_rates[i]
            bar.set_height(current_heights[i])
    return bars

ani = animation.FuncAnimation(fig, update, frames=50, interval=50, blit=False)

ani.save("fire_growth.gif", writer=animation.PillowWriter(fps=20))

plt.show()
"""),
        
        nbf.v4.new_code_cell("""
df = ucdsc.Data('population').dataframe()

fig = px.scatter(df, x="Longitude", y="Latitude", size="Population", hover_name="City", text="City",
                 color="Population", 
                 title="Interactive Population Map of Major US Cities")

fig.update_traces(textposition="top center", marker=dict(opacity=0.8))
fig.show()
"""),
        
        nbf.v4.new_code_cell("""
df = ucdsc.Data('temperatures').dataframe()
df = df.sort_values("Year")

fig = go.Figure()

fig.add_trace(go.Scatter(x=df["Year"], y=df["Mean"], mode="lines",
                         name="Global Mean Temperature Anomaly"))

fig.update_layout(title="Global Monthly Mean Temperature Anomaly (1880-Present)",
                  xaxis_title="Year", yaxis_title="Temperature Anomaly (°C)",
                  )

fig.show()
""")
    ]}
all_scripts['2/27/2025'] = {'nb': True,
                            'filename': 'pca.ipynb',
                            1: [
    nbf.v4.new_code_cell("""
import uconndatascienceclub as ucdsc
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
"""),

    nbf.v4.new_code_cell("""
df = ucdsc.Data().generate(dim=20, size=200, mean=[0, 200], sd=[10, 100], distributions=['normal', 'exponential'])
df.head()
"""),

    nbf.v4.new_code_cell("""
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

pca = PCA(n_components=10) 
X_pca = pca.fit_transform(X_scaled)

explained_variance = pca.explained_variance_ratio_
X_pca.shape
"""),

    nbf.v4.new_code_cell("""
plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.5, c='blue', edgecolors='k')
plt.xlabel(f"PC1 ({explained_variance[0]*100:.2f}% Variance)")
plt.ylabel(f"PC2 ({explained_variance[1]*100:.2f}% Variance)")
plt.title("PCA Projection of Dataset (First 2 Components)")
plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
plt.axvline(0, color='gray', linestyle='--', alpha=0.5)
plt.show()
"""),

    nbf.v4.new_code_cell("""
X = ucdsc.Data('automobile').dataframe()
X.head()
"""),

    nbf.v4.new_code_cell("""
X.replace('?', np.nan, inplace=True)
X.dropna(inplace=True)

x = X[["highway-mpg", "engine-size", "horsepower", "curb-weight"]]
y = X['price']
x.shape
"""),

    nbf.v4.new_code_cell("""
scaler = StandardScaler()
X_scaled = scaler.fit_transform(x)

pca = PCA(n_components=3)  
X_pca = pca.fit_transform(X_scaled)

explained_variance = pca.explained_variance_ratio_
explained_variance
"""),

    nbf.v4.new_code_cell("""
plt.bar(x=['pca1', 'pca2', 'pca3'], height=explained_variance)
plt.show()
""")
]}
#start a new all_scripts[date] here

def write(date):
    '''Writes the scripts that were used in the given meeting date'''

    if date not in all_scripts.keys():
        raise ValueError(f'Date not found. Acceptable dates: {available_dates()}.')
    
    nb = all_scripts[date]['nb']

    if nb:
        for key in all_scripts[date].keys():
  
            if key == 'nb':
                continue

            notebook = nbf.v4.new_notebook()
            valid_cells = []
            for cell_content in all_scripts[date][key]:
                if isinstance(cell_content, str):
                    valid_cells.append(nbf.v4.new_code_cell(cell_content)) 
                else:
                    valid_cells.append(cell_content)  

            notebook.cells.extend(valid_cells)

            nbf.validate(notebook)  

            with open(all_scripts[date]['filename'], 'w') as f:
                nbf.write(notebook, f)

    else:
        pass

def available_dates():
    return [key for key in all_scripts.keys()]

write('2/27/2025')