from road import RoadModel
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

def cell(agent):
    portrayal = {"Shape": "rect",
                 "Layer": 0,
                 "w": 1,
                 "h": 1,
                 "Filled": "true"}

    if agent.type == "road":
        portrayal["Color"] = "#1c1c1b"
    elif agent.type == "grass":
        portrayal["Color"] = "#81bd7b"
    elif agent.type == "water":
        portrayal["Color"] = "#5dc1e3"

    elif agent.type == "car":
        portrayal["Shape"] = "circle"
        portrayal["r"] = "0.8"
        portrayal["Layer"] = 1
        portrayal["Color"] = agent.color
        portrayal["text"] = agent.unique_id
        portrayal["text_color"] = "#ffffff"

    return portrayal


chart = ChartModule([{"Label": "AverageSpeed",
                      "Color": "#ff386a"}],
                    data_collector_name='datacollector')

if True:
    grid = CanvasGrid(cell, 50, 50, 800, 800)

    server = ModularServer(RoadModel, [grid, chart], "Road", {"N": 50, "width": 50,"height": 50})
    server.port = 9000

    server.launch()

else:
    params = {"width": 50, "height": 50, "N": range(10, 100, 10)}

    results = batch_run(
        RoadModel,
        parameters=params,
        iterations=10,
        max_steps=1000,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )

    results_df = pd.DataFrame(results)
    print(results_df.keys())

    pd.Index(['RunId', 'iteration', 'Step', 'width', 'height', 'N', 'AverageSpeed', 'AgentID',
              'Speed'],
             dtype='object')

    results_filtered = results_df[(results_df.AgentID == 0) & (results_df.Step == 500)]
    N_values = results_filtered.N.values
    if True:
        average_speed_values = results_filtered.AverageSpeed.values
        plt.plot(N_values, average_speed_values)
        plt.scatter(N_values, average_speed_values)
    else:
        N_values_unique = np.unique(np.array(N_values))
        average_speed_values = []
        for i,n in enumerate(N_values_unique):
            values = np.mean(results_filtered[(results_filtered.N == n)].AverageSpeed.values)
            average_speed_values = average_speed_values + values
        plt.plot(N_values_unique, average_speed_values)
        plt.scatter(N_values_unique, average_speed_values)

    plt.show()

    i = 0
