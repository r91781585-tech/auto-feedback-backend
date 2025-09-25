-- users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    user_type VARCHAR(50) CHECK (user_type IN ('student', 'educator')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- rubrics table
CREATE TABLE rubrics (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- criteria table
CREATE TABLE criteria (
    id SERIAL PRIMARY KEY,
    rubric_id INTEGER REFERENCES rubrics(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    max_score INTEGER
);

-- mentor_inputs table (was student_inputs)
CREATE TABLE mentor_inputs (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    rubric_id INTEGER REFERENCES rubrics(id) ON DELETE CASCADE,
    evaluator_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- performance_data table
CREATE TABLE performance_data (
    id SERIAL PRIMARY KEY,
    mentor_input_id INTEGER REFERENCES mentor_inputs(id) ON DELETE CASCADE,
    criterion_id INTEGER REFERENCES criteria(id) ON DELETE CASCADE,
    score INTEGER,
    remarks TEXT
);

-- feedbacks table
CREATE TABLE feedbacks (
    id SERIAL PRIMARY KEY,
    mentor_input_id INTEGER REFERENCES mentor_inputs(id) ON DELETE CASCADE,
    feedback_text TEXT,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
