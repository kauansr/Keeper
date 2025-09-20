# KEEPER
This is a project to help people shop by allowing them to enter the product name, price, expiration date, and their budget. The site will help you show what your budget can and cannot buy, alerting you if the date you entered is close to expiring.

## Technologies Used
- **Python**: The programming language used for data manipulation, model building, and evaluation.
- **JavaScript**: JavaScript for the frontend.
- **React.js**: Front-end framework used to build the user interface.
- **PostgreSQL**: Database used to protect and keep all data.
- **Sqlalchemy**: A python SQL toolkit ORM.
- **Pytest**: A framework for testing application.
- **Celery**: A system to process vast amount of messages.
- **Uvicorn**: An ASGI web server for python.


## Installation for Windows

Follow the steps below to set up the project.

1. Clone the repository:
    ```bash
    git clone https://github.com/kauansr/Keeper.git

    cd keeper
    ```

2. Backend (FastAPI)
    ```
    python -m venv venv

    venv\Scripts\activate

    pip install -r requirements.txt

    python main.py
    ```

3. Frontend (Reactjs)
    ```
    cd frontend

    npm install

    npm start
    ```

Create a **.env** file in the root directory of the project and add your real data. following the **.env.example**