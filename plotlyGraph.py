import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo



df = pd.read_csv('COMMON-PROCESSED.csv')


fig = go.Figure()

# Add traces
for source in df['Source'].unique():
    df_source = df[df['Source'] == source]
    fig.add_trace(go.Bar(
        x=df_source['Headline Sentiment'],
        y=df_source['Offense Rating'],
        name=source,
        visible=True
    ))

# Create dropdown
dropdown_options = []
for source in df['Source'].unique():
    dropdown_options.append({'label': source, 'value': source})

fig.update_layout(
    updatemenus=[dict(
        type="dropdown",
        direction="down",
        showactive=True,
        x=0.1,
        y=1.1,
        buttons=list([
            dict(
                args=[{"visible": [source == df['Source'].unique()[i] for i in range(len(df['Source'].unique()))]}],
                label=source,
                method="update"
            )
            for source in df['Source'].unique()
        ]),
    )],
)


pyo.plot(fig, filename='static\plotly\eachsource.html', auto_open=False)



# Group by source and calculate the mean offense rating
df_grouped = df.groupby('Source')['Offense Rating'].mean().reset_index()

# Create the bar chart using Plotly
fig = px.bar(df_grouped, x='Source', y='Offense Rating', title='Average Offense Rating by Source')

pyo.plot(fig, filename='static\plotly\\avg_off_bysrc.html', auto_open=False)



fig = px.bar(df, x='Source', y='Offense Rating', color='Headline Sentiment', title='Source vs Offense Rating')


pyo.plot(fig, filename='static\plotly\source.html', auto_open=False)


# group the data by author and calculate the mean offense rating
author_rating = df.groupby('Author')['Offense Rating'].mean()

# create the bar chart
fig = go.Figure(go.Bar(
    x=author_rating.index,
    y=author_rating.values,
    marker=dict(
        color=author_rating.values,
#         colorscale='viridis',
        colorscale='Redor',
        colorbar=dict(
            title='Offense Rating'
        )
    ),
    text=author_rating.values.round(2),
    textposition='auto',
))

# set the chart title and axis labels
fig.update_layout(
    title='Mean Offense Rating by Author',
    xaxis_title='Author',
    yaxis_title='Offense Rating',
)


pyo.plot(fig, filename='static\plotly\\author.html', auto_open=False)




# group the data by Headline sentiment and count the number of headlines in each category
sentiment_counts = df['Headline Sentiment'].value_counts()

# create the pie chart
fig = go.Figure(go.Pie(
    labels=sentiment_counts.index,
    values=sentiment_counts.values,
    pull=[0.05, 0.05, 0.05],  # pull the slices away from the center for emphasis
    hole=0.3,  # set the size of the center hole
    marker=dict(colors=['#00AF91', '#DA1212','#BFDB38','yellow', 'orange' ]),  # set the colors for each slice
))

# set the chart title
fig.update_layout(
    title='Headline Sentiment Pie Chart',
)


pyo.plot(fig, filename='static\plotly\pie.html', auto_open=False)

# convert the Published At column to datetime format and set it as the index
df['publishedAt'] = pd.to_datetime(df['publishedAt'])
df.set_index('publishedAt', inplace=True)

# group the data by date and calculate the mean Offense Rating for each date
daily_avg = df['Offense Rating'].resample('D').mean()

# create the line plot using Plotly
fig = go.Figure(go.Scatter(x=daily_avg.index, y=daily_avg.values, mode='lines'))

fig = go.Figure(go.Scatter(
    x=daily_avg.index,
    y=daily_avg.values,
    mode='lines+markers',
    hovertemplate='<b>Date: %{x}</b><br>Average Offense Rating: %{y:.2f}<br><a href="%{text}" target="_blank">Click for more info</a>',
    text=['http://example.com']*len(daily_avg.index) # set the target URLs for each point
))

# set the chart title and axis labels
fig.update_layout(
    title='Average Offense Rating by Date',
    xaxis_title='Date',
    yaxis_title='Offense Rating',
)


pyo.plot(fig, filename='static\plotly\\timeline.html', auto_open=False)

# # Create a range slider for offense rating
# offense_slider = {'type': 'range', 'min': df['Offense Rating'].min(), 'max': df['Offense Rating'].max(), 'step': 1, 'value': [df['Offense Rating'].min(), df['Offense Rating'].max()]}

# # Create the bar chart using Plotly Express
# fig = px.bar(df, x='Title', y='Offense Rating', range_y=[df['Offense Rating'].min(), df['Offense Rating'].max()], title='Title vs Offense Rating', 
#              labels={'Title': 'Title', 'Offense Rating': 'Offense Rating'},
#              hover_data=['Offense Rating'],
#              color='Offense Rating', color_continuous_scale='Reds',
#              category_orders={'Offense Rating': sorted(df['Offense Rating'].unique(), reverse=True)})

# # Update the layout to add the offense rating range slider
# fig.update_layout(
#     xaxis={'title': 'Title'},
#     yaxis={'title': 'Offense Rating'},
#     sliders=[{'visible': True, 'active': 0, 'steps': [{'label': str(i), 'method': 'update', 'args': [{'visible': [True if a <= df['Offense Rating'].between(b[0], b[1]).values[i] else False for i, a in enumerate(df['Offense Rating'])]}]}], 'currentvalue': {'visible': False}, 'transition': {'duration': 500}}
# ])




