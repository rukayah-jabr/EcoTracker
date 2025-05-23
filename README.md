# EcoTracker

## How to run?

### Prerequisites
- Python 3.13
- get API Key from Climatiq - emission factors
  - [climatiq](https://www.climatiq.io/)
- get API Key from - distance calculation
  - [openrouteservice](https://openrouteservice.org/)
- get API Key from Groq - LLM for categorization
  - [groq](https://console.groq.com/keys)
- get API KEY from Breact - LLM for classifying
  - [breact] (https://breact.ai/home/api-keys).

### Create a `.env` file
- copy the `.env.example` file and rename it to `.env`
- fill in the required fields

### Set Up Virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

### Install dependencies
```bash
pip install -r requirements.txt
```

**Everything should work fine now!**

## Adding dependencies
When a new dependency is installed using pip, make sure to update the `requirements.txt` file by running the following command:
```bash
pip freeze > requirements.txt
```
