from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Place:
    city: str
    country: str
    lat: float
    lon: float
    region: str  # continent or macro-region
    tidbits: List[str]  # lightweight facts to blend into personas
    cuisine: List[str]
    habits: List[str]

PLACES: List[Place] = [
    Place("Tokyo", "Japan", 35.6762, 139.6503, "Asia",
          ["high-speed trains", "neon-lit districts", "quiet shrines"],
          ["ramen", "sushi", "okonomiyaki"],
          ["bowing", "vending machine stops", "late-night convenience store runs"]),

    Place("Nairobi", "Kenya", -1.286389, 36.817223, "Africa",
          ["safari day trips", "bustling markets", "urban wildlife"],
          ["nyama choma", "ugali", "sukuma wiki"],
          ["early sunrises", "matatu rides", "football on weekends"]),

    Place("Reykjavík", "Iceland", 64.1466, -21.9426, "Europe",
          ["geothermal pools", "northern lights", "volcanic fields"],
          ["lamb stew", "skyr", "rye bread"],
          ["midnight sun walks", "wool sweaters", "soaking in hot springs"]),

    Place("Cairo", "Egypt", 30.0444, 31.2357, "Africa",
          ["desert winds", "Nile riverbanks", "ancient landmarks"],
          ["koshari", "falafel", "ful medames"],
          ["late dinners", "street tea", "bargaining at bazaars"]),

    Place("São Paulo", "Brazil", -23.5558, -46.6396, "South America",
          ["graffiti alleys", "sprawling skyline", "football culture"],
          ["feijoada", "pão de queijo", "coxinha"],
          ["late-night cafes", "subway commutes", "weekend churrasco"]),

    Place("Sydney", "Australia", -33.8688, 151.2093, "Oceania",
          ["harbour ferries", "beach mornings", "coastal walks"],
          ["flat white", "meat pies", "prawn barbie"],
          ["early swims", "sun protection rituals", "footy chats"]),

    Place("Mumbai", "India", 19.0760, 72.8777, "Asia",
          ["local trains", "monsoon bursts", "Bollywood billboards"],
          ["vada pav", "pani puri", "masala chai"],
          ["late work hours", "rickshaw rides", "festival fireworks"]),

    Place("Paris", "France", 48.8566, 2.3522, "Europe",
          ["Seine-side strolls", "iconic boulevards", "corner bakeries"],
          ["croissants", "baguette", "steak frites"],
          ["morning espresso", "late dinners", "gallery hopping"]),

    Place("New York", "USA", 40.7128, -74.0060, "North America",
          ["brownstone blocks", "subway screech", "skyline views"],
          ["slice pizza", "bagels", "halal carts"],
          ["fast walking", "tiny apartments", "late shows"]),

    Place("Vancouver", "Canada", 49.2827, -123.1207, "North America",
          ["mountain backdrops", "rainy days", "bike lanes"],
          ["sushi rolls", "poutine", "salmon"],
          ["weekend hikes", "umbrella stashes", "craft coffee"]),

    Place("Mexico City", "Mexico", 19.4326, -99.1332, "North America",
          ["lively plazas", "mariachi echoes", "mural-lined streets"],
          ["tacos al pastor", "tamales", "pozole"],
          ["late lunches", "metro rides", "street markets"]),

    Place("Istanbul", "Türkiye", 41.0082, 28.9784, "Europe/Asia",
          ["Bosporus ferries", "call to prayer", "historic bazaars"],
          ["simit", "kebap", "baklava"],
          ["tea breaks", "late breakfasts", "football derbies"]),

    Place("Cape Town", "South Africa", -33.9249, 18.4241, "Africa",
          ["Table Mountain views", "penguin beaches", "vineyard drives"],
          ["braai", "bobotie", "koeksisters"],
          ["windy afternoons", "trail runs", "wine weekends"]),

    Place("Buenos Aires", "Argentina", -34.6037, -58.3816, "South America",
          ["tango rhythms", "broad avenues", "bookstores"],
          ["asado", "empanadas", "dulce de leche"],
          ["late dinners", "mate sharing", "football chants"]),

    Place("Singapore", "Singapore", 1.3521, 103.8198, "Asia",
          ["hawker centres", "efficient MRT", "lush parks"],
          ["chicken rice", "laksa", "roti prata"],
          ["cleanliness", "night markets", "early commutes"]),

    Place("Rome", "Italy", 41.9028, 12.4964, "Europe",
          ["ancient ruins", "piazzas", "fountain corners"],
          ["carbonara", "gelato", "espresso"],
          ["evening passeggiata", "tiny cars", "cafe standing"]),

    Place("Bangkok", "Thailand", 13.7563, 100.5018, "Asia",
          ["canal boats", "night bazaars", "golden temples"],
          ["pad thai", "som tam", "mango sticky rice"],
          ["street food runs", "motorbike taxis", "late heat"]),

    Place("Honolulu", "USA (Hawaii)", 21.3099, -157.8581, "Oceania",
          ["trade winds", "beach sunsets", "ukulele tunes"],
          ["poke", "shave ice", "plate lunch"],
          ["slippahs", "aloha Fridays", "surf checks"]),

    Place("Anchorage", "USA (Alaska)", 61.2181, -149.9003, "North America",
          ["moose sightings", "long winter nights", "glacier views"],
          ["reindeer dogs", "salmon", "sourdough"],
          ["studded tires", "summer midnight light", "layered jackets"]),

    Place("London", "UK", 51.5072, -0.1276, "Europe",
          ["double-decker buses", "foggy mornings", "royal landmarks"],
          ["fish and chips", "full English breakfast", "tea"],
          ["queueing", "pub culture", "raincoats"]),

    Place("Berlin", "Germany", 52.5200, 13.4050, "Europe",
          ["graffiti walls", "techno clubs", "historic sites"],
          ["currywurst", "doner kebab", "pretzels"],
          ["late nights", "efficient trains", "biergartens"]),

    Place("Barcelona", "Spain", 41.3851, 2.1734, "Europe",
          ["Gaudí architecture", "beach promenades", "football chants"],
          ["paella", "tapas", "churros"],
          ["siestas", "late dinners", "festival parades"]),

    Place("Athens", "Greece", 37.9838, 23.7275, "Europe",
          ["ancient ruins", "sunlit hills", "olive groves"],
          ["souvlaki", "moussaka", "tzatziki"],
          ["coffee culture", "evening strolls", "island hopping"]),

    Place("Dubai", "UAE", 25.276987, 55.296249, "Asia",
          ["skyscrapers", "desert safaris", "luxury malls"],
          ["shawarma", "machboos", "luqaimat"],
          ["Friday brunches", "shopping festivals", "night drives"]),

    Place("Kuala Lumpur", "Malaysia", 3.1390, 101.6869, "Asia",
          ["Petronas Towers", "street food stalls", "rainforest edges"],
          ["nasi lemak", "roti canai", "satay"],
          ["night markets", "prayer calls", "rain showers"]),

    Place("Seoul", "South Korea", 37.5665, 126.9780, "Asia",
          ["K-pop billboards", "palace gates", "night shopping"],
          ["bibimbap", "kimchi", "bulgogi"],
          ["all-night cafes", "gaming culture", "subway rides"]),

    Place("Osaka", "Japan", 34.6937, 135.5023, "Asia",
          ["neon lights", "castle towers", "canal bridges"],
          ["takoyaki", "okonomiyaki", "kushikatsu"],
          ["fast talk", "friendly vibes", "night food runs"]),

    Place("Shanghai", "China", 31.2304, 121.4737, "Asia",
          ["skyline lights", "historic concessions", "bund walks"],
          ["xiaolongbao", "hotpot", "scallion pancakes"],
          ["early tai chi", "tea culture", "crowded subways"]),

    Place("Beijing", "China", 39.9042, 116.4074, "Asia",
          ["imperial palaces", "hutongs", "Great Wall trips"],
          ["Peking duck", "baozi", "zhajiangmian"],
          ["morning exercises", "long dinners", "tea houses"]),

    Place("Moscow", "Russia", 55.7558, 37.6173, "Europe/Asia",
          ["Red Square", "onion domes", "wide boulevards"],
          ["borscht", "pelmeni", "blini"],
          ["cold winters", "metro rides", "chess games"]),

    Place("Madrid", "Spain", 40.4168, -3.7038, "Europe",
          ["plazas", "royal palaces", "bustling tapas bars"],
          ["jamón ibérico", "tortilla española", "churros"],
          ["late-night strolls", "fiesta spirit", "football passion"]),

    Place("Lisbon", "Portugal", 38.7169, -9.1390, "Europe",
          ["tile walls", "tram rides", "hilltop views"],
          ["bacalhau", "pastéis de nata", "sardines"],
          ["fado music", "sunset miradouros", "slow lunches"]),

    Place("Amsterdam", "Netherlands", 52.3676, 4.9041, "Europe",
          ["canals", "bicycle lanes", "narrow houses"],
          ["stroopwafels", "herring", "pannenkoeken"],
          ["cycling commutes", "tulip season", "cafe terraces"]),

    Place("Brussels", "Belgium", 50.8503, 4.3517, "Europe",
          ["comic murals", "grand squares", "cobblestones"],
          ["waffles", "moules-frites", "chocolate"],
          ["beer culture", "multilingual chatter", "outdoor cafes"]),

    Place("Warsaw", "Poland", 52.2297, 21.0122, "Europe",
          ["rebuilt old town", "Soviet blocks", "cultural hubs"],
          ["pierogi", "bigos", "żurek"],
          ["winter coats", "tram rides", "Sunday strolls"]),

    Place("Prague", "Czech Republic", 50.0755, 14.4378, "Europe",
          ["castle hill", "cobblestone lanes", "Charles Bridge"],
          ["goulash", "svíčková", "pilsner"],
          ["beer halls", "music nights", "walking tours"]),

    Place("Vienna", "Austria", 48.2100, 16.3700, "Europe",
          ["opera houses", "imperial palaces", "coffee houses"],
          ["schnitzel", "apfelstrudel", "sacher torte"],
          ["classical concerts", "slow coffee", "museum afternoons"]),

    Place("Zurich", "Switzerland", 47.3769, 8.5417, "Europe",
          ["lakefront", "mountain views", "banking district"],
          ["fondue", "raclette", "chocolate"],
          ["train punctuality", "ski trips", "clean streets"]),

    Place("Stockholm", "Sweden", 59.3293, 18.0686, "Europe",
          ["island city", "design shops", "nordic light"],
          ["meatballs", "gravlax", "cinnamon buns"],
          ["fika breaks", "minimalist style", "sauna visits"]),

    Place("Helsinki", "Finland", 60.1699, 24.9384, "Europe",
          ["seaside saunas", "design blocks", "island ferries"],
          ["salmon soup", "rye bread", "karjalanpiirakka"],
          ["ice swimming", "quiet trams", "coffee rituals"]),

    Place("Oslo", "Norway", 59.9139, 10.7522, "Europe",
          ["fjord views", "wooden houses", "northern lights"],
          ["rakfisk", "brown cheese", "reindeer stew"],
          ["outdoor lifestyle", "ski weekends", "summer cabins"]),

    Place("Copenhagen", "Denmark", 55.6761, 12.5683, "Europe",
          ["harbour baths", "colorful houses", "bike culture"],
          ["smørrebrød", "frikadeller", "pastries"],
          ["cycling everywhere", "hygge evenings", "candlelight cafes"]),

    Place("Dublin", "Ireland", 53.3331, -6.2489, "Europe",
          ["pub songs", "Georgian doors", "river bridges"],
          ["Irish stew", "soda bread", "fish pie"],
          ["storytelling", "pub nights", "rainy days"]),

    Place("Edinburgh", "UK (Scotland)", 55.9533, -3.1883, "Europe",
          ["castle hill", "cobblestone alleys", "fringe festival"],
          ["haggis", "shortbread", "whisky"],
          ["ceilidh dancing", "pub storytelling", "rainy walks"]),

    Place("Glasgow", "UK (Scotland)", 55.8642, -4.2518, "Europe",
          ["Victorian architecture", "street art", "music venues"],
          ["deep-fried Mars bar", "scotch pie", "Irn-Bru"],
          ["football rivalries", "pub chatter", "late gigs"]),

    Place("Manchester", "UK", 53.4808, -2.2426, "Europe",
          ["red-brick mills", "football chants", "canal walks"],
          ["meat pie", "fish and chips", "black pudding"],
          ["pub nights", "rainy commutes", "football weekends"]),

    Place("Brisbane", "Australia", -27.4698, 153.0251, "Oceania",
          ["river walks", "botanic gardens", "sunny skies"],
          ["lamingtons", "Moreton Bay bugs", "steak sandwiches"],
          ["beach weekends", "barbecue evenings", "rugby chats"]),

    Place("Melbourne", "Australia", -37.8136, 144.9631, "Oceania",
          ["street art", "laneway cafes", "tram rides"],
          ["flat white", "meat pies", "parmas"],
          ["coffee culture", "AFL games", "gallery hopping"]),

    Place("Perth", "Australia", -31.9505, 115.8605, "Oceania",
          ["beach sunsets", "swan river", "vineyards"],
          ["rock lobster", "meat pie", "damper bread"],
          ["surf trips", "outdoor festivals", "beach runs"]),

    Place("Auckland", "New Zealand", -36.8509, 174.7645, "Oceania",
          ["volcanic hills", "harbour views", "island ferries"],
          ["hangi", "pavlova", "fish and chips"],
          ["rugby fandom", "weekend hikes", "island getaways"]),

    Place("Wellington", "New Zealand", -41.2865, 174.7762, "Oceania",
          ["windy streets", "film studios", "harbour walks"],
          ["flat whites", "fish and chips", "meat pies"],
          ["indie cinema", "craft beer", "art festivals"]),

    Place("Santiago", "Chile", -33.4489, -70.6693, "South America",
          ["Andes backdrop", "plazas", "vineyards"],
          ["empanadas", "pastel de choclo", "asado"],
          ["late dinners", "wine culture", "street protests"]),

    Place("Lima", "Peru", -12.0464, -77.0428, "South America",
          ["Pacific cliffs", "colonial plazas", "surf beaches"],
          ["ceviche", "lomo saltado", "anticuchos"],
          ["pisco nights", "festival parades", "coastal runs"]),

    Place("Bogotá", "Colombia", 4.7110, -74.0721, "South America",
          ["mountain backdrop", "colorful streets", "museums"],
          ["ajiaco", "arepas", "empanadas"],
          ["coffee culture", "late nights", "street dancing"]),

    Place("Medellín", "Colombia", 6.2442, -75.5812, "South America",
          ["cable cars", "flower festivals", "valley views"],
          ["bandeja paisa", "arepas", "empanadas"],
          ["friendly locals", "late nightlife", "soccer passion"]),

    Place("Quito", "Ecuador", -0.1807, -78.4678, "South America",
          ["volcano views", "historic churches", "plazas"],
          ["locro", "cuy", "empanadas"],
          ["market shopping", "evening strolls", "Andean music"]),

    Place("Caracas", "Venezuela", 10.4806, -66.9036, "South America",
          ["mountain backdrop", "plazas", "street markets"],
          ["arepas", "pabellón criollo", "hallaca"],
          ["family gatherings", "baseball fandom", "night music"]),

    Place("Havana", "Cuba", 23.1136, -82.3666, "North America",
          ["vintage cars", "colorful streets", "sea walls"],
          ["ropa vieja", "tostones", "mojitos"],
          ["salsa nights", "domino games", "street music"]),

    Place("San Juan", "Puerto Rico", 18.4655, -66.1057, "North America",
          ["fortresses", "cobblestone streets", "beachfront"],
          ["mofongo", "lechón", "pastelón"],
          ["music festivals", "late-night dancing", "baseball passion"]),

    Place("Kingston", "Jamaica", 18.0179, -76.8099, "North America",
          ["reggae beats", "blue mountains", "beaches"],
          ["jerk chicken", "ackee and saltfish", "patties"],
          ["dancehall nights", "island lingo", "street cricket"]),

    Place("Casablanca", "Morocco", 33.5731, -7.5898, "Africa",
          ["oceanfront mosque", "boulevards", "markets"],
          ["tagine", "couscous", "pastilla"],
          ["mint tea", "evening strolls", "souq shopping"]),

    Place("Marrakech", "Morocco", 31.6295, -7.9811, "Africa",
          ["red walls", "bustling souks", "desert edges"],
          ["tanjiya", "couscous", "chebakia"],
          ["market haggling", "tea rituals", "late evenings"]),

    Place("Lagos", "Nigeria", 6.5244, 3.3792, "Africa",
          ["traffic jams", "beach clubs", "skyline views"],
          ["jollof rice", "suya", "puff-puff"],
          ["afrobeats nights", "street parties", "football passion"]),

    Place("Abuja", "Nigeria", 9.0579, 7.4951, "Africa",
          ["modern skyline", "rock outcrops", "wide roads"],
          ["egusi soup", "akara", "jollof rice"],
          ["church gatherings", "community events", "nightlife"]),

    Place("Addis Ababa", "Ethiopia", 9.0192, 38.7525, "Africa",
          ["mountain backdrop", "coffee culture", "historic museums"],
          ["injera", "doro wat", "tibs"],
          ["coffee ceremonies", "Sunday markets", "orthodox chants"]),

    Place("Dakar", "Senegal", 14.7167, -17.4677, "Africa",
          ["ocean breezes", "colorful markets", "music festivals"],
          ["thieboudienne", "yassa", "mafé"],
          ["djembe drumming", "street football", "market haggling"]),

    Place("Accra", "Ghana", 5.5600, -0.2050, "Africa",
          ["beaches", "lively markets", "historic forts"],
          ["jollof rice", "kelewele", "banku"],
          ["afrobeats dancing", "friendly greetings", "colorful clothing"]),

    Place("Kigali", "Rwanda", -1.9441, 30.0619, "Africa",
          ["rolling hills", "clean streets", "memorial sites"],
          ["ugali", "isombe", "brochettes"],
          ["early mornings", "community work days", "coffee culture"]),

    Place("Dar es Salaam", "Tanzania", -6.7924, 39.2083, "Africa",
          ["Indian Ocean views", "markets", "beaches"],
          ["pilau", "ugali", "mishkaki"],
          ["evening strolls", "Swahili greetings", "music nights"]),

    Place("Johannesburg", "South Africa", -26.2041, 28.0473, "Africa",
          ["gold history", "street art", "urban parks"],
          ["bunny chow", "biltong", "boerewors"],
          ["braai weekends", "township tours", "street music"]),

    Place("Los Angeles", "USA", 34.0522, -118.2437, "North America",
          ["Hollywood signs", "beach drives", "freeways"],
          ["tacos", "avocado toast", "In-N-Out"],
          ["fitness culture", "film sets", "traffic life"]),

    Place("San Francisco", "USA", 37.7749, -122.4194, "North America",
          ["Golden Gate Bridge", "hilly streets", "tech hubs"],
          ["sourdough bread", "clam chowder", "mission burritos"],
          ["foggy mornings", "bike commutes", "startup hustle"]),

    Place("Chicago", "USA", 41.8781, -87.6298, "North America",
          ["skyscrapers", "lakefront", "windy weather"],
          ["deep-dish pizza", "Italian beef", "hot dogs"],
          ["sports loyalty", "blues music", "snowy winters"]),

    Place("Boston", "USA", 42.3601, -71.0589, "North America",
          ["historic streets", "harbour views", "universities"],
          ["clam chowder", "lobster rolls", "baked beans"],
          ["Red Sox pride", "ivy lectures", "fall foliage"]),

    Place("Washington, D.C.", "USA", 38.9072, -77.0369, "North America",
          ["monuments", "government buildings", "tree-lined avenues"],
          ["half-smokes", "crab cakes", "Ethiopian food"],
          ["political debates", "museum visits", "rush-hour traffic"]),

    Place("Miami", "USA", 25.7617, -80.1918, "North America",
          ["beaches", "art deco", "Cuban culture"],
          ["Cuban sandwich", "stone crab", "arepas"],
          ["nightclubs", "salsa dancing", "beach workouts"]),

    Place("Seattle", "USA", 47.6062, -122.3321, "North America",
          ["coffee shops", "rainy skyline", "mountain views"],
          ["salmon", "clam chowder", "coffee"],
          ["tech work", "hiking weekends", "indie music"]),

    Place("Toronto", "Canada", 43.6532, -79.3832, "North America",
          ["CN Tower", "diverse districts", "lakefront"],
          ["poutine", "peameal bacon", "butter tarts"],
          ["multicultural vibes", "cold winters", "hockey fandom"]),

    Place("Montreal", "Canada", 45.5017, -73.5673, "North America",
          ["cobblestone streets", "festivals", "french flair"],
          ["poutine", "bagels", "tourtière"],
          ["bilingual chatter", "winter carnivals", "café culture"]),

    Place("Calgary", "Canada", 51.0447, -114.0719, "North America",
          ["Rocky Mountain views", "oil towers", "Stampede fair"],
          ["beef steak", "ginger beef", "poutine"],
          ["cowboy hats", "winter sports", "hockey spirit"]),

    Place("Dubai", "UAE", 25.276987, 55.296249, "Asia",
          ["luxury malls", "desert safaris", "Burj Khalifa"],
          ["shawarma", "hummus", "machboos"],
          ["night shopping", "friday brunch", "desert drives"]),
]

DEFAULT_CENTER = (20.0, 0.0)  # world view
DEFAULT_ZOOM = 2
