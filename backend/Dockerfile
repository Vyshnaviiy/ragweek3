FROM public.ecr.aws/lambda/python:3.11

# Copy requirements first
COPY requirements.txt .

# Install dependencies into Lambda task root
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy application code
COPY . ${LAMBDA_TASK_ROOT}

# Lambda handler
CMD ["main.handler"]