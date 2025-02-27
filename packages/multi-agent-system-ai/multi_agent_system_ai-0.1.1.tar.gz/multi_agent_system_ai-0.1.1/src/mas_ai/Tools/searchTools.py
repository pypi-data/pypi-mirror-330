from langchain_community.document_loaders.web_base import WebBaseLoader
from typing import List, Optional, Literal,Dict,Any, Union
import os
import re, requests
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from datetime import datetime
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain.tools import tool
from pydantic import Field, BaseModel
from langchain_community.utilities.bing_search import BingSearchAPIWrapper
from langchain_google_community.search import GoogleSearchAPIWrapper
from langchain_google_community.search import GoogleSearchAPIWrapper
from ..Tools.utilities.platformData_utils.platformData_utils.youtube_api import YouTubeDataFetcher
from tavily import TavilyClient
from bs4 import BeautifulSoup
from langchain_core.documents import Document

"""Relies on 4 search engines to be set up in the .env file. Additionaly, YOUTUBE_DATA_API is required for youtube transcript scraping."""

ddg=DuckDuckGoSearchAPIWrapper()
tavily=TavilyClient(api_key=os.environ.get('TAVILY_API_KEY')) if os.getenv('TAVILY_API_KEY') else None
bing=BingSearchAPIWrapper(bing_subscription_key=os.environ.get('BING_API_KEY'),bing_search_url="https://api.bing.microsoft.com/v7.0/search") if os.getenv('BING_API_KEY') else None
google=GoogleSearchAPIWrapper(google_api_key=os.environ.get('GOOGLE_SERACH_API_KEY'), google_cse_id=os.environ.get('GOOGLE_CSE_ID')) if os.getenv('GOOGLE_SERACH_API_KEY') and os.getenv('GOOGLE_CSE_ID') else None
YOUTUBE = YouTubeDataFetcher(api_key=os.environ.get('YOUTUBE_DATA_API'))
#Models

class BingSchema(BaseModel):
    """schema For Bing Search"""
    snippet : str = Field(description='snippet of result')
    title : str= Field(description='title of result')
    link : str = Field(description='url of article')

