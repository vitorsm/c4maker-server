
INSERT INTO user (id, name, login, password) VALUES
('00000000-0000-0000-0000-000000000000', 'User 1', 'user', '$2b$12$eSoRK4Da8sEX3GSg56FKmujEq2JdeaMIt98nHKfdusf78UzzSaOCS'),
('00000000-0000-0000-0000-000000000001', 'User 2', 'user2', '$2b$12$eSoRK4Da8sEX3GSg56FKmujEq2JdeaMIt98nHKfdusf78UzzSaOCS');
INSERT INTO workspace (id, name, description, created_by, modified_by, created_at, modified_at) VALUES
('00000000-0000-0000-0000-000000000000', 'Workspace 1', 'Desc 1', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000', '2022-01-01 07:44:42', '2022-01-01 07:44:42'),
('00000000-0000-0000-0000-000000000001', 'Workspace 2', 'Desc 2', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000', '2022-01-01 07:44:42', '2022-01-01 07:44:42');

INSERT INTO diagram (id, name, description, diagram_type, workspace_id, created_by, modified_by, created_at, modified_at) VALUES
('00000000-0000-0000-0000-000000000000', 'Diagram 1', 'Desc 1', 'C4', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000', '2022-01-01 07:44:42', '2022-01-01 07:44:42');
INSERT INTO user_access (user_id, workspace_id, user_permission) VALUES ('00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000', 'EDIT');

INSERT INTO workspace_item (id, name, workspace_id, workspace_item_type, workspace_item_key, description, details, created_by, modified_by, created_at, modified_at) VALUES
('00000000-0000-0000-0000-000000000000', 'Item 1', '00000000-0000-0000-0000-000000000000', 'PERSONA', 'item1', 'Desc 1', 'Details 1', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000', '2022-01-01 07:44:42', '2022-01-01 07:44:42'),
('00000000-0000-0000-0000-000000000001', 'Item 2', '00000000-0000-0000-0000-000000000000', 'CONTAINER', 'item2', 'Desc 2', 'Details 2', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000', '2022-01-01 07:44:42', '2022-01-01 07:44:42'),
('00000000-0000-0000-0000-000000000002', 'Item 3', '00000000-0000-0000-0000-000000000000', 'CONTAINER', 'item3', 'Desc 3', 'Details 3', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000', '2022-01-01 07:44:42', '2022-01-01 07:44:42');

INSERT INTO diagram_item (id, diagram_id, parent_id, workspace_item_id, diagram_item_type, item_data) VALUES
('00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000', null, '00000000-0000-0000-0000-000000000000', 1, '{"position": {"x": 1, "y": 1, "width": 10, "height": 10}, "color": "white"}'),
('00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000000', null, '00000000-0000-0000-0000-000000000001', 1, '{"position": {"x": 1, "y": 1, "width": 10, "height": 10}, "color": "white"}'),
('00000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000002', 1, '{"position": {"x": 1, "y": 1, "width": 10, "height": 10}, "color": "white"}');

INSERT INTO diagram_item_relationship (from_diagram_item_id, to_diagram_item_id, description, details, diagram_type, data) VALUES
('00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000002', 'uses', 'details', 1, '{"from_position": {"x": 1, "y": 1, "width": 10, "height": 10}, "to_position": {"x": 1, "y": 1, "width": 10, "height": 10}}');
