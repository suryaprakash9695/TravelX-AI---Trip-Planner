# TravelX-AI - Trip Planner

🌍 **TravelX AI – Smart Trip Planner with Advanced Features**

TravelX AI is an intelligent trip planning web application that helps users plan personalized travel itineraries using AI. It simplifies travel planning by providing destination suggestions, day-wise itineraries, budget estimates, and travel insights based on user preferences.

## 🚀 Features

### Core Features
- 🤖 **AI-powered trip planning** - Powered by Ollama (Phi3 model)
- 📍 **Destination-based itinerary generation** - Personalized day-by-day plans
- 🗓️ **Day-wise travel schedule** - Organized morning, afternoon, evening activities
- 🌐 **User-friendly and responsive UI** - Beautiful gradient design
- ⚡ **Fast and efficient recommendations** - Instant itinerary generation
- 🧠 **Smart logic for optimized travel plans** - Multiple travel styles

### NEW Enhanced Features ✨

#### 💰 Budget Planning
- **Budget Calculator** - Estimate trip costs based on:
  - Budget type (Budget-Friendly, Moderate, Luxury)
  - Number of travelers
  - Destination region
  - Trip duration
- **Detailed Breakdown** - Daily and total costs for:
  - Accommodation
  - Food & Dining
  - Transportation
  - Activities & Entertainment
  - Miscellaneous expenses
- **Flight Cost Estimates** - Regional flight pricing
- **Money-Saving Tips** - Personalized tips based on budget type

#### 📚 Trip History & Management
- **Save All Trips** - Automatic trip history storage
- **Trip Statistics** - Track:
  - Total trips planned
  - Total days traveled
  - Most visited destinations
  - Average trip ratings
- **Rate & Review** - Rate your trips and add notes
- **Search & Filter** - Find past trips easily

#### 📤 Export Options
- **JSON Export** - Machine-readable trip data
- **iCalendar (.ics)** - Import trips to your calendar app
- **Markdown Export** - Beautiful formatted trip documents
- **Shareable Links** - Share trips with friends

#### ❤️ Favorites System
- **Save Favorite Destinations** - Keep track of places you love
- **Add Personal Notes** - Remember why you loved each place
- **Quick Access** - Plan return trips faster

#### 🗺️ Enhanced Mapping
- **Interactive Route Maps** - Powered by OpenStreetMap & Leaflet
- **Distance & Duration** - Accurate travel time estimates
- **Geocoding** - Convert place names to coordinates
- **Route Visualization** - See your journey path

#### 🌤️ Weather Integration
- **5-Day Forecast** - Weather predictions for your trip
- **Temperature & Conditions** - Plan activities accordingly
- **Visual Weather Cards** - Easy-to-read weather display

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3 (Modern gradients, animations, glassmorphism)
- JavaScript (ES6+)
- Leaflet.js (Interactive maps)

### Backend
- Python 3.12+
- Flask (Web framework)
- SQLite (Database)
- Flask-Sitemapper (SEO)

### AI & APIs
- **Ollama** - Local AI model (Phi3)
- **Visual Crossing Weather API** - Weather data
- **OpenStreetMap Nominatim** - Geocoding
- **OSRM** - Route calculation

### New Modules
- `budget_calculator.py` - Budget estimation engine
- `database.py` - SQLite database management
- `export_utils.py` - Export functionality (JSON, iCal, Markdown)
- `route_map.py` - Mapping and routing
- `local_ai.py` - AI itinerary generation

## 📦 Installation

### Prerequisites
1. **Python 3.12+** installed
2. **Ollama** installed and running
   ```bash
   # Install Ollama from https://ollama.ai
   # Pull the Phi3 model
   ollama pull phi3
   ```

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/TravelX-AI---Trip-Planner.git
   cd TravelX-AI---Trip-Planner
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Edit `.env` file:
   ```env
   FLASK_SECRET_KEY=your-secret-key-here
   WEATHER_API_KEY=your-visual-crossing-api-key
   ```
   
   Get Weather API key from: https://www.visualcrossing.com/

5. **Initialize database**
   ```bash
   # Database is auto-initialized on first run
   python app.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the app**
   
   Open browser: http://127.0.0.1:5000

## 🎯 Usage Guide

### Planning a Trip
1. Navigate to the home page
2. Fill in the trip planning form:
   - Source city
   - Destination city
   - Start date
   - Return date
   - Budget type (Budget/Moderate/Luxury)
   - Number of travelers
3. Click "Generate AI Itinerary"
4. View your personalized itinerary with:
   - Day-by-day activities
   - Budget breakdown
   - Weather forecast
   - Route map

### Managing Trips
- **View History**: Click "History" to see all past trips
- **Export Trip**: Choose JSON, Calendar, or Markdown format
- **Rate Trip**: Add ratings and notes to your trips
- **Delete Trip**: Remove trips you no longer need

### Favorites
- **Add Favorite**: Save destinations you love
- **Add Notes**: Remember why you loved each place
- **Quick Planning**: Use favorites for future trips

## 📊 Database Schema

### Tables
- `trip_history` - Stores all planned trips
- `user_preferences` - User settings and preferences
- `favorite_destinations` - Saved favorite places

## 🎨 Design Features

- **Modern UI/UX** - Clean, intuitive interface
- **Gradient Theme** - Beautiful pink gradient design
- **Glassmorphism** - Modern frosted glass effects
- **Responsive Design** - Works on all devices
- **Smooth Animations** - Engaging user experience
- **Accessibility** - WCAG compliant

## 🔒 Security Features

- **Content Security Policy (CSP)** - XSS protection
- **Secure Sessions** - Flask session management
- **Input Validation** - Form data sanitization
- **SQL Injection Prevention** - Parameterized queries

## 🎯 Future Enhancements

- 🌎 Real-time flight booking integration
- 🏨 Hotel recommendations & booking
- 📱 Mobile app version (React Native)
- 💬 Chat-based AI assistant
- 🔐 User authentication & accounts
- 🌍 Multi-language support
- 📊 Advanced analytics dashboard
- 🤝 Collaborative trip planning
- 📸 Photo gallery integration
- 🎫 Activity booking integration

## 👨‍💻 Team & Contributors

- **Surya Prakash Singh** – Lead Developer
- **Ritesh Tiwari** – Contributor

## 📜 License

This project is developed for academic and learning purposes.
Free to use and modify for educational use.

## 🙏 Acknowledgments

- Ollama team for the amazing local AI platform
- OpenStreetMap contributors
- Visual Crossing for weather data
- Flask community

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Contact: [Your Email]
- Website: https://teamtechpro.netlify.app/

---

**Made with ❤️ by Team TechPro**
