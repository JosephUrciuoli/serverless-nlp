# Serverless NLP

This repo contains an example of a serverless NLP workflow using AWS Batch, S3, and textract.

## Getting Started

As a prerequisite, you'll need [Docker](https://docs.docker.com/get-docker/) installed on your local machine and an AWS account.

### Developing Locally

1. At the project root, run `pip install -r requirements.txt`. You'll want Python 3.7 installed in a virtual environment of your choice.
2. Set up your AWS profile to point at the account you'll use to run the Batch jobs / store the data
3. Create a new repository in AWS Elastic Container Registry (ECR)
4. Copy `.env_template` to a new file in the same directory called `.env`. Add your AWS credentials, ECR repository, and preferred docker image name to the file. This will allow you to use the commands in the `Makefile`.
5. Run `make build && make push`. This will build your Docker image, and upload it to ECR.
6. Create a new S3 bucket you'll use to store the documents. Move the documents in the `data/` directory to a folder in the bucket named `documents`. These documents were sourced [a paper](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DJHVHB#__sid=js0) in the Harvard Dataverse.



## Data Source

https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DJHVHB#__sid=js0