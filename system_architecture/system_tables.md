# System Table Structure

This folder contains copy/paste-ready database structure docs.

## Files

- `system_tables.sql`: SQL script to create all requested tables.
- `system_tables.svg`: Visual ER diagram image.
- `system_tables.md`: This reference document.

## Quick Apply

```sql
-- PostgreSQL example
\i system_architecture/system_tables.sql
```

## Tables Included

- users
- tokens
- activity_log
- batch
- biological_assets
- equipments
- equipment_transaction

## Relationship Summary

- `tokens.user_id` -> `users.user_id`
- `activity_log.user_id` -> `users.user_id`
- `users.admin` -> `users.user_id` (self-reference)
- `users.forwarded_by` -> `users.user_id` (self-reference)
- `biological_assets.batch_id` -> `batch.batch_id`
- `equipment_transaction.quipment_id` -> `equipments.equipment_id`

## ER Diagram (Mermaid)

```mermaid
erDiagram
    users ||--o{ tokens : has
    users ||--o{ activity_log : creates
    users ||--o{ users : admin_of
    batch ||--o{ biological_assets : groups
    equipments ||--o{ equipment_transaction : has

    users {
        UUID user_id PK
        VARCHAR email
        VARCHAR password
        DATETIME vertified_at
        DATETIME created_at
        INT role
        UUID admin FK
        UUID acad_info_id
        UUID forwarded_by FK
    }

    tokens {
        UUID token_id PK
        VARCHAR value
        DATETIME expired_at
        DATETIME created_at
        UUID user_id FK
    }

    activity_log {
        UUID log_id PK
        VARCHAR user_name
        INT user_role
        VARCHAR module
        VARCHAR recorded
        DATETIME happended_at
        UUID user_id FK
    }

    batch {
        UUID batch_id PK
        DATE date_started
        DATE date_count
        INT male_count
        INT female_count
        INT total_population
        VARCHAR status
    }

    biological_assets {
        VARCHAR bio_assets_id PK
        VARCHAR description
        INT begin_qty
        DECIMAL begin_fair_val
        INT purchase_qty
        DECIMAL purchase_fair_val
        INT birth_qty
        DECIMAL birth_fair_val
        INT add_change_qty
        DECIMAL add_change_fair_val
        INT sale_qty
        DECIMAL sale_fair_val
        INT death_qty
        DECIMAL death_fair_val
        INT deduction_changes_qty
        DECIMAL deduction_change_fair_value
        VARCHAR remarks
        DATE record_date
        DATETIME created_at
        DATETIME updated_at
        UUID batch_id FK
    }

    equipments {
        UUID equipment_id PK
        VARCHAR name
        VARCHAR description
        INT quantity
        DECIMAL unit_value
        DECIMAL tiotal_value
        VARCHAR status
        DATE date_aquired
        VARCHAR remarks
    }

    equipment_transaction {
        UUID equipment_trans_id PK
        VARCHAR type
        INT quantity
        DATE transaction_date
        VARCHAR remarks
        UUID quipment_id FK
    }
```

## Naming Note

Requested field names were preserved as provided (including spellings like `vertified_at`, `happended_at`, `tiotal_value`, and `quipment_id`) so your copy/paste stays aligned with your request.
