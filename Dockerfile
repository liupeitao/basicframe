# 基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . /app

# 同 COPY只不过会自动解压缩
#ADD

# 安装项目依赖
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 安装 FFmpeg 和 FFprobe
RUN apt update && \
    apt install -y ffmpeg && \
#    \
#    ntp

# 配置 NTP 客户端
#RUN echo "server pool.ntp.org" >> /etc/ntp.conf

# 设置环境变量（如果需要）
ENV PYTHONPATH=/app

# 向主机暴漏端口
EXPOSE 8888 9999 8080 8889 8890

#向外暴漏挂载点
VOLUME /app/basicframe/assets

# 启动 NTP 客户端（后台方式）
#CMD service ntp start && tail -f /dev/null
CMD python basicframe/down/download_npr_multithread.py
#CMD python basicframe/playground/celery_work.py

