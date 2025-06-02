# 🌿 EcoTracker

**EcoTracker** is a prototype for an application which helps companies measure and analyze their carbon footprint. The goal is to offer companies a comprehensive and transparent  accounting of their CO2 emissions based on invoice data.  The application will automate the calculation of emission estimates and provide instant data insights. The results will enable companies to more quickly assess their carbon footprint and make informed decisions  about their own emissions.

## 🚀 Features

- Fetch data from Odoo (ERP system)
    
- Categorize products using LLMs (groq for labeling, breact for classifying)
    
- Estimate CO₂ emissions using Climatiq (product + delivery)
    
- Calculate delivery distances using OpenRouteService
        
- Intuitive UI displaying the emissions and diagrams

## 🔗 External Dependencies
This project relies on a separate application (maintained in a different repository) that provides invoice and purchase data from **Odoo**.  
You can find the data source repository here:

🔗 [ecotracker-odoo](https://github.com/jessicadraper/ecotracker-odoo)  
*Access may be restricted depending on permissions.*
Please clone the repo and run the app.py to proceed.

## 🛠 How to Run

### ✅ Prerequisites

- Python 3.13
- Node.js    
- API Keys:
    
    - [Climatiq](https://www.climatiq.io/) – for emission factors
        
    - [OpenRouteService](https://openrouteservice.org/) – for distance calculation
        
    - [GROQ](https://groq.com/) – for product labeling
        
    - [Breact](https://breact.ai/) – for product classification
        

### 🔐 Create a `.env` File

1.  Copy the `.env.example` file and rename it to `.env`
    
2.  Fill in your API keys and required fields
    

### ⚙️ Backend Set Up
```` bash
cd EcoTracker					# root
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
pip install -r requirements.txt
````
### 🌐 Backend API
Now you can interact with the backend directly via REST:
GET localhost:8000/calculate-emissions/?url=http://localhost:8069&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD

### ▶️Frontend Setup
 ```` bash
 cd frontend
 npm install
 npm run dev
 ````

Open browser https://localhost:3000

**🎉Everything should work fine now!** 🎉

### ➕ Adding New Dependencies
If you install a new package via pip, update the requirements file:
```` bash
pip freeze > requirements.txt
````

## 👥 Team

- Jessica Draper – Developer
- Albert Szulc – Developer
- Rukayah Jabr – Developer
- Wolfgang Radinger-Peer – Technical Supervisor
- Raphael Fakhir – Product Owner

### 📬 Contact

For questions or collaboration inquiries, please contact:  
📧 jessica.draper@stud.fh-campuswien.ac.at
📧 albert.szulc@stud.fh-campuswien.ac.at
📧 rukayah.jabr@stud.fh-campuswien.ac.at
📧 wolfgang.radinger-peer@edu.fh-campuswien.ac.at
📧 raphael@breact.ai
