
from drafter import *
from dataclasses import dataclass

from bakery import assert_equal

set_website_title("SkiScout")
set_site_information(
    author="Your Name",
    description="Compare Vermont ski resorts based on price, snow, weather, crowds, and distance.",
    sources="Thanks to the Drafter documentation.",planning=[],links=[])
hide_debug_information()
set_website_framed(False)

@dataclass
class State:
    resorts: list
    selected_resort: int
    sort_mode: str
    good_snow_only: bool

resorts = [{"id": 0, "name": "Killington Resort", "price": 99, "snowfall": 8, "snow_condition": "Excellent", "weather": "28 F, Sunny", "crowds": "Moderate", "distance": 85, "price_points": 9, "snow_points": 34, "weather_points": 18, "crowd_points": 13, "distance_points": 18},
    {"id": 1, "name": "Stowe Mountain Resort", "price": 95, "snowfall": 6, "snow_condition": "Very Good", "weather": "25 F, Partly Cloudy", "crowds": "Busy", "distance": 45, "price_points": 8, "snow_points": 32, "weather_points": 18, "crowd_points": 12, "distance_points": 18},
    {"id": 2, "name": "Sugarbush Resort", "price": 92, "snowfall": 5, "snow_condition": "Very Good", "weather": "27 F, Sunny", "crowds": "Moderate", "distance": 55, "price_points": 8, "snow_points": 30, "weather_points": 17, "crowd_points": 12, "distance_points": 17},
    {"id": 3, "name": "Jay Peak", "price": 89, "snowfall": 4, "snow_condition": "Good", "weather": "22 F, Cloudy", "crowds": "Low", "distance": 90, "price_points": 9, "snow_points": 28, "weather_points": 16, "crowd_points": 11, "distance_points": 14},
    {"id": 4, "name": "Mount Snow", "price": 85, "snowfall": 3, "snow_condition": "Good", "weather": "30 F, Sunny", "crowds": "Busy", "distance": 130, "price_points": 10, "snow_points": 25, "weather_points": 16, "crowd_points": 10, "distance_points": 11}]

def resort_score(resort):
    """calculates the total score for a resort"""
    score = (resort["price_points"]+ resort["snow_points"]+ resort["weather_points"]
             + resort["crowd_points"]+ resort["distance_points"])
    return score

def get_distance(resort):
    return resort["distance"]

def get_price(resort):
    return resort["price"]

def get_weather(resort):
    return resort["weather_points"]

def build_home_page(state):
    """creates the homepage with the resort rankings"""
    content = []
    content.append("SKISCOUT")
    content.append("Find the best mountain today!")
    content.append("Starting location: Burlington, Vermont")
    content.append("")
    content.append("Choose how to organize the resorts:")
    content.append(Button("Highest Score", "sort_by_score"))
    content.append(Button("Closest Resorts", "sort_by_distance"))
    content.append(Button("Lowest Ticket Price", "sort_by_price"))
    content.append(Button("Best Weather", "sort_by_weather"))
    content.append("")
    content.append(Button("Show Resorts With Good Snow", "filter_good_snow"))
    content.append(Button("Show All Resorts", "show_all_resorts"))
    content.append("")
    content.append("TOP 5 SKI RESORTS")
    content.append("")

    displayed_resorts = state.resorts.copy()

    if state.good_snow_only:
        displayed_resorts = [
            resort for resort in displayed_resorts
            if resort["snow_points"] >= 28]

    if state.sort_mode == "score":
        displayed_resorts = sorted(displayed_resorts, key=resort_score, reverse=True)

    if state.sort_mode == "distance":
        displayed_resorts = sorted(displayed_resorts, key=get_distance)

    if state.sort_mode == "price":
        displayed_resorts = sorted(displayed_resorts, key=get_price)

    if state.sort_mode == "weather":
        displayed_resorts = sorted(displayed_resorts, key=get_weather, reverse=True)

    for resort in displayed_resorts:
        content.append("-----------------------------")
        content.append(resort["name"])
        content.append("Score: " + str(resort_score(resort)) + "/100")
        content.append("Ticket Price: $" + str(resort["price"]))
        content.append("New Snow: " + str(resort["snowfall"]) + " inches")
        content.append("Distance: " + str(resort["distance"]) + " miles")
        content.append(Button("View Details", "resort_details", {"resort_id": resort["id"]}))

    content.append("")
    content.append("Scores are calculated using price, snow, weather, crowds, and distance.")
    content.append("The displayed resort information is sample data.")
    return Page(state, content)

@route
def index(state: State):
    """displays the homepage"""
    state.sort_mode = "score"
    state.good_snow_only = False
    return build_home_page(state)

@route
def resort_details(state: State, resort_id: int):
    """shows information about a selected resort"""
    state.selected_resort = resort_id
    resort = state.resorts[resort_id]
    content = []
    content.append("SKISCOUT")
    content.append("RESORT DETAILS")
    content.append("")
    content.append(resort["name"])
    content.append("Overall Score: " + str(resort_score(resort)) + "/100")
    content.append("")
    content.append("Ticket Price: $" + str(resort["price"]))
    content.append("New Snow: " + str(resort["snowfall"]) + " inches")
    content.append("Snow Conditions: " + resort["snow_condition"])
    content.append("Weather: " + resort["weather"])
    content.append("Crowds: " + resort["crowds"])
    content.append("Distance from Burlington: " + str(resort["distance"]) + " miles")
    content.append("")
    content.append("SCORE BREAKDOWN")
    content.append("Ticket Price: " + str(resort["price_points"]) + "/10")
    content.append("Snow Conditions: " + str(resort["snow_points"]) + "/35")
    content.append("Weather: " + str(resort["weather_points"]) + "/20")
    content.append("Crowds: " + str(resort["crowd_points"]) + "/15")
    content.append("Distance: " + str(resort["distance_points"]) + "/20")
    content.append("")
    content.append(Button("Back to Home", "index"))
    return Page(state, content)

@route
def sort_by_score(state: State):
    """sorts resorts by their total score"""
    state.sort_mode = "score"
    state.good_snow_only = False
    return build_home_page(state)

@route
def sort_by_distance(state: State):
    """sorts resorts by distance"""
    state.sort_mode = "distance"
    state.good_snow_only = False
    return build_home_page(state)

@route
def sort_by_price(state: State):
    """sorts resorts by ticket price"""
    state.sort_mode = "price"
    state.good_snow_only = False
    return build_home_page(state)

@route
def filter_good_snow(state: State):
    """shows resorts with good snow conditions"""
    state.good_snow_only = True
    return build_home_page(state)

@route
def show_all_resorts(state: State):
    """displays all five resorts"""
    state.good_snow_only = False
    return build_home_page(state)

@route
def sort_by_weather(state: State):
    """Sorts resorts by weather."""
    state.sort_mode = "weather"
    state.good_snow_only = False
    return build_home_page(state)

start_server(State(resorts=resorts,selected_resort=0,sort_mode="score",good_snow_only=False))


assert_equal(resort_score(resorts[0]), 92)
assert_equal(resort_score(resorts[1]), 88)
assert_equal(resort_score(resorts[2]), 84)
assert_equal(resort_score(resorts[3]), 78)
assert_equal(resort_score(resorts[4]), 72)

assert_equal(get_distance(resorts[0]), 85)
assert_equal(get_distance(resorts[1]), 45)

assert_equal(get_price(resorts[0]), 99)
assert_equal(get_price(resorts[4]), 85)

assert_equal(get_weather(resorts[0]), 18)
assert_equal(get_weather(resorts[4]), 16)

