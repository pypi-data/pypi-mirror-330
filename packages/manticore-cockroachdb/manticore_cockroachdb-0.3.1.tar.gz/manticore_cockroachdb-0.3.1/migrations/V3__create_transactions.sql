CREATE TABLE transactions (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    from_account UUID REFERENCES accounts(id),
                    to_account UUID REFERENCES accounts(id),
                    amount DECIMAL(19,4) NOT NULL,
                    type TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP WITH TIME ZONE,
                    description TEXT,
                    CONSTRAINT amount_positive CHECK (amount > 0.0000),
                    CONSTRAINT valid_type CHECK (type IN ('transfer', 'deposit', 'withdrawal')),
                    CONSTRAINT valid_status CHECK (status IN ('pending', 'completed', 'failed'))
                )

-- DOWN
DROP TABLE transactions