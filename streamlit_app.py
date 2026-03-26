####### IMPORTS
import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import datetime
from io import BytesIO


######## Generate lists to be used for drop downs later
Estimate_Types = ["Limestone","Paving Overlay","Aprons","Ditching","Milling","Shoulders","Spot Repair","Mowing"]
Townships = ["Argentine Township","Atlas Township","Clayton Township","Davison Township","Fenton Township",
             "Flint Township","Flushing Township","Forest Township","Gaines Township","Genesee Township",
             "Grand Blanc Township","Montrose Township","Mt. Morris Township","Mundy Township",
             "Richfield Township","Thetford Township","Vienna Township"]
Districts = ["Atlas","Linden","Metro","Montrose","Otisville","Swartz Creek"]
PaymentMethod_List = ["GCRC/Township","100% Township","CBDG","Neighborhood Funds"]


######### Equipment lists based on the Estimate types (maybe should be a dicitonary at some point)
Equipment_List = ["Limestone_Resurfacing_Equipment","Paving_Overlay_Equipment","Aprons_Equipment","Ditching_Equipment",
                  "Milling_Equipment","Shoulders_Equipment","Spot_Repair_Equipment","Mowing_Equipment"]


Limestone_Resurfacing_Equipment = ["Grader W/ Radio","Pickup W/ Radio","Tandem W/Tank","Walk-N-Roller"]

Paving_Overlay_Equipment = ["Trailer","Bobcat","Mill Head","Broom","Pickup W/ Radio","Swap Loader","Low Boy Tractor",
                             "Trailer","Asphalt Dis. Truck","Asphalt Paver","Water Tank","Crew Cab",
                             "Trailer","Asphalt Roller","Swap Loader"]

Aprons_Equipment = ["Pickup W/ Radio","Utility Truck","Tractor","Trailer","Asphalt Paver","Asphault Dis Truck",
                    "Swap Loader","Trailer","Water Tank","Asphalt Roller","Bobcat","Mill Head","Broom","Bucket",
                    "Pickup W/ Radio","Single Axle", "Trailer"]

Ditching_Equipment = ["Gradall W/ Radio","Tandem Truck W/ Radio","Tri Axle Truck W/ Radio",
                      "Pickup Truck W/ Radio","Laser"]

Milling_Equipment = ["Tri-Axle Dump Truck W/ Radio","Trailer","Bobcat","Mill Head","Broom","Pickup W/ Radio",
                     "Swap Loader"]

Shoulders_Equipment = ["Shoulder Machine","Roller","Tandem Truck","Pickup Truck","1-Ton Truck"]

Spot_Repair_Equipment = ["Gradall","Tandem Truck","Single Axle","Trailer","Roller","Road Grader"]

Mowing_Equipment = ["Arm Mower"]

### Link Equipment to jobs

job_equipment_map = {
    "Limestone": Limestone_Resurfacing_Equipment,
    "Paving Overlay": Paving_Overlay_Equipment,
    "Aprons": Aprons_Equipment,
    "Ditching": Ditching_Equipment,
    "Milling": Milling_Equipment,
    "Shoulders": Shoulders_Equipment,
    "Spot Repair": Spot_Repair_Equipment,
    "Mowing": Mowing_Equipment
}

### Create definition for variable equipment options

def build_equipment_df(equipment_list):
    return pd.DataFrame({
        "Equipment": equipment_list,
        "Quantity": [None] * len(equipment_list),
        "Hours": [None] * len(equipment_list),
        "Equipment Number": [""] * len(equipment_list)
    })

##### General Inputs for all sheets

st.title("Road Estimate Generator")

Estimate = st.selectbox("Type of Job", Estimate_Types)

Name = st.text_input("Name")

Date = st.date_input("Date")

district = st.selectbox("District", Districts)

township = st.selectbox("Township", Townships)

paymentmethod = st.selectbox("Payment Method",PaymentMethod_List)

road = st.text_input("Road Name")

road_limits = st.text_input ("Road Limits (Ex. Bristol to Maple)")

comments = st.text_input("Comments")

######## Dimensions inputs

st.header("Dimensions")

Dimcol1, Dimcol2, Dimcol3 = st.columns(3)

with Dimcol1:
    Dimensions_length = st.number_input("Length (Feet)", step=10)

with Dimcol2:
    Dimensions_width = st.number_input("Width (Feet)", step=1)

with Dimcol3:
    Dimensions_depth = st.number_input("Depth (Inches)", step=1)

########## Labor Inputs

st.header("Labor")

