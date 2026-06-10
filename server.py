from fastapi import FastAPI, Path, HTTPException, Query
from .queue.connection import queue
from .app.worker import process_query

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Server is up and running"}

@app.post("/chat")
def chat(
    query: str  = Query(...,description = "Chat Message") 
):
    #put query in queue
    job = queue.enqueue(process_query, query)

    return {"status":"queued","job_id": job.id}


@app.get("/result/{job_id}")
def get_results(
    job_id:str = Path(...,description="Job ID")
):
    
    job = queue.fetch_job(job_id=job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job ID Not Found")
    if not job.is_finished:
        return {"status": job.get_status()}
    
    results = job.return_value()

    return{"result" : results}