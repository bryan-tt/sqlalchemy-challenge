# sqlalchemy-challenge
## Background
Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area.
## Part 1: Analyze and Explore the Climate Data
In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database.
### Topics covered:
- Use the SQLAlchemy `create_engine()` function to connect to your SQLite database.
- Use the SQLAlchemy `automap_base()` function to reflect your tables into classes
- Save references to the classes named station and measurement.
- Link Python to the database by creating a SQLAlchemy session.
- `Inspect` module to inspect table schema
- `engine.execute(sql_statement)`
- `datetime module as dt`
    - `dt.datetime.strptime`
    - `dt.timedelta`
- `plt.plot_date`
- `plt.xticks(range, steps=n)`
- `plt.hist(bins=n)`
- SQL subqueries
- SQL windows functions
## Part 2: Design Your Climate API
- Flask setup
- Flask routes
    - `@app.route`
    - `jsonify()`
- Dynamic endpoints