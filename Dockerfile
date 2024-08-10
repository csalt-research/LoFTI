# Use the NVIDIA CUDA 12.3.2 devel image with Ubuntu 22.04 as the base image
FROM nvidia/cuda:12.3.2-devel-ubuntu22.04

# Set environment variables to ensure that Python 3 is used
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PATH=/usr/local/cuda/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# Install necessary packages
RUN apt-get update && apt-get install -y \
    python3-pip \
    git \
 && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip3 install huggingface-hub
RUN pip3 install datasets==2.20.0
RUN pip3 install openai==1.39.0
 
# Clone the llama.cpp repository
RUN git clone https://github.com/ggerganov/llama.cpp

# Change to the repository directory
WORKDIR llama.cpp

# Build the project
RUN make

# Install the Python bindings with CUDA support
RUN CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python

