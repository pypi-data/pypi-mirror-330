import rich

from port_forward_manager.core import models


def base_normalisation(record):
    record_id = str(record.get("id"))
    if len(str(record_id)) != 12:

        record["id"] = models.generate_uid()
        rich.print(f"Creating ID {record_id} vs {record["id"]} {len(record["id"])}")
        record_id = record["id"]


    return record_id


def normalise_import(settings):
    rich.print("Normalise import")

    group_index = {}
    schema_index = {}
    session_index = {}
    ssh_group_index = {}

    for record in settings.get("groups", []):
        record_id = base_normalisation(record)
        group_index[record_id] = models.Group(**record)

    # rich.print("Groups", group_index)

    for record in settings.get("schemas", []):
        record_id = base_normalisation(record)

        previous_group_id = str(record.get("group_id"))
        group = group_index.get(previous_group_id)
        if not group:
            rich.print(f"Error: Group not found {previous_group_id}")
            continue

        record['group_id'] = group.id
        record['active'] = False

        schema_index[record_id] = models.Schema(**record)

    # rich.print("Schemas", schema_index)

    for record in settings.get("sessions", []):
        record_id = base_normalisation(record)

        schema_id = str(record.get("schema_id"))
        schema = schema_index.get(schema_id)

        if not schema:
            rich.print(f"Session parent schema not found {schema_id}")
            continue

        record["schema_id"] = schema.id

        session_index[record_id] = models.Session(**record)

    # rich.print("Sessions", session_index)

    for record in settings.get("ssh_groups", []):
        record_id = str(record.get("id"))

        if len(str(record_id)) == 12:
            record["id"] = models.generate_uid()

        schema_id = str(record.get("schema_id"))
        schema = schema_index.get(schema_id)
        if not schema:
            rich.print(f"Error: SSHGroup schema not found {schema_id}")
            continue

        record["schema_id"] = schema.id
        ssh_group_index[record_id] = models.SSHGroup(**record)

    # rich.print("SSHGroups", ssh_group_index)

    settings["groups"] = list(group_index.values())
    settings["schemas"] = list(schema_index.values())
    settings["sessions"] = list(session_index.values())

    return settings


def import_settings(settings, prune):
    change_count = 0
    settings = normalise_import(settings)
    rich.print("Importing PFM DB DUMP")

    groups = {}
    schemas = {}
    sessions = {}

    # Import groups
    for group_definition in settings.get("groups", []):
        group = models.Group.find_by_id(group_definition.id)
        if not group:
            group = models.Group.find_by_label(group_definition.label)

        if not group:
            change_count += 1
            rich.print(f"* Creating group {group_definition.label} {group_definition.id}")
            models.Group.add(group_definition)
        else:
            for key, value in group_definition.dict().items():
                if key == "id":
                    group_definition.id = group.id
                    continue
                setattr(group, key, value)

        groups[group_definition.id] = group_definition

    # rich.print(f"Group insert: { groups }")
    if prune:
        for group in models.Group.index():
            # rich.print(f"* Checking group {group.label}")
            if group.id not in groups.keys():
                if not group.visible:
                    continue

                rich.print(f"  * Deleting group {group.label} - {group.id}")
                models.Group.delete(group)

    rich.print(f"Imported {change_count} groups")
    models.db_session.commit()

    # Import schemas
    for schema_definition in settings.get('schemas', []):
        # rich.print(f"Handling schema {schema_definition.id}")
        tmp_group = groups.get(schema_definition.group_id, {})

        # rich.print(f"  * Group", schema_definition.group_id, groups)
        group = models.Group.find_by_id(schema_definition.group_id)

        if not group:
            group = models.Group.find_by_label(tmp_group.get('label'))

        if not group:
            rich.print(f"IGNORING schema - Error could not find group {schema_definition.group_id}")
            continue

        schemas[schema_definition.id] = schema_definition.label

        schema = models.Schema.find_by_id(schema_definition.id)
        if not schema:
            change_count += 1
            # rich.print(f"* Importing schema {schema_definition.label}")
            group.schemas.append(schema_definition)
        elif not schema.active:
            # rich.print(f"* Update schema {schema_definition.label} {schema_definition.id}")
            for key, value in schema_definition.dict().items():
                setattr(schema, key, value)

    rich.print("Schemas prune")
    if prune:
        for schema in models.Schema.index():
            # rich.print(f"* Checking schema {schema.label}")
            if schema.id not in schemas.keys() and not schema.active:
                rich.print(f"  * Deleting schema {schema.id} {schema.label}")
                models.Schema.delete(schema)

    models.db_session.commit()

    # Import sessions
    for session_definition in settings.get("sessions"):
        schema_label = schemas.get(session_definition.schema_id)
        # rich.print(f"(yaml-import) Schema: {schema_label} '{session_definition.schema_id}'")

        schema = models.Schema.find_by_id(session_definition.schema_id)
        if not schema:
            rich.print(
                f"IGNORING session - Error could not find schema '{schema_label}'"
            )
            continue

        session = models.Session.find_by_id(session_definition.id)

        if not session:
            session = schema.get_session(
                session_definition.type,
                session_definition.hostname,
                session_definition.remote_port
            )

        if not session:
            change_count += 1
            print(
                f"    * Importing session {session_definition.type} {session_definition.hostname} {session_definition.remote_port}")
            if session_definition.local_port == 0:
                session_definition.local_port_dynamic = True

            schema.sessions.append(session_definition)
        else:
            for key in session.__fields__.keys() - ['connected', 'active']:
                value = getattr(session_definition, key)
                setattr(session, key, value)

        sessions[session_definition.id] = session_definition

    if prune:
        for session in models.Session.index():
            # rich.print(f"* Checking session {session.label}")
            if session.id not in sessions.keys() and not session.connected:
                rich.print(f"  * Deleting session")
                models.Session.delete(session)

    models.db_session.commit()

    # Import SSH groups
    for ssh_group in settings.get("sshGroups", []):
        schema = models.Schema.find_by_id(ssh_group.schema_id)
        if not schema:
            rich.print(
                f"IGNORING session - Error could not find schema '{ssh_group.schema_id}'"
            )
            continue

        group = schema.get_ssh_group(ssh_group.label)
        if not group:
            change_count += 1
            print(f"    * Importing SSH group {ssh_group.label}")

            schema.ssh_groups.append(ssh_group)

    models.db_session.commit()

    return change_count


def export_settings():
    return {
        "export_format": "db_dump",
        "version": "2.0",
        "groups": models.Group.get_state(),
        "schemas": models.Schema.get_state(),
        "sessions": models.Session.get_state(),
        "ssh_groups": models.SSHGroup.get_state(),
    }
