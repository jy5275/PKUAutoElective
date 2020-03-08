FROM python:slim

LABEL maintainer="you.siki@outlook.com"

RUN pip install --no-cache-dir \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    lxml requests numpy flask \
	Pillow sklearn joblib simplejson \
	&& pip3 install torch==1.4.0+cpu torchvision==0.5.0+cpu \
	-f https://download.pytorch.org/whl/torch_stable.html

ADD . /workspace

VOLUME [ "/config" ]

WORKDIR /workspace

CMD [ \
    "python", \
    "main.py" ]
