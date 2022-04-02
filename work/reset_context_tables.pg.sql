DROP TABLE context_entity_identifier;
DROP TABLE context_entity_identifier_type_type_list;
DROP TABLE context_entity_identifier_type;
DROP TABLE context_entity_relation_identifier;
DROP TABLE context_entity_relation_trait;
DROP TABLE context_entity_relation_type_trait;
DROP TABLE context_entity_relation_types;
DROP TABLE context_entity_relation;
DROP TABLE context_entity_relation_type;
DROP TABLE context_entity_trait;
DROP TABLE context_entity_type_trait;
DROP TABLE context_entity_types;
DROP TABLE context_entity;
DROP TABLE context_term_relation;
DROP TABLE context_term_relation_type;
DROP TABLE context_term;
DROP TABLE context_trait_type;
DROP TABLE context_entity_type;
DROP TABLE context_vocabulary;
DROP TABLE context_work_log;

-- remove migration log from django_migrations table so we can re-migrate.
DELETE FROM django_migrations WHERE app = 'context';
