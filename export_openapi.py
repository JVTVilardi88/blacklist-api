# export_openapi.py
from app import app
from openapi_generator import generate_openapi_spec
import json, os

OUTPUT_DIR = "docs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "openapi.json")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

spec = generate_openapi_spec(app)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=2, ensure_ascii=False)

print(f"Archivo OpenAPI generado en: {OUTPUT_FILE}")
