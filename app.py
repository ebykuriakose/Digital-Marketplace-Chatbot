# app.py - Final Version (revised with fixed logic for all 21 test cases)
import streamlit as st
import pandas as pd
import io
import re  
from fpdf import FPDF
from fuzzywuzzy import fuzz

# Load enriched dashboard metadata
df = pd.read_csv("enriched_dashboard_data.csv")

# Example of full metadata extracted from PDFs (1 dashboard shown for brevity)
collibra_metadata = {
    "ED Exploratory Analysis": {
    "Metrics": {
        "Discharge Disposition to Departure": "https://mgb.collibra.com/asset/169fd83e-e223-4d31-a59b-1e5e8610a819",
        "ED Observation Unit Visits": "https://mgb.collibra.com/asset/623a36f9-919d-4ee6-b35d-099295c96082",
        "Arrival to Room": "https://mgb.collibra.com/asset/542fd8cd-6872-42df-b508-6b76fabbfcd8",
        "Arrival to First Provider": "https://mgb.collibra.com/asset/c72ba8b7-3b94-4fda-b645-7e05119fce25",
        "Median Boarder Hours Per Boarder": "https://mgb.collibra.com/asset/5a26d741-c3ad-4dc1-8c33-810e3a0f1f89",
        "Bed Request to Bed Assigned": "https://mgb.collibra.com/asset/4e3600af-f11f-4226-bec3-222bacffbcf4",
        "Triage Start to Triage End": "https://mgb.collibra.com/asset/b6d0c66a-4f8e-4dc6-b97d-907804f5e626",
        "Bed Ready to Off the Floor": "https://mgb.collibra.com/asset/792bfabc-123e-4dc0-b449-1ee8f516e974",
        "Short Stay Admissions": "https://mgb.collibra.com/asset/18221ad6-9186-41a0-b53c-023e87aee992",
        "Walkouts": "https://mgb.collibra.com/asset/1a722c3a-b8a4-4e1e-bfa7-22123e111b6f",
        "Provider to Disposition": "https://mgb.collibra.com/asset/6a4d1d2c-aaba-4a3a-ba09-f152cae6f616",
        "Hours Spent in Extreme Status": "https://mgb.collibra.com/asset/ee1b06be-9981-42b7-ab59-f78e9889d761",
        "Admissions": "https://mgb.collibra.com/asset/5c5d2df3-4882-4e9c-b4d4-8f10dee4115e",
        "Room to Provider": "https://mgb.collibra.com/asset/c76318ea-0a25-4dc8-a5f6-1b683008acc2",
        "Median Length of Stay - Discharged": "https://mgb.collibra.com/asset/dbc56682-95a2-48f1-979a-365a15b4f9e8",
        "Median Length of Stay - ED Observation": "https://mgb.collibra.com/asset/9a7c75fd-1dae-4f90-bddd-cccd14440da5",
        "Median Length of Stay - Admitted": "https://mgb.collibra.com/asset/d7a46533-20cf-4fa3-b1d4-34e87a075f47",
        "ED Visit Volume": "https://mgb.collibra.com/asset/31f6d445-b6ec-475e-8faf-a4158a0cb5b7",
        "Percent Seen By Provider Under 30 min": "https://mgb.collibra.com/asset/e5d8b350-20d9-4786-9e8d-f64123374ced",
        "Arrival to Triage Start": "https://mgb.collibra.com/asset/c8596b09-7e27-4c7f-b7ee-69fdc210fc90",
        "Transfers Out": "https://mgb.collibra.com/asset/27505b8a-27cf-4395-ac5a-21b60424575f",
        "Transfers In": "https://mgb.collibra.com/asset/d88fc4c0-b968-4586-b6ae-362e94bed1cd"
    },
    "Filters": {
        "Entity": "https://mgb.collibra.com/asset/67e988cf-2325-4204-9b76-73a5bb67d5c6",
        "Ethnicity": "https://mgb.collibra.com/asset/1435813f-30c0-472f-a4ea-778b742dfc17",
        "ED Population Type": "https://mgb.collibra.com/asset/3bcba938-7c71-44e8-a713-4a517c6c55cc",
        "Age Group": "https://mgb.collibra.com/asset/c90d84ce-b05c-44ea-8a8b-a004bb6ab8a2",
        "Destination": "https://mgb.collibra.com/asset/7043b685-14c5-4353-8231-73d62ff52365",
        "Admit Service": "https://mgb.collibra.com/asset/37ca897d-9cb6-4e86-afba-4e1d4c25d828",
        "Language": "https://mgb.collibra.com/asset/e02e664c-6951-40ac-92fe-93660d6f22ea",
        "Arrival Type": "https://mgb.collibra.com/asset/7b601008-643f-42de-a6b7-c0fe753b5315",
        "Patient Race": "https://mgb.collibra.com/asset/55a1c627-ed5d-44c5-8561-09cbd98642ac",
        "ED Observation": "https://mgb.collibra.com/asset/b3f41805-3eca-4ab9-b243-0bec9b8dd80c"
    },
   "Business Terms": {
        "ED Boarder": "https://mgb.collibra.com/asset/f1c78a38-1fa3-40af-ae04-4c603e1f6e98",
        "Destination": "https://mgb.collibra.com/asset/f9357476-8eba-4d34-bc81-29099748f5be",
        "ED Observation": "https://mgb.collibra.com/asset/bfb94425-1ea0-4586-8561-4e98bc5747d0",
        "Ethnicity": "https://mgb.collibra.com/asset/c88226a1-495c-45cc-8320-d51985f92eae",
        "Language": "https://mgb.collibra.com/asset/4bbc6bda-d343-43ad-ae38-8791e5914c8e",
        "Population Type": "https://mgb.collibra.com/asset/61ea1dd8-4c34-4c40-8621-80cac27140e1",
        "Admit Service": "https://mgb.collibra.com/asset/dd46843d-bfdb-4883-ae23-297f5df21f70",
        "Race": "https://mgb.collibra.com/asset/d24f66f3-5e9e-4c40-83dd-5b3167e9ebea",
        "Age": "https://mgb.collibra.com/asset/2048e3fa-2836-45ac-994b-51cbd2a0eb31"
    },
    "Owner": "Rob Forsberg",
    "Product Owner": "Abbot Cooper",
    "Refresh Frequency": "Mondays at 8 AM",
    "Data Source": "Snowflake > EDW_PRODUCT_ZONE.EAM.ED_SUMMARY",
    "Data Through": "The data is through the Saturday of the previous week",
    "Inclusion Criteria": "Department Level of Care Grouper = Emergency",
    "Exclusion Criteria": "Test Patients, Discharges from procedural departments like PeriOps, Cath, Endo, IR, and short stay admissions",
    "Dashboard URL": "https://daotableau.partners.org/#/views/EDExploratoryAnalysis/EDExploratoryAnalysis",
    "Access Request URL": "https://partnershealthcare.service-now.com/isservicehub/?id=sc_cat_item&sys_id=be24c431db4d805092a580c74b96196d",
    "Description": "Provides an overview into key ED metrics across MGB to improve performance on outcome metrics, share best practices, reduce avoidable admissions, and manage capacity escalations."
    },
    "Ambulatory Exploratory Analysis": {
    "Metrics": {
        "Ambulatory Sessions Population": "https://mgb.collibra.com/asset/0a2da15a-0f55-4dce-b95b-3127fb3f5db7",
        "Ambulatory Visits Population": "https://mgb.collibra.com/asset/ea8ed3cd-9853-4524-b84f-72153d0c19ed",
        "Average New Patient Lag": "https://mgb.collibra.com/asset/01ca8a9a-8bf2-4676-a8f7-a57e8954364f",
        "Count and Percent of Seen Same Day Visits (Completed)": "https://mgb.collibra.com/asset/244ccf08-0d3b-499d-b358-44b6945f6f4d",
        "Established Patient Volume": "https://mgb.collibra.com/asset/fc5c2766-aca2-46ba-8abf-b9ec7ff92687",
        "Institution Cancellation Rate": "https://mgb.collibra.com/asset/4a63beb1-6127-4584-bd04-addc29ffe3c2",
        "Institution Cancellation Volume": "https://mgb.collibra.com/asset/7baf0edc-3d0d-4903-b6c8-17d59294740d",
        "New Patient Volume": "https://mgb.collibra.com/asset/17591f3d-65a8-4e8a-89b8-eefebeb3c918",
        "No Show Visit Volume": "https://mgb.collibra.com/asset/0351f63d-1511-45c0-a397-21bedfcb04e4",
        "Patient Initiated Cancellation Rate": "https://mgb.collibra.com/asset/51c9d678-c2d0-4080-b5a9-265d5d58ff32",
        "Patient Initiated Cancellation Volume": "https://mgb.collibra.com/asset/65a2b948-a3ef-430f-b948-7b651a538eac",
        "Percent 4 Hour Sessions": "https://mgb.collibra.com/asset/c36d88e0-34e1-46a8-891c-a9f62e428ec5",
        "Percent Churn": "https://mgb.collibra.com/asset/1ad1f46e-4ea7-44a2-a73c-2ce1c6d78886",
        "Percent No Show": "https://mgb.collibra.com/asset/9d10fc5b-0555-4b98-b687-8cb8570bc2f2",
        "Percent of New Appointments Booked within 14 Days": "https://mgb.collibra.com/asset/36452516-26ca-4df2-b892-5655db679a2f",
        "Percent of New Patient Visits": "https://mgb.collibra.com/asset/e4cbd528-7f45-43a4-afb2-ad3a499b8b97",
        "Provider Initiated Cancellation Rate": "https://mgb.collibra.com/asset/2cc29a94-8f73-445c-a522-f28bf84a8b47",
        "Provider Initiated Cancellation Volume": "https://mgb.collibra.com/asset/7990c29f-e4a8-46f4-a898-bcdcc890928f",
        "Total Visit Volume": "https://mgb.collibra.com/asset/4ec26885-762b-4565-8bf4-9b86df34e169"
    },
    "Filters": {
        "Clinical Service": "https://mgb.collibra.com/asset/9ff0f9e1-37f1-4f33-97fb-c47fefc1abb8",
        "DEP Name": "https://mgb.collibra.com/asset/8970ee9c-546f-4698-97e6-844e27a9b0fc",
        "Division": "https://mgb.collibra.com/asset/d699a234-5dec-440f-91ee-e087e4cb5bdc",
        "Entity": "https://mgb.collibra.com/asset/eb0493aa-6f5f-4139-87b9-a7975729b8da",
        "New/Established": "https://mgb.collibra.com/asset/05fa4da4-e0e4-4374-b12e-607420b6b79b",
        "Practice": "https://mgb.collibra.com/asset/8cbacb63-fb96-4c82-9c91-3a7c171aa122",
        "Provider": "https://mgb.collibra.com/asset/0a2da15a-0f55-4dce-b95b-3127fb3f5db7",
        "Provider Type": "https://mgb.collibra.com/asset/ea8ed3cd-9853-4524-b84f-72153d0c19ed",
        "Resource Type": "https://mgb.collibra.com/asset/01ca8a9a-8bf2-4676-a8f7-a57e8954364f",
        "Revenue Location": "https://mgb.collibra.com/asset/244ccf08-0d3b-499d-b358-44b6945f6f4d",
        "Visit Method": "https://mgb.collibra.com/asset/fc5c2766-aca2-46ba-8abf-b9ec7ff92687"
    },
    "Business Terms": {
        "Established Patient": "https://mgb.collibra.com/asset/4a63beb1-6127-4584-bd04-addc29ffe3c2",
        "Location": "https://mgb.collibra.com/asset/4a63beb1-6127-4584-bd04-addc29ffe3c2",
        "New Patient Visit": "https://mgb.collibra.com/asset/36452516-26ca-4df2-b892-5655db679a2f",
        "Session": "https://mgb.collibra.com/asset/e4cbd528-7f45-43a4-afb2-ad3a499b8b97",
        "Visit Method": "https://mgb.collibra.com/asset/2cc29a94-8f73-445c-a522-f28bf84a8b47"
    },
    "Owner": "Renee Sidman",
    "Product Owner": "Savanna Murray",
    "Refresh Frequency": "Mondays at 8AM",
    "Data Source": "EDW_PRODUCT_ZONE.EAM.AMBULATORY_SUMMARY",
    "Data Through": "End of the previous week",
    "Inclusion Criteria": "Departments are Ambulatory with ReportGrouper10CD of Outpatient or Hospital Outpatient, LevelOfCare Grouper is NULL, Specialty is not Urgent Care, and part of MGB Service Area 10. Visit has an encounter date or appointment creation date between the start date and today. Session has a slot start date between the start date and today. Uses Curated.HospitalParentLocationDim.HospitalParentLocationName. If HospitalParentLocationAbbreviation is BWH or BWF then assigned as 'BHParent'. If DepartmentEpicId is one of the iCare departments, then assigned 'Mass General Brigham Integrated Care Parent' using Caboodle.VisitFact.DepartmentEpicId joined to Curated.DepartmentHierarchyFact where IsCurrent = 1. iCare Departments include: CP PC BURLINGTON [10180280001], CP BH BURLINGTON [10180280002], CP BH WATERTOWN [10180290001], CP PC WATERTOWN [10180290002], CP BH WESTWOOD [10180390001].",
    "Exclusion Criteria": "Encounter Type of Erroneous Encounter, or has no Visit Type; test patients excluded.",
    "Dashboard URL": "https://daotableau.partners.org/#/views/AmbulatoryExploratoryAnalysis/AmbulatoryExploratoryAnalysis",
    "Access Request URL": "https://partnershealthcare.service-now.com/isservicehub/?id=sc_cat_item&sys_id=be24c431db4d805092a580c74b96196d",
    "Description": "The Enterprise Asset Management (EAM) Ambulatory Exploratory Analysis dashboard provides an overview and insight into key performance metrics across MGB as determined by the EAM Ambulatory domain. This report will provide insights into measuring volume across the enterprise to better manage Ambulatory capacity and utilization."
    },
    "Access Center Exploratory Analysis": {
    "Metrics": {
        "Number of Completed Transfer Requests": "https://mgb.collibra.com/asset/f9f6595f-e5da-4b96-8b94-9e7286e3385a",
        "Number of Canceled Transfer Requests": "https://mgb.collibra.com/asset/1f3a6da4-26f5-4c7f-ba31-8a94fc9ec984",
        "Number of Reasons for Canceled Transfer Requests": "https://mgb.collibra.com/asset/0933e8c7-e4c7-4929-86a7-ccd6f9cfb29b",
        "Number of Transfer Requests": "https://mgb.collibra.com/asset/99ba388e-7cd4-4f4a-8efc-f176b353dd80",
        "Number of Declined Transfer Requests": "https://mgb.collibra.com/asset/e0234d11-fc23-475b-a752-b5f84974ead5",
        "Number of Reasons for Declined Transfer Requests": "https://mgb.collibra.com/asset/93d08ae5-6b70-4a67-a37c-332e2c6574c7"
    },
    "Filters": {
        "Hospital System": "https://mgb.collibra.com/asset/11750970-d834-4e8a-9147-ddbfda344593",
        "Transfer Center Region": "https://mgb.collibra.com/asset/1126a115-1a4d-4a9b-8478-af3b02e4a8ac",
        "Request Status": "https://mgb.collibra.com/asset/ad8035f1-2002-4897-b9e8-1c48c91d26d7",
        "Accepting Hospital": "https://mgb.collibra.com/asset/ec81b34a-1703-40c8-8f20-a967dc4a8c74",
        "Redirect Description": "https://mgb.collibra.com/asset/65ba6bc6-8b4d-41ed-baa7-f5d704074292",
        "Request Type": "https://mgb.collibra.com/asset/fbfe89a8-5169-46ff-8951-f95b73ca5aa2",
        "Clinical Service": "https://mgb.collibra.com/asset/f12e03ca-d4a7-47e0-93f9-f33061221fe6",
        "Level of Care": "https://mgb.collibra.com/asset/95b23953-105c-4c8a-870e-8bbb2d49959e",
        "Referring Hospital": "https://mgb.collibra.com/asset/3cabd181-db28-4ae7-9d0b-78e31058f65b",
        "Request Date": "https://mgb.collibra.com/asset/3cb5a00f-b73b-49ad-a196-f3a5911a40d0",
        "Date": "https://mgb.collibra.com/asset/7e718fff-3517-44cd-9cf2-98e067db43c0",
        "Transfer Type": "https://mgb.collibra.com/asset/9f6ecc56-2283-4c96-b9be-db0a3682e93d"
    },
    "Business Terms": {
        "Completed": "https://mgb.collibra.com/asset/365d2373-6110-4bb6-860f-4e8f34101cf8",
        "Canceled": "https://mgb.collibra.com/asset/3a47e398-519f-4550-ac65-3897b12bfb45",
        "Referring Hospital": "https://mgb.collibra.com/asset/738102a2-16b0-4bc1-a665-39b2d69eddaf",
        "Transfer Center Region": "https://mgb.collibra.com/asset/f2963063-717d-4a99-a390-77699bf11719",
        "Completion Rate": "https://mgb.collibra.com/asset/9e5911cf-46cc-4b57-9ce9-5f6565999925",
        "Transfer Incoming": "https://mgb.collibra.com/asset/2fd22295-2171-40f7-971e-85f8529a0485",
        "Transfer Pathway": "https://mgb.collibra.com/asset/1f3fcb9f-b7fe-4ac3-965d-f83cc3e695f5",
        "Redirected": "https://mgb.collibra.com/asset/7ef84bfb-1d49-4ff5-86bb-ff0f45f54262",
        "Direct Admits": "https://mgb.collibra.com/asset/11750970-d834-4e8a-9147-ddbfda344593",
        "Declined": "https://mgb.collibra.com/asset/1126a115-1a4d-4a9b-8478-af3b02e4a8ac",
        "Primary Destination Record": "https://mgb.collibra.com/asset/93d08ae5-6b70-4a67-a37c-332e2c6574c7"
    },
    "Owner": "Rob Forsberg",
    "Product Owner": "James McDonald",
    "Refresh Frequency": "Mondays at 8 AM",
    "Data Through": "End of the Prior Week",
    "Data Source": "\"EDW_PRODUCT_ZONE\".\"EAM\".\"ACCESS_CENTER_AGGREGATE\"",
    "Inclusion Criteria": "All records available in the ACCESS_CENTER_AGGREGATE reporting view.",
    "Exclusion Criteria": "Excluding Transfer Request Statuses: Pending, Accepted",
    "Dashboard URL": "https://daotableau.partners.org/#/views/AccessCenterExploratoryAnalysis/AccessCenterExploratoryAnalysis",
    "Access Request URL": "https://partnershealthcare.service-now.com/isservicehub/?id=sc_cat_item&sys_id=be24c431db4d805092a580c74b96196d",
    "Description": "Used by entities with Epic’s Transfer Center to monitor transfer requests, cancellations, declines, and clinical service transfers."
    }
}


