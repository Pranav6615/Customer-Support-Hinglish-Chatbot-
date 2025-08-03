import openai
import time
import streamlit as st
# ✅ Step 0: Set your API key
openai.api_key = st.secrets["OPENAI_API_KEY"] 

# ✅ Step 1: Upload the training file
with open("train_hinglish_openai_chat.jsonl", "rb") as f:
    upload = openai.files.create(
        file=f,
        purpose="fine-tune"
    )

file_id = upload.id
print(f"📁 Uploaded file ID: {file_id}")

# ✅ Step 2: Start fine-tuning job
job = openai.fine_tuning.jobs.create(
    training_file=file_id,
    model="gpt-3.5-turbo-0125",
    hyperparameters={"n_epochs": 3}
)

job_id = job.id
print(f"🚀 Fine-tuning started: {job_id}")

# ✅ Step 3: Poll for job status
while True:
    status = openai.fine_tuning.jobs.retrieve(job_id).status
    print(f"⏳ Status: {status}")
    if status in ["succeeded", "failed", "cancelled"]:
        final = openai.fine_tuning.jobs.retrieve(job_id)
        print(f"✅ Training finished with status: {status}")
        if final.fine_tuned_model:
            print(f"🎯 Fine-tuned model: {final.fine_tuned_model}")
        break
    time.sleep(10)
