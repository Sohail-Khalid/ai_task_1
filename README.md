Local AI Chatbot with Open WebUI, Ollama, and DeepSeek-R1 (Dockerized)
Overview

1. Install Ollama 
```
    brew install -cask ollama
```

2. Install Deepseek

```
    ollama run deepseek-r1:1.5b
```
3. Install Docker
```
brew install --cask docker
```
4. Install open-webui using docker in  macOS
```
docker run -d -p 3000:8080 -v ollama:/root/.ollama -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:ollama
```

Now open-webui will start running locally on `localhost:3000` but it will not be connected to our ollama model to that we need to do some steps 
1. Go to setting
2. Then Go to admin setting
3. Click on connection here you will see ollama section here add this 
    ```http://host.docker.internal:11434```

    It will connnect our open-webui to ollama and now all our local model which we have installed using ollama will be avialable for us to connect with open-webui