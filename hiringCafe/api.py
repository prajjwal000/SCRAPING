import requests
import csv

cookies = {
    'ph_phc_PF366Udfg1etPsVw8cx8tlB6ePhBp7KO6E7ncWcXKtd_posthog': '%7B%22distinct_id%22%3A%2201957f56-fc38-7eea-929e-07ef644be8f2%22%2C%22%24sesid%22%3A%5Bnull%2Cnull%2Cnull%5D%7D',
}

headers = {
    'Host': 'hiring.cafe',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://hiring.cafe/',
    # Already added when you pass json=
    # 'Content-Type': 'application/json',
    # 'Content-Length': '3547',
    'Origin': 'https://hiring.cafe',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Dnt': '1',
    'Sec-Gpc': '1',
    'Priority': 'u=4',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    # Requests doesn't support trailers
    # 'Te': 'trailers',
    # 'Cookie': 'ph_phc_PF366Udfg1etPsVw8cx8tlB6ePhBp7KO6E7ncWcXKtd_posthog=%7B%22distinct_id%22%3A%2201957f56-fc38-7eea-929e-07ef644be8f2%22%2C%22%24sesid%22%3A%5Bnull%2Cnull%2Cnull%5D%7D',
}

json_data = {
    'size': 40,
    'page': 0,
    'searchState': {
        'geoLocRadius': 50,
        'selectedPlaceDetail': None,
        'locationSearchType': 'precise',
        'preciseLocationPreference': 'WITHIN_SPECIFIC_RADIUS',
        'broaderLocationPreference': 'ANY_JOB_WITHIN_REGION',
        'higherOrderPrefs': [
            'ANYWHERE_IN_CONTINENT',
            'ANYWHERE_IN_THE_WORLD',
        ],
        'flexibleRegions': [],
        'workplaceTypes': [
            'Remote',
            'Hybrid',
            'Onsite',
        ],
        'defaultToUserLocation': True,
        'userLocation': {
            'isLoadingUserCountry': True,
        },
        'physicalEnvironments': [
            'Office',
            'Outdoor',
            'Vehicle',
            'Industrial',
            'Customer-Facing',
        ],
        'physicalLaborIntensity': [
            'Low',
            'Medium',
            'High',
        ],
        'physicalPositions': [
            'Sitting',
            'Standing',
        ],
        'oralCommunicationLevels': [
            'Low',
            'Medium',
            'High',
        ],
        'computerUsageLevels': [
            'Low',
            'Medium',
            'High',
        ],
        'cognitiveDemandLevels': [
            'Low',
            'Medium',
            'High',
        ],
        'currency': {
            'label': 'Any',
            'value': None,
        },
        'frequency': {
            'label': 'Any',
            'value': None,
        },
        'minCompensationLowEnd': None,
        'minCompensationHighEnd': None,
        'maxCompensationLowEnd': None,
        'maxCompensationHighEnd': None,
        'restrictJobsToTransparentSalaries': False,
        'calcFrequency': 'Yearly',
        'commitmentTypes': [
            'Full Time',
            'Part Time',
            'Contract',
            'Internship',
            'Temporary',
            'Seasonal',
            'Volunteer',
        ],
        'jobTitleQuery': '',
        'jobDescriptionQuery': '',
        'associatesDegreeFieldsOfStudy': [],
        'excludedAssociatesDegreeFieldsOfStudy': [],
        'bachelorsDegreeFieldsOfStudy': [],
        'excludedBachelorsDegreeFieldsOfStudy': [],
        'mastersDegreeFieldsOfStudy': [],
        'excludedMastersDegreeFieldsOfStudy': [],
        'doctorateDegreeFieldsOfStudy': [],
        'excludedDoctorateDegreeFieldsOfStudy': [],
        'associatesDegreeRequirements': [],
        'bachelorsDegreeRequirements': [],
        'mastersDegreeRequirements': [],
        'doctorateDegreeRequirements': [],
        'licensesAndCertifications': [],
        'excludedLicensesAndCertifications': [],
        'excludeAllLicensesAndCertifications': False,
        'seniorityLevel': [
            'No Prior Experience Required',
            'Entry Level',
            'Mid Level',
            'Senior Level',
        ],
        'roleTypes': [
            'Individual Contributor',
            'People Manager',
        ],
        'roleYoeRange': [
            0,
            20,
        ],
        'excludeIfRoleYoeIsNotSpecified': False,
        'managementYoeRange': [
            0,
            20,
        ],
        'excludeIfManagementYoeIsNotSpecified': False,
        'securityClearances': [
            'None',
            'Confidential',
            'Secret',
            'Top Secret',
            'Top Secret/SCI',
            'Public Trust',
            'Interim Clearances',
            'Other',
        ],
        'languageRequirements': [],
        'excludedLanguageRequirements': [],
        'languageRequirementsOperator': 'OR',
        'excludeJobsWithAdditionalLanguageRequirements': False,
        'airTravelRequirement': [
            'None',
            'Minimal',
            'Moderate',
            'Extensive',
        ],
        'landTravelRequirement': [
            'None',
            'Minimal',
            'Moderate',
            'Extensive',
        ],
        'morningShiftWork': [],
        'eveningShiftWork': [],
        'overnightShiftWork': [],
        'weekendAvailabilityRequired': 'Doesn\'t Matter',
        'holidayAvailabilityRequired': 'Doesn\'t Matter',
        'overtimeRequired': 'Doesn\'t Matter',
        'onCallRequirements': [
            'None',
            'Occasional (once a month or less)',
            'Regular (once a week or more)',
        ],
        'benefitsAndPerks': [],
        'applicationFormEase': [],
        'companyNames': [],
        'excludedCompanyNames': [],
        'usaGovPref': None,
        'industries': [],
        'excludedIndustries': [],
        'companyKeywords': [],
        'companyKeywordsBooleanOperator': 'OR',
        'excludedCompanyKeywords': [],
        'hideJobTypes': [],
        'encouragedToApply': [],
        'searchQuery': 'software engineer',
        'dateFetchedPastNDays': 121,
        'hiddenCompanies': [],
        'user': None,
        'searchModeSelectedCompany': None,
        'departments': [],
        'restrictedSearchAttributes': [],
        'sortBy': 'default',
        'technologyKeywordsQuery': '',
        'requirementsKeywordsQuery': '',
        'companyPublicOrPrivate': 'all',
        'latestInvestmentYearRange': [
            None,
            None,
        ],
        'latestInvestmentSeries': [],
        'latestInvestmentAmount': None,
        'latestInvestmentCurrency': [],
        'investors': [],
        'excludedInvestors': [],
        'isNonProfit': 'all',
        'companySizeRanges': [],
        'minYearFounded': None,
        'maxYearFounded': None,
        'excludedLatestInvestmentSeries': [],
    },
}

