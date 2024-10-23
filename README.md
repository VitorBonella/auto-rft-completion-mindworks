# auto-rft-completion-mindworks
Auto RFT Completion Mindoworks


# Install instructions
The easiest way to deploy this app is by using docker, following thw steps below:

## Install docker
This may depend on the machine you're using and what OS it is running, so we recommend following the guide present on `https://docs.docker.com/engine/install/`

## Build the image
In the cloned directory, run the following command
`docker build -t autorft-mindworks .`
To check if the image was correctly built, run the command
`docker images`
You should see a autorft-mindworks image under the REPOSITORY column

## Running the container
Now that you have built the iamge, you can run the container by executing:
`docker run -p 8501:8501 autorft-mindworks`
The -p flag publishes the container's port 8501 to your server’s 8501 port, and that's the port you'll use to access the application later

## Open in the browser
You can now access the app in your browser simply using `http://0.0.0.0:8501` or `http://localhost:8501`, the address may vary if you're acessing it from another machine.
In this case, ask for yout IT manager to inform you the IP/Address you should access it from.

## How to get a gemini api key

Access https://aistudio.google.com/app/apikey?hl=pt-br , and create your api key.

# Running the application without docker
This path is not recommended, however, it can be a good debugging step and something the following developers of this aplication should use
## Install dependencies
In the cloned directory, run the following command
`pip install -r requirements.txt`

## Start application
To simply start the application you could get it running with the command below
`streamlit run main.py`
