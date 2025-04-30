class PlotGenerator:
    def __init__(self,  x_values, y_values, function_input):
       
        self.x_values = x_values
        self.y_values = y_values
        self.function_input = function_input

    def generate_plot(self, plot_widget):
        plot_widget.set_data(self.x_values, self.y_values, self.function_input)