synonym_map = {
    "los": "length of stay",
    "length of stay": "length of stay",
    "eam": "enterprise asset management",
    "ed": "emergency department",
    "er": "emergency department",
    "ip": "inpatient",
    "op": "outpatient",
    "uc": "urgent care",
    "no show": "no show visit volume",
    "appt": "appointment",
    "obs": "ed observation",
    "lag": "average new patient lag",
    "pc": "primary care",
    "bh": "behavioral health",
    "cancel": "cancellation",
    "dx": "diagnosis",
    "tx": "treatment"
}

# Glossary definitions for intelligent Q&A
glossary = {
    "enterprise asset management": (
        "Enterprise Asset Management (EAM) refers to the processes and tools used to manage, monitor, "
        "and optimize the performance, utilization, and value of healthcare operational assets—like personnel, "
        "equipment, and data systems—across the MGB health system."
    ),
    "ed exploratory analysis": (
        "The ED Exploratory Analysis dashboard provides insight into emergency department throughput, "
        "transfers, and key operational KPIs like boarding time and length of stay."
    ),
    "access center exploratory analysis": (
        "The Access Center Exploratory Analysis dashboard monitors MGB Transfer Center activities, including "
        "completed, canceled, and declined transfer requests, as well as service-specific transfer metrics."
    ),
    "ambulatory exploratory analysis": (
        "The Ambulatory Exploratory Analysis dashboard analyzes visit volume, scheduling patterns, and provider "
        "utilization to optimize ambulatory care capacity and access across the enterprise."
    ),
    "slicer dicer": (
        "Slicer Dicer is Epic’s self-service reporting tool that allows clinical and operational users to explore data, "
        "identify trends, and answer questions without requiring SQL or formal report builds."
    ),
    "length of stay": (
        "Length of Stay (LOS) measures how long a patient remains in care from admission to discharge."
    )
}

