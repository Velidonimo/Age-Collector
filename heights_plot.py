from bokeh.plotting import figure, output_file, show
import pandas


def build_plot(df, height):
    output_file("templates/plot.html")

    height_plot = figure()

if __name__ == '__main__':
    df = pandas.read_csv("test_heights.csv")
    build_plot(df, 173)





