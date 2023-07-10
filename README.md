# Requirements

Python 3.10

# Installation
To run the project, follow these steps:

1. Install [Docker](https://www.docker.com) on your system 

2. Clone the repository:
   ```bash
   git clone https://github.com/kra1dex/reeltime.git
   ```

3. Create `.env` file in the directory where located `settings.py` and paste there two variables: <br>
`EMAIL_HOST_USER=your_email@email.com` <br>
`EMAIL_HOST_PASSWORD=your_email_password`

4. Run the Docker image by executing the following command:
   ```bash
   docker-compose up
   ```

5. Open the terminal and create a superuser by running this command:
   ```bash
   docker-compose exec app sh -c "python manage.py createsuperuser"
   ```

Swagger documentation: http://127.0.0.1:8000/api/v1/schema/swagger-ui/
