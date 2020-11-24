from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.core.properties import Enum
import pandas


def rounding_heights(real_df):
    """Making a new DataFrame with heights rounded to 5"""
    real_df["Rounded_Height"] = real_df.Height // 5 * 5
    new_heights = list(range(real_df.Rounded_Height.min(), real_df.Rounded_Height.max() + 1, 5))
    new_heights_df = pandas.DataFrame(columns=("Height", "Population"))
    new_heights_df.Height = new_heights
    # summing population in each range
    new_heights_df.Population = [real_df.loc[real_df.Rounded_Height == height]["Population"].sum() for height in new_heights]
    return new_heights_df


def hover_tooltip(user_height, stat_height, number):
    """a func to fill the Hover column of Dataframe"""
    if stat_height == user_height:
        return f"Your number is between {number} people"
    else:
        return f"{number} people are this big"


def build_plot(stat_df, height):
    """Build a plot for given DataFrame and user_height"""
    # rounding heights
    height = height // 5 * 5
    stat_df = rounding_heights(stat_df)

    output_file("templates/plot.html")

    # adding a column shifted by 2.5 to show on plot
    stat_df["Shifted_height"] = stat_df.Height + 2.5
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

    stat_glyph = height_plot.vbar(x="Shifted_height", width=4.5, bottom=0,
                                  top="Population", color="darkorange", source=stat_cds)

    users_glyph = height_plot.vbar(x="Shifted_height", width=4.5, bottom=0,
                                   top="Population", color="darkgreen", source=users_cds)

    your_height_hover = HoverTool(tooltips="@Hover")
    height_plot.add_tools(your_height_hover)

    show(height_plot)


if __name__ == '__main__':
    df11 = pandas.read_csv("random_heights.csv")
    build_plot(df11, 189)





