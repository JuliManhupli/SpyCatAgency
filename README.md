# SpyCatAgency

## Local Development with Docker Compose

This document outlines the steps for setting up and running the project locally for development purposes using Docker
Compose.

## Prerequisites

- **Git** installed on your system. Download from https://git-scm.com/downloads if needed.
- **Docker** installed and running. Download from https://www.docker.com/get-started.

## Steps

**1. Clone the Repository**

Open a terminal and navigate to your desired project directory. Then, clone the repository using the following command:

```bash
git clone https://github.com/JuliManhupli/SpyCatAgency.git
cd Test-task
```

**2. Setting Up the Environment File**

1. Navigate to the root directory of your project.
2. Create a new file named `.env`.
3. Inside the `.env` file, paste the necessary environment variables specific to your project. These variables will
   likely be in the `.env.ini` format.

**3. Building Docker Containers**

After setting up the `.env` file, run the following command to build the Docker containers defined in your
`docker-compose.yml` file:

```bash
docker-compose build
```

**4. Starting Docker Containers**

Once the build process completes, run the following command to start the Docker containers in detached mode (meaning the
terminal will not be blocked):

```bash
docker-compose up -d
```

**5. Database Migrations (if applicable)**

If your project uses a database and requires migrations, run the following command to apply the migrations to the
database within the container:

```bash
docker-compose exec web python manage.py migrate
```

**6. Creating a Superuser (if applicable)**

If your project uses Django and requires a superuser for administrative tasks, run the following command:

```bash
docker-compose exec web python manage.py createsuperuser
```

**7. Accessing the Application**

Once the containers are running, you can access the application at the following URL (assuming your `docker-compose.yml`
file exposes port 8000):

```
http://localhost:8000
```

**8. API Documentation (if applicable)**

If your application has API documentation, you can access it at:

```
http://localhost:8000/api/docs
```

**9. Running Tests**

To run tests locally, execute the following command:

```bash
docker-compose exec web python manage.py test
```

**10. Stopping Docker Containers**

To stop the Docker containers, run the following command:

```bash
docker-compose down
```

## API Documentation

You can find the full API documentation for *The Spy Cat Agency* in [Postman Collection](https://www.postman.com/supply-cosmonaut-22611647/the-spy-cat-agency/overview).

This collection includes all endpoints for mission and target management, including assigning/removing cats, completing targets, and updating target notes.
