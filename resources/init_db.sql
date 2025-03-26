

CREATE TABLE user (
    id VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    login VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,

    PRIMARY KEY(id)
);

CREATE TABLE workspace (
    id VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NULL,

    created_by VARCHAR(36) NOT NULL,
    modified_by VARCHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    modified_at TIMESTAMP NOT NULL DEFAULT NOW(),

    PRIMARY KEY(id),
    FOREIGN KEY(created_by) REFERENCES user(id),
    FOREIGN KEY(modified_by) REFERENCES user(id)
);

CREATE TABLE workspace_item (
    id VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    workspace_id VARCHAR(36) NOT NULL,
    workspace_item_type VARCHAR(100) NOT NULL,
    workspace_item_key VARCHAR(255) NOT NULL,
    description VARCHAR(255) NULL,
    details VARCHAR(255) NULL,

    created_by VARCHAR(36) NOT NULL,
    modified_by VARCHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    modified_at TIMESTAMP NOT NULL DEFAULT NOW(),

    PRIMARY KEY(id),
    FOREIGN KEY(workspace_id) REFERENCES workspace(id),
    FOREIGN KEY(created_by) REFERENCES user(id),
    FOREIGN KEY(modified_by) REFERENCES user(id),

    UNIQUE KEY (workspace_item_key, workspace_id)
);

CREATE TABLE diagram (
    id VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NULL,
    diagram_type VARCHAR(100) NOT NULL,
    workspace_id VARCHAR(36) NOT NULL,

    created_by VARCHAR(36) NOT NULL,
    modified_by VARCHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    modified_at TIMESTAMP NOT NULL DEFAULT NOW(),

    PRIMARY KEY(id),
    FOREIGN KEY(created_by) REFERENCES user(id),
    FOREIGN KEY(modified_by) REFERENCES user(id),
    FOREIGN KEY(workspace_id) REFERENCES workspace(id)
);

CREATE TABLE user_access (
    user_id VARCHAR(36) NOT NULL,
    workspace_id VARCHAR(36) NOT NULL,
    user_permission VARCHAR(10) NOT NULL,

    PRIMARY KEY (user_id, workspace_id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (workspace_id) REFERENCES workspace(id) ON DELETE CASCADE
);

CREATE TABLE diagram_item (
    id VARCHAR(36) NOT NULL,
    diagram_id VARCHAR(36) NOT NULL,
    parent_id VARCHAR(36) NULL,
    workspace_item_id VARCHAR(36) NOT NULL,
    diagram_item_type INT NOT NULL,
    item_data JSON NULL,

    PRIMARY KEY(id),
    FOREIGN KEY(diagram_id) REFERENCES diagram(id) ON DELETE CASCADE,
    FOREIGN KEY(parent_id) REFERENCES diagram_item(id),
    FOREIGN KEY(workspace_item_id) REFERENCES workspace_item(id)
);

CREATE TABLE diagram_item_relationship (
    from_diagram_item_id VARCHAR(36) NOT NULL,
    to_diagram_item_id VARCHAR(36) NOT NULL,
    description VARCHAR(100) NOT NULL,
    details VARCHAR(255) NULL,
    diagram_type INT NOT NULL,
    data JSON NULL,

    PRIMARY KEY (from_diagram_item_id, to_diagram_item_id, description),
    FOREIGN KEY (from_diagram_item_id) REFERENCES diagram_item(id) ON DELETE CASCADE,
    FOREIGN KEY (to_diagram_item_id) REFERENCES diagram_item(id) ON DELETE CASCADE
);
