from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.core.properties import Enum
import pandas


def hover_tooltip(user_height, stat_height, number):
    """a func to fill the Hover column of Dataframe"""
    if stat_height == user_height:
        return f"Your number is between {number} people"
    else:
        return f"{number} people are this big"


def build_plot(stat_df, height):
    output_file("templates/plot.html")

    # adding a column for HoverTool
    stat_df["Hover"] = [hover_tooltip(height, st_ht, num) for st_ht, num in zip(stat_df.Height, stat_df.Population)]
    stat_cds = ColumnDataSource(stat_df)

    # DataFrame for the users glyph
    users_df = stat_df.loc[stat_df["Height"] == height]
    users_cds = ColumnDataSource(users_df)

    height_plot = figure(height=200, width=500, title="Height statistic",
                         x_axis_label="Height, cm", y_axis_label="Population",
                         tools="pan, wheel_zoom", active_scroll="wheel_zoom",
                         x_minor_ticks=2)

    stat_glyph = height_plot.vbar(x="Height", width=4, bottom=0,
                                  top="Population", color="darkorange", source=stat_cds)

    users_glyph = height_plot.vbar(x="Height", width=4, bottom=0,
                                   top="Population", color="darkgreen", source=users_cds)

    your_height_hover = HoverTool(tooltips="@Hover")
    height_plot.add_tools(your_height_hover)

    show(height_plot)

if __name__ == '__main__':
    df11 = pandas.read_csv("test_heights.csv")
    build_plot(df11, 180)





