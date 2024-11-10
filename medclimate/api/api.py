from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI instance with metadata
app = FastAPI(
    title="MedClimate API",          # Shows in API documentation
    description="API for climate data analysis in Medellin",
    version="0.1.0"
)

# CORS Middleware configuration
# This allows other websites/applications to call your API
app.add_middleware(
    CORSMiddleware,
    # Which origins (websites) can access your API:
    allow_origins=["*"],       # "*" means all origins are allowed
    # allow_origins=["http://localhost:3000"]  # More secure: only allow specific origins
    
    # Allow browsers to send credentials (cookies, authorization headers):
    allow_credentials=True,
    
    # Which HTTP methods are allowed:
    allow_methods=["*"],       # "*" means all methods (GET, POST, etc.)
    # allow_methods=["GET", "POST"]  # More secure: only specific methods
    
    # Which HTTP headers are allowed:
    allow_headers=["*"],       # "*" means all headers
)

# Define a route for the root endpoint "/"
@app.get("/")                 # HTTP GET method decorator
async def root():
    return {"message": "Welcome to MedClimate API"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Run the application if this file is run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)