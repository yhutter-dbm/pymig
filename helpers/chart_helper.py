import plotly.graph_objects as go
import plotly
class ChartHelper():

    @staticmethod
    def generate_bar_chart(x_data, y_data, title):
    	# See https://plotly.com/python/renderers/ for more information
    	fig = go.Figure(
        	data=[go.Bar(x = x_data, y = y_data)],
        	layout_title_text=title
        )
    	return plotly.offline.plot(fig, output_type="div")