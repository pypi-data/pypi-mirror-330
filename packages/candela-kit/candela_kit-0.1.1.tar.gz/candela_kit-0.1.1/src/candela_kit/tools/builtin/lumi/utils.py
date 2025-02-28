import yaml


def make_schema_yaml(p, main_cols_only=False) -> str:

    def make_row(col):
        row = {
            "name": col.field_name,
            "description": col.description,
            "type": col.dtype.name,
        }
        if not main_cols_only:
            row["is_main"] = col.is_main
        return row

    d = {
        "name": p.meta.name,
        "description": p.meta.description,
        "columns": [
            make_row(c) for c in p.meta.columns if c.is_main or not main_cols_only
        ],
    }
    return yaml.dump(d, sort_keys=False)
