FROM ubuntu:22.04

# تحديث النظام وتثبيت أدوات البرمجة الأساسية
RUN apt-get update && apt-get install -y openssh-server git python3 nodejs npm vim curl

# إعداد الـ SSH للدخول من الترمكس
RUN mkdir /var/run/sshd
RUN echo 'root:password123' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# فتح منفذ الـ SSH
EXPOSE 22

# تشغيل خدمة SSH
CMD ["/usr/sbin/sshd", "-D"]
