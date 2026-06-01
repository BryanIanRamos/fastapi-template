# Caraga Tourist Data - Seeding Guide

## Overview

All hardcoded Caraga, PH tourist data is stored in **`CARAGA_SEED_DATA.py`** and ready to seed your database.

## Data Included

### 📍 15 Tourist Areas

- Cloud 9 Beach (Siargao)
- Sohoton Caves
- Dinagat Islands
- Magpupungko Rock Pool
- Butuan City Museum
- Camiguin Island
- Cantilan Beach
- Nonoc Island Marine Sanctuary
- Surigao City
- Entablado Falls
- Bucas Grande Island
- Tandag Beach
- Bislig Bay
- Agusan Marsh Wildlife Sanctuary
- Cortes Reef

### 🎯 50 Activities

- 3-4 activities per tourist area
- Includes difficulty levels, duration, and pricing
- Examples: Surfing, Hiking, Diving, Snorkeling, Swimming, Photography, etc.

### ⭐ 60 Reviews

- 4 reviews per tourist area
- Ratings: 3-5 stars
- Realistic reviewer names and comments
- Varied feedback (positive, neutral, mixed)

### 📊 45 Visit Records

- Visit timestamps for June 2026
- Multiple traffic sources: organic, social_media, ad, travel_blog, direct
- Mix of registered users and anonymous visitors

### 🤖 15 Vector Embeddings

- AI embeddings for each tourist area
- Format: pgvector-compatible string arrays
- Useful for semantic search and recommendations

---

## How to Use

### Option 1: Seed Everything at Once

```powershell
python seed.py --all
```

### Option 2: Seed Individual Tourist Tables

```powershell
# Seed only tourist areas
python seed.py --table tourist_areas

# Seed only activities
python seed.py --table activities

# Seed only reviews
python seed.py --table reviews

# Seed only visits
python seed.py --table visits

# Seed only vectors
python seed.py --table vectors
```

### Option 3: Clear and Reseed

```powershell
# Clear all tourist tables and reseed
python seed.py --reset
```

---

## File Structure

```
project-root/
├── CARAGA_SEED_DATA.py                           # ← All hardcoded data
│
├── app/db/seeders/
│   ├── tourist_area_seeder.py                    # Uses CARAGA_TOURIST_AREAS
│   ├── activity_seeder.py                        # Uses AREA_ACTIVITIES
│   ├── review_seeder.py                          # Uses TOURIST_REVIEWS
│   ├── visit_seeder.py                           # Uses TOURIST_VISITS
│   └── tourist_area_vector_seeder.py             # Uses TOURIST_AREA_VECTORS
```

---

## Data Structure Reference

### Tourist Area Example

```python
{
    "area_id": 1,
    "name": "Siargao Island - Cloud 9 Beach",
    "description": "World-famous surfing destination...",
    "location": "Siargao Island, Surigao del Norte",
    "region": "Caraga",
    "latitude": 9.1078,
    "longitude": 126.0065,
    "category": "Beach & Surfing"
}
```

### Activity Example

```python
{
    "activity_id": 1,
    "area_id": 1,
    "activity_name": "Surfing Lessons",
    "description": "Professional surfing lessons for beginners and advanced surfers",
    "difficulty_level": "Beginner to Advanced",
    "estimated_duration": "2 hours",
    "price_range": "$25-50"
}
```

### Review Example

```python
{
    "review_id": 1,
    "area_id": 1,
    "user_name": "John Smith",
    "rating": 5,
    "comment": "Amazing surfing spot! Best waves I've ever rode..."
}
```

### Visit Example

```python
{
    "visit_id": 1,
    "area_id": 1,
    "user_id": 1,
    "source": "organic",
    "visit_time": "2026-05-01 08:30:00+08"
}
```

### Vector Example

