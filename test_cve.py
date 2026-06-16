from services.cve_service import get_cve_details

result = get_cve_details(
    "CVE-2024-3094"
)

print(result)