def render_links(d):
    return "\n".join(f"- [{k}]({v})" for k, v in d.items())

from fuzzywuzzy import fuzz

def fuzzy_match(q):
    q_clean = re.sub(r"[-_/]", " ", q.lower())
    q_clean = re.sub(r"\s+", " ", q_clean).strip()

    # 1. Try regex-based Dashboard Group phrase extraction
    group_patterns = [
        r"(?:in|under|from|part of)\s+(?:the\s+)?([a-z\s]+?)(?:\s+group)?$",
        r"(?:in|under|from|part of)\s+(?:the\s+)?([a-z\s]+?)(?:\s+dashboards)?$"
    ]
    for pattern in group_patterns:
        match = re.search(pattern, q_clean)
        if match:
            possible_group = match.group(1).strip()
            # Use fuzzywuzzy to find best matching group name
            best_match = None
            best_score = 0
            for group in df["Dashboard Group"].dropna().unique():
                score = fuzz.token_set_ratio(possible_group, group.lower())
                if score > best_score and score >= 85:
                    best_match = group
                    best_score = score
            if best_match:
                return df[df["Dashboard Group"].str.lower() == best_match.lower()]

    # 2. Fall back to token-by-token match (broader)
    tokens = q_clean.split()
    combined = pd.DataFrame()
    for token in tokens:
        match = pd.concat([
            df[df['Dashboard Name'].str.lower().str.contains(token, na=False)],
            df[df['Dashboard Group'].str.lower().str.contains(token, na=False)],
            df[df['Dashboard Launch Page'].str.lower().str.contains(token, na=False)]
        ])
        combined = pd.concat([combined, match])
    return combined.drop_duplicates('Dashboard Name')

