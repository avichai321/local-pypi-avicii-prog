FROM pypiserver/pypiserver:v2.1.1

# Copy the downloaded packages directory into the image
COPY ./packages /data/packages

# Expose port 8080
EXPOSE 8080

# Default command to run pypiserver (unauthenticated, serving /data/packages)
CMD ["-p", "8080", "-P", ".", "-a", ".", "/data/packages"]
