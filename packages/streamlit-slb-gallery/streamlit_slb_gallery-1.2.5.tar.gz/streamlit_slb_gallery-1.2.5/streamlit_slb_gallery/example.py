import os
import streamlit as st

from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthInteractive, OAuthClientCredentials
from streamlit_slb_gallery import streamlit_slb_gallery

def assign_auth(project_name):
        
    if project_name == "slb-test":        
        tenant_id = os.environ.get("CDF_SLBTEST_TENANT_ID") 
        client_id = os.environ.get("CDF_SLBTEST_CLIENT_ID") 
        client_secret = os.environ.get("CDF_SLBTEST_CLIENT_SECRET")
        cluster = os.environ.get("CDF_SLBTEST_CLUSTER")     
    elif project_name == "petronas-pma-dev" or project_name == "petronas-pma-playground":
        tenant_id = os.environ.get("CDF_PETRONASPMA_TENANT_ID") 
        cluster = os.environ.get("CDF_PETRONASPMA_CLUSTER") 
        client_id = os.environ.get("CDF_PETRONASPMA_CLIENT_ID") 
        client_secret = ""
    elif project_name == "hess-malaysia-dev":
        tenant_id = os.environ.get("CDF_HESSDEV_TENANT_ID") 
        client_id = os.environ.get("CDF_HESSDEV_CLIENT_ID") 
        client_secret = os.environ.get("CDF_HESSDEV_CLIENT_SECRET") 
        cluster = os.environ.get("CDF_HESSDEV_CLUSTER") 
    elif project_name == "hess-malaysia-prod":
        tenant_id = os.environ.get("CDF_HESSPROD_TENANT_ID") 
        client_id = os.environ.get("CDF_HESSPROD_CLIENT_ID") 
        client_secret = os.environ.get("CDF_HESSPROD_CLIENT_SECRET") 
        cluster = os.environ.get("CDF_HESSPROD_CLUSTER")     
    elif project_name == "mubadala-dev":
        tenant_id = os.environ.get("CDF_MUBADALADEV_TENANT_ID") 
        cluster = os.environ.get("CDF_MUBADALADEV_CLUSTER")
        client_id = os.environ.get("CDF_MUBADALADEV_CLIENT_ID") 
        client_secret = os.environ.get("CDF_MUBADALADEV_CLIENT_SECRET") 
           
    base_url = f"https://{cluster}.cognitedata.com"
    scopes = [f"{base_url}/.default"]
    
    return {
        "tenant_id": tenant_id, 
        "client_id": client_id, 
        "client_secret": client_secret, 
        "cluster": cluster,
        "base_url": base_url,
        "project_name": project_name,
        "scopes": scopes
    }

def interactive_client(project_name):
    
    auth_data: any = assign_auth(project_name)
    
    """Function to instantiate the CogniteClient, using the interactive auth flow"""
    return CogniteClient(
        ClientConfig(
            client_name=auth_data['project_name'],
            project=auth_data['project_name'],
            base_url=auth_data['base_url'],
            credentials=OAuthInteractive(
                authority_url=f"https://login.microsoftonline.com/{auth_data['tenant_id']}",
                client_id=auth_data['client_id'],
                scopes=auth_data['scopes'],
            ),
        )
    )

def client_credentials(project_name):
    
    auth_data = assign_auth(project_name)

    credentials = OAuthClientCredentials(
        token_url=f"https://login.microsoftonline.com/{auth_data['tenant_id']}/oauth2/v2.0/token", 
        client_id=auth_data['client_id'], 
        client_secret= auth_data['client_secret'],
        scopes=auth_data['scopes']
    )

    config = ClientConfig(
        client_name=auth_data['project_name'],
        project=auth_data['project_name'],
        base_url=auth_data['base_url'],
        credentials=credentials,
    )
    client = CogniteClient(config)

    return client

def connect(project_name):
    auth = assign_auth(project_name=project_name)  
    if auth["client_secret"] == "":
        return interactive_client(project_name)
    else:
        return client_credentials(project_name)

st.set_page_config(page_title="Streamlit Slb Gallery", layout='wide')
st.subheader("Streamlit Slb Gallery")

client: CogniteClient = connect("mubadala-dev")

cognite_token = client.iam.token

