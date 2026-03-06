import streamlit as st
import subprocess

st.set_page_config(page_title="AI Video Generator", page_icon="🎬", layout="centered")

st.title("🎬 AI Video Generator")
st.write("Enter a topic below to automatically research, script, and produce a video!")

topic = st.text_input("Enter Video Topic:", placeholder="e.g., The Future of Space Exploration")

if st.button("Generate Video", type="primary"):
    if not topic.strip():
        st.warning("Please enter a valid topic to proceed.")
    else:
        st.info(f"Initializing video creation for: **{topic}**")
        st.write("Please wait while the AI agents research, write the script, and compile your video. This might take a few minutes.")
        
        # Use a spinner to show progress
        with st.spinner("Generating video..."):
            try:
                # Execute the existing main.py pipeline
                process = subprocess.run(
                    ["python", "main.py", topic],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                st.success("Video generated successfully! 🎉")
                st.balloons()
                
                # Option to view logs
                with st.expander("View Execution Logs"):
                    st.text(process.stdout)
                    
            except subprocess.CalledProcessError as e:
                st.error("An error occurred during video generation.")
                with st.expander("View Error Logs"):
                    st.text(e.stderr)
                    if e.stdout:
                        st.text("Standard Output:")
                        st.text(e.stdout)
