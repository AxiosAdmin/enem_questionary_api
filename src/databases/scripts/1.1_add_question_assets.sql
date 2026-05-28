CREATE TABLE IF NOT EXISTS question_assets (
    id UUID DEFAULT gen_random_uuid() NOT NULL,
    question_id UUID NOT NULL,
    asset_type VARCHAR(20) NOT NULL,
    rendering_mode VARCHAR(20) NOT NULL,
    position VARCHAR(30) NOT NULL,
    display_order INTEGER DEFAULT 0 NOT NULL,
    storage_status VARCHAR(40) DEFAULT 'not_required' NOT NULL,
    title TEXT,
    caption TEXT,
    alt_text TEXT,
    source_label TEXT,
    content TEXT,
    storage_provider VARCHAR(30),
    storage_key TEXT,
    public_url TEXT,
    mime_type VARCHAR(100),
    metadata JSONB,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    CONSTRAINT question_assets_pkey PRIMARY KEY (id),
    CONSTRAINT question_assets_question_id_fkey FOREIGN KEY (question_id) REFERENCES questions (id) ON DELETE CASCADE,
    CONSTRAINT question_assets_asset_type_check CHECK (
        asset_type IN ('text', 'table', 'chart', 'image', 'map', 'diagram', 'infographic')
    ),
    CONSTRAINT question_assets_rendering_mode_check CHECK (
        rendering_mode IN ('inline_text', 'structured_data', 'generated_image')
    ),
    CONSTRAINT question_assets_position_check CHECK (
        position IN ('before_statement', 'after_statement')
    ),
    CONSTRAINT question_assets_storage_status_check CHECK (
        storage_status IN ('not_required', 'pending_storage_configuration', 'stored', 'generation_failed')
    )
);
