def calculate_risk(
    cvss,
    criticality,
    exposed
):

    multiplier = {
        "High":3,
        "Medium":2,
        "Low":1
    }

    exposure = 2 if exposed else 1

    return (
        cvss *
        multiplier[criticality] *
        exposure
    )