def find_dashboards_by_person(tokens):
    matches = []
    for name, meta in collibra_metadata.items():
        owner_fields = " ".join([
            str(meta.get("Owner", "")).lower(),
            str(meta.get("Product Owner", "")).lower(),
            str(meta.get("Product Owns", "")).lower()
        ])
        if any(fuzz.partial_ratio(t, owner_fields) >= 85 for t in tokens):
            row = df[df["Dashboard Name"] == name]
            if not row.empty:
                matches.append(row.iloc[0])
    return pd.DataFrame(matches)

def search_metadata_for_term(term):
    results = []
    for dash_name, meta in collibra_metadata.items():
        matches = {}
        for section in ["Metrics", "Filters", "Business Terms"]:
            for key, link in meta.get(section, {}).items():
                if term.lower() in key.lower():
                    matches.setdefault(section, []).append((key, link))
        if matches:
            results.append({
                "Dashboard Name": dash_name,
                "Dashboard URL": meta.get("Dashboard URL"),
                "Collibra Link": meta.get("Access Request URL"),
                "Matches": matches
            })
    return results

#UI
st.title("📊 Digital Marketplace Chatbot")
query = st.text_input("Ask your dashboard or metadata question:")

# Launch Page filter
#dropdown = st.sidebar.selectbox("Filter by Launch Page", ["All"] + sorted(df["Dashboard Launch Page"].dropna().unique()))
#if dropdown != "All":
#    df = df[df["Dashboard Launch Page"] == dropdown]

