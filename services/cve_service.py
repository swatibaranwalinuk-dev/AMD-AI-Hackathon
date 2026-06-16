import requests

def get_cve_details(cve_id):

    url = (
        f"https://services.nvd.nist.gov/rest/json/cves/2.0"
        f"?cveId={cve_id}"
    )

    try:

        response = requests.get(
            url,
            timeout=20
        )

        data = response.json()

        vulnerabilities = data.get(
            "vulnerabilities",
            []
        )

        if not vulnerabilities:

            return "CVE Not Found"

        cve = vulnerabilities[0]

        return cve

    except Exception as error:

        return str(error)
