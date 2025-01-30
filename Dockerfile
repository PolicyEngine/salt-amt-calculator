FROM ghcr.io/policyengine/policyengine:latest
RUN pip install streamlit
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
