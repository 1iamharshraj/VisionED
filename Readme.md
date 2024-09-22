
# VisionED : Automated Video Generation for Educators

This project enables educators to upload PowerPoint presentations (PPTs) along with optional images and automatically generates videos from the uploaded content. The project consists of a Django application for managing educator uploads and a FastAPI-based microservice for GPU-accelerated video generation.

## Features

- **Upload Management**: Educators can upload PPTs and optional images through a web interface.
- **Background Video Generation**: Videos are generated asynchronously from the uploaded content, with the option to leverage GPU acceleration.
- **Celery Task Queue**: Asynchronous task handling using Celery with RabbitMQ as the message broker.
- **Django Integration**: The generated videos are linked to the educator's upload and stored in Django's media directory.
- **Temporary Directory Management**: Temporary directories are used for processing and cleaned up after each request.
- **Node Media Server**: Serves the generated videos for streaming to students.
- **Tailwind CSS**: Used for styling the web interface.
- **Student Access**: Students can consume content uploaded by educators.

---

## Project Structure

```bash
├── GenerationServer               # FastAPI service for video generation
│   ├── gpu_env.yaml         # Conda environment for GPU
│   ├── app.py                    # FastAPI app for handling video generation requests
│   └── ...
├── edu_project/                   # Django project directory
├── home/                       # Django app for educator uploads and student content consumption
├── media/                         # Directory where generated videos are stored
├── static/                        # Static files for the web UI
├── templates/                     # HTML templates for the web UI
├── requirements.txt               # Python dependencies for Django app
├── manage.py                      # Django management script
├── media_server.js                # Node.js media server for streaming videos
└── README.md                      # Project readme file
```

---

## Requirements

### General Dependencies
- **Python** (>=3.10) for Django
- **Python** (>=3.7) for GPU services
- **Django** (>=4.0)
- **Celery** (>=5.2)
- **RabbitMQ** (>=3.9)
- **FastAPI** (>=0.85)
- **CUDA** (for GPU acceleration)

### GPU-Specific Dependencies
To leverage GPU acceleration, you'll need CUDA drivers and the dependencies listed in the `GenerationServer/conda-gpu_env.yaml` file.

---

## Setup Instructions

### Django Setup

1. **Clone the Repository**:

   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. **Set up the Virtual Environment and Install Dependencies**:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Apply Database Migrations**:

   ```bash
   python manage.py migrate
   ```

4. **Create a Superuser for Django Admin**:

   ```bash
   python manage.py createsuperuser
   ```

5. **Run the Django Development Server**:

   ```bash
   python manage.py runserver
   ```

Access the Django app at `http://localhost:8000`.

---

### FastAPI and GPU Server Setup

1. **Navigate to the Generation Server**:

   ```bash
   cd GenerationServer
   ```

2. **Set Up the Conda Environment**:

   Install the required GPU dependencies via conda:

   ```bash
   conda env create -f conda-gpu_env.yaml
   conda activate gpu_env
   ```

3. **Run the FastAPI Video Generation Service**:

   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8001
   ```

The FastAPI server will now be ready to process video generation requests.

---

### Node Media Server Setup

1. **Install Node.js**:

   If you haven't already, install Node.js from the [official website](https://nodejs.org/).

2. **Run the Media Server**:

   In the project root, run the media server using:

   ```bash
   node media_server.js
   ```

The media server will serve the generated videos for streaming.

---

### Celery & RabbitMQ Setup

1. **Install RabbitMQ**:

   Install RabbitMQ according to your OS. For Ubuntu, use:

   ```bash
   sudo apt-get install rabbitmq-server
   sudo systemctl enable rabbitmq-server
   sudo systemctl start rabbitmq-server
   ```

2. **Run Celery Worker**:

   In the project root, start a Celery worker to process background tasks:

   ```bash
   celery -A edu_project worker --loglevel=info
   ```

3. **Run Celery Beat (Optional)**:

   If you're using scheduled tasks, start the Celery beat scheduler:

   ```bash
   celery -A edu_project beat --loglevel=info
   ```

---

### Tailwind CSS Setup

1. **Install Tailwind CSS**:

   Navigate to the project directory where your `package.json` is located and run:

   ```bash
   npm install
   ```

2. **Build Tailwind CSS**:

   To build the CSS file, use the command:

   ```bash
   npx tailwindcss build -i  static/css/input.css -o static/css/output.css --watch 
   ```

This will compile your Tailwind CSS styles and watch for changes.

---

## Usage

1. **Educator Upload**: Educators upload their PowerPoint presentations and optional images using the web UI.
   
2. **Background Video Generation**: Uploaded files are sent to the FastAPI service for video generation, which runs asynchronously.

3. **Viewing Generated Videos**: Once the video is generated, educators can view or download the video from their dashboard, and students can stream the videos via the Node media server.

---

## Contributing

We welcome contributions! Please follow these steps to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push to your branch.
5. Open a pull request.

Please ensure that your code adheres to the project's coding standards and passes all tests.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
```

This README provides a comprehensive overview of your project, including all necessary setup instructions and features. Feel free to adjust any sections as needed!