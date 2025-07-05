from dash import Dash, dcc, html, Input, Output, dash_table, callback
import dash_mantine_components as dmc
import plotly.express as px

data = px.data.stocks()

app = Dash(__name__,)

app.layout = dmc.Container(
    [
        dmc.Title(
            "Equity prices - Line chart and Table data", align="center"),
        dmc.Space(h=20),
        dmc.Button("Download Table Data", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
        dmc.Space(h=10),
        dmc.MultiSelect(
            label="Select stock you like!",
            placeholder="Select all stocks you like!",
            id="stock-dropdown",
            value=["GOOG", "AAPL"],
            data=[{"label": i, "value": i} for i in data.columns[1:]],
        ),
        dmc.Space(h=60),
        dmc.SimpleGrid(
            [
                dcc.Graph(id="line_chart"),
                dash_table.DataTable(
                    data.to_dict("records"),
                    [{"name": i, "id": i} for i in data.columns],
                    page_size=10,
                    style_table={"overflow-x": "auto"},
                ),
            ],
            cols=2,
            id="simple_grid_layout",
            breakpoints=[
                {"maxWidth": 1500, "cols": 2, "spacing": "md"},
                {
                    "maxWidth": 992,
                    "cols": 1,
                    "spacing": "sm",
                },  # common screen size for small laptops
                {
                    "maxWidth": 768,
                    "cols": 1,
                    "spacing": "sm",
                },  # common screen size for tablets
            ],
        ),
    ],
    fluid=True,
)


@callback(
    Output("line_chart", "figure"),
    Input("stock-dropdown", "value"),
)
def select_stocks(stocks):
    fig = px.line(data_frame=data, x="date", y=stocks, template="simple_white")
    fig.update_layout(
        margin=dict(t=50, l=25, r=25, b=25), yaxis_title="Price", xaxis_title="Date"
    )
    return fig


@callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(data.to_csv, "mydf.csv")


if __name__ == "__main__":
    app.run_server(port = 2408)