def return_source_config() -> dict:
    """
    Detect query type using keyword matching and select appropriate sources.
    Returns a dictionary with the selected category as key and a list of sources as value.
    """
    source_config = {
        'academic': {
            'domains': [
                'harvard.edu',
                'mit.edu',
                'stanford.edu',
                'princeton.edu',
                'cam.ac.uk',
                'ox.ac.uk',
                'utoronto.ca',
                'berkeley.edu',
                'columbia.edu',
                'cornell.edu',
                'iitd.ac.in',
                'iitm.ac.in',
                'du.ac.in',
                'unimelb.edu.au',
                'ethz.ch',
                'nus.edu.sg',
                'ucl.ac.uk',
                'upenn.edu',
                'umich.edu',
                'csun.edu'
            ],
            'sources': [
                'Google Scholar',
                'PubMed',
                'JSTOR',
                'ResearchGate',
                'IEEE Xplore',
                'Scopus',
                'SpringerLink',
                'ScienceDirect',
                'Wiley Online Library',
                'SAGE Journals',
                'Taylor & Francis',
                'Elsevier',
                'Nature Publishing Group',
                'PLOS ONE',
                'ACM Digital Library',
                'Oxford Academic',
                'Cambridge Journals Online',
                'BioMed Central',
                'Emerald Insight',
                'ProQuest'
            ],
            'boosters': [
                'research',
                'study',
                'peer-reviewed',
                'journal'
            ]
        },
        'medical': {
            'domains': [
                'nih.gov',
                'who.int',
                'cdc.gov',
                'medlineplus.gov',
                'nejm.org',
                'lancet.com',
                'jamanetwork.com',
                'bmj.com',
                'clevelandclinic.org',
                'mayoclinic.org',
                'arizona.edu',
                'imperial.ac.uk',
                'manipal.edu',
                'aiims.edu',
                'sgul.ac.uk',
                'health.gov.au',
                'kaiserpermanente.org',
                'monash.edu',
                'charite.de',
                'mskcc.org'
            ],
            'sources': [
                'Cochrane Library',
                'Mayo Clinic',
                'WebMD',
                'Medscape',
                'Healthline',
                'Medical News Today',
                'BMJ',
                'JAMA',
                'NEJM',
                'The Lancet',
                'PubMed Health',
                'MedlinePlus',
                'MedPage Today',
                'India Medical Times',
                'Medical Express',
                'Science Daily (Health)',
                'Reuters Health',
                'Associated Press Health',
                'Nature Medicine',
                'PLOS Medicine'
            ],
            'boosters': [
                'clinical',
                'treatment',
                'diagnosis',
                'health'
            ]
        },
        'government': {
            'domains': [
                '.gov',
                'usa.gov',
                'india.gov.in',
                'gov.uk',
                'canada.ca',
                'gov.au',
                'europa.eu',
                'un.org',
                'worldbank.org',
                'imf.org',
                'who.int',
                'state.gov',
                'parliament.uk',
                'legislature.ca.gov',
                'ny.gov',
                'delhi.gov.in',
                'chicago.gov',
                'tokyo.metro.tokyo.lg.jp',
                'malaysia.gov.my',
                'gov.za'
            ],
            'sources': [
                'Census Bureau',
                'Government Publishing Office',
                'White House',
                'UK Parliament',
                'Press Information Bureau (India)',
                'Canada Statistics',
                'Australian Department of Finance',
                'European Commission',
                'United Nations',
                'World Bank',
                'IMF',
                'National Archives',
                'USA.gov',
                'GovTrack.us',
                'State Department',
                'Indian Ministry of Home Affairs',
                'Ministry of External Affairs (India)',
                'NYC.gov',
                'Gov.uk Press Office',
                'South African Government'
            ],
            'boosters': [
                'statistics',
                'policy',
                'legislation',
                'regulation'
            ]
        },
        'news': {
            'domains': [
                'reuters.com',
                'apnews.com',
                'bbc.com',
                'cnn.com',
                'theguardian.com',
                'aljazeera.com',
                'nytimes.com',
                'washingtonpost.com',
                'foxnews.com',
                'nbcnews.com',
                'abcnews.go.com',
                'usatoday.com',
                'latimes.com',
                'indianexpress.com',
                'timesofindia.indiatimes.com',
                'hindustantimes.com',
                'thehindu.com',
                'dw.com',
                'lemonde.fr',
                'rt.com'
            ],
            'sources': [
                'Reuters',
                'Associated Press',
                'BBC World Service',
                'CNN',
                'The Guardian',
                'Al Jazeera',
                'The New York Times',
                'The Washington Post',
                'Fox News',
                'NBC News',
                'ABC News',
                'USA Today',
                'Los Angeles Times',
                'Indian Express',
                'Times of India',
                'Hindustan Times',
                'The Hindu',
                'Deutsche Welle',
                'Le Monde',
                'RT'
            ],
            'boosters': [
                'report',
                'coverage',
                'analysis',
                'breaking'
            ]
        },
        'technology': {
            'domains': [
                'ieee.org',
                'techcrunch.com',
                'wired.com',
                'thenextweb.com',
                'engadget.com',
                'arstechnica.com',
                'venturebeat.com',
                'gadgetreview.com',
                'zdnet.com',
                'computing.co.uk',
                'digit.in',
                'ndtv.com/technology',
                'livemint.com/technology',
                'theverge.com',
                'mashable.com',
                'recode.net',
                'techradar.com',
                'pcmag.com',
                'slashdot.org',
                'infoworld.com'
            ],
            'sources': [
                'MIT Technology Review',
                'Ars Technica',
                'TechCrunch',
                'Wired',
                'The Next Web',
                'Engadget',
                'VentureBeat',
                'ZDNet',
                'CNET',
                'Digital Trends',
                'NDTV Gadgets (India)',
                'Livemint Tech (India)',
                'The Verge',
                'Mashable',
                'Recode',
                'TechRadar',
                'PCMag',
                'SlashGear',
                'InfoWorld',
                'Gizmodo'
            ],
            'boosters': [
                'innovation',
                'development',
                'emerging tech',
                'gadget'
            ]
        },
        'education': {
            'domains': [
                '.edu',
                'ed.gov',
                'khanacademy.org',
                'coursera.org',
                'edx.org',
                'udemy.com',
                'futurelearn.com',
                'open.edu',
                'mit.edu',
                'stanford.edu',
                'harvard.edu',
                'ox.ac.uk',
                'cam.ac.uk',
                'iitd.ac.in',
                'iitm.ac.in',
                'columbia.edu',
                'du.ac.in',
                'upgrad.com',
                'byjus.com',
                'unacademy.com'
            ],
            'sources': [
                'Coursera',
                'edX',
                'Khan Academy',
                'Udemy',
                'FutureLearn',
                'Open University',
                'MIT OpenCourseWare',
                'Stanford Online',
                'Harvard Online',
                'Oxford University Podcasts',
                'Cambridge University Press',
                'IIT Delhi Courses',
                'IIT Madras Courses',
                'Columbia Online',
                'Duke University Online',
                'UpGrad',
                'BYJU\'S',
                'Unacademy',
                'Swayam (India)',
                'NPTEL (India)'
            ],
            'boosters': [
                'courses',
                'tutorial',
                'lecture',
                'curriculum'
            ]
        },
        'finance': {
            'domains': [
                'finance.yahoo.com',
                'wsj.com',
                'bloomberg.com',
                'ft.com',
                'marketwatch.com',
                'investopedia.com',
                'cnbc.com',
                'reuters.com/finance',
                'forbes.com/finance',
                'moneycontrol.com',
                'economictimes.indiatimes.com',
                'livemint.com/market',
                'seekingalpha.com',
                'morningstar.com',
                'thestreet.com',
                'nerdwallet.com',
                'fortune.com',
                'nbcnews.com/finance',
                'business-standard.com',
                'indiainfoline.com'
            ],
            'sources': [
                'Bloomberg',
                'Reuters Business',
                'Financial Times',
                'Wall Street Journal',
                'CNBC',
                'Forbes',
                'MarketWatch',
                'Investopedia',
                'The Economic Times (India)',
                'Moneycontrol (India)',
                'Livemint',
                'Seeking Alpha',
                'Morningstar',
                'TheStreet',
                'NerdWallet',
                'Fortune',
                'Business Standard (India)',
                'India Infoline (India)',
                'Reuters Finance',
                'WSJ Pro'
            ],
            'boosters': [
                'stock',
                'market',
                'investment',
                'economy'
            ]
        },
        'sports': {
            'domains': [
                'espn.com',
                'bbc.com/sport',
                'sky.com/sport',
                'cbssports.com',
                'foxsports.com',
                'sports.yahoo.com',
                'cricbuzz.com',
                'espncricinfo.com',
                'nbcsports.com',
                'si.com',
                'bleacherreport.com',
                'goal.com',
                'skysports.com',
                'eurosport.com',
                'olympic.org',
                'officialnfl.com',
                'mlb.com',
                'nba.com',
                'nfl.com',
                'ncaa.com'
            ],
            'sources': [
                'ESPN',
                'BBC Sport',
                'Sky Sports',
                'CBS Sports',
                'Fox Sports',
                'Sports Illustrated',
                'Yahoo Sports',
                'Cricbuzz',
                'ESPN Cricinfo',
                'NBC Sports',
                'Bleacher Report',
                'Goal',
                'Sky Sports News',
                'Eurosport',
                'Olympic Channel',
                'NFL Network',
                'MLB Network',
                'NBA',
                'NCAA',
                'Sportskeeda (India)'
            ],
            'boosters': [
                'match',
                'tournament',
                'score',
                'league'
            ]
        },
        'entertainment': {
            'domains': [
                'imdb.com',
                'rottentomatoes.com',
                'variety.com',
                'hollywoodreporter.com',
                'tmz.com',
                'deadline.com',
                'ew.com',
                'billboard.com',
                'indiewire.com',
                'plex.tv',
                'metacritic.com',
                'screenrant.com',
                'ign.com',
                'spin.com',
                'rollingstone.com',
                'complex.com',
                'entertainmentweekly.com',
                'filmfare.com',
                'bollywoodhungama.com',
                'boxofficeindia.com'
            ],
            'sources': [
                'IMDb',
                'Rotten Tomatoes',
                'Variety',
                'The Hollywood Reporter',
                'TMZ',
                'Deadline',
                'Entertainment Weekly',
                'Billboard',
                'IndieWire',
                'Plex',
                'Metacritic',
                'Screen Rant',
                'IGN',
                'Spin',
                'Rolling Stone',
                'Complex',
                'Entertainment Weekly',
                'Filmfare',
                'Bollywood Hungama',
                'Box Office India'
            ],
            'boosters': [
                'movie',
                'show',
                'celebrity',
                'award'
            ]
        },
        'business': {
            'domains': [
                'forbes.com',
                'businessinsider.com',
                'wsj.com',
                'economist.com',
                'fortune.com',
                'bloomberg.com',
                'reuters.com/business',
                'marketwatch.com',
                'ft.com',
                'inc.com',
                'cbc.ca/business',
                'ndtv.com/business',
                'livemint.com/business',
                'moneycontrol.com',
                'indiainfoline.com',
                'seekingalpha.com',
                'thestreet.com',
                'zerohedge.com',
                'investors.com',
                'nasdaq.com'
            ],
            'sources': [
                'Forbes',
                'Business Insider',
                'Wall Street Journal',
                'The Economist',
                'Fortune',
                'Bloomberg',
                'Reuters Business',
                'MarketWatch',
                'Financial Times',
                'Inc.',
                'CBC Business',
                'NDTV Profit (India)',
                'Livemint',
                'Moneycontrol (India)',
                'India Infoline (India)',
                'Seeking Alpha',
                'TheStreet',
                'Zero Hedge',
                'Investors.com',
                'Nasdaq'
            ],
            'boosters': [
                'market',
                'strategy',
                'corporate',
                'finance'
            ]
        },
        'health': {
            'domains': [
                'healthline.com',
                'webmd.com',
                'mayoclinic.org',
                'medlineplus.gov',
                'clevelandclinic.org',
                'emedicine.medscape.com',
                'upmc.com/health',
                'johnshopkinssmedicine.org',
                'uchospitals.edu',
                'niddk.nih.gov',
                'diabetes.org',
                'heart.org',
                'arthritis.org',
                'cancer.gov',
                'precisionmedicine.nih.gov',
                'aiims.edu',
                'manipalhospitals.com',
                'apollohospitals.com',
                'fortishealthcare.com',
                'maxhealthcare.in'
            ],
            'sources': [
                'Healthline',
                'WebMD',
                'Mayo Clinic',
                'MedlinePlus',
                'Cleveland Clinic',
                'Medscape',
                'Johns Hopkins Medicine',
                'UPMC Health',
                'NIH',
                'American Diabetes Association',
                'American Heart Association',
                'Arthritis Foundation',
                'National Cancer Institute',
                'Precision Medicine Network',
                'AIIMS (India)',
                'Manipal Hospitals (India)',
                'Apollo Hospitals (India)',
                'Fortis Healthcare (India)',
                'Max Healthcare (India)',
                'MedPage Today'
            ],
            'boosters': [
                'wellness',
                'nutrition',
                'fitness',
                'lifestyle'
            ]
        },
        'science': {
            'domains': [
                'nature.com',
                'sciencemag.org',
                'phys.org',
                'plos.org',
                'sciencealert.net',
                'live-science.com',
                'sciencedaily.com',
                'researchgate.net',
                'sciam.com',
                'bbcearth.com',
                'nationalgeographic.com',
                'nytimes.com/section/science',
                'forbes.com/science',
                'technologyreview.com',
                'europa.eu',
                'un.org',
                'news.un.org',
                'astronomy.com',
                'icmje.org',
                'genengnews.com'
            ],
            'sources': [
                'Nature',
                'Science',
                'Scientific American',
                'PLOS ONE',
                'ScienceAlert',
                'Live Science',
                'ScienceDaily',
                'ResearchGate',
                'Smithsonian Magazine (Science)',
                'BBC Earth',
                'National Geographic',
                'New York Times Science',
                'Forbes Science',
                'MIT Technology Review',
                'European Commission – Science',
                'United Nations – Science',
                'UN News – Science',
                'Astronomy Magazine',
                'ICMJE',
                'GEN'
            ],
            'boosters': [
                'research',
                'discovery',
                'experiment',
                'study'
            ]
        },
        'travel': {
            'domains': [
                'tripadvisor.com',
                'lonelyplanet.com',
                'booking.com',
                'expedia.com',
                'agoda.com',
                'airbnb.com',
                'skyscanner.com',
                'travelocity.com',
                'orbitz.com',
                'makemytrip.com',
                'cleartrip.com',
                'yatra.com',
                'trip.com',
                'trivago.com',
                'travelandleisure.com',
                'cntraveler.com',
                'frommers.com',
                'fodors.com',
                'roughguides.com',
                'travelzoo.com'
            ],
            'sources': [
                'TripAdvisor',
                'Lonely Planet',
                'Booking.com',
                'Expedia',
                'Agoda',
                'Airbnb',
                'Skyscanner',
                'Travelocity',
                'Orbitz',
                'MakeMyTrip (India)',
                'Cleartrip (India)',
                'Yatra (India)',
                'Trip.com',
                'Trivago',
                'Travel + Leisure',
                'Condé Nast Traveler',
                'Frommer\'s',
                'Fodor\'s',
                'Rough Guides',
                'Travelzoo'
            ],
            'boosters': [
                'destination',
                'itinerary',
                'vacation',
                'tourism'
            ]
        }
    }
    return source_config




