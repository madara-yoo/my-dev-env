FROM ubuntu:22.04
RUN apt-get update && apt-get install -y curl nodejs npm
RUN npm install -g code-server
EXPOSE 8080
# هذا الأمر سيشغل محرر الكود ويفتحه على منفذ 8080
CMD ["code-server", "--bind-addr", "0.0.0.0:8080", "--auth", "none"]