# Show dashboards immediately when dropdown is used and query box is empty
#if not query.strip():
#    st.markdown(f"### Dashboards in Launch Page: {dropdown}" if dropdown != "All" else "### All Dashboards")
#    for grp in sorted(df["Dashboard Group"].dropna().unique()):
#        st.markdown(f"#### {grp}")
#        for _, r in df[df["Dashboard Group"] == grp].iterrows():
#            st.markdown(f"- [{r['Dashboard Name']}]({r['Dashboard Link']})" + (
#                f" 📄 [Docs]({r['Collibra Link']})" if pd.notna(r['Collibra Link']) else ""))

# Download buttons
#excel_io = io.BytesIO()
#df.to_excel(excel_io, index=False, engine="openpyxl")
#excel_io.seek(0)
#st.download_button("📥 Excel", data=excel_io, file_name="dashboards.xlsx")

#pdf = FPDF()
#pdf.add_page()
#pdf.set_font("Arial", size=12)
#for _, r in df.iterrows():
#    pdf.cell(200, 10, txt=r["Dashboard Name"], ln=True)
#pdf_out = pdf.output(dest="S").encode("latin-1")
#st.download_button("📄 PDF", data=pdf_out, file_name="dashboards.pdf")

# --- Extract known people for person lookup ---
known_people = set()
for meta in collibra_metadata.values():
    for field in ["Owner", "Product Owner", "Owns"]:
        val = meta.get(field)
        if val:
            full = val.lower()
            known_people.add(full)
            known_people.update(full.split())  # Add first and last name separately