def arxiv(query: str)->str:
    "Only provides research papers based on query."
    arxiv_wrapper=ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=20000)
    arxiv=ArxivQueryRun(api_wrapper=arxiv_wrapper)
    return arxiv.run(query)

def wikipedia(query: str)->str:
    "A wrapper tool around Wikipedia."

    api_wrapper=WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=2000)
    wiki=WikipediaQueryRun(api_wrapper=api_wrapper)
    return wiki.run(query)


def credibility_filter(result: dict) -> bool:
    """
    Apply an enhanced CRAAP test (Currency, Relevance, Authority, Accuracy, Purpose)
    to a search result.
    
    The result is expected to be a dict containing:
      - 'year': publication year (int)
      - 'content': text content (str)
      - 'url': source URL (str)
      - 'tags': list of tags (list)
    """
    current_year = datetime.now().year
    year = result.get('year', current_year)
    content = result.get('content', '')
    url = result.get('url', '')
    tags = result.get('tags', [])

    criteria = {
        'currency': (current_year - year) <= 5,
        'relevance': len(content) > 500,  # Checks for content depth
        'authority': any(ext in url for ext in ['.gov', '.edu', 'jstor.org', 'who.int']),
        'accuracy': ('peer-reviewed' in tags or 'verified' in tags),
        'purpose': 'commercial' not in url.lower()
    }
    # Must pass at least 4 of the 5 criteria.
    return sum(criteria.values()) >= 4

