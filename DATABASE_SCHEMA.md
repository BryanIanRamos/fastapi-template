# FastAPI Template - Complete Database Schema

## Table of Contents

1. [Users System](#users-system)
2. [Tourist Area System](#tourist-area-system)
3. [Relationship Diagram](#relationship-diagram)
4. [Key Constraints & Indexes](#key-constraints--indexes)

---

## Users System

### 1. `users` Table

**Purpose:** Core user accounts and authentication

| Column        | Type           | Constraints                   | Description                              |
| ------------- | -------------- | ----------------------------- | ---------------------------------------- |
| `user_id`     | UUID           | PRIMARY KEY, UNIQUE, NOT NULL | Auto-generated user identifier           |
| `username`    | VARCHAR(255)   | UNIQUE, INDEX, NOT NULL       | Login username                           |
| `email`       | VARCHAR(100)   | INDEX, NOT NULL, UNIQUE       | User email (UNIQUE via constraint)       |
| `password`    | VARCHAR        | NOT NULL                      | Hashed password (bcrypt)                 |
| `first_name`  | VARCHAR(255)   | NULLABLE                      | User first name                          |
| `last_name`   | VARCHAR(255)   | NULLABLE                      | User last name                           |
| `is_active`   | INTEGER        | DEFAULT: 1, NOT NULL          | Active status (1 = active, 0 = inactive) |
| `role`        | INTEGER        | NULLABLE                      | User role/permission level               |
| `verified_at` | TIMESTAMP (TZ) | NULLABLE                      | Email verification timestamp             |
| `created_at`  | TIMESTAMP (TZ) | DEFAULT: now(), NOT NULL      | Record creation time                     |
| `updated_at`  | TIMESTAMP (TZ) | DEFAULT: now(), NOT NULL      | Last update time                         |

**Relationships:**

- 1:1 with `profiles` (via `user_id`)
- 1:many with `tokens` (via `user_id`)
- 1:many with `sessions` (via `user_id`)
- 1:many with `tasks` (via `user_id`)

---

### 2. `profiles` Table

**Purpose:** Extended user profile information

| Column                | Type           | Constraints                                            | Description                       |
| --------------------- | -------------- | ------------------------------------------------------ | --------------------------------- |
| `profile_id`          | UUID           | PRIMARY KEY, NOT NULL                                  | Auto-generated profile identifier |
| `user_id`             | UUID           | FOREIGN KEY → `users.user_id`, UNIQUE, INDEX, NOT NULL | Link to user (1:1)                |
| `first_name`          | VARCHAR(100)   | NOT NULL                                               | Profile first name                |
| `last_name`           | VARCHAR(100)   | NOT NULL                                               | Profile last name                 |
| `phone_number`        | VARCHAR(20)    | NULLABLE                                               | Contact phone                     |
| `birthday`            | DATE           | NULLABLE                                               | User birth date                   |
| `gender`              | VARCHAR(20)    | NULLABLE                                               | Gender (M/F/Other)                |
| `profile_picture_url` | TEXT           | NULLABLE                                               | URL to profile image              |
| `created_at`          | TIMESTAMP (TZ) | DEFAULT: now(), NOT NULL                               | Record creation time              |
| `updated_at`          | TIMESTAMP (TZ) | DEFAULT: now(), NOT NULL                               | Last update time                  |

**Relationships:**

- 1:1 with `users` (backref: `profile`)

---

### 3. `tokens` Table

**Purpose:** JWT authentication tokens

| Column       | Type           | Constraints                                    | Description                     |
| ------------ | -------------- | ---------------------------------------------- | ------------------------------- |
| `token_id`   | UUID           | PRIMARY KEY, NOT NULL                          | Auto-generated token identifier |
| `user_id`    | UUID           | FOREIGN KEY → `users.user_id`, INDEX, NOT NULL | Link to user                    |
| `token`      | VARCHAR        | UNIQUE, INDEX, NOT NULL                        | JWT token string                |
| `expires_at` | TIMESTAMP (TZ) | NOT NULL                                       | Token expiration time           |
| `revoked`    | BOOLEAN        | DEFAULT: False, NOT NULL                       | Token revocation status         |
| `created_at` | TIMESTAMP (TZ) | DEFAULT: now(), NOT NULL                       | Record creation time            |

**Relationships:**

- Many:1 with `users` (backref: `tokens`)
- 1:many with `sessions` (via `token_id`)

---

### 4. `sessions` Table

**Purpose:** User device/login sessions

| Column        | Type           | Constraints                                      | Description                            |
| ------------- | -------------- | ------------------------------------------------ | -------------------------------------- |
| `session_id`  | UUID           | PRIMARY KEY, NOT NULL                            | Auto-generated session identifier      |
| `user_id`     | UUID           | FOREIGN KEY → `users.user_id`, INDEX, NOT NULL   | Link to user                           |
| `token_id`    | UUID           | FOREIGN KEY → `tokens.token_id`, INDEX, NOT NULL | Link to token                          |
| `device_name` | VARCHAR(255)   | NULLABLE                                         | Device name (e.g., "iPhone", "Chrome") |
| `user_agent`  | TEXT           | NULLABLE                                         | Browser/app user agent string          |
| `ip_address`  | VARCHAR(45)    | NULLABLE                                         | IPv4 or IPv6 address                   |
| `is_active`   | BOOLEAN        | DEFAULT: True, NOT NULL                          | Session active status                  |
| `last_active` | TIMESTAMP (TZ) | DEFAULT: now(), NOT NULL                         | Last activity time                     |
| `created_at`  | TIMESTAMP (TZ) | DEFAULT: now(), NOT NULL                         | Session creation time                  |

**Relationships:**

- Many:1 with `users` (backref: `sessions`)
- Many:1 with `tokens` (backref: `sessions`)

---

### 5. `tasks` Table

**Purpose:** User tasks/todo items (CRUD example)

| Column        | Type           | Constraints                             | Description                             |
| ------------- | -------------- | --------------------------------------- | --------------------------------------- |
| `id`          | INTEGER        | PRIMARY KEY, INDEX, NOT NULL            | Auto-increment task ID                  |
| `title`       | VARCHAR(255)   | NOT NULL                                | Task title                              |
| `description` | TEXT           | NULLABLE                                | Detailed description                    |
| `status`      | VARCHAR(50)    | DEFAULT: "pending", NOT NULL            | Status: pending, in_progress, completed |
| `user_id`     | UUID           | FOREIGN KEY → `users.user_id`, NOT NULL | Link to task owner                      |
| `created_at`  | TIMESTAMP (TZ) | DEFAULT: now(), NOT NULL                | Record creation time                    |
| `updated_at`  | TIMESTAMP (TZ) | DEFAULT: now(), NOT NULL                | Last update time                        |

**Relationships:**

- Many:1 with `users` (backref: `tasks`)

---

## Tourist Area System

### 6. `tourist_area` Table

**Purpose:** Tourist attraction locations and information

| Column        | Type           | Constraints                  | Description                                   |
| ------------- | -------------- | ---------------------------- | --------------------------------------------- |
| `area_id`     | INTEGER        | PRIMARY KEY, INDEX, NOT NULL | Auto-increment area ID                        |
| `name`        | TEXT           | NOT NULL                     | Area name (e.g., "Eiffel Tower")              |
| `description` | TEXT           | NULLABLE                     | Detailed area description                     |
| `location`    | TEXT           | NULLABLE                     | Address/street location                       |
| `region`      | TEXT           | NULLABLE                     | Region/state/province                         |
| `latitude`    | FLOAT          | NULLABLE                     | Geographic latitude coordinate                |
| `longitude`   | FLOAT          | NULLABLE                     | Geographic longitude coordinate               |
| `category`    | TEXT           | NULLABLE                     | Category (e.g., "Monument", "Park", "Museum") |
| `created_at`  | TIMESTAMP (TZ) | DEFAULT: now(), NOT NULL     | Record creation time                          |

**Relationships:**

- 1:many with `area_activities` (via `area_id`, CASCADE delete)
- 1:many with `tourist_area_vectors` (via `area_id`, CASCADE delete)
- 1:many with `tourist_reviews` (via `area_id`, CASCADE delete)
- 1:many with `tourist_visits` (via `area_id`, CASCADE delete)

---

### 7. `area_activities` Table

**Purpose:** Activities/things to do at each tourist area

| Column               | Type           | Constraints                                                           | Description                           |
| -------------------- | -------------- | --------------------------------------------------------------------- | ------------------------------------- |
| `activity_id`        | INTEGER        | PRIMARY KEY, INDEX, NOT NULL                                          | Auto-increment activity ID            |
| `area_id`            | INTEGER        | FOREIGN KEY → `tourist_area.area_id`, INDEX, NOT NULL, CASCADE DELETE | Link to area                          |
| `activity_name`      | TEXT           | NULLABLE                                                              | Activity name (e.g., "Guided Tour")   |
| `description`        | TEXT           | NULLABLE                                                              | Activity description                  |
| `difficulty_level`   | TEXT           | NULLABLE                                                              | Difficulty level (Easy, Medium, Hard) |
| `estimated_duration` | TEXT           | NULLABLE                                                              | Duration (e.g., "2 hours")            |
| `price_range`        | TEXT           | NULLABLE                                                              | Price info (e.g., "$20-50")           |
| `created_at`         | TIMESTAMP (TZ) | DEFAULT: now(), NOT NULL                                              | Record creation time                  |

**Relationships:**

- Many:1 with `tourist_area` (backref: `activities`)

---

### 8. `tourist_area_vectors` Table

**Purpose:** Vector embeddings for semantic/AI search

| Column       | Type           | Constraints                                                           | Description                                          |
| ------------ | -------------- | --------------------------------------------------------------------- | ---------------------------------------------------- |
| `vector_id`  | INTEGER        | PRIMARY KEY, INDEX, NOT NULL                                          | Auto-increment vector ID                             |
| `area_id`    | INTEGER        | FOREIGN KEY → `tourist_area.area_id`, INDEX, NOT NULL, CASCADE DELETE | Link to area                                         |
| `content`    | TEXT           | NULLABLE                                                              | Vector source content/text                           |
| `embedding`  | VARCHAR        | NULLABLE                                                              | Vector embedding (as string; use pgvector extension) |
| `created_at` | TIMESTAMP (TZ) | DEFAULT: now(), NOT NULL                                              | Record creation time                                 |

**Relationships:**

- Many:1 with `tourist_area` (backref: `vectors`)

---

### 9. `tourist_reviews` Table

**Purpose:** User reviews of tourist areas

| Column       | Type           | Constraints                                                           | Description              |
| ------------ | -------------- | --------------------------------------------------------------------- | ------------------------ |
| `review_id`  | INTEGER        | PRIMARY KEY, INDEX, NOT NULL                                          | Auto-increment review ID |
| `area_id`    | INTEGER        | FOREIGN KEY → `tourist_area.area_id`, INDEX, NOT NULL, CASCADE DELETE | Link to area             |
| `user_name`  | TEXT           | NULLABLE                                                              | Reviewer name            |
| `rating`     | INTEGER        | NOT NULL, CHECK: 1-5                                                  | Star rating (1-5)        |
| `comment`    | TEXT           | NULLABLE                                                              | Review text/comment      |
| `created_at` | TIMESTAMP (TZ) | DEFAULT: now(), NOT NULL                                              | Review creation time     |

**Relationships:**

- Many:1 with `tourist_area` (backref: `reviews`)

**Constraints:**

- `ck_rating_range`: `rating >= 1 AND rating <= 5`

---

### 10. `tourist_visits` Table

**Purpose:** Visit tracking/analytics for tourist areas

| Column       | Type           | Constraints                                                           | Description                                      |
| ------------ | -------------- | --------------------------------------------------------------------- | ------------------------------------------------ |
| `visit_id`   | INTEGER        | PRIMARY KEY, INDEX, NOT NULL                                          | Auto-increment visit ID                          |
| `area_id`    | INTEGER        | FOREIGN KEY → `tourist_area.area_id`, INDEX, NOT NULL, CASCADE DELETE | Link to area                                     |
| `user_id`    | INTEGER        | NULLABLE                                                              | Visitor ID (external user, not FK)               |
| `source`     | VARCHAR        | NULLABLE                                                              | Traffic source (e.g., "organic", "ad", "direct") |
| `visit_time` | TIMESTAMP (TZ) | DEFAULT: now(), NOT NULL                                              | Visit timestamp                                  |

**Relationships:**

- Many:1 with `tourist_area` (backref: `visits`)

---

## Relationship Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER SYSTEM DOMAIN                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  users (PK: user_id - UUID)                                │
│    ├─ 1:1 ──→ profiles (FK: user_id)                       │
│    ├─ 1:∞ ──→ tokens (FK: user_id)                         │
│    │           └─ ∞:1 ──→ sessions (FK: token_id)          │
│    ├─ 1:∞ ──→ sessions (FK: user_id)                       │
│    └─ 1:∞ ──→ tasks (FK: user_id)                          │
│                                                              │
│  tokens (PK: token_id - UUID, FK: user_id)                 │
│    └─ 1:∞ ──→ sessions (FK: token_id)                      │
│                                                              │
│  sessions (PK: session_id - UUID)                          │
│    ├─ FK: user_id → users                                  │
│    └─ FK: token_id → tokens                                │
│                                                              │
│  profiles (PK: profile_id - UUID, FK: user_id - UNIQUE)   │
│                                                              │
│  tasks (PK: id - INTEGER, FK: user_id)                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              TOURIST AREA SYSTEM DOMAIN                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  tourist_area (PK: area_id - INTEGER)                      │
│    ├─ 1:∞ ──→ area_activities (FK: area_id) [CASCADE]      │
│    ├─ 1:∞ ──→ tourist_area_vectors (FK: area_id) [CASCADE] │
│    ├─ 1:∞ ──→ tourist_reviews (FK: area_id) [CASCADE]      │
│    └─ 1:∞ ──→ tourist_visits (FK: area_id) [CASCADE]       │
│                                                              │
│  area_activities (PK: activity_id - INTEGER)              │
│    └─ FK: area_id → tourist_area                           │
│                                                              │
│  tourist_area_vectors (PK: vector_id - INTEGER)           │
│    └─ FK: area_id → tourist_area                           │
│                                                              │
│  tourist_reviews (PK: review_id - INTEGER)                │
│    └─ FK: area_id → tourist_area                           │
│                                                              │
│  tourist_visits (PK: visit_id - INTEGER)                  │
│    └─ FK: area_id → tourist_area                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Constraints & Indexes

### Unique Constraints

- `users.username` - UNIQUE
- `users.email` - UNIQUE
- `tokens.token` - UNIQUE
- `profiles.user_id` - UNIQUE (1:1 relationship)

### Foreign Key Constraints

- **CASCADE DELETE**: All tourist area child tables delete when parent area is deleted
  - `area_activities.area_id`
  - `tourist_area_vectors.area_id`
  - `tourist_reviews.area_id`
  - `tourist_visits.area_id`

### Check Constraints

- `tourist_reviews.rating` - Must be between 1 and 5

### Indexes

- All PRIMARY KEY columns (auto-indexed)
- `users.username`, `users.email`
- `tokens.token`, `tokens.user_id`
- `sessions.user_id`, `sessions.token_id`
- `tasks.user_id`
- All foreign key columns for faster joins

### Default Values

- `users.is_active` = 1
- `users.created_at` = CURRENT_TIMESTAMP
- `users.updated_at` = CURRENT_TIMESTAMP
- `tokens.revoked` = False
- `tasks.status` = "pending"
- `sessions.is_active` = True
- All `created_at` fields = CURRENT_TIMESTAMP
- All `updated_at` fields = CURRENT_TIMESTAMP

---

## Data Type Reference

| Type              | Used In                                   | Description                             |
| ----------------- | ----------------------------------------- | --------------------------------------- |
| UUID (PostgreSQL) | user_id, profile_id, token_id, session_id | Universally unique identifier (128-bit) |
| VARCHAR(n)        | usernames, emails, devices                | Variable-length strings                 |
| TEXT              | descriptions, comments, content           | Large text blocks                       |
| INTEGER           | area_id, review_id, rating                | Whole numbers                           |
| FLOAT             | latitude, longitude                       | Decimal numbers                         |
| BOOLEAN           | revoked, is_active                        | True/False values                       |
| DATE              | birthday                                  | Date without time                       |
| TIMESTAMP (TZ)    | created_at, updated_at, etc.              | Date and time with timezone             |

---

## Sample Query Examples (PostgreSQL)

### Get user with all related data

```sql
SELECT u.*, p.*, COUNT(DISTINCT t.token_id) as token_count,
       COUNT(DISTINCT s.session_id) as session_count
FROM users u
LEFT JOIN profiles p ON u.user_id = p.user_id
LEFT JOIN tokens t ON u.user_id = t.user_id
LEFT JOIN sessions s ON u.user_id = s.user_id
WHERE u.user_id = 'xxx-xxx-xxx'
GROUP BY u.user_id, p.profile_id;
```

### Get tourist area with all related data

```sql
SELECT ta.*,
       COUNT(DISTINCT aa.activity_id) as activity_count,
       COUNT(DISTINCT tr.review_id) as review_count,
       AVG(tr.rating) as avg_rating,
       COUNT(DISTINCT tv.visit_id) as total_visits
FROM tourist_area ta
LEFT JOIN area_activities aa ON ta.area_id = aa.area_id
LEFT JOIN tourist_reviews tr ON ta.area_id = tr.area_id
LEFT JOIN tourist_visits tv ON ta.area_id = tv.area_id
WHERE ta.region = 'Paris'
GROUP BY ta.area_id;
```

### Get active sessions per user

```sql
SELECT u.username, COUNT(s.session_id) as active_sessions
FROM users u
LEFT JOIN sessions s ON u.user_id = s.user_id AND s.is_active = true
GROUP BY u.user_id
ORDER BY active_sessions DESC;
```

### Get top-rated tourist areas

```sql
SELECT ta.name, ta.region, AVG(tr.rating) as avg_rating, COUNT(tr.review_id) as review_count
FROM tourist_area ta
LEFT JOIN tourist_reviews tr ON ta.area_id = tr.area_id
GROUP BY ta.area_id
ORDER BY avg_rating DESC
LIMIT 10;
```

---

## Notes for Seeding

When creating seeds, follow this order to maintain foreign key integrity:

1. **users** - Base table
2. **profiles** - Depends on users
3. **tokens** - Depends on users
4. **sessions** - Depends on users AND tokens
5. **tasks** - Depends on users
6. **tourist_area** - Independent
7. **area_activities** - Depends on tourist_area
8. **tourist_area_vectors** - Depends on tourist_area
9. **tourist_reviews** - Depends on tourist_area
10. **tourist_visits** - Depends on tourist_area
