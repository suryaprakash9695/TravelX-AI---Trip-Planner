"""
Budget calculator for TravelX AI
Estimates trip costs based on destination and preferences
"""

# Average daily costs by destination type (in USD)
DESTINATION_COSTS = {
    "budget": {
        "accommodation": 25,
        "food": 15,
        "transport": 10,
        "activities": 15,
        "misc": 10
    },
    "moderate": {
        "accommodation": 60,
        "food": 35,
        "transport": 20,
        "activities": 30,
        "misc": 20
    },
    "luxury": {
        "accommodation": 150,
        "food": 80,
        "transport": 50,
        "activities": 70,
        "misc": 50
    }
}

# Regional multipliers
REGIONAL_MULTIPLIERS = {
    "southeast_asia": 0.7,
    "south_asia": 0.6,
    "eastern_europe": 0.8,
    "western_europe": 1.3,
    "north_america": 1.2,
    "oceania": 1.4,
    "middle_east": 1.1,
    "africa": 0.75,
    "south_america": 0.8,
    "default": 1.0
}

def estimate_budget(days, budget_type="moderate", region="default", travelers=1):
    """
    Calculate estimated trip budget
    
    Args:
        days: Number of days
        budget_type: "budget", "moderate", or "luxury"
        region: Geographic region
        travelers: Number of travelers
    
    Returns:
        Dictionary with budget breakdown
    """
    if budget_type not in DESTINATION_COSTS:
        budget_type = "moderate"
    
    if region not in REGIONAL_MULTIPLIERS:
        region = "default"
    
    base_costs = DESTINATION_COSTS[budget_type]
    multiplier = REGIONAL_MULTIPLIERS[region]
    
    # Calculate daily costs
    daily_breakdown = {}
    daily_total = 0
    
    for category, cost in base_costs.items():
        adjusted_cost = cost * multiplier * travelers
        daily_breakdown[category] = round(adjusted_cost, 2)
        daily_total += adjusted_cost
    
    # Calculate trip totals
    trip_breakdown = {}
    for category, daily_cost in daily_breakdown.items():
        trip_breakdown[category] = round(daily_cost * days, 2)
    
    total_cost = round(daily_total * days, 2)
    
    # Add flight estimate (rough estimate)
    flight_estimate = estimate_flight_cost(region, travelers)
    
    return {
        "daily_breakdown": daily_breakdown,
        "daily_total": round(daily_total, 2),
        "trip_breakdown": trip_breakdown,
        "trip_total": total_cost,
        "flight_estimate": flight_estimate,
        "grand_total": round(total_cost + flight_estimate, 2),
        "budget_type": budget_type,
        "travelers": travelers,
        "days": days
    }

def estimate_flight_cost(region, travelers=1):
    """Estimate flight costs based on region"""
    base_flight_costs = {
        "southeast_asia": 600,
        "south_asia": 700,
        "eastern_europe": 400,
        "western_europe": 500,
        "north_america": 350,
        "oceania": 1200,
        "middle_east": 650,
        "africa": 800,
        "south_america": 700,
        "default": 500
    }
    
    base_cost = base_flight_costs.get(region, base_flight_costs["default"])
    return round(base_cost * travelers, 2)

def get_budget_tips(budget_type):
    """Get money-saving tips based on budget type"""
    tips = {
        "budget": [
            "Stay in hostels or budget hotels",
            "Use public transportation",
            "Eat at local restaurants and street food",
            "Book activities in advance for discounts",
            "Travel during off-peak season"
        ],
        "moderate": [
            "Mix hotels with Airbnb stays",
            "Use ride-sharing apps",
            "Try a mix of local and tourist restaurants",
            "Book popular attractions online",
            "Look for combo deals on activities"
        ],
        "luxury": [
            "Book boutique hotels or resorts",
            "Consider private transfers",
            "Dine at recommended restaurants",
            "Book exclusive experiences",
            "Hire local guides for personalized tours"
        ]
    }
    
    return tips.get(budget_type, tips["moderate"])

def compare_budgets(days, region="default", travelers=1):
    """Compare all budget types"""
    comparison = {}
    
    for budget_type in ["budget", "moderate", "luxury"]:
        comparison[budget_type] = estimate_budget(days, budget_type, region, travelers)
    
    return comparison