def construct_query(query, category):
    # Retrieve the configuration for the given category;
    # if not found, default to 'academic'
    config = return_source_config().get(category.lower(), return_source_config()['academic'])
    
    # Join all the domains using OR
    domain_operators = ' OR '.join(config['domains'])
    # Join all the sources with quotes (in case they have spaces) using OR
    source_terms = ' OR '.join([source for source in config['sources']])
    # Join all booster keywords using a space
    boosters = ' '.join(config['boosters'])
    
    # Combine the individual parts into components:
    components = [
        f'({query})',
        f'({domain_operators})' if domain_operators else '',
        f'{source_terms}' if source_terms else '',
        boosters
    ]
    
    # Filter out any empty components and join them with spaces
    final_query = ' '.join([component for component in components if component])
    
    final_query = final_query
    return final_query

def current_datetime_location_weather(query: str = "What is the current time, location, and weather here?") -> dict:
    """
    Returns the current time, location, and optionally the weather for only current user.
    """
    # Step 1: Get Current Time
    now = datetime.now()
    current_time = now.strftime("%A, %B %d, %Y, %I:%M %p")

    # Step 2: Get Current Location
    try:
        # geolocator = Nominatim(user_agent="geoapiExercises")
        location_data = requests.get("https://ipinfo.io").json()
        location = {
            "city": location_data.get('city','unknown'),
            "state": location_data.get('region','unknown'),
            "country": location_data.get('country','unknown'),
            "latitude": location_data["loc"].split(",")[0],
            "longitude": location_data["loc"].split(",")[1],
        }
    except Exception as e:
        location = {"error": f"Could not fetch location: {str(e)}"}

    # Step 3: Get Current Weather (if requested)
    weather_data = {}
    try:
        api_key = os.environ.get('OPENWEATHER_API_KEY')  # Replace with your OpenWeatherMap API key
        lat, lon = location["latitude"], location["longitude"]
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(weather_url).json()
        weather_data = {
            "temperature": response["main"]["temp"],
            "description": response["weather"][0]["description"],
            "humidity": response["main"]["humidity"],
            "wind_speed": response["wind"]["speed"],
            "city": response.get("name", "Unknown"),
        }
    except Exception as e:
        weather_data = {"error": f"Could not fetch weather data: {str(e)}"}

    # Combine Results
    result = {
        "current_time": current_time,
        "location": location,
        "weather": weather_data,
    }

    return result