response = requests.post('https://hiring.cafe/api/search-jobs',
                         cookies=cookies, headers=headers, json=json_data, verify=False)
data = response.json()

job_data = []
for job_entry in data.get("results", []):
    job_info = job_entry.get("job_information", {})
    v5_data = job_entry.get("v5_processed_job_data", {})
    company_data = job_entry.get("v5_processed_company_data", {})

    job = {
        "title": job_info.get("title"),
        "core_job_title": v5_data.get("core_job_title"),
        "company_name": company_data.get("name"),
        "company_sector_and_industry": company_data.get("industries"),
        "company_website": company_data.get("website"),
        "language_requirements": v5_data.get("language_requirements"),
        "technical_tools": v5_data.get("technical_tools"),
        "yearly_min_compensation": v5_data.get("yearly_min_compensation"),
        "yearly_max_compensation": v5_data.get("yearly_max_compensation"),
        "workplace_countries": v5_data.get("workplace_countries"),
        "workplace_states": v5_data.get("workplace_states"),
        "workplace_cities": v5_data.get("workplace_cities"),
        "formatted_workplace_location": v5_data.get("formatted_workplace_location"),
        "apply_url": job_entry.get("apply_url"),
    }
    job_data.append(job)

# Get header from first entry if it exists
header = job_data[0].keys() if job_data else []

csv_file = "output.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    writer.writerows(job_data)

print("Data written to output.csv")
