import calliope
import pandas as pd
import plotly.express as px


def _load_electricity_df(model_path):
    """Load and return the hourly power flow dataframe and color map from a saved model."""
    model = calliope.read_netcdf(model_path)
    colors = model.inputs.color.to_series().to_dict()
    df = (
        (model.results.flow_out.fillna(0) - model.results.flow_in.fillna(0))
        .sel(carriers="power")
        .sum("nodes")
        .to_series()
        .where(lambda x: x != 0)
        .dropna()
        .to_frame("Dispatch (MWh)")
        .reset_index()
    )
    return df, colors


def _aggregate_df(df, freq, label):
    """Aggregate hourly df to a given pandas offset frequency (e.g. 'D', 'W', '4D')."""
    df = df.copy().set_index("timesteps")
    return (
        df.groupby([pd.Grouper(freq=freq), "techs"])["Dispatch (MWh)"]
        .sum()
        .reset_index()
        .rename(columns={"timesteps": label})
    )


def _build_dispatch_fig(df_agg, x_col, colors, xaxis_title):
    """Build a Plotly bar+line dispatch figure from an aggregated dataframe."""
    df_demand = df_agg[df_agg.techs == "demand_power"]
    df_other = df_agg[df_agg.techs != "demand_power"]

    fig = px.bar(
        df_other,
        x=x_col,
        y="Dispatch (MWh)",
        color="techs",
        color_discrete_map=colors,
        barmode="relative",
    )
    fig.add_scatter(
        x=df_demand[x_col],
        y=-1 * df_demand["Dispatch (MWh)"],
        mode="lines",
        line=dict(color="black", width=2),
        name="demand",
    )
    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title="Dispatch (MWh)",
        bargap=0.1,
    )
    return fig


def plot_dispatch(model_path, plot_export_path):
    """Hourly dispatch plot (original, one bar per hour)."""
    model = calliope.read_netcdf(model_path)
    colors = model.inputs.color.to_series().to_dict()

    df_electricity = (
        (model.results.flow_out.fillna(0) - model.results.flow_in.fillna(0))
        .sel(carriers="power")
        .sum("nodes")
        .to_series()
        .where(lambda x: x != 0)
        .dropna()
        .to_frame("Dispatch (MWh)")
        .reset_index()
    )
    df_electricity_demand = df_electricity[df_electricity.techs == "demand_power"]
    df_electricity_other = df_electricity[df_electricity.techs != "demand_power"]

    fig = px.bar(
        df_electricity_other,
        x="timesteps",
        y="Dispatch (MWh)",
        color="techs",
        color_discrete_map=colors,
    )
    fig.add_scatter(
        x=df_electricity_demand.timesteps,
        y=-1 * df_electricity_demand["Dispatch (MWh)"],
        marker_color="black",
        name="demand",
    )
    fig.show()
    fig.write_html(plot_export_path)


def plot_dispatch_daily(model_path, plot_export_path):
    """Daily dispatch plot (~365 bars). Good for spotting weekday/weekend patterns."""
    df, colors = _load_electricity_df(model_path)
    df_agg = _aggregate_df(df, "D", "day")
    fig = _build_dispatch_fig(df_agg, "day", colors, "Day")
    fig.show()
    fig.write_html(plot_export_path)


def plot_dispatch_4day(model_path, plot_export_path):
    """4-day aggregated dispatch plot (~91 bars). Good balance of detail and readability."""
    df, colors = _load_electricity_df(model_path)
    df_agg = _aggregate_df(df, "4D", "4-day period")
    fig = _build_dispatch_fig(df_agg, "4-day period", colors, "4-Day Period")
    fig.show()
    fig.write_html(plot_export_path)


def plot_dispatch_weekly(model_path, plot_export_path):
    """Weekly dispatch plot (~52 bars). Good for seasonal overview."""
    df, colors = _load_electricity_df(model_path)
    df_agg = _aggregate_df(df, "W", "week")
    fig = _build_dispatch_fig(df_agg, "week", colors, "Week")
    fig.show()
    fig.write_html(plot_export_path)


def plot_load_duration_curve(dataframe, plot_export_path, x_label='count', y_label='value'):

    df = dataframe
    column = df.columns[0]
    df = df.sort_values(by=column, ascending=False)
    df.index = [i for i in range(1, len(df.index) + 1)]

    fig = px.line(
        df,
    )
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
    )
    fig.show()
    fig.write_html(plot_export_path)