from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Optional, Union

@tool("Search Tool", return_direct=False)
def search_tool(
    query: Union[Optional[str], Optional[List[str]]],
    source_categories: Optional[List[str]] = None,
    Scrape: Optional[bool] = False,
    Weather: Optional[bool] = False
) -> Dict[str, Any]:
    """
    General Search Tool to search internet data across all categories providing search results.
    If results contain important links,you may scrape those url(s). Use your brain to make best use of this tool.
    How to search?

    - target keywords in first search
    - extract key links and sorces from that.
    - enhance search on them.
    - halt after gathering info.

    Parameters:
      - query: your query in str OR (if Scrape=True) a comma-separated list of URLs.
      - max_results: Maximum number of results to return per category.
      - source_categories: List of categories to search (e.g., ['academic', 'health', 'tech', 'news','shopping','food','education','finance','science','travel','government','youtube'(for video search)]).
      - Scrape: If True, `query` = list of URLs to scrape List[str].
      - Weather: If True, returns weather of user's current location only.
    """
    aggregated_results: Dict[str, Any] = {}

    if Scrape:
        return web_data_scraper(query=query)
    if Weather:
        return current_datetime_location_weather()

    if isinstance(query, list):
        query = ",".join(query)

    category_searchEngine_mapping = {
        "general": ["google"],
        "academic": ["google","arxiv", "wikipedia"],
        "medical": ["google", "duckduckgo", "wikipedia"],
        "government": ["google", "duckduckgo"],
        "news": ["google","tavily","duckduckgo"],
        "tech": ["google", "duckduckgo","tavily"],
        "education": ["google","arxiv", "wikipedia"],
        "finance": ["google", "duckduckgo"],
        "sports": ["google","bing", "duckduckgo"],
        "entertainment": ["google","bing", "duckduckgo"],
        "business": ["google", "duckduckgo", "tavily"],
        "health": ["google", "duckduckgo", "wikipedia"],
        "science": ["google","arxiv", "duckduckgo"],
        "travel": ["google", "duckduckgo", "tavily"],
        "youtube":["youtubeApi"],
        "amazon":["google","bing"],
        "food": ['google']
    }
    max_results=3

    if not source_categories:
        source_categories = ["academic", "general"]
    elif isinstance(source_categories, str):
        source_categories = [source_categories] if source_categories in category_searchEngine_mapping else ["academic", "tech"]
    elif isinstance(source_categories, list):
        if len(source_categories)>3:
            source_categories=source_categories[:2]
        source_categories = [cat for cat in source_categories if cat in category_searchEngine_mapping]
        if not source_categories:
            source_categories = ["news"]


    def fetch_results(category: str):
        """Helper function to search in a single category across multiple engines in parallel."""
        aggregated_results[category] = []
        tools_to_use = category_searchEngine_mapping.get(category.lower(), ["google"])
        constructed_query = query
        
        results = []
        with ThreadPoolExecutor() as executor:
            future_to_engine = {
                executor.submit(search_with_engine, tool, constructed_query, max_results, category): tool
                for tool in tools_to_use
            }

            for future in as_completed(future_to_engine):
                try:
                    results.extend(future.result())
                except Exception as e:
                    print(f"Error fetching results from {future_to_engine[future]}: {e}")
        
        aggregated_results[category] = results

    def search_with_engine(tool_name: str, constructed_query: str, max_results: int, category: str):
        """Runs a search using the given tool name and returns the results."""
        results = []
        if tool_name == "arxiv":
            results.append(arxiv(query))
        elif tool_name == "wikipedia":
            results.append(wikipedia(query))
        elif tool_name=="youtubeApi":
            results.append(get_video_details_from_query(query))
        elif tool_name == "bing":
            bing_results = bing.results(construct_query(constructed_query, category), num_results=max_results)
            for res in bing_results:
                try:
                    parsed_res = BingSchema.model_validate_json(str(res).replace("'", '"')).model_dump()
                    results.append(parsed_res)
                except Exception:
                    continue
        elif tool_name=="google":
            google_results = google.results(query=construct_query(constructed_query,category=category), num_results=max_results)

            results.extend(google_results)
        elif tool_name == "tavily":
            tavily_results = tavily.search(query=query, max_results=max_results, topic="news" if category == "news" else "general", include_images=False)
            if tavily_results:
                # results.extend([{"title": r["title"], "content": r["content"], "link": r["url"]} for r in tavily_results.get('results', [])])
                results.extend([{"title": r["title"], "content": r["content"]} for r in tavily_results.get('results', [])])
        elif tool_name == "duckduckgo":
            ddg_results = ddg._ddgs_news(query=query, max_results=max_results)
            results.extend([{"title": r["title"], "content": r["body"], "link": r["url"]} for r in ddg_results])
        
        return results

    # Execute all category searches in parallel
    with ThreadPoolExecutor() as executor:
        executor.map(fetch_results, source_categories)

    return aggregated_results




