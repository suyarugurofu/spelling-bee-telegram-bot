CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    training_level INTEGER DEFAULT 1,
    tts_accent TEXT DEFAULT 'com'
);

CREATE TABLE IF NOT EXISTS words (
    id SERIAL PRIMARY KEY,
    word TEXT UNIQUE NOT NULL,
    initial_level INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS word_progress (
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    word_id INTEGER REFERENCES words(id) ON DELETE CASCADE,
    correct_count INTEGER DEFAULT 0,
    is_learned BOOLEAN DEFAULT FALSE,
    last_seen_session_id INTEGER,
    PRIMARY KEY (user_id, word_id)
);

CREATE TABLE IF NOT EXISTS training_sessions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    started_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS word_attempts (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    word_id INTEGER REFERENCES words(id) ON DELETE CASCADE,
    is_correct BOOLEAN NOT NULL,
    session_id INTEGER REFERENCES training_sessions(id) ON DELETE CASCADE
);
