# HealthCare-Chatbot
## An AI-powered chatbot that enables users to upload healthcare-related PDF documents and ask questions based on their content. The system uses Retrieval-Augmented Generation (RAG) to provide accurate, context-aware responses along with source citations.
________________________________________
🚀 Features
•	📄 Upload multiple PDF documents
•	💬 Interactive chatbot interface
•	🔍 Context-aware answers using RAG
•	📚 Source citations (document + page reference)
•	⚡ Fast semantic search using FAISS
•	🖥️ Streamlit-based UI
•	🐳 Docker support for easy deployment
________________________________________
🏗️ Tech Stack
•	LLM: Google Gemini (via LangChain)
•	Framework: LangChain
•	Embeddings: HuggingFace (all-MiniLM-L6-v2)
•	Vector Store: FAISS
•	UI: Streamlit
•	PDF Processing: PyPDF
•	Containerization: Docker
________________________________________
📂 Project Structure
healthcare-chatbot/
│
├── app/
│ ├── main.py
│ └── pdfextractor.py
│
├── requirements.txt
├── Dockerfile
├── README.md
└── .env
________________________________________
⚙️ Local Setup
1.	Clone repository
git clone YOUR_REPO_LINK
cd healthcare-chatbot
________________________________________
2.	Create virtual environment
python -m venv .venv
.venv\Scripts\activate
________________________________________
3.	Install dependencies
pip install -r requirements.txt
________________________________________
4.	Add API key
Create a .env file:
GOOGLE_API_KEY=your_api_key_here
________________________________________
5.	Run the app
streamlit run app/main.py
Open in browser:
http://localhost:8501
________________________________________
🐳 Docker Setup
Build image:
docker build -t healthcare-chatbot .
Run container:
docker run -p 8501:8501 -e GOOGLE_API_KEY=your_api_key_here healthcare-chatbot
________________________________________
🧠 How It Works
1.	Upload PDF documents
2.	Extract text using PyPDF
3.	Split text into chunks
4.	Generate embeddings using HuggingFace
5.	Store embeddings in FAISS
6.	Retrieve relevant chunks based on query
7.	Generate response using Gemini LLM
8.	Display answer with source citations
________________________________________
⚠️ Limitations
•	Citations are approximate (chunk-based)
•	Requires API key for Gemini
•	Docker may need admin/system permissions
________________________________________
🚀 Future Improvements
•	Accurate page-level citations
•	Chat memory support
•	Improved UI (chat bubbles, streaming)
•	Agentic AI workflows
•	Cloud deployment (AWS/GCP)
________________________________________
👨‍💻 Author
Developed as part of a Data Science / Generative AI Internship project.



