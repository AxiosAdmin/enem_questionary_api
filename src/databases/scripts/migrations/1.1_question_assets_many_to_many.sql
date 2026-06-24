CREATE TABLE IF NOT EXISTS question_asset_questions (
    question_id UUID NOT NULL,
    question_asset_id UUID NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL,
    CONSTRAINT question_asset_questions_pkey PRIMARY KEY (question_id, question_asset_id),
    CONSTRAINT question_asset_questions_question_id_fkey FOREIGN KEY (question_id) REFERENCES questions (id) ON DELETE CASCADE,
    CONSTRAINT question_asset_questions_question_asset_id_fkey FOREIGN KEY (question_asset_id) REFERENCES question_assets (id) ON DELETE CASCADE
);

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'question_assets'
          AND column_name = 'question_id'
    ) THEN
        INSERT INTO question_asset_questions (
            question_id,
            question_asset_id,
            created_at
        )
        SELECT
            question_id,
            id,
            COALESCE(created_at, now())
        FROM question_assets
        WHERE question_id IS NOT NULL
        ON CONFLICT (question_id, question_asset_id) DO NOTHING;

        ALTER TABLE question_assets
            DROP CONSTRAINT IF EXISTS question_assets_question_id_fkey;

        ALTER TABLE question_assets
            DROP COLUMN IF EXISTS question_id;
    END IF;
END $$;
