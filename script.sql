/*
CREATE TABLE tasks (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	status VARCHAR, 
	estimated_duration INTEGER, 
	start_timestamp INTEGER, 
	consume_timestamp INTEGER, 
	markdown_content VARCHAR, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_tasks_id ON tasks (id);
CREATE TABLE columns (
	id INTEGER NOT NULL, 
	task_order TEXT, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_columns_id ON columns (id);
CREATE TABLE column_orders (
	id INTEGER NOT NULL, 
	column_order TEXT, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_column_orders_id ON column_orders (id);
*/
