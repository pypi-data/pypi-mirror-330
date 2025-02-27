import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_slb_gallery",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3000",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_slb_gallery", path=build_dir)

def streamlit_slb_gallery(
    data: dict, 
    token: str, 
    key=None
):  
    component_value = _component_func(
        data=data, 
        token=token, 
        key=key
    )
    return component_value