```python
{
    "vector_id": 1,
    "area_id": 1,
    "content": "Cloud 9 Beach Siargao surfing waves sand crystal clear water...",
    "embedding": "[0.12, 0.45, -0.23, 0.56, 0.34, -0.12, 0.78, 0.23, -0.45, 0.89]"
}
```

---

## Testing Models with Real Data

### Test Tourist Area Retrieval

```python
# Get all Caraga tourist areas
areas = session.query(TouristArea).filter_by(region="Caraga").all()
assert len(areas) == 15

# Get activities for an area
area = session.query(TouristArea).filter_by(area_id=1).first()
activities = area.activities
assert len(activities) == 4
```

### Test Reviews and Ratings

```python
# Get reviews for an area
reviews = session.query(TouristReview).filter_by(area_id=1).all()
assert len(reviews) == 4

# Calculate average rating
avg_rating = sum(r.rating for r in reviews) / len(reviews)
assert avg_rating >= 3.0 and avg_rating <= 5.0
```

### Test Visit Analytics

```python
# Get visit analytics
total_visits = session.query(TouristVisit).filter_by(area_id=1).count()
assert total_visits > 0

# Group by source
from sqlalchemy import func
visit_sources = session.query(
    TouristVisit.source,
    func.count(TouristVisit.visit_id)
).group_by(TouristVisit.source).all()
```

### Test Vector Embeddings

```python
# Get vector for semantic search
vector = session.query(TouristAreaVector).filter_by(area_id=1).first()
assert vector.embedding is not None
assert "beach" in vector.content.lower() or "surfing" in vector.content.lower()
```

---

## Quick Stats

| Table                | Count | Notes                       |
| -------------------- | ----- | --------------------------- |
| tourist_area         | 15    | All unique Caraga locations |
| area_activities      | 50    | 3-4 per area                |
| tourist_reviews      | 60    | 4 per area, ratings 3-5     |
| tourist_visits       | 45    | May 2026 timestamps         |
| tourist_area_vectors | 15    | One per area                |

---

## Notes for Development

1. **Timestamps**: All visit records use June 2026 dates for consistency
2. **Embeddings**: Vector embeddings are mock 10-dimensional arrays (use real embeddings in production)
3. **User IDs**: Some visits have `user_id=None` to simulate anonymous visitors
4. **Locations**: All locations use real Caraga, PH coordinates (latitude/longitude)
5. **Realistic Data**: Names, reviews, and details are realistic for testing UI/business logic

---

## Extending the Data

To add more Caraga attractions:

1. Open `CARAGA_SEED_DATA.py`
2. Add new entries to `CARAGA_TOURIST_AREAS`
3. Add related activities to `AREA_ACTIVITIES`
4. Add reviews to `TOURIST_REVIEWS`
5. Add visits to `TOURIST_VISITS`
6. Add embedding to `TOURIST_AREA_VECTORS`
7. Run `python seed.py --reset` to reseed

---

## Troubleshooting

### Import Error: "No module named 'CARAGA_SEED_DATA'"

Make sure `CARAGA_SEED_DATA.py` is in the project root directory, not in a subdirectory.

### Foreign Key Constraint Error

Ensure you seed tables in this order:

1. tourist_area
2. area_activities
3. tourist_reviews
4. tourist_visits
5. tourist_area_vectors

### Duplicate Key Error

Run `python seed.py --reset` to clear all tourist tables and reseed fresh.

---

## Files Modified

- ✅ `CARAGA_SEED_DATA.py` - Created with all hardcoded data
- ✅ `app/db/seeders/tourist_area_seeder.py` - Updated to use hardcoded data
- ✅ `app/db/seeders/activity_seeder.py` - Updated to use hardcoded data
- ✅ `app/db/seeders/review_seeder.py` - Updated to use hardcoded data
- ✅ `app/db/seeders/visit_seeder.py` - Updated to use hardcoded data
- ✅ `app/db/seeders/tourist_area_vector_seeder.py` - Updated to use hardcoded data

Now your database is ready with real Caraga tourist data! 🇵🇭✨
