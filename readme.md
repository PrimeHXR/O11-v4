Installation Guide

1. Clone the repository: 
    git clone https://github.com/PrimeHXR/O11-v4

2. Navigate to the project directory:
    cd o11-v4

3. Install Docker:
    snap install docker

4. Build the Docker image:
    sudo docker build -t o11-v4 .

5. Choose between Node.js or Python. DON'T FORGET TO ADD YOUR SERVER IP ADDRESS!

    Node.js (default):
        sudo docker run -d -p 80:80 -p 443:443 -p 5454:5454 -p 8484:8484 -e IP_ADDRESS=SERVER-IP-HERE -e SERVER_TYPE=nodejs --name o11 o11-v4
    
    Python:
        sudo docker run -d -p 80:80 -p 443:443 -p 5454:5454 -p 8484:8484 -e IP_ADDRESS=SERVER-IP-HERE -e SERVER_TYPE=python --name o11 o11-v4

6. Access the Web Panel:

    URL: http://SERVER-IP-HERE:8484
    Credentials: admin:admin