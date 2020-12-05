import plotly.graph_objects as go

custom_plot_template = dict(
    layout=go.Layout(font=dict(color='black'), legend=dict(bordercolor="Black",
                                                           borderwidth=1, traceorder="reversed"),
                     plot_bgcolor="white",
                     xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#e6e6e6', linecolor="black",
                                ),
                     yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#e6e6e6', linecolor="black",
                                ),
                     hovermode="closest"
                     )
)
