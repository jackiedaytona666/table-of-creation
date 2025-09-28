
# 🚕 Edmonton Foot Traffic Scraper

**A web scraping system to help Edmonton cab drivers find high-demand locations and events, delivered via Ko-fi subscription.**

---

## � Project Overview

This project collects real-time and historical foot traffic data in Edmonton, focusing on events and locations where people are likely to need rides (concerts, sports, festivals, nightlife, etc.). The data is designed to help cab drivers optimize their routes and earnings, accessible through a Ko-fi subscription service.   

<!-- I do want to add in after this that we are going to be adding in to the best of our ability adults sporting leagues times like baseball and stuff is big for needing cabs things like piano, recitals and dance recitals concerts at schools where you know grandparents would be in attendance retirement home Pickleball leagues where they have to leave the retirement home perhaps you know maybe maybe they are Cabining so getting in contact with event coordinators for alternative outlet so this isn't your typical scrape. We're going to look deeper than most people have really ever thought to go as well. There's a lot of times where there's concerts and things that are happening at halls that you may not necessarily know about yeah so try and keep that in mind will add that in as well will try to utilize Claude for language analysis and stuff with Twitter API we could probably pay attention to Reddit as well and I have access to like an underground like electronic. I got a few different underground, electronic Facebook groups that I have access to like messages and stuff so yeah.. I just thought of this too. There's so much construction in Edmonton. It's disrupting a lot of bus traffic right now so maybe pay attention to that and then somehow we'll see if we can't get information on these areas. There was mentioned. I think GPT might've said something about there does exist a company who does have and gives out, but it's difficult to come by bone mapping data but they don't just give it away, but I'm cute-->

### 🎯 Key Features

- Scrapes event and venue data from public sources
- Identifies high-demand locations and times
- Stores and organizes data for easy access
- Designed for integration with a Ko-fi-based access system


---

## 🏗️ Project Structure

```
edmonton_foot_traffic_scraper/
  ├── scrapers/
  │   ├── events_scraper.py
  │   ├── venues_scraper.py
  │   └── utils.py
  ├── data/
  ├── docs/
  │   └── architecture.md
  ├── tests/
  │   └── test_scrapers.py
  ├── main.py
  ├── requirements.txt
  └── README.md
```

---

## 🚀 Getting Started

1. **Clone the repository**
2. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```
3. **Run the scraper:**
	```bash
	python main.py
	```

---

## 📝 Documentation

- All modules and functions are documented with docstrings.
- See `docs/architecture.md` for system design and data flow.
- Example usage and configuration are provided in the code comments.

---

## 🛡️ Error Handling & Logging

- Robust error handling for network and parsing issues
- Logging of key events and errors
- Graceful failure and retry logic

---

## 🤝 Contributing

1. Fork the repo and create a feature branch
2. Add your code with clear comments and docstrings
3. Add or update tests in `tests/`
4. Submit a pull request with a clear description

---

## 💡 Future Improvements

- Ko-fi integration for access control
- Web dashboard for data visualization
- Cloud data storage

---

*Built to help Edmonton cab drivers thrive!*
