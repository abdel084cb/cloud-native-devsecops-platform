#!/bin/bash
docker run -d \
  --name cloud-native-devsecops-api \
  -p 127.0.0.1:8001:8000 \
  --read-only \
  --tmpfs /tmp \
  --cap-drop ALL \
  --security-opt no-new-privileges:true \
  cloud-native-devsecops-api:dev