def web_data_scraper(
    query: Union[str, List[str]], 
    mode: str = 'default'
) -> List[str]:
    """General-purpose web scraper with Jina AI integration
    
    Args:
        query: URL string or list of URLs
        mode: 'normal' for WebBaseLoader, 'jina' for Jina Reader API
    
    Returns:
        List of cleaned text contents or error messages
    """
    
    def extract_urls(text: str) -> List[str]:
        """Robust URL validator"""
        url_pattern = r"(https?://(?:www\.)?[a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+(?:/\S*)?)"
        return list(set(re.findall(url_pattern, text)))

    def clean_content(html: str) -> str:
        """Universal HTML cleaner"""
        soup = BeautifulSoup(html, features="lxml")
        elements_to_remove = ['script', 'style', 'nav', 'footer', 'header',
                             'aside', 'noscript', 'meta', 'form', 'iframe', 'img']
        [element.decompose() for element in soup(elements_to_remove)]
        return re.sub(r'\n{3,}', '\n\n', soup.get_text(separator='\n', strip=True))

    # URL processing
    urls = query if isinstance(query, list) else extract_urls(query)
    if not urls:
        return ["No valid URLs found"]
    
    processed_content = []
    if len(urls)>5:
        urls=urls[:3]
    for url in urls:
        try:
            if mode.lower() == 'jina':
                # Jina API integration
                api_key = os.getenv("JINA_API_KEY")
                if not api_key:
                    raise ValueError("JINA_API_KEY environment variable required")
                
                response = requests.get(
                    f"https://r.jina.ai/{url}",
                    headers={"Authorization": f"Bearer {api_key}"}
                )
                response.raise_for_status()
                cleaned = response.text.strip()
                
            else:  # Default to WebBaseLoader
                docs = WebBaseLoader(url).load()
                cleaned = '\n\n'.join([clean_content(d.page_content) for d in docs])
                
            processed_content.append(cleaned)
            
        except Exception as e:
            processed_content.append(f"Error processing {url}: {str(e)}")
    
    return processed_content
    

