# OpenAPI Reference

## Sources

- Local backend Swagger UI: `http://localhost:8080/docs`
- Local backend OpenAPI JSON: `http://localhost:8080/openapi.json`
- Repository OpenAPI YAML: [`openapi.yaml`](../openapi.yaml)

## Regenerate OpenAPI YAML

From project root:

```bash
python3 - <<'PY'
import yaml
from main import app
with open('openapi.yaml', 'w', encoding='utf-8') as f:
    yaml.safe_dump(app.openapi(), f, sort_keys=False)
print('wrote openapi.yaml')
PY
```

## Notes

The GitHub Pages docs build copies `openapi.yaml` into the published site artifact for reference.