def show_main_content():
    
    st.session_state["selected_datetime_from"] = st.selectbox(key="start_date", label="Start Date", options=["2025-01-01 00:00:00","2024-07-02 06:00:00","2024-07-03 06:00:00","2024-07-04 06:00:00","2024-07-05 06:00:00", "2024-01-22 06:00:00"], )	
    st.session_state["selected_datetime_to"] = st.selectbox(key="end_date", label="End Date", options=["2025-01-31 00:00:00","2024-11-29 06:00:00","2024-07-03 06:00:00","2024-07-04 06:00:00","2024-07-05 06:00:00", "2025-01-22 06:00:00"])	
    
    st.session_state.selected_deck = st.selectbox(label="Deck", options=["Main Deck", "Upper Deck"])
    
    if "selected_data" in st.session_state:
        st.write(st.session_state.selected_data)

@st.fragment       
def show_streamlit_slb_gallery():      
    if "selected_datetime_from" in st.session_state and "selected_datetime_to" in st.session_state:
        st.session_state.selected_data = streamlit_slb_gallery(
            data={
                "height": 600, 
                "items_per_page": 10, 
                "event_start_time": st.session_state["selected_datetime_from"], 
                "event_end_time": st.session_state["selected_datetime_to"], 
                "event_type": "PPE_VIOLATION", 
                "load_delay": 2000,
                # "selected_object": {
                #     "type": "camera",
                #     "id": 2,
                #     "externalId": "AYS310",
                #     "name": "Camera 2"
                # },
                "limit": 1000
                },
            token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImltaTBZMnowZFlLeEJ0dEFxS19UdDVoWUJUayIsImtpZCI6ImltaTBZMnowZFlLeEJ0dEFxS19UdDVoWUJUayJ9.eyJhdWQiOiJodHRwczovL2F6LXNpbi1zcC0wMDEuY29nbml0ZWRhdGEuY29tIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvNmUzMDJmZTktMTE4Ni00MjgxLTlmYjMtOTQ0ZDdiYjgyOGNjLyIsImlhdCI6MTc0MDU1MTM1OSwibmJmIjoxNzQwNTUxMzU5LCJleHAiOjE3NDA1NTUyNTksImFpbyI6ImsyUmdZRkNSdk8rbzRMeEd2dm5oOXY0RmRnV3FBQT09IiwiYXBwaWQiOiJlOWNhOWQzNy02ZGNjLTRlYjktOTg2YS0xN2M1ZWY4YjM5MzQiLCJhcHBpZGFjciI6IjEiLCJncm91cHMiOlsiNGZhYzhhNWMtNjQzNC00MzQwLTgzMTQtNWRiOWQ0ZjdjNzBiIl0sImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzZlMzAyZmU5LTExODYtNDI4MS05ZmIzLTk0NGQ3YmI4MjhjYy8iLCJvaWQiOiIzOGVhNmM4Zi0wY2Q4LTRhMTctOTIxMi03MTY2OTUzYjc4MmYiLCJyaCI6IjEuQWNZQTZTOHdib1lSZ1VLZnM1Uk5lN2dvekVMc1hQNlk0cWhPcWZkVmZLbTFVYTdHQUFER0FBLiIsInN1YiI6IjM4ZWE2YzhmLTBjZDgtNGExNy05MjEyLTcxNjY5NTNiNzgyZiIsInRpZCI6IjZlMzAyZmU5LTExODYtNDI4MS05ZmIzLTk0NGQ3YmI4MjhjYyIsInV0aSI6Il9YdnFJQkhna1V5bU96a01qT3RNQVEiLCJ2ZXIiOiIxLjAifQ.SWwDdj4iuugXtxNw1L_6woXTl8CyeBdrDKhBHjKMzcaHOrvNjZdIm1PWQZa2HHdM7YCfyBihCS-fA9tg0MaaSOrzlrsVupo72L_KoJUWl5vUv7inU9jy0_pyP5iVcXR7okLlVMPfdZXX6tuSR7MHpOw56_VUfIippv8w9xW_TbB6804Bw5zu_A1vrk1oqy9P9Y2gbnXeVZN-gIMwMYg0lEHJ5bU3-cUBs9kuIt68JYGu_4dWeWzO6VvORmz6GoP2HcPELrwUFaiTo-o9Ae5BIk3CMIRKRCAbHZ_TZgpSUN1Ku2HFrCIaP3NYm_rbX7xipcz67PoHoqIxun49747hkA",
            key="streamlit_slb_gallery"
        )
        st.write(st.session_state.selected_data)

main_content, gallery = st.columns([1,1])

with main_content:
    show_main_content()
    
with gallery:
    show_streamlit_slb_gallery()



