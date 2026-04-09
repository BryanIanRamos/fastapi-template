-- System Architecture Tables (PostgreSQL-friendly SQL)
-- Notes:
-- 1) Column names keep your requested naming, including: vertified_at, happended_at, tiotal_value, quipment_id.
-- 2) UUID values are expected to be provided by the application unless you add DB-side defaults.

BEGIN;

CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    vertified_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    role INTEGER NOT NULL DEFAULT 0,
    admin UUID NULL,
    acad_info_id UUID NULL,
    forwarded_by UUID NULL,
    CONSTRAINT fk_users_admin FOREIGN KEY (admin) REFERENCES users(user_id),
    CONSTRAINT fk_users_forwarded_by FOREIGN KEY (forwarded_by) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS tokens (
    token_id UUID PRIMARY KEY,
    value VARCHAR(100) NOT NULL,
    expired_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id UUID NOT NULL,
    CONSTRAINT fk_tokens_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS activity_log (
    log_id UUID PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    user_role INTEGER NOT NULL,
    module VARCHAR(100) NOT NULL,
    recorded VARCHAR(255) NOT NULL,
    happended_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id UUID NULL,
    CONSTRAINT fk_activity_log_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS batch (
    batch_id UUID PRIMARY KEY,
    date_started DATE NOT NULL,
    date_count DATE NOT NULL,
    male_count INTEGER NOT NULL DEFAULT 0,
    female_count INTEGER NOT NULL DEFAULT 0,
    total_population INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS biological_assets (
    bio_assets_id VARCHAR(100) PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    begin_qty INTEGER NOT NULL DEFAULT 0,
    begin_fair_val DECIMAL(14, 2) NOT NULL DEFAULT 0,
    purchase_qty INTEGER NOT NULL DEFAULT 0,
    purchase_fair_val DECIMAL(14, 2) NOT NULL DEFAULT 0,
    birth_qty INTEGER NOT NULL DEFAULT 0,
    birth_fair_val DECIMAL(14, 2) NOT NULL DEFAULT 0,
    add_change_qty INTEGER NOT NULL DEFAULT 0,
    add_change_fair_val DECIMAL(14, 2) NOT NULL DEFAULT 0,
    sale_qty INTEGER NOT NULL DEFAULT 0,
    sale_fair_val DECIMAL(14, 2) NOT NULL DEFAULT 0,
    death_qty INTEGER NOT NULL DEFAULT 0,
    death_fair_val DECIMAL(14, 2) NOT NULL DEFAULT 0,
    deduction_changes_qty INTEGER NOT NULL DEFAULT 0,
    deduction_change_fair_value DECIMAL(14, 2) NOT NULL DEFAULT 0,
    remarks VARCHAR(255) NULL,
    record_date DATE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    batch_id UUID NOT NULL,
    CONSTRAINT fk_bio_assets_batch FOREIGN KEY (batch_id) REFERENCES batch(batch_id)
);

CREATE TABLE IF NOT EXISTS equipments (
    equipment_id UUID PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description VARCHAR(255) NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    unit_value DECIMAL(14, 2) NOT NULL DEFAULT 0,
    tiotal_value DECIMAL(14, 2) NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL,
    date_aquired DATE NULL,
    remarks VARCHAR(255) NULL
);

CREATE TABLE IF NOT EXISTS equipment_transaction (
    equipment_trans_id UUID PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    transaction_date DATE NOT NULL,
    remarks VARCHAR(255) NULL,
    quipment_id UUID NOT NULL,
    CONSTRAINT fk_equipment_tx_equipment FOREIGN KEY (quipment_id) REFERENCES equipments(equipment_id)
);

CREATE INDEX IF NOT EXISTS idx_tokens_user_id ON tokens(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_log_user_id ON activity_log(user_id);
CREATE INDEX IF NOT EXISTS idx_biological_assets_batch_id ON biological_assets(batch_id);
CREATE INDEX IF NOT EXISTS idx_equipment_transaction_quipment_id ON equipment_transaction(quipment_id);

COMMIT;
