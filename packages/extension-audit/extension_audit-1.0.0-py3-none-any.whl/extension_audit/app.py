import streamlit as st
import json
import sys

def display_results(fp, tp):
    st.title("JSON to Markdown Viewer")

    try:
        json_obj_1 = fp[0] if fp else {}
        json_obj_2 = tp[0] if tp else {}
        
        st.header('first-party requests')
        st.write(json_obj_1)

        st.header('third-party header')
        st.write(json_obj_2)
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please check your input.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        json_data = json.loads(sys.argv[1])  # Decode JSON from argument
        fp, tp = json_data.get("fp", {}), json_data.get("tp", {})
    else:
        fp, tp = {}, {}

    display_results(fp, tp)
