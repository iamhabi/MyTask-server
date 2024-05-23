-- Your SQL goes here
DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    is_done TEXT NOT NULL,
    group_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    created TEXT NOT NULL,
    due_date TEXT NOT NULL
)