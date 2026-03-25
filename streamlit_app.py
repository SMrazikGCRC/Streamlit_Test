import streamlit as st
import pandas as pd

st.title("Road Estimate Generator")

Estimate_Types = ["Limestone","HMA Resurfacing","Aprons","Ditching","Milling, Paving and Shoulders","Paving Overlay (only) and Shoulders","Chip Seal","Spot Repair","Mowing"]
Townships = ["Argentine Township","Atlas Township","Clayton Township","Davison Township","Fenton Township","Flint Township","Flushing Township","Forest Township","Gaines Township","Genesee Township","Grand Blanc Township","Montrose Township","Mt. Morrish Township","Mundy Township","Richfield Township","Thetford Township","Vienna Township"]
Districts = ["Atlas","Linden","Metro","Montrose","Otisville","Swartz Creek"]
PaymentMethod_List = ["GCRC/Township","100% Township","CBDG"]

Limestone_Equipment = ["Grader W/ Radio","Pickup W/ Radio","Tandem W/Tank","Walk-N-Roller"]
HMA_Resurfacing_Equipment = ["Trailer","Bobcat","Mill Head","Broom","Pickup W/ Radio","Swap Loader","Low Boy Tractor","Asphalt Dis. Truck","Asphalt Paver","Water Tank","Crew Cab","Asphalt Roller","Swap Loader"]
Aprons_Equipment = ["Pickup W/ Radio","Utility Truck","Tractor","Trailer","Asphalt Paver","Asphault Dis Truck","Swap Loader","Water Tank","Asphalt Roller","Bobcat","Mill Head","Broom","Bucket","Pickup W/ Radio","Single Axle"]
Ditching_Equipment = ["Gradall W/ Radio","Tandem Truck W/ Radio","Tri Axle Truck W/ Radio","Pickup Truck W/ Radio","Laser"]
Paving_Overlay_Equipment = ["Trailer","Bobcat","Mill Head","Broom","Pickup W/ Radio","Swap Loader","Low Boy Tractor","Trailer","Asphalt Dis. Truck","Asphalt Paver","Water Tank","Crew Cab","Trailer","Asphalt Roller","Swap Loader","Pickup W/ Radio"]
Milling_Equipment = ["Tri-Axle Dump Truck W/ Radio","Trailer","Bobcat","Mill Head","Broom","Pickup W/ Radio","Swap Loader","Pickup W/ Radio"]
Shoulders_Equipment = ["Shoulder Machine","Roller","Tandem Truck","Pickup Truck","1-Ton Truck"]
Spot_Repair_Equipment = ["Gradall","Tandem Truck","Single Axle","Trailer","Roller","Road Grader"]
Mowing_Equipment = ["Arm Mower"]


Estimate = st.selectbox("Type of Job", Estimate_Types)
Name = st.text_input("Name")
Date = st.date_input("Date")
district = st.selectbox("District", Districts)
township = st.selectbox("Township", Townships)
paymentmethod = st.selectbox("Payment Method",PaymentMethod_List)
road = st.text_input("Road Name")
road_limits = st.text_input ("Road Limits (Ex. Bristol to Maple)")
comments = st.text_input("Comments")

st.header("Dimensions")

Dimcol1, Dimcol2, Dimcol3 = st.columns(3)

with Dimcol1:
    Dimensions_length = st.number_input("Length (Feet)", step=10)

with Dimcol2:
    Dimensions_width = st.number_input("Width (Feet)", step=1)

with Dimcol3:
    Dimensions_depth = st.number_input("Depth (Inches", step=1)

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

st.header("Dust Control")

DCcol1, DCcol2 = st.columns(2)

with DCcol1:
    gallons = st.number_input("Gallons", step=1)

with DCcol2:
    deliveries = st.number_input("Deliveries", step=1)

st.header("Notes")

notes = st.text_input("Notes")

st.header("Equipment")

EQcol1, EQcol2, EQcol3, EQcol4 = st.columns(4)

with EQcol1:
    st.subheader("Equipment Description")

with EQcol2:
    st.subheader("Quantity Used")

with EQcol3:
    st.subheader("Hours of Use")

with EQcol4:
    st.subheader("Equipment Number")


if st.button("Generate Excel"):
    
    data = {
        "Road Name": [road],
        "Township": [township],

    }

    df = pd.DataFrame(data)

    file = "project.xlsx"
    df.to_excel(file, index=False)

    with open(file, "rb") as f:
        st.download_button(
            "Download Excel",
            f,
            file_name="project.xlsx"
        )