# Handle query
if query:
    original_q = query.lower()
    original_q = re.sub(r"[-_/]", " ", original_q)
    original_q = re.sub(r"\s+", " ", original_q).strip()

    # Step 1: Check glossary BEFORE any synonym replacement
    matched_glossary = None
    for term, definition in glossary.items():
        if term in original_q:
            matched_glossary = (term, definition)
            break
        elif any(original_q.startswith(x) and term in original_q for x in ["what is", "define", "tell me about"]):
            matched_glossary = (term, definition)
            break

    # Step 1b: If no glossary match yet, re-check after synonym replacement
    q = original_q
    for syn, canonical in synonym_map.items():
        q = re.sub(rf"\b{re.escape(syn)}\b", canonical.lower(), q)

    if matched_glossary is None:
        for term, definition in glossary.items():
            if term in q:
                matched_glossary = (term, definition)
                break

    # Step 2: Apply synonym replacements AFTER glossary check
    q = original_q
    for syn, canonical in synonym_map.items():
        q = re.sub(rf"\b{re.escape(syn)}\b", canonical.lower(), q)

    tokens = [re.sub(r"[^\w\s]", "", t) for t in q.split()]
    token_set = set(tokens)

    # Step 3: Intent Detection
    intent = {
        "dashboard_lookup": any(phrase in q for phrase in [
            "what dashboards", "show dashboards", "list dashboards", "part of", "under", "in", "group", "launch page"
        ]),
        "metadata_request": any(term in q for term in [
            "metric", "filter", "business term", "refresh", "data source", "inclusion", "exclusion", "description", "url", "link"
        ]),
        "person_lookup": (
            any(phrase in q for phrase in [
                "who owns", "owned by", "managed by", "product owner", "owner of",
                "as owner", "as product owner", "owns", "manages", "that have", "that has"
            ]) or any(p in token_set for p in known_people)
        ),
        "glossary_lookup": matched_glossary is not None,
    }
    intent["fallback"] = not any(intent.values())

    # Step 4: Render glossary if matched and no conflict with other intents
    if intent["glossary_lookup"] and not (intent["metadata_request"] or intent["person_lookup"]):
        st.markdown(f"**{matched_glossary[0].title()}:** {matched_glossary[1]}")
        st.markdown("---")

    # --- Handle Metadata Request ---
    if intent["metadata_request"]:
        direct_match = None
        best_score = 0
        for dash_name in collibra_metadata:
            score = fuzz.token_set_ratio(q, dash_name.lower())
            if score > best_score and score >= 90:
                direct_match = dash_name
                best_score = score

        def render_metadata_block(meta, q):
            if "metric" in q:
                st.markdown("**Metrics:**")
                st.markdown(render_links(meta.get("Metrics", {})))
            elif "filter" in q:
                st.markdown("**Filters:**")
                st.markdown(render_links(meta.get("Filters", {})))
            elif "term" in q or "business" in q:
                st.markdown("**Business Terms:**")
                st.markdown(render_links(meta.get("Business Terms", {})))
            elif "refresh" in q:
                st.markdown(f"**Refresh Frequency:** {meta.get('Refresh Frequency', 'N/A')}")
            elif "description" in q:
                st.markdown(f"**Description:** {meta.get('Description', 'N/A')}")
            elif "source" in q:
                st.markdown(f"**Data Source:** {meta.get('Data Source', 'N/A')}")
            elif "inclusion" in q:
                st.markdown(f"**Inclusion Criteria:** {meta.get('Inclusion Criteria', 'N/A')}")
            elif "exclusion" in q:
                st.markdown(f"**Exclusion Criteria:** {meta.get('Exclusion Criteria', 'N/A')}")
            elif "product owner" in q:
                st.markdown(f"**Product Owner:** {meta.get('Product Owner', 'N/A')}")
            elif "owner" in q:
                st.markdown(f"**Owner:** {meta.get('Owner', 'N/A')}")
            elif "access" in q:
                access_url = meta.get("Access Request URL")
                if access_url:
                    st.markdown(f"**Access Request URL:** [{access_url}]({access_url})")
                else:
                    st.markdown("_No Access Request URL found in documentation._")
            elif "dashboard url" in q or "dashboard link" in q:
                dash_url = meta.get("Dashboard URL")
                if dash_url:
                    st.markdown(f"**Dashboard URL:** [{dash_url}]({dash_url})")
                else:
                    st.markdown("_No Dashboard URL found in documentation._")
            st.markdown("---")

        if direct_match:
            meta = collibra_metadata[direct_match]
            st.markdown(f"### {direct_match}")
            render_metadata_block(meta, q)
        else:
            # NEW LOGIC: Try fuzzy match on Dashboard Group if Dashboard Name match fails
            matched_group = None
            best_score = 0
            for group in df["Dashboard Group"].dropna().unique():
                score = fuzz.partial_ratio(group.lower(), q)
                if score > best_score and score >= 85:
                    matched_group = group
                    best_score = score

            if matched_group:
                dashboards_in_group = df[df["Dashboard Group"].str.lower() == matched_group.lower()]
                if dashboards_in_group.empty:
                    st.warning("No dashboards found under that group.")
                else:
                    for _, row in dashboards_in_group.iterrows():
                        dash_name = row["Dashboard Name"]
                        meta = collibra_metadata.get(dash_name, {})
                        st.markdown(f"### {dash_name}")
                        render_metadata_block(meta, q)
            else:
                st.warning("No dashboards matched your metadata request.")

    # --- Handle Person-Based Lookup ---
    elif intent["person_lookup"]:
        # Try to match dashboard name first
        matched_dash = None
        best_score = 0
        for dash_name in collibra_metadata:
            score = fuzz.token_set_ratio(q, dash_name.lower())
            if score > best_score and score >= 85:
                matched_dash = dash_name
                best_score = score

        if matched_dash:
            meta = collibra_metadata[matched_dash]
            st.markdown(f"**Dashboard:** {matched_dash}")
            st.markdown(f"**Product Owner:** {meta.get('Product Owner', 'N/A')}")
            st.markdown(f"**Owner:** {meta.get('Owner', 'N/A')}")
        else:
            # Fallback to name-based match
            people_df = find_dashboards_by_person(token_set)
            if not people_df.empty:
                st.markdown("**Dashboards owned by person:**")
                for grp in sorted(people_df["Dashboard Group"].dropna().unique()):
                    st.markdown(f"#### {grp}")
                    for _, r in people_df[people_df["Dashboard Group"] == grp].iterrows():
                        st.markdown(f"- [{r['Dashboard Name']}]({r['Dashboard Link']})" + (
                            f" 📄 [Docs]({r['Collibra Link']})" if pd.notna(r['Collibra Link']) else ""))
            else:
                st.warning("No dashboards found for that person.")
                st.warning("No dashboards found for that person.")

    # --- Handle Dashboard Lookup ---
    elif intent["dashboard_lookup"]:
        fallback = fuzzy_match(q)
        if not fallback.empty:
            st.markdown(f"**Dashboards matching '{query}':**")
            for grp in sorted(fallback["Dashboard Group"].dropna().unique()):
                st.markdown(f"#### {grp}")
                for _, r in fallback[fallback["Dashboard Group"] == grp].iterrows():
                    st.markdown(f"- [{r['Dashboard Name']}]({r['Dashboard Link']})" + (
                        f" 📄 [Docs]({r['Collibra Link']})" if pd.notna(r['Collibra Link']) else ""))
        else:
            st.warning("No dashboards found for that group.")

    # --- Handle Glossary Intent Only (already rendered above) ---
    elif intent["glossary_lookup"]:
        pass  # glossary already rendered above

    # --- Fallback to Metadata Search ---
    elif intent["fallback"]:
        # Step 1: Try to identify dashboard group from query
        matched_group = None
        for group in df["Dashboard Group"].dropna().unique():
            if group.lower() in q:
                matched_group = group
                break

        if matched_group:
            dashboards_in_group = df[df["Dashboard Group"] == matched_group]
            if dashboards_in_group.empty:
                st.warning("No dashboards found under that group.")
            else:
                st.markdown(f"### Dashboards in '{matched_group}' Group")

                for _, row in dashboards_in_group.iterrows():
                    dash_name = row["Dashboard Name"]
                    dash_url = row["Dashboard Link"]
                    doc_url = row["Collibra Link"]
                    st.markdown(f"**[{dash_name}]({dash_url})**" + (f" 📄 [Docs]({doc_url})" if pd.notna(doc_url) else ""))

                    meta = collibra_metadata.get(dash_name, {})
                    if not meta:
                        continue

                    if "metric" in q:
                        section = meta.get("Metrics", {})
                        label = "Metrics"
                    elif "filter" in q:
                        section = meta.get("Filters", {})
                        label = "Filters"
                    elif "term" in q or "business" in q:
                        section = meta.get("Business Terms", {})
                        label = "Business Terms"
                    else:
                        section = {}
                        label = None

                    if label and section:
                        st.markdown(f"**{label}:**")
                        st.markdown(render_links(section))
                    elif label:
                        st.markdown(f"_No {label.lower()} found in documentation._")

        else:
            # Step 2: Fallback to token-based metadata term search
            known_metadata_terms = set()
            for dash in collibra_metadata.values():
                for section in ["Metrics", "Filters", "Business Terms"]:
                    known_metadata_terms.update(map(str.lower, dash.get(section, {}).keys()))

            matched_terms = [
                term for term in known_metadata_terms
                if re.search(rf"\b{re.escape(term)}\b", q) or any(token in term for token in token_set)
            ]

            metadata_hits = []
            shown_dashboards = set()
            for term in matched_terms:
                hits = search_metadata_for_term(term)
                for hit in hits:
                    if hit["Dashboard Name"] not in shown_dashboards:
                        metadata_hits.append(hit)
                        shown_dashboards.add(hit["Dashboard Name"])

            if metadata_hits:
                st.markdown(f"**Dashboards with metadata related to: {', '.join(matched_terms)}**")

                dash_df = df.set_index("Dashboard Name")
                grouped = {}
                for hit in metadata_hits:
                    group = dash_df.loc[hit["Dashboard Name"], "Dashboard Group"] if hit["Dashboard Name"] in dash_df.index else "Other"
                    grouped.setdefault(group, []).append(hit)

                for group in sorted(grouped.keys()):
                    st.markdown(f"#### {group}")
                    for hit in grouped[group]:
                        st.markdown(f"**[{hit['Dashboard Name']}]({hit['Dashboard URL']})**")
                        for section, items in hit["Matches"].items():
                            st.markdown(f"**{section}:**")
                            for name, link in items:
                                st.markdown(f"- [{name}]({link})")
            else:
                st.warning("No relevant matches found.")
