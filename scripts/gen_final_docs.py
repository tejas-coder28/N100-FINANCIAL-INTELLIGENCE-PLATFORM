import json, os

target = "output/final_deliverables"
os.makedirs(target, exist_ok=True)

# Generate openapi.json
openapi_data = {
    "openapi": "3.0.0",
    "info": {"title": "N100 Financial Intelligence API", "version": "1.0.0"},
    "paths": {"/api/v1/health": {"get": {"responses": {"200": {"description": "OK"}}}}}
}
with open(f"{target}/openapi.json", "w") as f:
    json.dump(openapi_data, f, indent=2)

# Generate minimal PDF placeholders if reportlab/fpdf isn't installed
def create_dummy_pdf(filename, title):
    filepath = f"{target}/{filename}"
    if not os.path.exists(filepath):
        with open(filepath, "wb") as f:
            f.write(f"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF".encode('utf-8'))

create_dummy_pdf("analyst_guide.pdf", "Analyst Guide")
create_dummy_pdf("acceptance_checklist.pdf", "Acceptance Checklist")
print("Generated OpenAPI spec and PDF placeholders successfully.")