-- SQLite to create a new db from scratch compatable with the python code

CREATE TABLE "employees" (
	"employee_id"	INTEGER UNIQUE,
	"first_name"	TEXT NOT NULL,
	"last_name"		TEXT NOT NULL,
	"email"			TEXT NOT NULL,
	"pin"			TEXT NOT NULL,
	"registered_at"	TEXT DEFAULT (datetime('now', 'localtime')),
	"active"		INTEGER DEFAULT 1,
	PRIMARY KEY("employee_id" AUTOINCREMENT)
);
UPDATE sqlite_sequence SET seq = 100 WHERE name = 'employees';

CREATE TABLE "tasks" (
	"task_id"		INTEGER UNIQUE,
	"sender_id"		INTEGER NOT NULL,
	"receiver_id"	INTEGER NOT NULL,
	"created_at"	TEXT DEFAULT (datetime('now', 'localtime')),
	"modified_at"	TEXT DEFAULT (datetime('now', 'localtime')),
	"title"			TEXT,
	"body"			TEXT,
	"reference"		TEXT,
	"due_at"		TEXT,
	"starred"		INTEGER DEFAULT 0,
	"status"		INTEGER,
	"expected_at"	TEXT,
	"reply"			TEXT,
	"archived"		INTEGER DEFAULT 0,
	PRIMARY KEY("task_id" AUTOINCREMENT),
	FOREIGN KEY("receiver_id") REFERENCES "employees"("employee_id"),
	FOREIGN KEY("sender_id") REFERENCES "employees"("employee_id")
);
UPDATE sqlite_sequence SET seq = 100000 WHERE name = 'tasks';

-- Detailed tasks view to create a full report for work manager

CREATE VIEW report AS
SELECT
    tasks.task_id,
	tasks.created_at,
	CONCAT(sender.first_name, ' ', sender.last_name) AS sender_full_name,
	tasks.due_at,
	tasks.starred,
    tasks.title,
    tasks.body,
    tasks.reference,
	CONCAT(receiver.first_name, ' ', receiver.last_name) AS receiver_full_name,
    tasks.reply,
    tasks.expected_at,
    tasks.status,
    tasks.modified_at,
    
	CASE
        WHEN tasks.due_at IS NOT NULL THEN
            CAST((julianday(tasks.due_at) - julianday(tasks.created_at)) AS INTEGER)
        ELSE NULL
    END AS due_window,
	
	CASE
        WHEN tasks.expected_at IS NOT NULL THEN
            CAST((julianday(tasks.expected_at) - julianday(tasks.created_at)) AS INTEGER)
        ELSE NULL
    END AS expected_duration,
	
    CASE
        WHEN tasks.expected_at IS NOT NULL AND tasks.due_at IS NOT NULL THEN
            CAST((julianday(tasks.expected_at) - julianday(tasks.due_at)) AS INTEGER)
        ELSE NULL
    END AS expected_delay,
	
	CASE
        WHEN tasks.status = 0 OR tasks.status IS NULL THEN
            CAST((julianday('now') - julianday(tasks.created_at)) AS INTEGER)
        ELSE NULL
    END AS today_elapsed,
	
    CASE
        WHEN (tasks.status = 0 OR tasks.status IS NULL) AND tasks.due_at IS NOT NULL THEN
            CAST((julianday('now') - julianday(tasks.due_at)) AS INTEGER)
        ELSE NULL
    END AS today_delay,
    
	CASE
        WHEN tasks.status = 1 THEN
            CAST((julianday(tasks.modified_at) - julianday(tasks.created_at)) AS INTEGER)
        ELSE NULL
    END AS actual_duration,
	
    CASE
        WHEN tasks.status = 1 AND tasks.due_at IS NOT NULL THEN
            CAST((julianday(tasks.modified_at) - julianday(tasks.due_at)) AS INTEGER)
        ELSE NULL
    END AS actual_delay
	
FROM
    tasks
JOIN employees AS sender ON tasks.sender_id = sender.employee_id
JOIN employees AS receiver ON tasks.receiver_id = receiver.employee_id
WHERE tasks.archived = 0;
