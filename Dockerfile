FROM ubuntu:22.04

# تثبيت الأدوات الضرورية
RUN apt-get update && apt-get install -y curl nodejs npm
# تثبيت محرر الكود
RUN npm install -g code-server

# فتح منفذ التواصل
EXPOSE 8080

# تشغيل المحرر عند فتح السيرفر
CMD ["code-server", "--bind-addr", "0.0.0.0:8080", "--auth", "none"]