@tool('Youtube_Transcript', return_direct=False)
def youtube_transcript(video_url:str, chunk_id = 1):
    """This tool Splits youtube transcript of a YouTube video into chunks if its length exceeds 2000 words. 
    Call this tool repeatedly to recieve all chunks (till full). 
    Summarize each chunk upon receiving it, retaining key information. 
    Refine and improve the overall summary as subsequent chunks are processed.
    You can retrieve specific chunk using chunk_id parameter.
    PARAMETERS:
    video_url: str = url of the video (https://...)
    chunk_id:int = chunk id of the above video.
    """
    
    if video_url=='None':
        return "You provided None as video_url or chunk_id.Please provide correct details."
    elif chunk_id==None:
        chunk_id=1
    elif isinstance(chunk_id,str):
        if any(word in chunk_id for word in ['none','null']):
            chunk_id=1
        else:
            chunk_id=int(chunk_id)
    
    for video in YOUTUBE.videos:
        print(video)
        print('------------------------------------------------\n')
        if video_url==video['video_url']:
            for transcript in video['transcripts']:
                if chunk_id==transcript['chunk_id']:
                    return {"transcript":transcript, "no_of_chunks":video['no_of_chunks']}
    return YOUTUBE.extract_transcript_with_details(video_url=video_url)


def get_video_details_from_query(query):
    video_details={}
    video_ids=YOUTUBE.get_video_id_from_query(query=query,max_results=5)
    for video_id in video_ids:
        video_details[video_id]=YOUTUBE.fetch_video_details(video_id=video_id)

    return video_details



