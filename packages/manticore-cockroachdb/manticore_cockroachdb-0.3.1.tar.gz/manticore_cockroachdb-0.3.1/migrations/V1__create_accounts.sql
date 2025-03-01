CREATE TABLE accounts (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    owner TEXT NOT NULL,
                    balance DECIMAL(19,4) NOT NULL DEFAULT 0.0000,
                    type TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT balance_non_negative CHECK (balance >= 0.0000)
                )

-- DOWN
DROP TABLE accounts