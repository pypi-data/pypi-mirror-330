ALTER TABLE accounts 
                ADD COLUMN status TEXT NOT NULL DEFAULT 'active',
                ADD COLUMN email TEXT UNIQUE,
                ADD COLUMN last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                ADD CONSTRAINT valid_status CHECK (status IN ('active', 'inactive', 'suspended'))

-- DOWN
ALTER TABLE accounts 
                DROP COLUMN status,
                DROP COLUMN email,
                DROP COLUMN last_updated