DaysWorked = st.number_input("Number of Days Worked", step=1)

st.subheader("Regular Hours")

Regcol1, Regcol2 = st.columns(2)

with Regcol1:
    ROperatorCount = st.number_input("Number of Operators - Regular", step=1)
    RForemanCount = st.number_input("Number of Foreman - Regular", step=1)

with Regcol2:
    RoperatorHours = st.number_input("Operator Hours - Regular", step=1)
    RForemanHours = st.number_input("Foreman Hours - Regular", step=1)





st.subheader("Overtime Hours")

OTcol1, OTcol2 = st.columns(2)

with OTcol1:
    OTOperatorCount = st.number_input("Number of Operators - OT", step=1)
    OTForemanCount = st.number_input("Number of Foreman - OT", step=1)

with OTcol2:
    OTOperatorHours = st.number_input("Operator Hours - OT", step=1)
    OTFormeanHours = st.number_input("Foreman Hours - OT", step=1)



#### Dust Control Inputs


st.header("Dust Control")

DCcol1, DCcol2 = st.columns(2)

with DCcol1:
    gallons = st.number_input("Gallons", step=1)

with DCcol2:
    deliveries = st.number_input("Deliveries", step=1)




###### Notes inputs

st.header("Notes")

notes = st.text_input("Notes")


###### Equipment Inputs


# old attempt at equipment

# st.header("Equipment")

# EQcol1, EQcol2, EQcol3, EQcol4 = st.columns(4)

# with EQcol1:
#     st.subheader("Equipment Name/Description")
# #    for i in Estimate_Types:
# #        if i == Estimate:
# #            for j in Equipment_List:
# #                if j == Estimate:

# with EQcol2:
#     st.subheader("Quantity Used")

# with EQcol3:
#     st.subheader("Hours of Use")

# with EQcol4:
#     st.subheader("Equipment Number")

### Chat GPT assisted varying length equipment table

st.header("Equipment")

# Get default equipment based on selected job
default_equipment = job_equipment_map.get(Estimate, [])

# Initialize session state
if "equipment_df" not in st.session_state:
    st.session_state.equipment_df = build_equipment_df(default_equipment)
    st.session_state.last_estimate = Estimate

# Reset table when job type changes
if Estimate != st.session_state.last_estimate:
    st.session_state.equipment_df = build_equipment_df(default_equipment)
    st.session_state.last_estimate = Estimate

# Editable table
edited_equipment = st.data_editor(
    st.session_state.equipment_df,
    num_rows="dynamic",   #allows adding new equipment
    use_container_width=True
)







############ GENERATE EXCEL

st.divider()

### Load Workbook

timestamp = datetime.datetime.now().strftime("%Y%m%d")

title_road = road.replace(" ", "_").replace("/", "")

filename = f"{title_road}_{Estimate}_{timestamp}.xlsx"

if st.button("Generate Excel"):
    wb = load_workbook("Estimate_Template.xlsx")
    sheet = wb["Sheet1"]
    sheet["B1"] = Estimate
    sheet["B2"] = Name
    sheet["B3"] = Date.strftime("%m/%d/%Y")
    sheet["B4"] = district
    sheet["B5"] = township
    sheet["B6"] = paymentmethod
    sheet["B7"] = road
    sheet["B8"] = road_limits
    sheet["B9"] = comments
    sheet["B10"] = Dimensions_length
    sheet["B11"] = Dimensions_width
    sheet["B12"] = Dimensions_depth
    sheet["B13"] = DaysWorked
    sheet["B14"] = ROperatorCount
    sheet["B15"] = RForemanCount
    sheet["B16"] = RoperatorHours
    sheet["B17"] = RForemanHours
    sheet["B18"] = OTOperatorCount
    sheet["B19"] = OTForemanCount
    sheet["B20"] = OTOperatorHours
    sheet["B21"] = OTFormeanHours
    sheet["B22"] = gallons
    sheet["B23"] = deliveries
    sheet["B24"] = notes
    
    start_row = 26

    for i, row in edited_equipment.iterrows():
        excel_row = start_row + i

        sheet[f"B{excel_row}"] = row["Equipment"]
        sheet[f"C{excel_row}"] = row["Quantity"]
        sheet[f"D{excel_row}"] = row["Hours"]
        sheet[f"E{excel_row}"] = row["Equipment Number"]
        
    output = BytesIO()
    wb.save(output)
    output.seek(0)
        
### Download Button
    st.download_button(
        label="Download Estimate",
        data=output,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
