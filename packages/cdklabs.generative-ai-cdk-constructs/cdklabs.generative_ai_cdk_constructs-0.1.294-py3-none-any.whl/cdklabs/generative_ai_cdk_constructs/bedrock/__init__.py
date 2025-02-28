r'''
# Amazon Bedrock Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **Language**                                                                                   | **Package**                             |
| :--------------------------------------------------------------------------------------------- | --------------------------------------- |
| ![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) TypeScript | `@cdklabs/generative-ai-cdk-constructs` |
| ![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python             | `cdklabs.generative_ai_cdk_constructs`  |
| ![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java                   | `io.github.cdklabs.generative_ai_cdk_constructs`|
| ![.Net](https://docs.aws.amazon.com/cdk/api/latest/img/dotnet32.png) .Net                   | `CdkLabs.GenerativeAICdkConstructs`|
| ![Go](https://docs.aws.amazon.com/cdk/api/latest/img/go32.png) Go                   | `github.com/cdklabs/generative-ai-cdk-constructs-go/generative-ai-cdk-constructs`|

[Amazon Bedrock](https://aws.amazon.com/bedrock/) is a fully managed service that offers a choice of high-performing foundation models (FMs) from leading AI companies and Amazon through a single API, along with a broad set of capabilities you need to build generative AI applications with security, privacy, and responsible AI.

This construct library facilitates the deployment of Knowledge Bases, Bedrock Agents, Guardrails, Prompt Management, and Inference Pipelines. It leverages underlying CloudFormation L1 resources to provision these Bedrock features.

## Table of contents

* [API](#api)
* [Knowledge Bases](#knowledge-bases)

  * [Vector Knowledge Base](#vector-knowledge-base)
  * [Kendra Knowledge Base](#kendra-knowledge-base)
* [Agents](#agents)
* [Guardrails](#bedrock-guardrails)
* [Prompt management](#prompt-management)
* [Application inference profile](#application-inference-profile)

## API

See the [API documentation](../../../apidocs/namespaces/bedrock/README.md).

## Knowledge Bases

Amazon Bedrock Knowledge Bases enable you to provide foundation models and agents with contextual information from your company’s private data sources. This enhances the relevance, accuracy, and customization of their responses.

### Vector Knowledge Base

#### Create a vector Knowledge Base

A vector index on a vector store is required to create a vector Knowledge Base. This construct currently supports [Amazon OpenSearch Serverless](../opensearchserverless), [Amazon RDS Aurora PostgreSQL](../amazonaurora/), [Pinecone](../pinecone/) . By default, this resource will create an OpenSearch Serverless vector collection and index for each Knowledge Base you create, but you can provide an existing collection and/or index to have more control. For other resources you need to have the vector stores already created and credentials stored in AWS Secrets Manager. For Aurora, the construct provides an option to create a default `AmazonAuroraDefaultVectorStore` construct that will provision the vector store backed by Amazon Aurora for you. To learn more you can read [here](../amazonaurora/README.md).

The resource accepts an `instruction` prop that is provided to any Bedrock Agent it is associated with so the agent can decide when to query the Knowledge Base.

#### Vector Knowledge Base Properties

| Name | Type | Required | Description |
|---|---|---|---|
| embeddingsModel | BedrockFoundationModel | Yes | The embeddings model for the knowledge base |
| name | string | No | The name of the knowledge base |
| vectorType | VectorType | No | The vector type to store vector embeddings |
| description | string | No | The description of the knowledge base |
| instruction | string | No | Instructions for agents based on the design and type of information of the Knowledge Base that will impact how Agents interact with the Knowledge Base |
| existingRole | iam.IRole | No | Existing IAM role with a policy statement granting permission to invoke the specific embeddings model |
| indexName | string | No | The name of the vector index (only applicable if vectorStore is of type VectorCollection) |
| vectorField | string | No | The name of the field in the vector index (only applicable if vectorStore is of type VectorCollection) |
| vectorStore | VectorCollection | PineconeVectorStore | AmazonAuroraVectorStore | ExistingAmazonAuroraVectorStore | No | The vector store for the knowledge base |
| vectorIndex | VectorIndex | No | The vector index for the OpenSearch Serverless backed knowledge base |
| knowledgeBaseState | string | No | Specifies whether to use the knowledge base or not when sending an InvokeAgent request |
| tags | Record<string, string> | No | Tag (KEY-VALUE) bedrock agent resource |

### Initializer

Example of `OpenSearch Serverless`:

TypeScript

```python
import * as s3 from 'aws-cdk-lib/aws-s3';
import { bedrock } from '@cdklabs/generative-ai-cdk-constructs';

const kb = new bedrock.VectorKnowledgeBase(this, 'KnowledgeBase', {
  embeddingsModel: bedrock.BedrockFoundationModel.TITAN_EMBED_TEXT_V1,
  instruction: 'Use this knowledge base to answer questions about books. ' + 'It contains the full text of novels.',
});

const docBucket = new s3.Bucket(this, 'DocBucket');

new bedrock.S3DataSource(this, 'DataSource', {
  bucket: docBucket,
  knowledgeBase: kb,
  dataSourceName: 'books',
  chunkingStrategy: bedrock.ChunkingStrategy.fixedSize({
    maxTokens: 500,
    overlapPercentage: 20,
  }),
});
```

Python

```python

from aws_cdk import (
    aws_s3 as s3,
)
from cdklabs.generative_ai_cdk_constructs import (
    bedrock
)

kb = bedrock.VectorKnowledgeBase(self, 'KnowledgeBase',
            embeddings_model= bedrock.BedrockFoundationModel.TITAN_EMBED_TEXT_V1,
            instruction=  'Use this knowledge base to answer questions about books. ' +
    'It contains the full text of novels.'
        )

docBucket = s3.Bucket(self, 'DockBucket')

bedrock.S3DataSource(self, 'DataSource',
    bucket= docBucket,
    knowledge_base=kb,
    data_source_name='books',
    chunking_strategy= bedrock.ChunkingStrategy.FIXED_SIZE,
)

```

Example of `Amazon RDS Aurora PostgreSQL`:

TypeScript

```python
import * as s3 from 'aws-cdk-lib/aws-s3';
import { amazonaurora, bedrock } from '@cdklabs/generative-ai-cdk-constructs';

// Dimension of your vector embedding
embeddingsModelVectorDimension = 1024;
const auroraDb = new amazonaurora.AmazonAuroraVectorStore(stack, 'AuroraDefaultVectorStore', {
  embeddingsModelVectorDimension: embeddingsModelVectorDimension,
});

const kb = new bedrock.VectorKnowledgeBase(this, 'KnowledgeBase', {
  vectorStore: auroraDb,
  embeddingsModelVectorDimension: embeddingsModelVectorDimension,
  instruction: 'Use this knowledge base to answer questions about books. ' + 'It contains the full text of novels.',
});

const docBucket = new s3.Bucket(this, 'DocBucket');

new bedrock.S3DataSource(this, 'DataSource', {
  bucket: docBucket,
  knowledgeBase: kb,
  dataSourceName: 'books',
  chunkingStrategy: bedrock.ChunkingStrategy.FIXED_SIZE,
});
```

Python

```python

from aws_cdk import (
    aws_s3 as s3,
    aws_rds as rds,
    aws_ec2 as ec2,
    Stack,
    ArnFormat
)
from cdklabs.generative_ai_cdk_constructs import (
    bedrock,
    amazonaurora,
)

# Dimension of your vector embedding
embeddings_model_vector_dimension = 1024
aurora_db = amazonaurora.AmazonAuroraVectorStore(self, 'AuroraDefaultVectorStore',
  embeddings_model_vector_dimension=embeddings_model_vector_dimension
)

kb = bedrock.VectorKnowledgeBase(self, 'KnowledgeBase',
            vector_store= aurora_db,
            embeddings_model_vector_dimension=embeddings_model_vector_dimension,
            instruction=  'Use this knowledge base to answer questions about books. ' +
    'It contains the full text of novels.'
        )

docBucket = s3.Bucket(self, 'DockBucket')

bedrock.S3DataSource(self, 'DataSource',
    bucket= docBucket,
    knowledge_base=kb,
    data_source_name='books',
    chunking_strategy= bedrock.ChunkingStrategy.FIXED_SIZE,
)

```

Example of importing existing `Amazon RDS Aurora PostgreSQL` using `fromExistingAuroraVectorStore()` method.
**Note** - you need to provide `clusterIdentifier`, `databaseName`, `vpc`, `secret` and `auroraSecurityGroupId` used in deployment of your existing RDS Amazon Aurora DB, as well as `embeddingsModel` that you want to be used by a Knowledge Base for chunking:

TypeScript

```python
import * as s3 from "aws-cdk-lib/aws-s3";
import { amazonaurora, bedrock } from '@cdklabs/generative-ai-cdk-constructs';

const auroraDb = aurora.AmazonAuroraVectorStore.fromExistingAuroraVectorStore(stack, 'ExistingAuroraVectorStore', {
  clusterIdentifier: 'aurora-serverless-vector-cluster',
  databaseName: 'bedrock_vector_db',
  schemaName: 'bedrock_integration',
  tableName: 'bedrock_kb',
  vectorField: 'embedding',
  textField: 'chunks',
  metadataField: 'metadata',
  primaryKeyField: 'id',
  embeddingsModel: bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3,
  vpc: cdk.aws_ec2.Vpc.fromLookup(stack, 'VPC', {
    vpcId: 'vpc-0c1a234567ee8bc90',
  }),
  auroraSecurityGroupId: 'sg-012ef345678c98a76',,
  secret: cdk.aws_rds.DatabaseSecret.fromSecretCompleteArn(
    stack,
    'Secret',
    cdk.Stack.of(stack).formatArn({
      service: 'secretsmanager',
      resource: 'secret',
      resourceName: 'rds-db-credentials/cluster-1234567890',
      region: cdk.Stack.of(stack).region,
      account: cdk.Stack.of(stack).account,
      arnFormat: cdk.ArnFormat.COLON_RESOURCE_NAME,
    }),
  ),
});

const kb = new bedrock.VectorKnowledgeBase(this, "KnowledgeBase", {
  vectorStore: auroraDb,
  embeddingsModel: bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3,
  instruction:
    "Use this knowledge base to answer questions about books. " +
    "It contains the full text of novels.",
});

const docBucket = new s3.Bucket(this, "DocBucket");

new bedrock.S3DataSource(this, "DataSource", {
  bucket: docBucket,
  knowledgeBase: kb,
  dataSourceName: "books",
  chunkingStrategy: bedrock.ChunkingStrategy.FIXED_SIZE,
});
```

Python

```python

from aws_cdk import (
    aws_s3 as s3,
    aws_rds as rds,
    aws_ec2 as ec2,
    Stack,
    ArnFormat
)
from cdklabs.generative_ai_cdk_constructs import (
    bedrock,
    amazonaurora,
)

aurora_db = amazonaurora.AmazonAuroraVectorStore.from_existing_aurora_vector_store(
    self, 'ExistingAuroraVectorStore',
    cluster_identifier='aurora-serverless-vector-cluster',
    database_name='bedrock_vector_db',
    schema_name='bedrock_integration',
    table_name='bedrock_kb',
    vector_field='embedding',
    text_field='chunks',
    metadata_field='metadata',
    primary_key_field='id',
    embeddings_model=bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3,
    vpc=ec2.Vpc.from_lookup(self, 'VPC', vpc_id='vpc-0c1a234567ee8bc90'),
    aurora_security_group_id='sg-012ef345678c98a76',,
    secret=rds.DatabaseSecret.from_secret_complete_arn(
        self,
        'Secret',
        Stack.of(self).format_arn(
            service= 'secretsmanager',
            resource= 'secret',
            resource_name= 'rds-db-credentials/cluster-1234567890',
            region= Stack.of(self).region,
            account= Stack.of(self).account,
            arn_format= ArnFormat.COLON_RESOURCE_NAME
        )
    )
)

kb = bedrock.VectorKnowledgeBase(self, 'KnowledgeBase',
            vector_store= aurora_db,
            embeddings_model= bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3,
            instruction=  'Use this knowledge base to answer questions about books. ' +
    'It contains the full text of novels.'
        )

docBucket = s3.Bucket(self, 'DockBucket')

bedrock.S3DataSource(self, 'DataSource',
    bucket= docBucket,
    knowledge_base=kb,
    data_source_name='books',
    chunking_strategy= bedrock.ChunkingStrategy.FIXED_SIZE,
)
```

Example of `Pinecone` (manual, you must have Pinecone vector store created):

TypeScript

```python
import * as s3 from 'aws-cdk-lib/aws-s3';
import { pinecone, bedrock } from '@cdklabs/generative-ai-cdk-constructs';

const pineconeds = new pinecone.PineconeVectorStore({
  connectionString: 'https://your-index-1234567.svc.gcp-starter.pinecone.io',
  credentialsSecretArn: 'arn:aws:secretsmanager:your-region:123456789876:secret:your-key-name',
  textField: 'question',
  metadataField: 'metadata',
});

const kb = new bedrock.VectorKnowledgeBase(this, 'KnowledgeBase', {
  vectorStore: pineconeds,
  embeddingsModel: bedrock.BedrockFoundationModel.TITAN_EMBED_TEXT_V1,
  instruction: 'Use this knowledge base to answer questions about books. ' + 'It contains the full text of novels.',
});

const docBucket = new s3.Bucket(this, 'DocBucket');

new bedrock.S3DataSource(this, 'DataSource', {
  bucket: docBucket,
  knowledgeBase: kb,
  dataSourceName: 'books',
  chunkingStrategy: bedrock.ChunkingStrategy.FIXED_SIZE,
});
```

Python

```python

from aws_cdk import (
    aws_s3 as s3,
)
from cdklabs.generative_ai_cdk_constructs import (
    bedrock,
    pinecone,
)

pineconevs = pinecone.PineconeVectorStore(
            connection_string='https://your-index-1234567.svc.gcp-starter.pinecone.io',
            credentials_secret_arn='arn:aws:secretsmanager:your-region:123456789876:secret:your-key-name',
            text_field='question',
            metadata_field='metadata'
        )

kb = bedrock.VectorKnowledgeBase(self, 'KnowledgeBase',
            vector_store= pineconevs,
            embeddings_model= bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3,
            instruction=  'Use this knowledge base to answer questions about books. ' +
    'It contains the full text of novels.'
        )

docBucket = s3.Bucket(self, 'DockBucket')

bedrock.S3DataSource(self, 'DataSource',
    bucket= docBucket,
    knowledge_base=kb,
    data_source_name='books',
    chunking_strategy= bedrock.ChunkingStrategy.FIXED_SIZE,
)
```

#### Vector Knowledge Base - Vector Type

The data type for the vectors when using a model to convert text into vector embeddings. Embeddings type may impact the availability of some embeddings models and vector stores. The following vector types are available:

* Floating point: More precise vector representation of the text, but more costly in storage.
* Binary: Not as precise vector representation of the text, but not as costly in storage as a standard floating-point (float32). Not all embedding models and vector stores support binary embeddings

See [Supported embeddings models](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-supported.html) for information on the available models and their vector data types.

Typescript

```python
const app = new cdk.App();
const stack = new cdk.Stack(app, 'aws-cdk-bedrock-data-sources-integ-test');

const kb = new VectorKnowledgeBase(stack, 'MyKnowledgeBase', {
  name: 'MyKnowledgeBase',
  vectorType: bedrock.VectorType.BINARY,
  embeddingsModel: BedrockFoundationModel.COHERE_EMBED_MULTILINGUAL_V3,
});
```

Python

```python

from aws_cdk import (
    aws_s3 as s3,
)
from cdklabs.generative_ai_cdk_constructs import (
    bedrock
)

kb = bedrock.VectorKnowledgeBase(self, 'KnowledgeBase',
    name= 'MyKnowledgeBase',
    vector_type= bedrock.VectorType.BINARY,
    embeddings_model= bedrock.BedrockFoundationModel.COHERE_EMBED_MULTILINGUAL_V3,
)
```

#### Vector Knowledge Base - Data Sources

Data sources are the various repositories or systems from which information is extracted and ingested into the
knowledge base. These sources provide the raw content that will be processed, indexed, and made available for
querying within the knowledge base system. Data sources can include various types of systems such as document
management systems, databases, file storage systems, and content management platforms. Suuported Data Sources
include Amazon S3 buckets, Web Crawlers, SharePoint sites, Salesforce instances, and Confluence spaces.

* **Amazon S3**. You can either create a new data source using the `bedrock.S3DataSource(..)` class, or using the
  `kb.addS3DataSource(..)`.
* **Web Crawler**. You can either create a new data source using the `bedrock.WebCrawlerDataSource(..)` class, or using the
  `kb.addWebCrawlerDataSource(..)`.
* **Confluence**. You can either create a new data source using the `bedrock.ConfluenceDataSource(..)` class, or using the
  `kb.addConfluenceDataSource(..)`.
* **SharePoint**. You can either create a new data source using the `bedrock.SharePointDataSource(..)` class, or using the
  `kb.addSharePointDataSource(..)`.
* **Salesforce**. You can either create a new data source using the `bedrock.SalesforceDataSource(..)` class, or using the
  `kb.addSalesforceDataSource(..)`.

Typescript

```python
const app = new cdk.App();
const stack = new cdk.Stack(app, 'aws-cdk-bedrock-data-sources-integ-test');

const kb = new VectorKnowledgeBase(stack, 'MyKnowledgeBase', {
  name: 'MyKnowledgeBase',
  embeddingsModel: BedrockFoundationModel.COHERE_EMBED_MULTILINGUAL_V3,
});

const bucket = new Bucket(stack, 'Bucket', {});
const lambdaFunction = new Function(stack, 'MyFunction', {
  runtime: cdk.aws_lambda.Runtime.PYTHON_3_9,
  handler: 'index.handler',
  code: cdk.aws_lambda.Code.fromInline('print("Hello, World!")'),
});

const secret = new Secret(stack, 'Secret');
const key = new Key(stack, 'Key');

kb.addWebCrawlerDataSource({
  sourceUrls: ['https://docs.aws.amazon.com/'],
  chunkingStrategy: ChunkingStrategy.HIERARCHICAL_COHERE,
  customTransformation: CustomTransformation.lambda({
    lambdaFunction: lambdaFunction,
    s3BucketUri: `s3://${bucket.bucketName}/chunk-processor/`,
  }),
});

kb.addS3DataSource({
  bucket,
  chunkingStrategy: ChunkingStrategy.SEMANTIC,
  parsingStrategy: ParsingStategy.foundationModel({
    model: BedrockFoundationModel.ANTHROPIC_CLAUDE_SONNET_V1_0,
  }),
});

kb.addConfluenceDataSource({
  dataSourceName: 'TestDataSource',
  authSecret: secret,
  kmsKey: key,
  confluenceUrl: 'https://example.atlassian.net',
  filters: [
    {
      objectType: ConfluenceObjectType.ATTACHMENT,
      includePatterns: ['.*\\.pdf'],
      excludePatterns: ['.*private.*\\.pdf'],
    },
    {
      objectType: ConfluenceObjectType.PAGE,
      includePatterns: ['.*public.*\\.pdf'],
      excludePatterns: ['.*confidential.*\\.pdf'],
    },
  ],
});

kb.addSalesforceDataSource({
  authSecret: secret,
  endpoint: 'https://your-instance.my.salesforce.com',
  kmsKey: key,
  filters: [
    {
      objectType: SalesforceObjectType.ATTACHMENT,
      includePatterns: ['.*\\.pdf'],
      excludePatterns: ['.*private.*\\.pdf'],
    },
    {
      objectType: SalesforceObjectType.CONTRACT,
      includePatterns: ['.*public.*\\.pdf'],
      excludePatterns: ['.*confidential.*\\.pdf'],
    },
  ],
});

kb.addSharePointDataSource({
  dataSourceName: 'SharepointDataSource',
  authSecret: secret,
  kmsKey: key,
  domain: 'yourdomain',
  siteUrls: ['https://yourdomain.sharepoint.com/sites/mysite'],
  tenantId: '888d0b57-69f1-4fb8-957f-e1f0bedf64de',
  filters: [
    {
      objectType: SharePointObjectType.PAGE,
      includePatterns: ['.*\\.pdf'],
      excludePatterns: ['.*private.*\\.pdf'],
    },
    {
      objectType: SharePointObjectType.FILE,
      includePatterns: ['.*public.*\\.pdf'],
      excludePatterns: ['.*confidential.*\\.pdf'],
    },
  ],
});
```

Python

```python
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_secretsmanager as secretsmanager,
    aws_kms as kms
)
from constructs import Construct
from cdklabs.generative_ai_cdk_constructs import (
    bedrock
)

class PythonTestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        kb = bedrock.VectorKnowledgeBase(self, 'MyKnowledgeBase',
                    embeddings_model= bedrock.BedrockFoundationModel.COHERE_EMBED_MULTILINGUAL_V3,
                )

        docBucket = s3.Bucket(self, 'Bucket')

        function = _lambda.Function(self, 'MyFunction',
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler='index.handler',
            code=_lambda.Code.from_inline('print("Hello, World!")'),
        )

        kb.add_web_crawler_data_source(
            source_urls= ['https://docs.aws.amazon.com/'],
            chunking_strategy= bedrock.ChunkingStrategy.HIERARCHICAL_COHERE,
            custom_transformation= bedrock.CustomTransformation.lambda_(
                lambda_function= function,
                s3_bucket_uri= f's3://{docBucket.bucket_name}/chunk-processor/'
            )
        )

        kb.add_s3_data_source(
            bucket= docBucket,
            chunking_strategy= bedrock.ChunkingStrategy.SEMANTIC,
            parsing_strategy= bedrock.ParsingStategy.foundation_model(
                parsing_model= bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V1_0.as_i_model(self)
            )
        )

        secret = secretsmanager.Secret(self, 'Secret')
        key = kms.Key(self, 'Key')

        kb.add_confluence_data_source(
            data_source_name='TestDataSource',
            auth_secret=secret,
            kms_key=key,
            confluence_url='https://example.atlassian.net',
            filters=[
                bedrock.ConfluenceCrawlingFilters(
                    object_type=bedrock.ConfluenceObjectType.ATTACHMENT,
                    include_patterns= [".*\\.pdf"],
                    exclude_patterns= [".*private.*\\.pdf"],
                ),
                bedrock.ConfluenceCrawlingFilters(
                    object_type=bedrock.ConfluenceObjectType.PAGE,
                    include_patterns= [".*public.*\\.pdf"],
                    exclude_patterns= [".*confidential.*\\.pdf"],
                ),
            ]
        )

        kb.add_salesforce_data_source(
            auth_secret=secret,
            endpoint='https://your-instance.my.salesforce.com',
            kms_key=key,
            filters=[
                bedrock.SalesforceCrawlingFilters(
                    object_type=bedrock.SalesforceObjectType.ATTACHMENT,
                    include_patterns= [".*\\.pdf"],
                    exclude_patterns= [".*private.*\\.pdf"],
                ),
                bedrock.SalesforceCrawlingFilters(
                    object_type=bedrock.SalesforceObjectType.CONTRACT,
                    include_patterns= [".*public.*\\.pdf"],
                    exclude_patterns= [".*confidential.*\\.pdf"],
                ),
            ]
        )

        kb.add_share_point_data_source(
            data_source_name='SharepointDataSource',
            auth_secret=secret,
            kms_key=key,
            domain='yourDomain',
            site_urls= ['https://yourdomain.sharepoint.com/sites/mysite'],
            tenant_id='888d0b57-69f1-4fb8-957f-e1f0bedf64de',
            filters=[
                bedrock.SharePointCrawlingFilters(
                    object_type=bedrock.SharePointObjectType.PAGE,
                    include_patterns= [".*\\.pdf"],
                    exclude_patterns= [".*private.*\\.pdf"],
                ),
                bedrock.SharePointCrawlingFilters(
                    object_type=bedrock.SharePointObjectType.FILE,
                    include_patterns= [".*public.*\\.pdf"],
                    exclude_patterns= [".*confidential.*\\.pdf"],
                ),
            ]
        )

```

#### Vector Knowledge Base - Chunking Strategies

* **Default Chunking**: Applies Fixed Chunking with the default chunk size of 300 tokens and 20% overlap.

  TypeScript

  ```python
  ChunkingStrategy.DEFAULT;
  ```

  Python

  ```python
  ChunkingStrategy.DEFAULT
  ```
* **Fixed Size Chunking**: This method divides the data into fixed-size chunks, with each chunk
  containing a predetermined number of tokens. This strategy is useful when the data is uniform
  in size and structure.
  Typescript

  TypeScript

  ```python
  // Fixed Size Chunking with sane defaults.
  ChunkingStrategy.FIXED_SIZE;

  // Fixed Size Chunking with custom values.
  ChunkingStrategy.fixedSize({ maxTokens: 200, overlapPercentage: 25 });
  ```

  Python

  ```python
  # Fixed Size Chunking with sane defaults.
  ChunkingStrategy.FIXED_SIZE

  # Fixed Size Chunking with custom values.
  ChunkingStrategy.fixed_size(
    max_tokens= 200,
    overlap_percentage= 25
  )
  ```
* **Hierarchical Chunking**: This strategy organizes data into layers of chunks, with the first
  layer containing large chunks and the second layer containing smaller chunks derived from the first.
  It is ideal for data with inherent hierarchies or nested structures.

  TypeScript

  ```python
  // Hierarchical Chunking with the default for Cohere Models.
  ChunkingStrategy.HIERARCHICAL_COHERE;

  // Hierarchical Chunking with the default for Titan Models.
  ChunkingStrategy.HIERARCHICAL_TITAN;

  // Hierarchical Chunking with custom values. Tthe maximum chunk size depends on the model.
  // Amazon Titan Text Embeddings: 8192. Cohere Embed models: 512
  ChunkingStrategy.hierarchical({
    overlapTokens: 60,
    maxParentTokenSize: 1500,
    maxChildTokenSize: 300,
  });
  ```

  Python

  ```python
  # Hierarchical Chunking with the default for Cohere Models.
  ChunkingStrategy.HIERARCHICAL_COHERE

  # Hierarchical Chunking with the default for Titan Models.
  ChunkingStrategy.HIERARCHICAL_TITAN

  # Hierarchical Chunking with custom values. Tthe maximum chunk size depends on the model.
  # Amazon Titan Text Embeddings: 8192. Cohere Embed models: 512
  chunking_strategy= ChunkingStrategy.hierarchical(
      overlap_tokens=60,
      max_parent_token_size=1500,
      max_child_token_size=300
  )
  ```
* **Semantic Chunking**: This method splits data into smaller documents based on groups of similar
  content derived from the text using natural language processing. It helps preserve contextual
  relationships and ensures accurate and contextually appropriate results.

  TypeScript

  ```python
  // Semantic Chunking with sane defaults.
  ChunkingStrategy.SEMANTIC;

  // Semantic Chunking with custom values.
  ChunkingStrategy.semantic({ bufferSize: 0, breakpointPercentileThreshold: 95, maxTokens: 300 });
  ```

  Python

  ```python
  # Semantic Chunking with sane defaults.
  ChunkingStrategy.SEMANTIC

  # Semantic Chunking with custom values.
  ChunkingStrategy.semantic(
    buffer_size=0,
    breakpoint_percentile_threshold=95,
    max_tokens=300
  )
  ```
* **No Chunking**: This strategy treats each file as one chunk. If you choose this option,
  you may want to pre-process your documents by splitting them into separate files.

  TypeScript

  ```python
  ChunkingStrategy.NONE;
  ```

  Python

  ```python
  ChunkingStrategy.NONE
  ```

#### Vector Knowledge Base - Parsing Strategy

A parsing strategy in Amazon Bedrock is a configuration that determines how the service
processes and interprets the contents of a document. It involves converting the document's
contents into text and splitting it into smaller chunks for analysis. Amazon Bedrock offers
two parsing strategies:

* **Default Parsing Strategy**: This strategy converts the document's contents into text
  and splits it into chunks using a predefined approach. It is suitable for most use cases
  but may not be optimal for specific document types or requirements.
* **Foundation Model Parsing Strategy**: This strategy uses a foundation model to describe
  the contents of the document. It is particularly useful for improved processing of PDF files
  with tables and images. To use this strategy, set the `parsingStrategy` in a data source as below.

  TypeScript

  ```python
  bedrock.ParsingStategy.foundationModel({
    model: BedrockFoundationModel.ANTHROPIC_CLAUDE_SONNET_V1_0,
  });
  ```

  Python

  ```python
  bedrock.ParsingStategy.foundation_model(
      parsing_model=BedrockFoundationModel.ANTHROPIC_CLAUDE_SONNET_V1_0
  )
  ```

#### Knowledge Base - Custom Transformation

Custom Transformation in Amazon Bedrock is a feature that allows you to create and apply
custom processing steps to documents moving through a data source ingestion pipeline.

Custom Transformation uses AWS Lambda functions to process documents, enabling you to
perform custom operations such as data extraction, normalization, or enrichment. To
create a custom transformation, set the `customTransformation` in a data source as below.

TypeScript

```python
CustomTransformation.lambda({
lambdaFunction: lambdaFunction,
s3BucketUri: `s3://${bucket.bucketName}/chunk-processor/`,
}),
```

Python

```python
CustomTransformation.lambda_(
  lambda_function= function,
  s3_bucket_uri= f's3://{docBucket.bucket_name}/chunk-processor/'
)
```

### Kendra Knowledge Base

#### Create a Kendra Knowledge Base

With Amazon Bedrock Knowledge Bases, you can build a knowledge base from an Amazon Kendra GenAI index to create more sophisticated and accurate Retrieval Augmented Generation (RAG)-powered digital assistants. By combining an Amazon Kendra GenAI index with Amazon Bedrock Knowledge Bases, you can:

* Reuse your indexed content across multiple Amazon Bedrock applications without rebuilding indexes or re-ingesting data.
* Leverage the advanced GenAI capabilities of Amazon Bedrock while benefiting from the high-accuracy information retrieval of Amazon Kendra.
* Customize your digital assistant's behavior using the tools of Amazon Bedrock while maintaining the semantic accuracy of an Amazon Kendra GenAI index.

#### Kendra Knowledge Base properties

| Name | Type | Required | Description |
|------|------|----------|-------------|
| kendraIndex | IKendraGenAiIndex | Yes | The Kendra Index to use for the knowledge base. |
| name | string | No | The name of the knowledge base. If not provided, a name will be auto-generated. |
| description | string | No | Description of the knowledge base. |
| instruction | string | No | Instructions for the knowledge base. |
| existingRole | iam.IRole | No | An existing IAM role to use for the knowledge base. If not provided, a new role will be created. |

#### Initializer

TypeScript

```python
import * as s3 from 'aws-cdk-lib/aws-s3';
import { bedrock, kendra } from '@cdklabs/generative-ai-cdk-constructs';

const cmk = new kms.Key(stack, 'cmk', {});

// you can create a new index using the api below
const index = new kendra.KendraGenAiIndex(this, 'index', {
  name: 'kendra-index-cdk',
  kmsKey: cmk,
  documentCapacityUnits: 1, // 40K documents
  queryCapacityUnits: 1,    // 0.2 QPS
});

// or import an existing one
const index = kendra.KendraGenAiIndex.fromAttrs(this, 'myindex', {
  indexId: 'myindex',
  role: myRole
});

new bedrock.KendraKnowledgeBase(this, 'kb', {
  name: 'kendra-kb-cdk',
  kendraIndex: index,
});
```

Python

```py
from aws_cdk import aws_kms as kms
from cdklabs.generative_ai_cdk_constructs import bedrock, kendra

# Create a KMS key
cmk = kms.Key(stack, 'cmk')

# Create a new Kendra index
index = kendra.KendraGenAiIndex(self, 'index',
    name='kendra-index-cdk',
    kms_key=cmk,
    document_capacity_units=1,  # 40K documents
    query_capacity_units=1      # 0.2 QPS
)

# Or import an existing index
index = kendra.KendraGenAiIndex.from_attrs(self, 'myindex',
    index_id='myindex',
    role=my_role
)

# Create a Kendra Knowledge Base
kb = bedrock.KendraKnowledgeBase(self, 'kb',
    name='kendra-kb-cdk',
    kendra_index=index
)
```

## Agents

Amazon Bedrock Agents allow generative AI applications to automate complex, multistep tasks by seamlessly integrating with your company’s systems, APIs, and data sources.

### Agent Properties

| Name | Type | Required | Description |
|---|---|---|---|
| name | string | No | The name of the agent. Defaults to a name generated by CDK |
| instruction | string | Yes | The instruction used by the agent that determines how it will perform its task. Must have a minimum of 40 characters |
| foundationModel | IInvokable | Yes | The foundation model used for orchestration by the agent |
| existingRole | iam.IRole | No | The existing IAM Role for the agent to use. Must have a trust policy allowing Bedrock service to assume the role. Defaults to a new created role |
| shouldPrepareAgent | boolean | No | Specifies whether to automatically update the `DRAFT` version of the agent after making changes. Defaults to false |
| idleSessionTTL | Duration | No | How long sessions should be kept open for the agent. Session expires if no conversation occurs during this time. Defaults to 1 hour |
| kmsKey | kms.IKey | No | The KMS key of the agent if custom encryption is configured. Defaults to AWS managed key |
| description | string | No | A description of the agent. Defaults to no description |
| knowledgeBases | IKnowledgeBase[] | No | The KnowledgeBases associated with the agent |
| actionGroups | AgentActionGroup[] | No | The Action Groups associated with the agent |
| guardrail | IGuardrail | No | The guardrail that will be associated with the agent |
| promptOverrideConfiguration | PromptOverrideConfiguration | No | Overrides some prompt templates in different parts of an agent sequence configuration |
| userInputEnabled | boolean | No | Select whether the agent can prompt additional information from the user when it lacks enough information. Defaults to false |
| codeInterpreterEnabled | boolean | No | Select whether the agent can generate, run, and troubleshoot code when trying to complete a task. Defaults to false |
| forceDelete | boolean | No | Whether to delete the resource even if it's in use. Defaults to true |

### Create an Agent

The following example creates an Agent with a simple instruction and default prompts that consults a Knowledge Base.

### Initializer

TypeScript

```python
const agent = new bedrock.Agent(this, 'Agent', {
  foundationModel: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_HAIKU_V1_0,
  instruction: 'You are a helpful and friendly agent that answers questions about literature.',
});

agent.addKnowledgeBase(kb);
```

Python

```python
agent = bedrock.Agent(
    self,
    "Agent",
    foundation_model=bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_HAIKU_V1_0,
    instruction="You are a helpful and friendly agent that answers questions about insurance claims.",
)
  agent.add_knowledge_base(kb)
```

You can also use system defined inference profiles to enable cross region inference requests for supported models. For instance:

TypeScript

```python
const cris = bedrock.CrossRegionInferenceProfile.fromConfig({
  geoRegion: bedrock.CrossRegionInferenceProfileRegion.US,
  model: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V1_0,
});

const agent = new bedrock.Agent(this, 'Agent', {
  foundationModel: cris,
  instruction: 'You are a helpful and friendly agent that answers questions about agriculture.',
});
```

Python

```python
cris = bedrock.CrossRegionInferenceProfile.from_config(
  geo_region= bedrock.CrossRegionInferenceProfileRegion.US,
  model= bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V1_0
)

agent = bedrock.Agent(
    self,
    "Agent",
    foundation_model=cris,
    instruction="You are a helpful and friendly agent that answers questions about agriculture.",
)
```

For more information on cross region inference, please refer to [System defined inference profiles](#system-defined-inference-profiles)

### Action Groups

An action group defines functions your agent can call. The functions are Lambda functions. The action group uses an OpenAPI schema to tell the agent what your functions do and how to call them.

### Action Group Properties

| Name | Type | Required | Description |
|---|---|---|---|
| name | string | Yes | The name of the action group |
| description | string | No | A description of the action group |
| apiSchema | ApiSchema | No | The API Schema |
| executor | ActionGroupExecutor | No | The action group executor |
| enabled | boolean | No | Specifies whether the action group is available for the agent to invoke or not when sending an InvokeAgent request. Defaults to true |
| forceDelete | boolean | No | Specifies whether to delete the resource even if it's in use. Defaults to false |
| functionSchema | CfnAgent.FunctionSchemaProperty | No | Defines functions that each define parameters that the agent needs to invoke from the user |
| parentActionGroupSignature | ParentActionGroupSignature | No | The AWS Defined signature for enabling certain capabilities in your agent. When specified, description, apiSchema, and actionGroupExecutor must be blank |

### Initializer

```python
const actionGroupFunction = new lambda_python.PythonFunction(this, 'ActionGroupFunction', {
  runtime: lambda.Runtime.PYTHON_3_12,
  entry: path.join(__dirname, '../lambda/action-group'),
});

const actionGroup = new AgentActionGroup({
  name: 'query-library',
  description: 'Use these functions to get information about the books in the library.',
  executor: bedrock.ActionGroupExecutor.fromlambdaFunction(actionGroupFunction),
  enabled: true,
  apiSchema: bedrock.ApiSchema.fromLocalAsset(path.join(__dirname, 'action-group.yaml')),
});

agent.addActionGroup(actionGroup);
```

Python

```python

action_group_function = PythonFunction(
            self,
            "LambdaFunction",
            runtime=Runtime.PYTHON_3_12,
            entry="./lambda",
            index="app.py",
            handler="lambda_handler",
)

actionGroup = bedrock.AgentActionGroup(
    name="query-library",
    description="Use these functions to get information about the books in the library.",
    executor= bedrock.ActionGroupExecutor.fromlambda_function(action_group_function),
    enabled=True,
    api_schema=bedrock.ApiSchema.from_local_asset("action-group.yaml"))

agent.add_action_group(actionGroup)
```

### Prepare the Agent

The `Agent` constructs take an optional parameter `shouldPrepareAgent` to indicate that the Agent should be prepared after any updates to an agent, Knowledge Base association, or action group. This may increase the time to create and update those resources. By default, this value is false .

Creating an agent alias will not prepare the agent, so if you create an alias using the `AgentAlias` resource then you should set `shouldPrepareAgent` to ***true***.

#### Prompt Overrides

Bedrock Agents allows you to customize the prompts and LLM configuration for its different steps. You can disable steps or create a new prompt template. Prompt templates can be inserted from plain text files.

TypeScript

```python
import { readFileSync } from 'fs';

const file = readFileSync(prompt_path, 'utf-8');

const agent = new bedrock.Agent(this, 'Agent', {
      foundationModel: bedrock.BedrockFoundationModel.AMAZON_NOVA_LITE_V1,
      instruction: 'You are a helpful and friendly agent that answers questions about literature.',
      userInputEnabled: true,
      codeInterpreterEnabled: false,
      shouldPrepareAgent:true,
      promptOverrideConfiguration: bedrock.PromptOverrideConfiguration.fromSteps(
        [
          {
            stepType: bedrock.AgentStepType.PRE_PROCESSING,
            stepEnabled: true,
            customPromptTemplate: file,
            inferenceConfig: {
              temperature: 0.0,
              topP: 1,
              topK: 250,
              maximumLength: 1,
              stopSequences: ["\n\nHuman:"],
            },
          }
        ]
      )
    });
```

Python

```python
orchestration = open('prompts/orchestration.txt', encoding="utf-8").read()
agent = bedrock.Agent(self, "Agent",
            foundation_model=bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_V2_1,
            instruction="You are a helpful and friendly agent that answers questions about insurance claims.",
            user_input_enabled=True,
            code_interpreter_enabled=False,
            should_prepare_agent=True,
            prompt_override_configuration= bedrock.PromptOverrideConfiguration.from_steps(
                steps=[
                    bedrock.PromptStepConfiguration(
                        step_type=bedrock.AgentStepType.PRE_PROCESSING,
                        step_enabled= True,
                        custom_prompt_template= file,
                        inference_config=bedrock.InferenceConfiguration(
                            temperature=0.0,
                            top_k=250,
                            top_p=1,
                            maximum_length=1,
                            stop_sequences=['\n\nHuman:'],
                        )
                    ),
                ]
            ),
        )
```

### Agent Alias

After you have sufficiently iterated on your working draft and are satisfied with the behavior of your agent, you can set it up for deployment and integration into your application by creating aliases of your agent.

To deploy your agent, you need to create an alias. During alias creation, Amazon Bedrock automatically creates a version of your agent. The alias points to this newly created version. You can point the alias to a previously created version if necessary. You then configure your application to make API calls to that alias.

By default, the `Agent` resource does not create any aliases, and you can use the 'DRAFT' version.

#### Specific version

You can use the `AgentAlias` resource if you want to create an Alias for an existing Agent.

TypeScript

```python
const agentAlias2 = new bedrock.AgentAlias(this, 'myalias2', {
  aliasName: 'myalias',
  agent: agent,
  agentVersion: '1', // optional
  description: 'mytest'
});
```

Python

```python
agent_alias_2 = bedrock.AgentAlias(self, 'myalias2',
    alias_name='myalias',
    agent=agent,
    agent_version='1', # optional
    description='mytest'
)
```

## Bedrock Guardrails

Amazon Bedrock's Guardrails feature enables you to implement robust governance and control mechanisms for your generative AI applications, ensuring alignment with your specific use cases and responsible AI policies. Guardrails empowers you to create multiple tailored policy configurations, each designed to address the unique requirements and constraints of different use cases. These policy configurations can then be seamlessly applied across multiple foundation models (FMs) and Agents, ensuring a consistent user experience and standardizing safety, security, and privacy controls throughout your generative AI ecosystem.

With Guardrails, you can define and enforce granular, customizable policies to precisely govern the behavior of your generative AI applications. You can configure the following policies in a guardrail to avoid undesirable and harmful content and remove sensitive information for privacy protection.

Content filters – Adjust filter strengths to block input prompts or model responses containing harmful content.

Denied topics – Define a set of topics that are undesirable in the context of your application. These topics will be blocked if detected in user queries or model responses.

Word filters – Configure filters to block undesirable words, phrases, and profanity. Such words can include offensive terms, competitor names etc.

Sensitive information filters – Block or mask sensitive information such as personally identifiable information (PII) or custom regex in user inputs and model responses.

You can create a Guardrail with a minimum blockedInputMessaging ,blockedOutputsMessaging and default content filter policy.

TypeScript

```python
const guardrails = new bedrock.Guardrail(this, 'bedrockGuardrails', {
  name: 'my-BedrockGuardrails',
  description: 'Legal ethical guardrails.',
});

// Optional - Add Sensitive information filters

guardrail.addPIIFilter({
  type: PIIType.General.ADDRESS,
  action: GuardrailAction.ANONYMIZE,
});

guardrail.addRegexFilter({
  name: 'TestRegexFilter',
  description: 'This is a test regex filter',
  pattern: '/^[A-Z]{2}d{6}$/',
  action: bedrock.GuardrailAction.ANONYMIZE,
});

// Optional - Add contextual grounding

guardrail.addContextualGroundingFilter({
  type: ContextualGroundingFilterType.GROUNDING,
  threshold: 0.95,
});

guardrail.addContextualGroundingFilter({
  type: ContextualGroundingFilterType.RELEVANCE,
  threshold: 0.95,
});

// Optional - Add Denied topics . You can use a Topic or create your custom Topic

guardrail.addDeniedTopicFilter(Topic.FINANCIAL_ADVICE);
guardrail.addDeniedTopicFilter(
  Topic.custom({
    name: 'Legal_Advice',
    definition:
      'Offering guidance or suggestions on legal matters, legal actions, interpretation of laws, or legal rights and responsibilities.',
    examples: [
      'Can I sue someone for this?',
      'What are my legal rights in this situation?',
      'Is this action against the law?',
      'What should I do to file a legal complaint?',
      'Can you explain this law to me?',
    ],
  })
);

// Optional - Add Word filters. You can upload words from a file with addWordFilterFromFile function.
guardrail.addWordFilter('drugs');
guardrail.addManagedWordListFilter(ManagedWordFilterType.PROFANITY);
guardrails.addWordFilterFromFile('./scripts/wordsPolicy.csv');

// versioning - if you change any guardrail configuration, a new version will be created
guardrails.createVersion('testversion');

// Importing existing guardrail
const importedGuardrail = bedrock.Guardrail.fromGuardrailAttributes(stack, 'TestGuardrail', {
  guardrailArn: 'arn:aws:bedrock:us-east-1:123456789012:guardrail/oygh3o8g7rtl',
  guardrailVersion: '1', //optional
  kmsKey: kmsKey, //optional
});

// Importing Guardrails created through the L1 CDK CfnGuardrail construct
const cfnGuardrail = new CfnGuardrail(this, 'MyCfnGuardrail', {
  blockedInputMessaging: 'blockedInputMessaging',
  blockedOutputsMessaging: 'blockedOutputsMessaging',
  name: 'namemycfnguardrails',
  wordPolicyConfig: {
    wordsConfig: [
      {
        text: 'drugs',
      },
    ],
  },
});

const importedGuardrail = bedrock.Guardrail.fromCfnGuardrail(cfnGuardrail);
```

Python

```python
    guardrail = bedrock.Guardrail(self, 'myGuardrails',
        name='my-BedrockGuardrails',
        description= "Legal ethical guardrails.")

    # Optional - Add Sensitive information filters

    guardrail.add_pii_filter(
        type= bedrock.pii_type.General.ADDRESS,
        action= bedrock.GuardrailAction.ANONYMIZE,
    )

    guardrail.add_regex_filter(
        name= "TestRegexFilter",
        description= "This is a test regex filter",
        pattern= "/^[A-Z]{2}d{6}$/",
        action= bedrock.GuardrailAction.ANONYMIZE,
    )

    # Optional - Add contextual grounding

    guardrail.add_contextual_grounding_filter(
        type= bedrock.ContextualGroundingFilterType.GROUNDING,
        threshold= 0.95,
    )

    # Optional - Add Denied topics . You can use default Topic or create your custom Topic with createTopic function. The default Topics can also be overwritten.

    guardrail.add_contextual_grounding_filter(
        type= bedrock.ContextualGroundingFilterType.RELEVANCE,
        threshold= 0.95,
    )

    guardrail.add_denied_topic_filter(bedrock.Topic.FINANCIAL_ADVICE)

    guardrail.add_denied_topic_filter(
      bedrock.Topic.custom(
        name= "Legal_Advice",
        definition=
            "Offering guidance or suggestions on legal matters, legal actions, interpretation of laws, or legal rights and responsibilities.",
        examples= [
            "Can I sue someone for this?",
            "What are my legal rights in this situation?",
            "Is this action against the law?",
            "What should I do to file a legal complaint?",
            "Can you explain this law to me?",
        ]
      )
    )

    # Optional - Add Word filters. You can upload words from a file with addWordFilterFromFile function.
    guardrail.add_word_filter("drugs")
    guardrail.add_managed_word_list_filter(bedrock.ManagedWordFilterType.PROFANITY)
    guardrail.add_word_filter_from_file("./scripts/wordsPolicy.csv")

    # versioning - if you change any guardrail configuration, a new version will be created
    guardrail.create_version("testversion")

    # Importing existing guardrail
    imported_guardrail = bedrock.Guardrail.from_guardrail_attributes(self, "TestGuardrail",
      guardrail_arn="arn:aws:bedrock:us-east-1:123456789012:guardrail/oygh3o8g7rtl",
      guardrail_version="1",
      kms_key=kms_key
    )

    # Importing Guardrails created through the L1 CDK CfnGuardrail construct
    cfn_guardrail = cfnbedrock.CfnGuardrail(self, "MyCfnGuardrail",
        blocked_input_messaging="blockedInputMessaging",
        blocked_outputs_messaging="blockedOutputsMessaging",
        name="name",

        # the properties below are optional
        word_policy_config=cfnbedrock.CfnGuardrail.WordPolicyConfigProperty(
            words_config=[cfnbedrock.CfnGuardrail.WordConfigProperty(
                text="drugs"
            )]
        )
    )

    imported_guardrail = bedrock.Guardrail.from_cfn_guardrail(cfn_guardrail)



```

## Prompt management

Amazon Bedrock provides the ability to create and save prompts using Prompt management so that you can save
time by applying the same prompt to different workflows. You can include variables in the prompt so that you can
adjust the prompt for different use case.

The `Prompt` resource allows you to create a new prompt.
Example of a basic Text `Prompt`:

**TypeScript**

```python
const cmk = new kms.Key(this, 'cmk', {});
const claudeModel = BedrockFoundationModel.ANTHROPIC_CLAUDE_SONNET_V1_0;

const variant1 = PromptVariant.text({
  variantName: 'variant1',
  model: claudeModel,
  promptVariables: ['topic'],
  promptText: 'This is my first text prompt. Please summarize our conversation on: {{topic}}.',
  inferenceConfiguration: {
    temperature: 1.0,
    topP: 0.999,
    maxTokens: 2000,
  },
});

const prompt1 = new Prompt(this, 'prompt1', {
  promptName: 'prompt1',
  description: 'my first prompt',
  defaultVariant: variant1,
  variants: [variant1],
  kmsKey: cmk,
});
```

Python

```python
        cmk = kms.Key(self, "cmk")
        claude_model = bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_SONNET_V1_0

        variant1 = bedrock.PromptVariant.text(
            variant_name="variant1",
            model=claude_model,
            prompt_variables=["topic"],
            prompt_text="This is my first text prompt. Please summarize our conversation on: {{topic}}.",
            inference_configuration={
                "temperature": 1.0,
                "top_p": 0.999,
                "max_tokens": 2000,
            }
        )

        prompt = bedrock.Prompt(
            self,
            "myprompt",
            prompt_name="prompt1",
            description="my first prompt",
            default_variant=variant1,
            variants=[variant1],
            kms_key=cmk
        )
```

Example of a "Chat" `Prompt`. Use this template type when the model supports the Converse API or the Anthropic Claude Messages API.
This allows you to include a System prompt and previous User messages and Assistant messages for context.

**TypeScript**

```python
const cmk = new kms.Key(this, 'cmk', {});

const variantChat = PromptVariant.chat({
  variantName: 'variant1',
  model: BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V1_0,
  messages: [
    ChatMessage.userMessage('From now on, you speak Japanese!'),
    ChatMessage.assistantMessage('Konnichiwa!'),
    ChatMessage.userMessage('From now on, you speak {{language}}!'),
  ],
  system: 'You are a helpful assistant that only speaks the language you`re told.',
  promptVariables: ['language'],
  toolConfiguration: {
    toolChoice: ToolChoice.AUTO,
    tools: [
      {
        toolSpec: {
          name: 'top_song',
          description: 'Get the most popular song played on a radio station.',
          inputSchema: {
            json: {
              type: 'object',
              properties: {
                sign: {
                  type: 'string',
                  description:
                    'The call sign for the radio station for which you want the most popular song. Example calls signs are WZPZ and WKR.',
                },
              },
              required: ['sign'],
            },
          },
        },
      },
    ],
  },
});

new Prompt(stack, 'prompt1', {
  promptName: 'prompt-chat',
  description: 'my first chat prompt',
  defaultVariant: variantChat,
  variants: [variantChat],
  kmsKey: cmk,
});
```

Python

```python

# Create KMS key
        cmk = kms.Key(self, "cmk")

        # Create tool specification
        tool_spec = CfnPrompt.ToolSpecificationProperty(
            name="top_song",
            description="Get the most popular song played on a radio station.",
            input_schema=CfnPrompt.ToolInputSchemaProperty(
                json={
                    "type": "object",
                    "properties": {
                        "sign": {
                            "type": "string",
                            "description": "The call sign for the radio station for which you want the most popular song. Example calls signs are WZPZ and WKR."
                        }
                    },
                    "required": ["sign"]
                }
            )
        )

        # Create tool configuration
        tool_config = bedrock.ToolConfiguration(
            tool_choice=bedrock.ToolChoice.AUTO,
            tools=[
                CfnPrompt.ToolProperty(
                    tool_spec=tool_spec
                )
            ]
        )

        # Create chat variant
        variant_chat = bedrock.PromptVariant.chat(
            variant_name="variant1",
            model=bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V1_0,
            messages=[
                bedrock.ChatMessage.user("From now on, you speak Japanese!"),
                bedrock.ChatMessage.assistant("Konnichiwa!"),
                bedrock.ChatMessage.user("From now on, you speak {{language}}!"),
            ],
            system="You are a helpful assistant that only speaks the language you're told.",
            prompt_variables=["language"],
            tool_configuration=tool_config
        )

        # Create prompt
        prompt = bedrock.Prompt(
            self,
            "prompt1",
            prompt_name="prompt-chat",
            description="my first chat prompt",
            default_variant=variant_chat,
            variants=[variant_chat],
            kms_key=cmk
        )

```

### Prompt Variants

Prompt variants in the context of Amazon Bedrock refer to alternative configurations of a prompt,
including its message or the model and inference configurations used. Prompt variants allow you
to create different versions of a prompt, test them, and save the variant that works best for
your use case. You can add prompt variants to a prompt by creating a `PromptVariant` object and
specify the variants on prompt creation, or by using the `.addVariant(..)` method on a `Prompt` object.

Example of `PromptVariant`:

**TypeScript**

```python
...

const variant2 = PromptVariant.text({
  variantName: "variant2",
  model: claudeModel,
  promptVariables: [ "topic" ],
  promptText: "This is my second text prompt. Please summarize our conversation on: {{topic}}.",
  inferenceConfiguration: {
    temperature: 0.5,
    topP: 0.999,
    maxTokens: 2000,
  },
});

prompt1.addVariant(variant2);
```

Python

```python

        variant2 = bedrock.PromptVariant.text(
            variant_name="variant2",
            model=claude_model,
            prompt_variables=["topic"],
            prompt_text="This is my second text prompt. Please summarize our conversation on: {{topic}}.",
            inference_configuration={
                "temperature": 0.5,
                "topP": 0.999,
                "maxTokens": 2000,
            }
        )

        prompt.add_variant(variant2)
```

### Prompt routing

Amazon Bedrock intelligent prompt routing provides a single serverless endpoint for efficiently routing requests between different foundational models within the same model family.
It can help you optimize for response quality and cost. They offer a comprehensive solution for managing multiple AI models through a single serverless endpoint,
simplifying the process for you. Intelligent prompt routing predicts the performance of each model for each request, and dynamically routes each request to the model
that it predicts is most likely to give the desired response at the lowest cost.
More information about prompt routing in the [documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html)

**TypeScript**

```python
const variant = PromptVariant.text({
  variantName: 'variant1',
  promptText: 'What is the capital of France?',
  model: PromptRouter.fromDefaultId(DefaultPromptRouterIdentifier.ANTHROPIC_CLAUDE_V1, region),
});

new Prompt(stack, 'Prompt', {
  promptName: 'prompt-router-test',
  variants: [variant],
});
```

**Python**

```py
variant = bedrock.PromptVariant.text(
    variant_name='variant1',
    prompt_text='What is the capital of France?',
    model=bedrock.PromptRouter.from_default_id(bedrock.DefaultPromptRouterIdentifier.ANTHROPIC_CLAUDE_V1, region),
)

bedrock.Prompt(self, 'Prompt',
    prompt_name='prompt-router-test',
    variants=[variant],
)
```

### Prompt Version

A prompt version is a snapshot of a prompt at a specific point in time that you
create when you are satisfied with a set of configurations. Versions allow you to
deploy your prompt and easily switch between different configurations for your
prompt and update your application with the most appropriate version for your
use-case.

You can create a Prompt version by using the `PromptVersion` class or by using the `.createVersion(..)`
on a `Prompt` object. It is recommended to use the `.createVersion(..)` method. It uses a hash based mechanism
to update the version whenever a certain configuration property changes.

**TypeScript**

```python
new PromptVersion(prompt1, 'my first version');
```

```python
bedrock.PromptVersion(self, "my first version")

```

or alternatively:

```python
prompt1.createVersion('my first version');
```

```python
prompt.create_version("version1", "my first version")
```

## System defined inference profiles

You can build a CrossRegionInferenceProfile using a system defined inference profile. The inference profile will route requests to the Regions defined in the cross region (system-defined) inference profile that you choose. You can find the system defined inference profiles by navigating to your console (Amazon Bedrock -> Cross-region inference) or programmatically, for instance using [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_inference_profiles.html).

Before using creating a CrossRegionInferenceProfile, ensure that you have access to the models and regions defined in the inference profiles. For instance, if you see the system defined inference profile "us.anthropic.claude-3-5-sonnet-20241022-v2:0" defined in your region, the table mentions that inference requests will be routed to US East (Virginia) us-east-1, US East (Ohio) us-east-2 and US West (Oregon) us-west-2. Thus, you need to have model access enabled in those regions for the model `anthropic.claude-3-5-sonnet-20241022-v2:0`. You can then create the CrossRegionInferenceProfile as follows:

TypeScript

```python
const cris = bedrock.CrossRegionInferenceProfile.fromConfig({
  geoRegion: bedrock.CrossRegionInferenceProfileRegion.US,
  model: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V2_0,
});
```

Python

```python
cris = bedrock.CrossRegionInferenceProfile.from_config(
  geo_region= bedrock.CrossRegionInferenceProfileRegion.US,
  model= bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V2_0
)
```

## Application inference profile

You can create an application inference profile with one or more Regions to track usage and costs when invoking a model.

To create an application inference profile for one Region, specify a foundation model. Usage and costs for requests made to that Region with that model will be tracked.

To create an application inference profile for multiple Regions, specify a cross region (system-defined) inference profile. The inference profile will route requests to the Regions defined in the cross region (system-defined) inference profile that you choose. Usage and costs for requests made to the Regions in the inference profile will be tracked. You can find the system defined inference profiles by navigating to your console (Amazon Bedrock -> Cross-region inference) or programmatically, for instance using [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_inference_profiles.html):

```
bedrock = session.client("bedrock", region_name="us-east-1")
bedrock.list_inference_profiles(typeEquals='SYSTEM_DEFINED')
```

Before using application inference profiles, ensure that:

* You have appropriate IAM permissions
* You have access to the models and regions defined in the inference profiles
* Ensure proper configuration of the required API permissions for inference profile-related actions

Specifically the role you are assuming needs to have permissions for following actions in the IAM policy

```
"Action": [
      "bedrock:GetInferenceProfile",
      "bedrock:ListInferenceProfiles",
      "bedrock:DeleteInferenceProfile"
      "bedrock:TagResource",
      "bedrock:UntagResource",
      "bedrock:ListTagsForResource"
  ]
```

You can restrict to specific resources by applying "Resources" tag in the IAM policy.

```
"Resource": ["arn:aws:bedrock:*:*:application-inference-profile/*"]
```

TypeScript

```python
// Create an application inference profile for one Region
// You can use the 'bedrock.BedrockFoundationModel' or pass the arn as a string
const appInfProfile1 = new ApplicationInferenceProfile(this, 'myapplicationprofile', {
  inferenceProfileName: 'claude 3 sonnet v1',
  modelSource: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_SONNET_V1_0,
  tags: [{ key: 'test', value: 'test' }],
});

// To create an application inference profile across regions, specify the cross region inference profile
const cris = bedrock.CrossRegionInferenceProfile.fromConfig({
  geoRegion: bedrock.CrossRegionInferenceProfileRegion.US,
  model: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V2_0,
});

const appInfProfile2 = new ApplicationInferenceProfile(this, 'myapplicationprofile2', {
  inferenceProfileName: 'claude 3 sonnet v1',
  modelSource: cris,
});

// Import a Cfn L1 construct created application inference profile
const cfnapp = new CfnApplicationInferenceProfile(this, 'mytestaip3', {
  inferenceProfileName: 'mytest',
  modelSource: {
    copyFrom: 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0',
  },
});

const appInfProfile3 = bedrock.ApplicationInferenceProfile.fromCfnApplicationInferenceProfile(cfnapp);

// Import an inference profile through attributes
const appInfProfile4 = bedrock.ApplicationInferenceProfile.fromApplicationInferenceProfileAttributes(this, 'TestAIP', {
  inferenceProfileArn: 'arn:aws:bedrock:us-east-1:XXXXX:application-inference-profile/ID',
  inferenceProfileIdentifier: 'arn:aws:bedrock:us-east-1:XXXXXXX:application-inference-profile/ID',
});
```

Python

```python

# Create an application inference profile for one Region
# You can use the 'bedrock.BedrockFoundationModel' or pass the arn as a string
appInfProfile1 = bedrock.ApplicationInferenceProfile(self, 'myapplicationprofile',
  inference_profile_name='claude 3 sonnet v1',
  model_source=bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_SONNET_V1_0,
  tags=[CfnTag(
    key="key",
    value="value"
  )]
)

# To create an application inference profile across regions, specify the cross region inference profile
cris = bedrock.CrossRegionInferenceProfile.from_config(
  geo_region= bedrock.CrossRegionInferenceProfileRegion.US,
  model= bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V2_0
)

appInfProfile2 = bedrock.ApplicationInferenceProfile(self, 'myapplicationprofile2',
  inference_profile_name='claude 35 sonnet v2',
  model_source=cris
)

# Import an inference profile through attributes
appInfProfile3 = bedrock.ApplicationInferenceProfile.from_application_inference_profile_attributes(self, 'TestAIP',
  inference_profile_arn='arn:aws:bedrock:us-east-1:XXXXX:application-inference-profile/ID',
  inference_profile_identifier='arn:aws:bedrock:us-east-1:XXXXXXX:application-inference-profile/ID',
)

# Import a Cfn L1 construct created application inference profile
cfnaip = CfnApplicationInferenceProfile(this, 'mytestaip4',
  inference_profile_name='mytest',
  model_source= CfnApplicationInferenceProfile.InferenceProfileModelSourceProperty(
    copy_from='arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'
  ),
)

appInfProfile4 = bedrock.ApplicationInferenceProfile.from_cfn_application_inference_profile(cfnaip);
```
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_bedrock as _aws_cdk_aws_bedrock_ceddda9d
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import constructs as _constructs_77d1e7e8
from ..amazonaurora import (
    AmazonAuroraVectorStore as _AmazonAuroraVectorStore_bde12a1e,
    ExistingAmazonAuroraVectorStore as _ExistingAmazonAuroraVectorStore_f7ccb819,
)
from ..kendra import IKendraGenAiIndex as _IKendraGenAiIndex_da04f105
from ..opensearch_vectorindex import VectorIndex as _VectorIndex_e5d266e9
from ..opensearchserverless import VectorCollection as _VectorCollection_91bfdaa9
from ..pinecone import PineconeVectorStore as _PineconeVectorStore_c017c196
from .pii_type import (
    CanadaSpecific as _CanadaSpecific_f80239d8,
    Finance as _Finance_2430d674,
    General as _General_e613aa3a,
    InformationTechnology as _InformationTechnology_2f99a404,
    UKSpecific as _UKSpecific_c9314648,
    USASpecific as _USASpecific_fa88de63,
)


class ActionGroupExecutor(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ActionGroupExecutor",
):
    '''(experimental) Defines how fulfillment of the action group is handled after the necessary information has been elicited from the user.

    Valid executors are:

    - Lambda function
    - Return Control

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/action-handle.html
    :stability: experimental
    '''

    @jsii.member(jsii_name="fromlambdaFunction")
    @builtins.classmethod
    def fromlambda_function(
        cls,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    ) -> "ActionGroupExecutor":
        '''(experimental) Defines an action group with a Lambda function containing the business logic.

        :param lambda_function: - Lambda function to be called by the action group.

        :see: https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d66975a777761af2c2afa135a0c71acee1d35ee3de96016c47f3c26f3d1d382)
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
        return typing.cast("ActionGroupExecutor", jsii.sinvoke(cls, "fromlambdaFunction", [lambda_function]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RETURN_CONTROL")
    def RETURN_CONTROL(cls) -> "ActionGroupExecutor":
        '''(experimental) Returns the action group invocation results directly in the InvokeAgent response.

        The information and parameters can be sent to your own systems to yield results.

        :see: https://docs.aws.amazon.com/bedrock/latest/userguide/agents-returncontrol.html
        :stability: experimental
        '''
        return typing.cast("ActionGroupExecutor", jsii.sget(cls, "RETURN_CONTROL"))

    @builtins.property
    @jsii.member(jsii_name="customControl")
    def custom_control(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customControl"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction], jsii.get(self, "lambdaFunction"))


class AgentActionGroup(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentActionGroup",
):
    '''(experimental) ****************************************************************************                        DEF - Action Group Class ***************************************************************************.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        name: builtins.str,
        api_schema: typing.Optional["ApiSchema"] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        executor: typing.Optional[ActionGroupExecutor] = None,
        force_delete: typing.Optional[builtins.bool] = None,
        function_schema: typing.Optional[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.FunctionSchemaProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        parent_action_group_signature: typing.Optional["ParentActionGroupSignature"] = None,
    ) -> None:
        '''
        :param name: (experimental) The name of the action group.
        :param api_schema: (experimental) The API Schema. Default: - No API Schema
        :param description: (experimental) A description of the action group. Default: - No description
        :param enabled: (experimental) Specifies whether the action group is available for the agent to invoke or not when sending an InvokeAgent request. Default: true
        :param executor: (experimental) The action group executor. Default: - No executor
        :param force_delete: (experimental) Specifies whether to delete the resource even if it's in use. Default: false
        :param function_schema: (experimental) Defines functions that each define parameters that the agent needs to invoke from the user. NO L2 yet as this doesn't make much sense IMHO
        :param parent_action_group_signature: (experimental) The AWS Defined signature for enabling certain capabilities in your agent. When this property is specified, you must leave the description, apiSchema, and actionGroupExecutor fields blank for this action group

        :stability: experimental
        '''
        props = AgentActionGroupProps(
            name=name,
            api_schema=api_schema,
            description=description,
            enabled=enabled,
            executor=executor,
            force_delete=force_delete,
            function_schema=function_schema,
            parent_action_group_signature=parent_action_group_signature,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="codeInterpreter")
    @builtins.classmethod
    def code_interpreter(cls, enabled: builtins.bool) -> "AgentActionGroup":
        '''(experimental) Defines an action group that allows your agent to request the user for additional information when trying to complete a task.

        :param enabled: Specifies whether the action group is available for the agent.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4482a2286d1aa9365ffd4769d5c935c3786542f444b664ea9da29cb2b875990)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        return typing.cast("AgentActionGroup", jsii.sinvoke(cls, "codeInterpreter", [enabled]))

    @jsii.member(jsii_name="userInput")
    @builtins.classmethod
    def user_input(cls, enabled: builtins.bool) -> "AgentActionGroup":
        '''(experimental) Defines an action group that allows your agent to request the user for additional information when trying to complete a task.

        :param enabled: Specifies whether the action group is available for the agent.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f35ff4a8218c89e3d2dece2516fdae627f224c02993b718a265d95f3b21a74a9)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        return typing.cast("AgentActionGroup", jsii.sinvoke(cls, "userInput", [enabled]))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> builtins.bool:
        '''(experimental) Whether this action group is available for the agent to invoke or not.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the action group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="apiSchema")
    def api_schema(self) -> typing.Optional["ApiSchema"]:
        '''(experimental) The api schema for this action group (if defined).

        :stability: experimental
        '''
        return typing.cast(typing.Optional["ApiSchema"], jsii.get(self, "apiSchema"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the action group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="executor")
    def executor(self) -> typing.Optional[ActionGroupExecutor]:
        '''(experimental) The action group executor for this action group (if defined).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[ActionGroupExecutor], jsii.get(self, "executor"))

    @builtins.property
    @jsii.member(jsii_name="forceDelete")
    def force_delete(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to delete the resource even if it's in use.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "forceDelete"))

    @builtins.property
    @jsii.member(jsii_name="functionSchema")
    def function_schema(
        self,
    ) -> typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.FunctionSchemaProperty]:
        '''(experimental) The function schema for this action group (if defined).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.FunctionSchemaProperty], jsii.get(self, "functionSchema"))

    @builtins.property
    @jsii.member(jsii_name="parentActionGroupSignature")
    def parent_action_group_signature(
        self,
    ) -> typing.Optional["ParentActionGroupSignature"]:
        '''(experimental) The AWS Defined signature (if defined).

        :stability: experimental
        '''
        return typing.cast(typing.Optional["ParentActionGroupSignature"], jsii.get(self, "parentActionGroupSignature"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentActionGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "api_schema": "apiSchema",
        "description": "description",
        "enabled": "enabled",
        "executor": "executor",
        "force_delete": "forceDelete",
        "function_schema": "functionSchema",
        "parent_action_group_signature": "parentActionGroupSignature",
    },
)
class AgentActionGroupProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        api_schema: typing.Optional["ApiSchema"] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        executor: typing.Optional[ActionGroupExecutor] = None,
        force_delete: typing.Optional[builtins.bool] = None,
        function_schema: typing.Optional[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.FunctionSchemaProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        parent_action_group_signature: typing.Optional["ParentActionGroupSignature"] = None,
    ) -> None:
        '''(experimental) ****************************************************************************                        PROPS - Action Group Class ***************************************************************************.

        :param name: (experimental) The name of the action group.
        :param api_schema: (experimental) The API Schema. Default: - No API Schema
        :param description: (experimental) A description of the action group. Default: - No description
        :param enabled: (experimental) Specifies whether the action group is available for the agent to invoke or not when sending an InvokeAgent request. Default: true
        :param executor: (experimental) The action group executor. Default: - No executor
        :param force_delete: (experimental) Specifies whether to delete the resource even if it's in use. Default: false
        :param function_schema: (experimental) Defines functions that each define parameters that the agent needs to invoke from the user. NO L2 yet as this doesn't make much sense IMHO
        :param parent_action_group_signature: (experimental) The AWS Defined signature for enabling certain capabilities in your agent. When this property is specified, you must leave the description, apiSchema, and actionGroupExecutor fields blank for this action group

        :stability: experimental
        '''
        if isinstance(function_schema, dict):
            function_schema = _aws_cdk_aws_bedrock_ceddda9d.CfnAgent.FunctionSchemaProperty(**function_schema)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47b674f810daa9a7bde371ad21ea6944cc41d81e91b4c04fca71b8f52c01288)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument api_schema", value=api_schema, expected_type=type_hints["api_schema"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument executor", value=executor, expected_type=type_hints["executor"])
            check_type(argname="argument force_delete", value=force_delete, expected_type=type_hints["force_delete"])
            check_type(argname="argument function_schema", value=function_schema, expected_type=type_hints["function_schema"])
            check_type(argname="argument parent_action_group_signature", value=parent_action_group_signature, expected_type=type_hints["parent_action_group_signature"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if api_schema is not None:
            self._values["api_schema"] = api_schema
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if executor is not None:
            self._values["executor"] = executor
        if force_delete is not None:
            self._values["force_delete"] = force_delete
        if function_schema is not None:
            self._values["function_schema"] = function_schema
        if parent_action_group_signature is not None:
            self._values["parent_action_group_signature"] = parent_action_group_signature

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the action group.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_schema(self) -> typing.Optional["ApiSchema"]:
        '''(experimental) The API Schema.

        :default: - No API Schema

        :stability: experimental
        '''
        result = self._values.get("api_schema")
        return typing.cast(typing.Optional["ApiSchema"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the action group.

        :default: - No description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether the action group is available for the agent to invoke or not when sending an InvokeAgent request.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def executor(self) -> typing.Optional[ActionGroupExecutor]:
        '''(experimental) The action group executor.

        :default: - No executor

        :stability: experimental
        '''
        result = self._values.get("executor")
        return typing.cast(typing.Optional[ActionGroupExecutor], result)

    @builtins.property
    def force_delete(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to delete the resource even if it's in use.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("force_delete")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def function_schema(
        self,
    ) -> typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.FunctionSchemaProperty]:
        '''(experimental) Defines functions that each define parameters that the agent needs to invoke from the user.

        NO L2 yet as this doesn't make much sense IMHO

        :stability: experimental
        '''
        result = self._values.get("function_schema")
        return typing.cast(typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.FunctionSchemaProperty], result)

    @builtins.property
    def parent_action_group_signature(
        self,
    ) -> typing.Optional["ParentActionGroupSignature"]:
        '''(experimental) The AWS Defined signature for enabling certain capabilities in your agent.

        When this property is specified, you must leave the description, apiSchema,
        and actionGroupExecutor fields blank for this action group

        :stability: experimental
        '''
        result = self._values.get("parent_action_group_signature")
        return typing.cast(typing.Optional["ParentActionGroupSignature"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentActionGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentAliasAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "agent": "agent",
        "agent_version": "agentVersion",
        "alias_id": "aliasId",
        "alias_name": "aliasName",
    },
)
class AgentAliasAttributes:
    def __init__(
        self,
        *,
        agent: "IAgent",
        agent_version: builtins.str,
        alias_id: builtins.str,
        alias_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Attributes needed to create an import.

        :param agent: (experimental) The underlying agent for this alias.
        :param agent_version: (experimental) The agent version for this alias.
        :param alias_id: (experimental) The Id of the agent alias.
        :param alias_name: (experimental) The name of the agent alias.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c673a16aeefb1b29db08c60a2c30c29e637ee706bdb0fd7a8cfe1a1fc9a2c2c8)
            check_type(argname="argument agent", value=agent, expected_type=type_hints["agent"])
            check_type(argname="argument agent_version", value=agent_version, expected_type=type_hints["agent_version"])
            check_type(argname="argument alias_id", value=alias_id, expected_type=type_hints["alias_id"])
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent": agent,
            "agent_version": agent_version,
            "alias_id": alias_id,
        }
        if alias_name is not None:
            self._values["alias_name"] = alias_name

    @builtins.property
    def agent(self) -> "IAgent":
        '''(experimental) The underlying agent for this alias.

        :stability: experimental
        '''
        result = self._values.get("agent")
        assert result is not None, "Required property 'agent' is missing"
        return typing.cast("IAgent", result)

    @builtins.property
    def agent_version(self) -> builtins.str:
        '''(experimental) The agent version for this alias.

        :stability: experimental
        '''
        result = self._values.get("agent_version")
        assert result is not None, "Required property 'agent_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alias_id(self) -> builtins.str:
        '''(experimental) The Id of the agent alias.

        :stability: experimental
        '''
        result = self._values.get("alias_id")
        assert result is not None, "Required property 'alias_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alias_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the agent alias.

        :stability: experimental
        '''
        result = self._values.get("alias_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentAliasAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentAliasProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent": "agent",
        "agent_version": "agentVersion",
        "alias_name": "aliasName",
        "description": "description",
    },
)
class AgentAliasProps:
    def __init__(
        self,
        *,
        agent: "IAgent",
        agent_version: typing.Optional[builtins.str] = None,
        alias_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for creating a CDK-Managed Agent Alias.

        :param agent: (experimental) The agent associated to this alias.
        :param agent_version: (experimental) The version of the agent to associate with the agent alias. Default: - Creates a new version of the agent.
        :param alias_name: (experimental) The name for the agent alias. Default: - "latest-{hash}"
        :param description: (experimental) Description for the agent alias.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cae66eefc5f4c5599e0686171b63cba4b3c09493c31167b8afaa8bff00da6cc)
            check_type(argname="argument agent", value=agent, expected_type=type_hints["agent"])
            check_type(argname="argument agent_version", value=agent_version, expected_type=type_hints["agent_version"])
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent": agent,
        }
        if agent_version is not None:
            self._values["agent_version"] = agent_version
        if alias_name is not None:
            self._values["alias_name"] = alias_name
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def agent(self) -> "IAgent":
        '''(experimental) The agent associated to this alias.

        :stability: experimental
        '''
        result = self._values.get("agent")
        assert result is not None, "Required property 'agent' is missing"
        return typing.cast("IAgent", result)

    @builtins.property
    def agent_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the agent to associate with the agent alias.

        :default: - Creates a new version of the agent.

        :stability: experimental
        '''
        result = self._values.get("agent_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alias_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for the agent alias.

        :default: - "latest-{hash}"

        :stability: experimental
        '''
        result = self._values.get("alias_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description for the agent alias.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentAliasProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "agent_arn": "agentArn",
        "role_arn": "roleArn",
        "agent_version": "agentVersion",
        "kms_key_arn": "kmsKeyArn",
        "last_updated": "lastUpdated",
    },
)
class AgentAttributes:
    def __init__(
        self,
        *,
        agent_arn: builtins.str,
        role_arn: builtins.str,
        agent_version: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        last_updated: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Attributes for specifying an imported Bedrock Agent.

        :param agent_arn: (experimental) The ARN of the agent.
        :param role_arn: (experimental) The ARN of the IAM role associated to the agent.
        :param agent_version: (experimental) The agent version. If no explicit versions have been created, leave this empty to use the DRAFT version. Otherwise, use the version number (e.g. 1).
        :param kms_key_arn: (experimental) Optional KMS encryption key associated with this agent.
        :param last_updated: (experimental) When this agent was last updated.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae1875c8eb70cd3926525174ad613e977ffed1dda090873c972d973ad219927c)
            check_type(argname="argument agent_arn", value=agent_arn, expected_type=type_hints["agent_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument agent_version", value=agent_version, expected_type=type_hints["agent_version"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument last_updated", value=last_updated, expected_type=type_hints["last_updated"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_arn": agent_arn,
            "role_arn": role_arn,
        }
        if agent_version is not None:
            self._values["agent_version"] = agent_version
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if last_updated is not None:
            self._values["last_updated"] = last_updated

    @builtins.property
    def agent_arn(self) -> builtins.str:
        '''(experimental) The ARN of the agent.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:agent/OKDSJOGKMO"@attributeundefined
        '''
        result = self._values.get("agent_arn")
        assert result is not None, "Required property 'agent_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''(experimental) The ARN of the IAM role associated to the agent.

        :stability: experimental

        Example::

            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"@attributeundefined
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The agent version.

        If no explicit versions have been created,
        leave this  empty to use the DRAFT version. Otherwise, use the
        version number (e.g. 1).

        :stability: experimental
        '''
        result = self._values.get("agent_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional KMS encryption key associated with this agent.

        :stability: experimental
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_updated(self) -> typing.Optional[builtins.str]:
        '''(experimental) When this agent was last updated.

        :stability: experimental
        '''
        result = self._values.get("last_updated")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentProps",
    jsii_struct_bases=[],
    name_mapping={
        "foundation_model": "foundationModel",
        "instruction": "instruction",
        "action_groups": "actionGroups",
        "code_interpreter_enabled": "codeInterpreterEnabled",
        "description": "description",
        "existing_role": "existingRole",
        "force_delete": "forceDelete",
        "guardrail": "guardrail",
        "idle_session_ttl": "idleSessionTTL",
        "kms_key": "kmsKey",
        "knowledge_bases": "knowledgeBases",
        "name": "name",
        "prompt_override_configuration": "promptOverrideConfiguration",
        "should_prepare_agent": "shouldPrepareAgent",
        "user_input_enabled": "userInputEnabled",
    },
)
class AgentProps:
    def __init__(
        self,
        *,
        foundation_model: "IInvokable",
        instruction: builtins.str,
        action_groups: typing.Optional[typing.Sequence[AgentActionGroup]] = None,
        code_interpreter_enabled: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        force_delete: typing.Optional[builtins.bool] = None,
        guardrail: typing.Optional["IGuardrail"] = None,
        idle_session_ttl: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        knowledge_bases: typing.Optional[typing.Sequence["IKnowledgeBase"]] = None,
        name: typing.Optional[builtins.str] = None,
        prompt_override_configuration: typing.Optional["PromptOverrideConfiguration"] = None,
        should_prepare_agent: typing.Optional[builtins.bool] = None,
        user_input_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for creating a CDK managed Bedrock Agent.

        :param foundation_model: (experimental) The foundation model used for orchestration by the agent.
        :param instruction: (experimental) The instruction used by the agent. This determines how the agent will perform his task. This instruction must have a minimum of 40 characters.
        :param action_groups: (experimental) The Action Groups associated with the agent.
        :param code_interpreter_enabled: (experimental) Select whether the agent can generate, run, and troubleshoot code when trying to complete a task. Default: - false
        :param description: (experimental) A description of the agent. Default: - No description is provided.
        :param existing_role: (experimental) The existing IAM Role for the agent to use. Ensure the role has a trust policy that allows the Bedrock service to assume the role. Default: - A new role is created for you.
        :param force_delete: (experimental) Whether to delete the resource even if it's in use. Default: - true
        :param guardrail: (experimental) The guardrail that will be associated with the agent.
        :param idle_session_ttl: (experimental) How long sessions should be kept open for the agent. If no conversation occurs during this time, the session expires and Amazon Bedrock deletes any data provided before the timeout. Default: - 1 hour
        :param kms_key: (experimental) The KMS key of the agent if custom encryption is configured. Default: - An AWS managed key is used.
        :param knowledge_bases: (experimental) The KnowledgeBases associated with the agent.
        :param name: (experimental) The name of the agent. Default: - A name is generated by CDK.
        :param prompt_override_configuration: (experimental) Overrides some prompt templates in different parts of an agent sequence configuration. Default: - No overrides are provided.
        :param should_prepare_agent: (experimental) Specifies whether to automatically update the ``DRAFT`` version of the agent after making changes to the agent. The ``DRAFT`` version can be continually iterated upon during internal development. Default: - false
        :param user_input_enabled: (experimental) Select whether the agent can prompt additional information from the user when it does not have enough information to respond to an utterance. Default: - false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c5254c1c0482eaa66699188ff0467d936350a386bbe823d4ef46c9ba982f91c)
            check_type(argname="argument foundation_model", value=foundation_model, expected_type=type_hints["foundation_model"])
            check_type(argname="argument instruction", value=instruction, expected_type=type_hints["instruction"])
            check_type(argname="argument action_groups", value=action_groups, expected_type=type_hints["action_groups"])
            check_type(argname="argument code_interpreter_enabled", value=code_interpreter_enabled, expected_type=type_hints["code_interpreter_enabled"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument existing_role", value=existing_role, expected_type=type_hints["existing_role"])
            check_type(argname="argument force_delete", value=force_delete, expected_type=type_hints["force_delete"])
            check_type(argname="argument guardrail", value=guardrail, expected_type=type_hints["guardrail"])
            check_type(argname="argument idle_session_ttl", value=idle_session_ttl, expected_type=type_hints["idle_session_ttl"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument knowledge_bases", value=knowledge_bases, expected_type=type_hints["knowledge_bases"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument prompt_override_configuration", value=prompt_override_configuration, expected_type=type_hints["prompt_override_configuration"])
            check_type(argname="argument should_prepare_agent", value=should_prepare_agent, expected_type=type_hints["should_prepare_agent"])
            check_type(argname="argument user_input_enabled", value=user_input_enabled, expected_type=type_hints["user_input_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "foundation_model": foundation_model,
            "instruction": instruction,
        }
        if action_groups is not None:
            self._values["action_groups"] = action_groups
        if code_interpreter_enabled is not None:
            self._values["code_interpreter_enabled"] = code_interpreter_enabled
        if description is not None:
            self._values["description"] = description
        if existing_role is not None:
            self._values["existing_role"] = existing_role
        if force_delete is not None:
            self._values["force_delete"] = force_delete
        if guardrail is not None:
            self._values["guardrail"] = guardrail
        if idle_session_ttl is not None:
            self._values["idle_session_ttl"] = idle_session_ttl
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if knowledge_bases is not None:
            self._values["knowledge_bases"] = knowledge_bases
        if name is not None:
            self._values["name"] = name
        if prompt_override_configuration is not None:
            self._values["prompt_override_configuration"] = prompt_override_configuration
        if should_prepare_agent is not None:
            self._values["should_prepare_agent"] = should_prepare_agent
        if user_input_enabled is not None:
            self._values["user_input_enabled"] = user_input_enabled

    @builtins.property
    def foundation_model(self) -> "IInvokable":
        '''(experimental) The foundation model used for orchestration by the agent.

        :stability: experimental
        '''
        result = self._values.get("foundation_model")
        assert result is not None, "Required property 'foundation_model' is missing"
        return typing.cast("IInvokable", result)

    @builtins.property
    def instruction(self) -> builtins.str:
        '''(experimental) The instruction used by the agent.

        This determines how the agent will perform his task.
        This instruction must have a minimum of 40 characters.

        :stability: experimental
        '''
        result = self._values.get("instruction")
        assert result is not None, "Required property 'instruction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action_groups(self) -> typing.Optional[typing.List[AgentActionGroup]]:
        '''(experimental) The Action Groups associated with the agent.

        :stability: experimental
        '''
        result = self._values.get("action_groups")
        return typing.cast(typing.Optional[typing.List[AgentActionGroup]], result)

    @builtins.property
    def code_interpreter_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Select whether the agent can generate, run, and troubleshoot code when trying to complete a task.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("code_interpreter_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the agent.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def existing_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The existing IAM Role for the agent to use.

        Ensure the role has a trust policy that allows the Bedrock service to assume the role.

        :default: - A new role is created for you.

        :stability: experimental
        '''
        result = self._values.get("existing_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def force_delete(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to delete the resource even if it's in use.

        :default: - true

        :stability: experimental
        '''
        result = self._values.get("force_delete")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def guardrail(self) -> typing.Optional["IGuardrail"]:
        '''(experimental) The guardrail that will be associated with the agent.

        :stability: experimental
        '''
        result = self._values.get("guardrail")
        return typing.cast(typing.Optional["IGuardrail"], result)

    @builtins.property
    def idle_session_ttl(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) How long sessions should be kept open for the agent.

        If no conversation occurs
        during this time, the session expires and Amazon Bedrock deletes any data
        provided before the timeout.

        :default: - 1 hour

        :stability: experimental
        '''
        result = self._values.get("idle_session_ttl")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key of the agent if custom encryption is configured.

        :default: - An AWS managed key is used.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def knowledge_bases(self) -> typing.Optional[typing.List["IKnowledgeBase"]]:
        '''(experimental) The KnowledgeBases associated with the agent.

        :stability: experimental
        '''
        result = self._values.get("knowledge_bases")
        return typing.cast(typing.Optional[typing.List["IKnowledgeBase"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the agent.

        :default: - A name is generated by CDK.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prompt_override_configuration(
        self,
    ) -> typing.Optional["PromptOverrideConfiguration"]:
        '''(experimental) Overrides some prompt templates in different parts of an agent sequence configuration.

        :default: - No overrides are provided.

        :stability: experimental
        '''
        result = self._values.get("prompt_override_configuration")
        return typing.cast(typing.Optional["PromptOverrideConfiguration"], result)

    @builtins.property
    def should_prepare_agent(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to automatically update the ``DRAFT`` version of the agent after making changes to the agent.

        The ``DRAFT`` version can be continually iterated
        upon during internal development.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("should_prepare_agent")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def user_input_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Select whether the agent can prompt additional information from the user when it does not have enough information to respond to an utterance.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("user_input_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentStepType")
class AgentStepType(enum.Enum):
    '''(experimental) The step in the agent sequence where to set a specific prompt configuration.

    :stability: experimental
    '''

    PRE_PROCESSING = "PRE_PROCESSING"
    '''
    :stability: experimental
    '''
    ORCHESTRATION = "ORCHESTRATION"
    '''
    :stability: experimental
    '''
    POST_PROCESSING = "POST_PROCESSING"
    '''
    :stability: experimental
    '''
    KNOWLEDGE_BASE_RESPONSE_GENERATION = "KNOWLEDGE_BASE_RESPONSE_GENERATION"
    '''
    :stability: experimental
    '''


class ApiSchema(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ApiSchema",
):
    '''(experimental) Represents the concept of an API Schema for a Bedrock Agent Action Group.

    :stability: experimental
    '''

    def __init__(
        self,
        s3_file: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.Location, typing.Dict[builtins.str, typing.Any]]] = None,
        inline_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Constructor accessible only to extending classes.

        :param s3_file: -
        :param inline_schema: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9e9990488025ce0d3337500e926f885584cf0e74d3bd85a5bb26807188ae82a)
            check_type(argname="argument s3_file", value=s3_file, expected_type=type_hints["s3_file"])
            check_type(argname="argument inline_schema", value=inline_schema, expected_type=type_hints["inline_schema"])
        jsii.create(self.__class__, self, [s3_file, inline_schema])

    @jsii.member(jsii_name="fromInline")
    @builtins.classmethod
    def from_inline(cls, schema: builtins.str) -> "InlineApiSchema":
        '''(experimental) Creates an API Schema from an inline string.

        :param schema: - the JSON or YAML payload defining the OpenAPI schema for the action group.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c2792cc1fa0f16747e3820d17877eef4b648c9b158bc65527d5d5c852652166)
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        return typing.cast("InlineApiSchema", jsii.sinvoke(cls, "fromInline", [schema]))

    @jsii.member(jsii_name="fromLocalAsset")
    @builtins.classmethod
    def from_local_asset(cls, path: builtins.str) -> "InlineApiSchema":
        '''(experimental) Creates an API Schema from a local file.

        :param path: - the path to the local file containing the OpenAPI schema for the action group.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__054b5777af191a7d5068e3619e43fd80fa172483666692ce34f8e2f5ed6246f3)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("InlineApiSchema", jsii.sinvoke(cls, "fromLocalAsset", [path]))

    @jsii.member(jsii_name="fromS3File")
    @builtins.classmethod
    def from_s3_file(
        cls,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        object_key: builtins.str,
    ) -> "S3ApiSchema":
        '''(experimental) Creates an API Schema from an S3 File.

        :param bucket: - the bucket containing the local file containing the OpenAPI schema for the action group.
        :param object_key: - object key in the bucket.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e985add44eef93f1230fa0ea2845a5132786479af068992c0d8ab98020ad9c58)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument object_key", value=object_key, expected_type=type_hints["object_key"])
        return typing.cast("S3ApiSchema", jsii.sinvoke(cls, "fromS3File", [bucket, object_key]))

    @builtins.property
    @jsii.member(jsii_name="inlineSchema")
    def inline_schema(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inlineSchema"))

    @builtins.property
    @jsii.member(jsii_name="s3File")
    def s3_file(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.Location]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.Location], jsii.get(self, "s3File"))


class _ApiSchemaProxy(ApiSchema):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ApiSchema).__jsii_proxy_class__ = lambda : _ApiSchemaProxy


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ApplicationInferenceProfileAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "inference_profile_arn": "inferenceProfileArn",
        "inference_profile_identifier": "inferenceProfileIdentifier",
    },
)
class ApplicationInferenceProfileAttributes:
    def __init__(
        self,
        *,
        inference_profile_arn: builtins.str,
        inference_profile_identifier: builtins.str,
    ) -> None:
        '''(experimental) ****************************************************************************                     ATTRS FOR IMPORTED CONSTRUCT ***************************************************************************.

        :param inference_profile_arn: (experimental) The ARN of the application inference profile.
        :param inference_profile_identifier: (experimental) The ID or Amazon Resource Name (ARN) of the inference profile.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48ea34e402b2535f2082177ac38775e1034896579d3693772035c4f45ca2d654)
            check_type(argname="argument inference_profile_arn", value=inference_profile_arn, expected_type=type_hints["inference_profile_arn"])
            check_type(argname="argument inference_profile_identifier", value=inference_profile_identifier, expected_type=type_hints["inference_profile_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "inference_profile_arn": inference_profile_arn,
            "inference_profile_identifier": inference_profile_identifier,
        }

    @builtins.property
    def inference_profile_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application inference profile.

        :stability: experimental
        '''
        result = self._values.get("inference_profile_arn")
        assert result is not None, "Required property 'inference_profile_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def inference_profile_identifier(self) -> builtins.str:
        '''(experimental) The ID or Amazon Resource Name (ARN) of the inference profile.

        :stability: experimental
        '''
        result = self._values.get("inference_profile_identifier")
        assert result is not None, "Required property 'inference_profile_identifier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationInferenceProfileAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ApplicationInferenceProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "inference_profile_name": "inferenceProfileName",
        "model_source": "modelSource",
        "description": "description",
        "tags": "tags",
    },
)
class ApplicationInferenceProfileProps:
    def __init__(
        self,
        *,
        inference_profile_name: builtins.str,
        model_source: "IInvokable",
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Properties for creating a ApplicationInferenceProfile.

        :param inference_profile_name: (experimental) The name of the inference profile.
        :param model_source: (experimental) To create an application inference profile for one Region, specify a foundation model. Usage and costs for requests made to that Region with that model will be tracked. To create an application inference profile for multiple Regions, specify a cross region (system-defined) inference profile. The inference profile will route requests to the Regions defined in the cross region (system-defined) inference profile that you choose. Usage and costs for requests made to the Regions in the inference profile will be tracked.
        :param description: (experimental) Description of the inference profile.
        :param tags: (experimental) A list of tags associated with the inference profile.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c9200d651e22ff89688db78ff2bdec2a56b7d93a7d2cb347b49efafe13b581c)
            check_type(argname="argument inference_profile_name", value=inference_profile_name, expected_type=type_hints["inference_profile_name"])
            check_type(argname="argument model_source", value=model_source, expected_type=type_hints["model_source"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "inference_profile_name": inference_profile_name,
            "model_source": model_source,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def inference_profile_name(self) -> builtins.str:
        '''(experimental) The name of the inference profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-applicationinferenceprofile.html#cfn-bedrock-applicationinferenceprofile-inferenceprofilename
        :stability: experimental
        '''
        result = self._values.get("inference_profile_name")
        assert result is not None, "Required property 'inference_profile_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def model_source(self) -> "IInvokable":
        '''(experimental) To create an application inference profile for one Region, specify a foundation model.

        Usage and costs for requests made to that Region with that model will be tracked.

        To create an application inference profile for multiple Regions,
        specify a cross region (system-defined) inference profile.
        The inference profile will route requests to the Regions defined in
        the cross region (system-defined) inference profile that you choose.
        Usage and costs for requests made to the Regions in the inference profile will be tracked.

        :stability: experimental
        '''
        result = self._values.get("model_source")
        assert result is not None, "Required property 'model_source' is missing"
        return typing.cast("IInvokable", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of the inference profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-applicationinferenceprofile.html#cfn-bedrock-applicationinferenceprofile-description
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''(experimental) A list of tags associated with the inference profile.

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationInferenceProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.BedrockFoundationModelProps",
    jsii_struct_bases=[],
    name_mapping={
        "supported_vector_type": "supportedVectorType",
        "supports_agents": "supportsAgents",
        "supports_cross_region": "supportsCrossRegion",
        "supports_knowledge_base": "supportsKnowledgeBase",
        "vector_dimensions": "vectorDimensions",
    },
)
class BedrockFoundationModelProps:
    def __init__(
        self,
        *,
        supported_vector_type: typing.Optional[typing.Sequence["VectorType"]] = None,
        supports_agents: typing.Optional[builtins.bool] = None,
        supports_cross_region: typing.Optional[builtins.bool] = None,
        supports_knowledge_base: typing.Optional[builtins.bool] = None,
        vector_dimensions: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param supported_vector_type: (experimental) Embeddings models have different supported vector types.
        :param supports_agents: (experimental) Bedrock Agents can use this model. Default: - false
        :param supports_cross_region: (experimental) Can be used with a Cross-Region Inference Profile. Default: - false
        :param supports_knowledge_base: (experimental) Bedrock Knowledge Base can use this model. Default: - false
        :param vector_dimensions: (experimental) Embedding models have different vector dimensions. Only applicable for embedding models.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e1a21a71ca2d85f4b0cb18a5ce955b8c59bb0c4403b3d6f750c90739061d548)
            check_type(argname="argument supported_vector_type", value=supported_vector_type, expected_type=type_hints["supported_vector_type"])
            check_type(argname="argument supports_agents", value=supports_agents, expected_type=type_hints["supports_agents"])
            check_type(argname="argument supports_cross_region", value=supports_cross_region, expected_type=type_hints["supports_cross_region"])
            check_type(argname="argument supports_knowledge_base", value=supports_knowledge_base, expected_type=type_hints["supports_knowledge_base"])
            check_type(argname="argument vector_dimensions", value=vector_dimensions, expected_type=type_hints["vector_dimensions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if supported_vector_type is not None:
            self._values["supported_vector_type"] = supported_vector_type
        if supports_agents is not None:
            self._values["supports_agents"] = supports_agents
        if supports_cross_region is not None:
            self._values["supports_cross_region"] = supports_cross_region
        if supports_knowledge_base is not None:
            self._values["supports_knowledge_base"] = supports_knowledge_base
        if vector_dimensions is not None:
            self._values["vector_dimensions"] = vector_dimensions

    @builtins.property
    def supported_vector_type(self) -> typing.Optional[typing.List["VectorType"]]:
        '''(experimental) Embeddings models have different supported vector types.

        :stability: experimental
        '''
        result = self._values.get("supported_vector_type")
        return typing.cast(typing.Optional[typing.List["VectorType"]], result)

    @builtins.property
    def supports_agents(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Bedrock Agents can use this model.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("supports_agents")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def supports_cross_region(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Can be used with a Cross-Region Inference Profile.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("supports_cross_region")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def supports_knowledge_base(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Bedrock Knowledge Base can use this model.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("supports_knowledge_base")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vector_dimensions(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Embedding models have different vector dimensions.

        Only applicable for embedding models.

        :stability: experimental
        '''
        result = self._values.get("vector_dimensions")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockFoundationModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChatMessage(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ChatMessage",
):
    '''
    :stability: experimental
    '''

    def __init__(self, role: "ChatMessageRole", text: builtins.str) -> None:
        '''
        :param role: -
        :param text: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134f5f0222c6822adcdaa44fe72c823a3907b61a0e4f1dc0a388befd7e412755)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        jsii.create(self.__class__, self, [role, text])

    @jsii.member(jsii_name="assistant")
    @builtins.classmethod
    def assistant(cls, text: builtins.str) -> "ChatMessage":
        '''
        :param text: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5063cf1ecc7fe858c159acb9c143817eaaf014910bfb9cc7c9f7cfdbb225227)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        return typing.cast("ChatMessage", jsii.sinvoke(cls, "assistant", [text]))

    @jsii.member(jsii_name="user")
    @builtins.classmethod
    def user(cls, text: builtins.str) -> "ChatMessage":
        '''
        :param text: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e85bd735be93f1bf58d001d28c9e0b750bc2a7477c6bb774c806f0be1b6c8fa)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        return typing.cast("ChatMessage", jsii.sinvoke(cls, "user", [text]))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> "ChatMessageRole":
        '''
        :stability: experimental
        '''
        return typing.cast("ChatMessageRole", jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "text"))


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ChatMessageRole")
class ChatMessageRole(enum.Enum):
    '''
    :stability: experimental
    '''

    USER = "USER"
    '''(experimental) This role represents the human user in the conversation.

    Inputs from the
    user guide  the conversation and prompt responses from the assistant.

    :stability: experimental
    '''
    ASSISTANT = "ASSISTANT"
    '''(experimental) This is the role of the model itself, responding to user inputs based on the context set by the system.

    :stability: experimental
    '''


class ChunkingStrategy(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ChunkingStrategy",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="fixedSize")
    @builtins.classmethod
    def fixed_size(
        cls,
        *,
        max_tokens: jsii.Number,
        overlap_percentage: jsii.Number,
    ) -> "ChunkingStrategy":
        '''(experimental) Method for customizing a fixed sized chunking strategy.

        :param max_tokens: The maximum number of tokens to include in a chunk.
        :param overlap_percentage: The percentage of overlap between adjacent chunks of a data source.

        :stability: experimental
        '''
        props = _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.FixedSizeChunkingConfigurationProperty(
            max_tokens=max_tokens, overlap_percentage=overlap_percentage
        )

        return typing.cast("ChunkingStrategy", jsii.sinvoke(cls, "fixedSize", [props]))

    @jsii.member(jsii_name="hierarchical")
    @builtins.classmethod
    def hierarchical(
        cls,
        *,
        max_child_token_size: jsii.Number,
        max_parent_token_size: jsii.Number,
        overlap_tokens: jsii.Number,
    ) -> "ChunkingStrategy":
        '''(experimental) Method for customizing a hierarchical chunking strategy.

        For custom chunking, the maximum token chunk size depends on the model.

        - Amazon Titan Text Embeddings: 8192
        - Cohere Embed models: 512

        :param max_child_token_size: (experimental) Maximum number of tokens that a child chunk can contain. Keep in mind the maximum chunk size depends on the embedding model chosen.
        :param max_parent_token_size: (experimental) Maximum number of tokens that a parent chunk can contain. Keep in mind the maximum chunk size depends on the embedding model chosen.
        :param overlap_tokens: (experimental) The overlap tokens between adjacent chunks.

        :stability: experimental
        '''
        props = HierarchicalChunkingProps(
            max_child_token_size=max_child_token_size,
            max_parent_token_size=max_parent_token_size,
            overlap_tokens=overlap_tokens,
        )

        return typing.cast("ChunkingStrategy", jsii.sinvoke(cls, "hierarchical", [props]))

    @jsii.member(jsii_name="semantic")
    @builtins.classmethod
    def semantic(
        cls,
        *,
        breakpoint_percentile_threshold: jsii.Number,
        buffer_size: jsii.Number,
        max_tokens: jsii.Number,
    ) -> "ChunkingStrategy":
        '''(experimental) Method for customizing a semantic chunking strategy.

        For custom chunking, the maximum token chunk size depends on the model.

        - Amazon Titan Text Embeddings: 8192
        - Cohere Embed models: 512

        :param breakpoint_percentile_threshold: The dissimilarity threshold for splitting chunks.
        :param buffer_size: The buffer size.
        :param max_tokens: The maximum number of tokens that a chunk can contain.

        :stability: experimental
        '''
        props = _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.SemanticChunkingConfigurationProperty(
            breakpoint_percentile_threshold=breakpoint_percentile_threshold,
            buffer_size=buffer_size,
            max_tokens=max_tokens,
        )

        return typing.cast("ChunkingStrategy", jsii.sinvoke(cls, "semantic", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT")
    def DEFAULT(cls) -> "ChunkingStrategy":
        '''(experimental) Fixed Sized Chunking with the default chunk size of 300 tokens and 20% overlap.

        :stability: experimental
        '''
        return typing.cast("ChunkingStrategy", jsii.sget(cls, "DEFAULT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FIXED_SIZE")
    def FIXED_SIZE(cls) -> "ChunkingStrategy":
        '''(experimental) Fixed Sized Chunking with the default chunk size of 300 tokens and 20% overlap.

        You can adjust these values based on your specific requirements using the
        ``ChunkingStrategy.fixedSize(params)`` method.

        :stability: experimental
        '''
        return typing.cast("ChunkingStrategy", jsii.sget(cls, "FIXED_SIZE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HIERARCHICAL_COHERE")
    def HIERARCHICAL_COHERE(cls) -> "ChunkingStrategy":
        '''(experimental) Hierarchical Chunking with the default for Cohere Models.

        - Overlap tokens: 30
        - Max parent token size: 500
        - Max child token size: 100

        :stability: experimental
        '''
        return typing.cast("ChunkingStrategy", jsii.sget(cls, "HIERARCHICAL_COHERE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HIERARCHICAL_TITAN")
    def HIERARCHICAL_TITAN(cls) -> "ChunkingStrategy":
        '''(experimental) Hierarchical Chunking with the default for Titan Models.

        - Overlap tokens: 60
        - Max parent token size: 1500
        - Max child token size: 300

        :stability: experimental
        '''
        return typing.cast("ChunkingStrategy", jsii.sget(cls, "HIERARCHICAL_TITAN"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NONE")
    def NONE(cls) -> "ChunkingStrategy":
        '''(experimental) Amazon Bedrock treats each file as one chunk.

        Suitable for documents that
        are already pre-processed or text split.

        :stability: experimental
        '''
        return typing.cast("ChunkingStrategy", jsii.sget(cls, "NONE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SEMANTIC")
    def SEMANTIC(cls) -> "ChunkingStrategy":
        '''(experimental) Semantic Chunking with the default of bufferSize: 0, breakpointPercentileThreshold: 95, and maxTokens: 300.

        You can adjust these values based on your specific requirements using the
        ``ChunkingStrategy.semantic(params)`` method.

        :stability: experimental
        '''
        return typing.cast("ChunkingStrategy", jsii.sget(cls, "SEMANTIC"))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    @abc.abstractmethod
    def configuration(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ChunkingConfigurationProperty:
        '''(experimental) The CloudFormation property representation of this configuration.

        :stability: experimental
        '''
        ...

    @configuration.setter
    @abc.abstractmethod
    def configuration(
        self,
        value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ChunkingConfigurationProperty,
    ) -> None:
        ...


class _ChunkingStrategyProxy(ChunkingStrategy):
    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ChunkingConfigurationProperty:
        '''(experimental) The CloudFormation property representation of this configuration.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ChunkingConfigurationProperty, jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(
        self,
        value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ChunkingConfigurationProperty,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc8c95b7bfa78b1915cee9f049873d2af67238c73953179ae4f9479b54751ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ChunkingStrategy).__jsii_proxy_class__ = lambda : _ChunkingStrategyProxy


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CommonKnowledgeBaseAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "execution_role_arn": "executionRoleArn",
        "knowledge_base_id": "knowledgeBaseId",
        "description": "description",
        "instruction": "instruction",
        "knowledge_base_state": "knowledgeBaseState",
    },
)
class CommonKnowledgeBaseAttributes:
    def __init__(
        self,
        *,
        execution_role_arn: builtins.str,
        knowledge_base_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        instruction: typing.Optional[builtins.str] = None,
        knowledge_base_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Common properties for importing a knowledge base (of any type) created outside of this stack.

        :param execution_role_arn: (experimental) The Service Execution Role associated with the knowledge base.
        :param knowledge_base_id: (experimental) The ID of the knowledge base.
        :param description: (experimental) The description of the knowledge base. Default: - No description provided.
        :param instruction: (experimental) Instructions for agents based on the design and type of information of the Knowledge Base. This will impact how Agents interact with the Knowledge Base. Default: - No description provided.
        :param knowledge_base_state: (experimental) Specifies whether to use the knowledge base or not when sending an InvokeAgent request. Default: - ENABLED

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e39ca943fffc8eee1fd4bcb58c8e99b2ceda8714caf2e11e757c97dc51b4a9e)
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument knowledge_base_id", value=knowledge_base_id, expected_type=type_hints["knowledge_base_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument instruction", value=instruction, expected_type=type_hints["instruction"])
            check_type(argname="argument knowledge_base_state", value=knowledge_base_state, expected_type=type_hints["knowledge_base_state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execution_role_arn": execution_role_arn,
            "knowledge_base_id": knowledge_base_id,
        }
        if description is not None:
            self._values["description"] = description
        if instruction is not None:
            self._values["instruction"] = instruction
        if knowledge_base_state is not None:
            self._values["knowledge_base_state"] = knowledge_base_state

    @builtins.property
    def execution_role_arn(self) -> builtins.str:
        '''(experimental) The Service Execution Role associated with the knowledge base.

        :stability: experimental

        Example::

            "arn:aws:iam::123456789012:role/AmazonBedrockExecutionRoleForKnowledgeBaseawscdkbdgeBaseKB12345678"
        '''
        result = self._values.get("execution_role_arn")
        assert result is not None, "Required property 'execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def knowledge_base_id(self) -> builtins.str:
        '''(experimental) The ID of the knowledge base.

        :stability: experimental

        Example::

            "KB12345678"
        '''
        result = self._values.get("knowledge_base_id")
        assert result is not None, "Required property 'knowledge_base_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the knowledge base.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) Instructions for agents based on the design and type of information of the Knowledge Base.

        This will impact how Agents interact with the Knowledge Base.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("instruction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def knowledge_base_state(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies whether to use the knowledge base or not when sending an InvokeAgent request.

        :default: - ENABLED

        :stability: experimental
        '''
        result = self._values.get("knowledge_base_state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonKnowledgeBaseAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CommonKnowledgeBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "existing_role": "existingRole",
        "instruction": "instruction",
        "name": "name",
    },
)
class CommonKnowledgeBaseProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        instruction: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Common properties for creating any type of new Knowledge Base.

        :param description: (experimental) The description of the knowledge base. Default: - No description provided.
        :param existing_role: (experimental) Existing IAM role with policy statements granting appropriate permissions to invoke the specific embeddings models. Any entity (e.g., an AWS service or application) that assumes this role will be able to invoke or use the specified embeddings model within the Bedrock service.
        :param instruction: (experimental) A narrative description of the knowledge base. A Bedrock Agent can use this instruction to determine if it should query this Knowledge Base. Default: - No description provided.
        :param name: (experimental) The name of the knowledge base.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b338369fcf3800b974be16fc9d16c5bbb6e844c94ab39431bdb5db8741f5f7a)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument existing_role", value=existing_role, expected_type=type_hints["existing_role"])
            check_type(argname="argument instruction", value=instruction, expected_type=type_hints["instruction"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if existing_role is not None:
            self._values["existing_role"] = existing_role
        if instruction is not None:
            self._values["instruction"] = instruction
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the knowledge base.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def existing_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) Existing IAM role with policy statements granting appropriate permissions to invoke the specific embeddings models.

        Any entity (e.g., an AWS service or application) that assumes
        this role will be able to invoke or use the
        specified embeddings model within the Bedrock service.

        :stability: experimental
        '''
        result = self._values.get("existing_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) A narrative description of the knowledge base.

        A Bedrock Agent can use this instruction to determine if it should
        query this Knowledge Base.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("instruction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the knowledge base.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonKnowledgeBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CommonPromptVariantProps",
    jsii_struct_bases=[],
    name_mapping={
        "model": "model",
        "variant_name": "variantName",
        "prompt_variables": "promptVariables",
    },
)
class CommonPromptVariantProps:
    def __init__(
        self,
        *,
        model: "IInvokable",
        variant_name: builtins.str,
        prompt_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param model: (experimental) The model which is used to run the prompt. The model could be a foundation model, a custom model, or a provisioned model.
        :param variant_name: (experimental) The name of the prompt variant.
        :param prompt_variables: (experimental) The variables in the prompt template that can be filled in at runtime.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb2752ca933595bdb580dc70b29b9d7fea9196785967ed1f46d44fff8b435477)
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
            check_type(argname="argument variant_name", value=variant_name, expected_type=type_hints["variant_name"])
            check_type(argname="argument prompt_variables", value=prompt_variables, expected_type=type_hints["prompt_variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "model": model,
            "variant_name": variant_name,
        }
        if prompt_variables is not None:
            self._values["prompt_variables"] = prompt_variables

    @builtins.property
    def model(self) -> "IInvokable":
        '''(experimental) The model which is used to run the prompt.

        The model could be a foundation
        model, a custom model, or a provisioned model.

        :stability: experimental
        '''
        result = self._values.get("model")
        assert result is not None, "Required property 'model' is missing"
        return typing.cast("IInvokable", result)

    @builtins.property
    def variant_name(self) -> builtins.str:
        '''(experimental) The name of the prompt variant.

        :stability: experimental
        '''
        result = self._values.get("variant_name")
        assert result is not None, "Required property 'variant_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prompt_variables(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The variables in the prompt template that can be filled in at runtime.

        :stability: experimental
        '''
        result = self._values.get("prompt_variables")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonPromptVariantProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ConfluenceCrawlingFilters",
    jsii_struct_bases=[],
    name_mapping={
        "object_type": "objectType",
        "exclude_patterns": "excludePatterns",
        "include_patterns": "includePatterns",
    },
)
class ConfluenceCrawlingFilters:
    def __init__(
        self,
        *,
        object_type: "ConfluenceObjectType",
        exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Defines filters for crawling Confluence content.

        These filters allow you to include or exclude specific content based on object types and patterns.

        - For Spaces: Use the unique space key
        - For Pages: Use the main page title
        - For Blogs: Use the main blog title
        - For Comments: Use "Re: Page/Blog Title"
        - For Attachments: Use the filename with extension

        :param object_type: (experimental) The type of Confluence object to apply the filters to.
        :param exclude_patterns: (experimental) Regular expression patterns to exclude content. Content matching these patterns will not be crawled, even if it matches an include pattern.
        :param include_patterns: (experimental) Regular expression patterns to include content. If specified, only content matching these patterns will be crawled.

        :stability: experimental
        :remarks:

        - You can specify inclusion and exclusion patterns using regular expressions.
        - If both inclusion and exclusion patterns match a document, the exclusion takes precedence.

        Example::

            {
              objectType: ConfluenceObjectType.ATTACHMENT,
              excludePatterns: [".*private.*\\.pdf"]
            }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba4b91ab5b955d9d72d8af6f07cdc07ac568ef117419de41dca7871ad32d6b8)
            check_type(argname="argument object_type", value=object_type, expected_type=type_hints["object_type"])
            check_type(argname="argument exclude_patterns", value=exclude_patterns, expected_type=type_hints["exclude_patterns"])
            check_type(argname="argument include_patterns", value=include_patterns, expected_type=type_hints["include_patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_type": object_type,
        }
        if exclude_patterns is not None:
            self._values["exclude_patterns"] = exclude_patterns
        if include_patterns is not None:
            self._values["include_patterns"] = include_patterns

    @builtins.property
    def object_type(self) -> "ConfluenceObjectType":
        '''(experimental) The type of Confluence object to apply the filters to.

        :stability: experimental
        '''
        result = self._values.get("object_type")
        assert result is not None, "Required property 'object_type' is missing"
        return typing.cast("ConfluenceObjectType", result)

    @builtins.property
    def exclude_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Regular expression patterns to exclude content.

        Content matching these patterns will not be crawled, even if it matches an include pattern.

        :stability: experimental
        '''
        result = self._values.get("exclude_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Regular expression patterns to include content.

        If specified, only content matching these patterns will be crawled.

        :stability: experimental
        '''
        result = self._values.get("include_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfluenceCrawlingFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ConfluenceDataSourceAuthType"
)
class ConfluenceDataSourceAuthType(enum.Enum):
    '''(experimental) The different authentication types available to connect to your Confluence instance.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/confluence-data-source-connector.html#configuration-confluence-connector
    :stability: experimental
    '''

    OAUTH2_CLIENT_CREDENTIALS = "OAUTH2_CLIENT_CREDENTIALS"
    '''(experimental) Your secret authentication credentials in AWS Secrets Manager should include: - ``confluenceAppKey`` - ``confluenceAppSecret`` - ``confluenceAccessToken`` - ``confluenceRefreshToken``.

    :stability: experimental
    '''
    BASIC = "BASIC"
    '''(experimental) Your secret authentication credentials in AWS Secrets Manager should include:  - ``username`` (email of admin account)  - ``password`` (API token).

    :stability: experimental
    '''


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ConfluenceObjectType"
)
class ConfluenceObjectType(enum.Enum):
    '''(experimental) Represents the different types of content objects in Confluence that can be crawled by the data source.

    :stability: experimental
    '''

    SPACE = "SPACE"
    '''
    :stability: experimental
    '''
    PAGE = "PAGE"
    '''
    :stability: experimental
    '''
    BLOG = "BLOG"
    '''
    :stability: experimental
    '''
    COMMENT = "COMMENT"
    '''
    :stability: experimental
    '''
    ATTACHMENT = "ATTACHMENT"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ContentFilter",
    jsii_struct_bases=[],
    name_mapping={
        "input_strength": "inputStrength",
        "output_strength": "outputStrength",
        "type": "type",
    },
)
class ContentFilter:
    def __init__(
        self,
        *,
        input_strength: "ContentFilterStrength",
        output_strength: "ContentFilterStrength",
        type: "ContentFilterType",
    ) -> None:
        '''(experimental) Interface to declare a content filter.

        :param input_strength: (experimental) The strength of the content filter to apply to prompts / user input.
        :param output_strength: (experimental) The strength of the content filter to apply to model responses.
        :param type: (experimental) The type of harmful category that the content filter is applied to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a9140c0049260b2d312c4a80d1b958e9761476560ef6b565d603fce991e815)
            check_type(argname="argument input_strength", value=input_strength, expected_type=type_hints["input_strength"])
            check_type(argname="argument output_strength", value=output_strength, expected_type=type_hints["output_strength"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "input_strength": input_strength,
            "output_strength": output_strength,
            "type": type,
        }

    @builtins.property
    def input_strength(self) -> "ContentFilterStrength":
        '''(experimental) The strength of the content filter to apply to prompts / user input.

        :stability: experimental
        '''
        result = self._values.get("input_strength")
        assert result is not None, "Required property 'input_strength' is missing"
        return typing.cast("ContentFilterStrength", result)

    @builtins.property
    def output_strength(self) -> "ContentFilterStrength":
        '''(experimental) The strength of the content filter to apply to model responses.

        :stability: experimental
        '''
        result = self._values.get("output_strength")
        assert result is not None, "Required property 'output_strength' is missing"
        return typing.cast("ContentFilterStrength", result)

    @builtins.property
    def type(self) -> "ContentFilterType":
        '''(experimental) The type of harmful category that the content filter is applied to.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("ContentFilterType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContentFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ContentFilterStrength"
)
class ContentFilterStrength(enum.Enum):
    '''(experimental) The strength of the content filter.

    As you increase the filter strength,
    the likelihood of filtering harmful content increases and the probability
    of seeing harmful content in your application reduces.

    :stability: experimental
    '''

    NONE = "NONE"
    '''
    :stability: experimental
    '''
    LOW = "LOW"
    '''
    :stability: experimental
    '''
    MEDIUM = "MEDIUM"
    '''
    :stability: experimental
    '''
    HIGH = "HIGH"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ContentFilterType")
class ContentFilterType(enum.Enum):
    '''(experimental) The type of harmful category usable in a content filter.

    :stability: experimental
    '''

    SEXUAL = "SEXUAL"
    '''(experimental) Describes input prompts and model responses that indicates sexual interest, activity, or arousal using direct or indirect references to body parts, physical traits, or sex.

    :stability: experimental
    '''
    VIOLENCE = "VIOLENCE"
    '''(experimental) Describes input prompts and model responses that includes glorification of or threats to inflict physical pain, hurt, or injury toward a person, group or thing.

    :stability: experimental
    '''
    HATE = "HATE"
    '''(experimental) Describes input prompts and model responses that discriminate, criticize, insult, denounce, or dehumanize a person or group on the basis of an identity (such as race, ethnicity, gender, religion, sexual orientation, ability, and national origin).

    :stability: experimental
    '''
    INSULTS = "INSULTS"
    '''(experimental) Describes input prompts and model responses that includes demeaning, humiliating, mocking, insulting, or belittling language.

    This type of language is also labeled
    as bullying.

    :stability: experimental
    '''
    MISCONDUCT = "MISCONDUCT"
    '''(experimental) Describes input prompts and model responses that seeks or provides information about engaging in misconduct activity, or harming, defrauding, or taking advantage of a person, group or institution.

    :stability: experimental
    '''
    PROMPT_ATTACK = "PROMPT_ATTACK"
    '''(experimental) Enable to detect and block user inputs attempting to override system instructions.

    To avoid misclassifying system prompts as a prompt attack and ensure that the filters
    are selectively applied to user inputs, use input tagging.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ContextualGroundingFilter",
    jsii_struct_bases=[],
    name_mapping={"threshold": "threshold", "type": "type"},
)
class ContextualGroundingFilter:
    def __init__(
        self,
        *,
        threshold: jsii.Number,
        type: "ContextualGroundingFilterType",
    ) -> None:
        '''(experimental) Interface to define a Contextual Grounding Filter.

        :param threshold: (experimental) The threshold for the contextual grounding filter. - ``0`` (blocks nothing) - ``0.99`` (blocks almost everything)
        :param type: (experimental) The type of contextual grounding filter.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e4288f485be62d723f6fe133287e8c88a90f455b2dec35e5c4095e4ba4cd69)
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
            "type": type,
        }

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''(experimental) The threshold for the contextual grounding filter.

        - ``0`` (blocks nothing)
        - ``0.99`` (blocks almost everything)

        :stability: experimental
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> "ContextualGroundingFilterType":
        '''(experimental) The type of contextual grounding filter.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("ContextualGroundingFilterType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContextualGroundingFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ContextualGroundingFilterType"
)
class ContextualGroundingFilterType(enum.Enum):
    '''(experimental) The type of contextual grounding filter.

    :stability: experimental
    '''

    GROUNDING = "GROUNDING"
    '''(experimental) Grounding score represents the confidence that the model response is factually correct and grounded in the source.

    If the model response has a lower score than
    the defined threshold, the response will be blocked and the configured blocked
    message will be returned to the user. A higher threshold level blocks more responses.

    :stability: experimental
    '''
    RELEVANCE = "RELEVANCE"
    '''(experimental) Relevance score represents the confidence that the model response is relevant to the user's query.

    If the model response has a lower score than the defined
    threshold, the response will be blocked and the configured blocked message will
    be returned to the user. A higher threshold level blocks more responses.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CrawlingFilters",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_patterns": "excludePatterns",
        "include_patterns": "includePatterns",
    },
)
class CrawlingFilters:
    def __init__(
        self,
        *,
        exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) The filters (regular expression patterns) to include or exclude in the crawling in accordance with your scope.

        :param exclude_patterns: (experimental) Exclude paths.
        :param include_patterns: (experimental) Include patterns.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf8789f899b4cf122996f24d6718a644cc2bc6a74788ac86472a28afaba4e33f)
            check_type(argname="argument exclude_patterns", value=exclude_patterns, expected_type=type_hints["exclude_patterns"])
            check_type(argname="argument include_patterns", value=include_patterns, expected_type=type_hints["include_patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_patterns is not None:
            self._values["exclude_patterns"] = exclude_patterns
        if include_patterns is not None:
            self._values["include_patterns"] = include_patterns

    @builtins.property
    def exclude_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Exclude paths.

        :stability: experimental
        '''
        result = self._values.get("exclude_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Include patterns.

        :stability: experimental
        '''
        result = self._values.get("include_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrawlingFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CrawlingScope")
class CrawlingScope(enum.Enum):
    '''(experimental) The scope of the crawling.

    :stability: experimental
    '''

    HOST_ONLY = "HOST_ONLY"
    '''(experimental) Crawls only web pages that belong to the same host or primary domain.

    :stability: experimental
    '''
    SUBDOMAINS = "SUBDOMAINS"
    '''(experimental) Includes subdomains in addition to the host or primary domain, i.e. web pages that contain "aws.amazon.com" can also include sub domain "docs.aws.amazon.com".

    :stability: experimental
    '''
    DEFAULT = "DEFAULT"
    '''(experimental) Limit crawling to web pages that belong to the same host and with the same initial URL path.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CrossRegionInferenceProfileProps",
    jsii_struct_bases=[],
    name_mapping={"geo_region": "geoRegion", "model": "model"},
)
class CrossRegionInferenceProfileProps:
    def __init__(
        self,
        *,
        geo_region: "CrossRegionInferenceProfileRegion",
        model: "BedrockFoundationModel",
    ) -> None:
        '''(experimental) ****************************************************************************                       PROPS FOR NEW CONSTRUCT ***************************************************************************.

        :param geo_region: (experimental) The geographic region where the traffic is going to be distributed. Routing factors in user traffic, demand and utilization of resources.
        :param model: (experimental) A model supporting cross-region inference.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0779b391b71e321d48d3445f56e45aa413e6050e51f0b7161ca653bdbdd424ab)
            check_type(argname="argument geo_region", value=geo_region, expected_type=type_hints["geo_region"])
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "geo_region": geo_region,
            "model": model,
        }

    @builtins.property
    def geo_region(self) -> "CrossRegionInferenceProfileRegion":
        '''(experimental) The geographic region where the traffic is going to be distributed.

        Routing
        factors in user traffic, demand and utilization of resources.

        :stability: experimental
        '''
        result = self._values.get("geo_region")
        assert result is not None, "Required property 'geo_region' is missing"
        return typing.cast("CrossRegionInferenceProfileRegion", result)

    @builtins.property
    def model(self) -> "BedrockFoundationModel":
        '''(experimental) A model supporting cross-region inference.

        :see: https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference-support.html
        :stability: experimental
        '''
        result = self._values.get("model")
        assert result is not None, "Required property 'model' is missing"
        return typing.cast("BedrockFoundationModel", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrossRegionInferenceProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CrossRegionInferenceProfileRegion"
)
class CrossRegionInferenceProfileRegion(enum.Enum):
    '''
    :stability: experimental
    '''

    EU = "EU"
    '''(experimental) Cross-region Inference Identifier for the European area.

    According to the model chosen, this might include:

    - Frankfurt (``eu-central-1``)
    - Ireland (``eu-west-1``)
    - Paris (``eu-west-3``)

    :stability: experimental
    '''
    US = "US"
    '''(experimental) Cross-region Inference Identifier for the United States area.

    According to the model chosen, this might include:

    - N. Virginia (``us-east-1``)
    - Oregon (``us-west-2``)
    - Ohio (``us-east-2``)

    :stability: experimental
    '''
    APAC = "APAC"
    '''(experimental) Cross-region Inference Identifier for the Asia-Pacific area.

    According to the model chosen, this might include:

    - Tokyo (``ap-northeast-1``)
    - Seoul (``ap-northeast-2``)
    - Mumbai (``ap-south-1``)
    - Singapore (``ap-southeast-1``)
    - Sydney (``ap-southeast-2``)

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CustomParserProps",
    jsii_struct_bases=[],
    name_mapping={"parser": "parser", "steps": "steps"},
)
class CustomParserProps:
    def __init__(
        self,
        *,
        parser: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction] = None,
        steps: typing.Optional[typing.Sequence[typing.Union["PromptStepConfigurationCustomParser", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param parser: 
        :param steps: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c75718aff5128dcd74c4fa51ae85d75a9e02a9beda7f7d3f7170e5d1d876dd73)
            check_type(argname="argument parser", value=parser, expected_type=type_hints["parser"])
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if parser is not None:
            self._values["parser"] = parser
        if steps is not None:
            self._values["steps"] = steps

    @builtins.property
    def parser(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction]:
        '''
        :stability: experimental
        '''
        result = self._values.get("parser")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction], result)

    @builtins.property
    def steps(
        self,
    ) -> typing.Optional[typing.List["PromptStepConfigurationCustomParser"]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("steps")
        return typing.cast(typing.Optional[typing.List["PromptStepConfigurationCustomParser"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomParserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CustomTopicProps",
    jsii_struct_bases=[],
    name_mapping={"definition": "definition", "examples": "examples", "name": "name"},
)
class CustomTopicProps:
    def __init__(
        self,
        *,
        definition: builtins.str,
        examples: typing.Sequence[builtins.str],
        name: builtins.str,
    ) -> None:
        '''(experimental) Interface for creating a custom Topic.

        :param definition: (experimental) Provide a clear definition to detect and block user inputs and FM responses that fall into this topic. Avoid starting with "don't".
        :param examples: (experimental) Representative phrases that refer to the topic. These phrases can represent a user input or a model response. Add up to 5 phrases, up to 100 characters each.
        :param name: (experimental) The name of the topic to deny.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7afa8690bf8def1351745b409bf75b1c9388f7690948642485ab500130f04eab)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument examples", value=examples, expected_type=type_hints["examples"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
            "examples": examples,
            "name": name,
        }

    @builtins.property
    def definition(self) -> builtins.str:
        '''(experimental) Provide a clear definition to detect and block user inputs and FM responses that fall into this topic.

        Avoid starting with "don't".

        :stability: experimental

        Example::

            `Investment advice refers to inquiries, guidance, or recommendations
            regarding the management or allocation of funds or assets with the goal of
            generating returns or achieving specific financial objectives.`
        '''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def examples(self) -> typing.List[builtins.str]:
        '''(experimental) Representative phrases that refer to the topic.

        These phrases can represent
        a user input or a model response. Add up to 5 phrases, up to 100 characters
        each.

        :stability: experimental

        Example::

            "Where should I invest my money?"
        '''
        result = self._values.get("examples")
        assert result is not None, "Required property 'examples' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the topic to deny.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomTopicProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomTransformation(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CustomTransformation",
):
    '''(experimental) Represents a custom transformation configuration for a data source ingestion.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking-parsing.html#kb-custom-transformation
    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="lambda")
    @builtins.classmethod
    def lambda_(
        cls,
        *,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        s3_bucket_uri: builtins.str,
    ) -> "CustomTransformation":
        '''(experimental) This feature allows you to use a Lambda function to inject your own logic into the knowledge base ingestion process.

        :param lambda_function: (experimental) The Lambda function to use for custom document processing.
        :param s3_bucket_uri: (experimental) An S3 bucket URL/path to store input documents for Lambda processing and to store the output of the processed documents.

        :see: https://github.com/aws-samples/amazon-bedrock-samples/blob/main/knowledge-bases/features-examples/02-optimizing-accuracy-retrieved-results/advanced_chunking_options.ipynb
        :stability: experimental
        '''
        props = LambdaCustomTransformationProps(
            lambda_function=lambda_function, s3_bucket_uri=s3_bucket_uri
        )

        return typing.cast("CustomTransformation", jsii.sinvoke(cls, "lambda", [props]))

    @jsii.member(jsii_name="generatePolicyStatements")
    @abc.abstractmethod
    def generate_policy_statements(
        self,
        scope: _constructs_77d1e7e8.Construct,
    ) -> typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]:
        '''
        :param scope: -

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="configuration")
    @abc.abstractmethod
    def configuration(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.CustomTransformationConfigurationProperty:
        '''(experimental) The CloudFormation property representation of this custom transformation configuration.

        :stability: experimental
        '''
        ...

    @configuration.setter
    @abc.abstractmethod
    def configuration(
        self,
        value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.CustomTransformationConfigurationProperty,
    ) -> None:
        ...


class _CustomTransformationProxy(CustomTransformation):
    @jsii.member(jsii_name="generatePolicyStatements")
    def generate_policy_statements(
        self,
        scope: _constructs_77d1e7e8.Construct,
    ) -> typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]:
        '''
        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__898a06e70f7f1a8abcf9e8433317e047be3a6f52316351b0d22de8a49154fb6c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement], jsii.invoke(self, "generatePolicyStatements", [scope]))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.CustomTransformationConfigurationProperty:
        '''(experimental) The CloudFormation property representation of this custom transformation configuration.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.CustomTransformationConfigurationProperty, jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(
        self,
        value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.CustomTransformationConfigurationProperty,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ea7d98a453ed23a6d13ca01317dfc8f56bd010bb3d771347e4898118887260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, CustomTransformation).__jsii_proxy_class__ = lambda : _CustomTransformationProxy


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.DataDeletionPolicy"
)
class DataDeletionPolicy(enum.Enum):
    '''(experimental) Specifies the policy for handling data when a data source resource is deleted.

    This policy affects the vector embeddings created from the data source.

    :stability: experimental
    '''

    DELETE = "DELETE"
    '''(experimental) Deletes all vector embeddings derived from the data source upon deletion of a data source resource.

    :stability: experimental
    '''
    RETAIN = "RETAIN"
    '''(experimental) Retains all vector embeddings derived from the data source even after deletion of a data source resource.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.DataSourceAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
    },
)
class DataSourceAssociationProps:
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> None:
        '''(experimental) Properties common for creating any of the different data source types.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3370fd8035498a3339649efe16f36fa523a3b651e8f4e3f2f7cc83f1af7f2c0)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional["ParsingStategy"]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional["ParsingStategy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSourceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.DataSourceType")
class DataSourceType(enum.Enum):
    '''(experimental) Represents the types of data sources that can be associated to an Knowledge Base.

    :stability: experimental
    '''

    S3 = "S3"
    '''(experimental) Amazon S3 Bucket data source.

    :stability: experimental
    '''
    CONFLUENCE = "CONFLUENCE"
    '''(experimental) Confluence Cloud Instance data source.

    :stability: experimental
    '''
    SALESFORCE = "SALESFORCE"
    '''(experimental) Salesforce instance data source.

    :stability: experimental
    '''
    SHAREPOINT = "SHAREPOINT"
    '''(experimental) Microsoft SharePoint instance data source.

    :stability: experimental
    '''
    WEB_CRAWLER = "WEB_CRAWLER"
    '''(experimental) Web Crawler data source.

    Extracts content from authorized public web pages using a crawler.

    :stability: experimental
    '''


class DefaultPromptRouterIdentifier(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.DefaultPromptRouterIdentifier",
):
    '''(experimental) Represents identifiers for default prompt routers in Bedrock.

    :stability: experimental
    '''

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_V1")
    def ANTHROPIC_CLAUDE_V1(cls) -> "DefaultPromptRouterIdentifier":
        '''(experimental) Anthropic Claude V1 router configuration.

        :stability: experimental
        '''
        return typing.cast("DefaultPromptRouterIdentifier", jsii.sget(cls, "ANTHROPIC_CLAUDE_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_3_1")
    def META_LLAMA_3_1(cls) -> "DefaultPromptRouterIdentifier":
        '''(experimental) Meta Llama 3.1 router configuration.

        :stability: experimental
        '''
        return typing.cast("DefaultPromptRouterIdentifier", jsii.sget(cls, "META_LLAMA_3_1"))

    @builtins.property
    @jsii.member(jsii_name="promptRouterId")
    def prompt_router_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptRouterId"))

    @builtins.property
    @jsii.member(jsii_name="routingModels")
    def routing_models(self) -> typing.List["BedrockFoundationModel"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List["BedrockFoundationModel"], jsii.get(self, "routingModels"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.FoundationModelParsingStategyProps",
    jsii_struct_bases=[],
    name_mapping={
        "parsing_model": "parsingModel",
        "parsing_modality": "parsingModality",
        "parsing_prompt": "parsingPrompt",
    },
)
class FoundationModelParsingStategyProps:
    def __init__(
        self,
        *,
        parsing_model: "IInvokable",
        parsing_modality: typing.Optional["ParsingModality"] = None,
        parsing_prompt: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for configuring a Foundation Model parsing strategy.

        :param parsing_model: (experimental) The Foundation Model to use for parsing non-textual information. Currently supported models are Claude 3 Sonnet and Claude 3 Haiku.
        :param parsing_modality: (experimental) Specifies whether to enable parsing of multimodal data, including both text and/or images. Default: undefined - Text only
        :param parsing_prompt: (experimental) Custom prompt to instruct the parser on how to interpret the document. Default: - Uses the default instruction prompt as provided in the AWS Console.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed85f0ccfdf38b650635f35650195519e14f924af93233cef46e2fd5af61295)
            check_type(argname="argument parsing_model", value=parsing_model, expected_type=type_hints["parsing_model"])
            check_type(argname="argument parsing_modality", value=parsing_modality, expected_type=type_hints["parsing_modality"])
            check_type(argname="argument parsing_prompt", value=parsing_prompt, expected_type=type_hints["parsing_prompt"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parsing_model": parsing_model,
        }
        if parsing_modality is not None:
            self._values["parsing_modality"] = parsing_modality
        if parsing_prompt is not None:
            self._values["parsing_prompt"] = parsing_prompt

    @builtins.property
    def parsing_model(self) -> "IInvokable":
        '''(experimental) The Foundation Model to use for parsing non-textual information.

        Currently supported models are Claude 3 Sonnet and Claude 3 Haiku.

        :stability: experimental
        '''
        result = self._values.get("parsing_model")
        assert result is not None, "Required property 'parsing_model' is missing"
        return typing.cast("IInvokable", result)

    @builtins.property
    def parsing_modality(self) -> typing.Optional["ParsingModality"]:
        '''(experimental) Specifies whether to enable parsing of multimodal data, including both text and/or images.

        :default: undefined - Text only

        :stability: experimental
        '''
        result = self._values.get("parsing_modality")
        return typing.cast(typing.Optional["ParsingModality"], result)

    @builtins.property
    def parsing_prompt(self) -> typing.Optional[builtins.str]:
        '''(experimental) Custom prompt to instruct the parser on how to interpret the document.

        :default: - Uses the default instruction prompt as provided in the AWS Console.

        :stability: experimental
        '''
        result = self._values.get("parsing_prompt")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FoundationModelParsingStategyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.GuardrailAction")
class GuardrailAction(enum.Enum):
    '''(experimental) Guardrail action when a sensitive entity is detected.

    :stability: experimental
    '''

    BLOCK = "BLOCK"
    '''(experimental) If sensitive information is detected in the prompt or response, the guardrail blocks all the content and returns a message that you configure.

    :stability: experimental
    '''
    ANONYMIZE = "ANONYMIZE"
    '''(experimental) If sensitive information is detected in the model response, the guardrail masks it with an identifier, the sensitive information is masked and replaced with identifier tags (for example: [NAME-1], [NAME-2], [EMAIL-1], etc.).

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.GuardrailAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "guardrail_arn": "guardrailArn",
        "guardrail_version": "guardrailVersion",
        "kms_key": "kmsKey",
    },
)
class GuardrailAttributes:
    def __init__(
        self,
        *,
        guardrail_arn: builtins.str,
        guardrail_version: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> None:
        '''(experimental) ****************************************************************************                     ATTRS FOR IMPORTED CONSTRUCT ***************************************************************************.

        :param guardrail_arn: (experimental) The ARN of the guardrail. At least one of guardrailArn or guardrailId must be defined in order to initialize a guardrail ref.
        :param guardrail_version: (experimental) The version of the guardrail. Default: "DRAFT"
        :param kms_key: (experimental) The KMS key of the guardrail if custom encryption is configured. Default: undefined - Means data is encrypted by default with a AWS-managed key

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b140b7ab54824449cb92973af6b36eb6cf61ab0c9257fdf79c5d510e1f60ff)
            check_type(argname="argument guardrail_arn", value=guardrail_arn, expected_type=type_hints["guardrail_arn"])
            check_type(argname="argument guardrail_version", value=guardrail_version, expected_type=type_hints["guardrail_version"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "guardrail_arn": guardrail_arn,
        }
        if guardrail_version is not None:
            self._values["guardrail_version"] = guardrail_version
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def guardrail_arn(self) -> builtins.str:
        '''(experimental) The ARN of the guardrail.

        At least one of guardrailArn or guardrailId must be
        defined in order to initialize a guardrail ref.

        :stability: experimental
        '''
        result = self._values.get("guardrail_arn")
        assert result is not None, "Required property 'guardrail_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def guardrail_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the guardrail.

        :default: "DRAFT"

        :stability: experimental
        '''
        result = self._values.get("guardrail_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key of the guardrail if custom encryption is configured.

        :default: undefined - Means data is encrypted by default with a AWS-managed key

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GuardrailAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.GuardrailProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "blocked_input_messaging": "blockedInputMessaging",
        "blocked_outputs_messaging": "blockedOutputsMessaging",
        "content_filters": "contentFilters",
        "contextual_grounding_filters": "contextualGroundingFilters",
        "denied_topics": "deniedTopics",
        "description": "description",
        "kms_key": "kmsKey",
        "managed_word_list_filters": "managedWordListFilters",
        "pii_filters": "piiFilters",
        "regex_filters": "regexFilters",
        "word_filters": "wordFilters",
    },
)
class GuardrailProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        blocked_input_messaging: typing.Optional[builtins.str] = None,
        blocked_outputs_messaging: typing.Optional[builtins.str] = None,
        content_filters: typing.Optional[typing.Sequence[typing.Union[ContentFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
        contextual_grounding_filters: typing.Optional[typing.Sequence[typing.Union[ContextualGroundingFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
        denied_topics: typing.Optional[typing.Sequence["Topic"]] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        managed_word_list_filters: typing.Optional[typing.Sequence["ManagedWordFilterType"]] = None,
        pii_filters: typing.Optional[typing.Sequence[typing.Union["PIIFilter", typing.Dict[builtins.str, typing.Any]]]] = None,
        regex_filters: typing.Optional[typing.Sequence[typing.Union["RegexFilter", typing.Dict[builtins.str, typing.Any]]]] = None,
        word_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties for creating a Guardrail.

        :param name: (experimental) The name of the guardrail.
        :param blocked_input_messaging: (experimental) The message to return when the guardrail blocks a prompt. Default: "Sorry, your query violates our usage policy."
        :param blocked_outputs_messaging: (experimental) The message to return when the guardrail blocks a model response. Default: "Sorry, I am unable to answer your question because of our usage policy."
        :param content_filters: (experimental) The content filters to apply to the guardrail. Note, if one of
        :param contextual_grounding_filters: (experimental) The contextual grounding filters to apply to the guardrail.
        :param denied_topics: (experimental) Up to 30 denied topics to block user inputs or model responses associated with the topic.
        :param description: (experimental) The description of the guardrail.
        :param kms_key: (experimental) A custom KMS key to use for encrypting data. Default: "Your data is encrypted by default with a key that AWS owns and manages for you."
        :param managed_word_list_filters: (experimental) The managed word filters to apply to the guardrail.
        :param pii_filters: (experimental) The PII filters to apply to the guardrail.
        :param regex_filters: (experimental) The regular expression (regex) filters to apply to the guardrail.
        :param word_filters: (experimental) The word filters to apply to the guardrail.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb9d19859a6750c938be49617894f02e36de79c2e5a05a9cb6d6eac91e68d0ea)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument blocked_input_messaging", value=blocked_input_messaging, expected_type=type_hints["blocked_input_messaging"])
            check_type(argname="argument blocked_outputs_messaging", value=blocked_outputs_messaging, expected_type=type_hints["blocked_outputs_messaging"])
            check_type(argname="argument content_filters", value=content_filters, expected_type=type_hints["content_filters"])
            check_type(argname="argument contextual_grounding_filters", value=contextual_grounding_filters, expected_type=type_hints["contextual_grounding_filters"])
            check_type(argname="argument denied_topics", value=denied_topics, expected_type=type_hints["denied_topics"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument managed_word_list_filters", value=managed_word_list_filters, expected_type=type_hints["managed_word_list_filters"])
            check_type(argname="argument pii_filters", value=pii_filters, expected_type=type_hints["pii_filters"])
            check_type(argname="argument regex_filters", value=regex_filters, expected_type=type_hints["regex_filters"])
            check_type(argname="argument word_filters", value=word_filters, expected_type=type_hints["word_filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if blocked_input_messaging is not None:
            self._values["blocked_input_messaging"] = blocked_input_messaging
        if blocked_outputs_messaging is not None:
            self._values["blocked_outputs_messaging"] = blocked_outputs_messaging
        if content_filters is not None:
            self._values["content_filters"] = content_filters
        if contextual_grounding_filters is not None:
            self._values["contextual_grounding_filters"] = contextual_grounding_filters
        if denied_topics is not None:
            self._values["denied_topics"] = denied_topics
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if managed_word_list_filters is not None:
            self._values["managed_word_list_filters"] = managed_word_list_filters
        if pii_filters is not None:
            self._values["pii_filters"] = pii_filters
        if regex_filters is not None:
            self._values["regex_filters"] = regex_filters
        if word_filters is not None:
            self._values["word_filters"] = word_filters

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the guardrail.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def blocked_input_messaging(self) -> typing.Optional[builtins.str]:
        '''(experimental) The message to return when the guardrail blocks a prompt.

        :default: "Sorry, your query violates our usage policy."

        :stability: experimental
        '''
        result = self._values.get("blocked_input_messaging")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def blocked_outputs_messaging(self) -> typing.Optional[builtins.str]:
        '''(experimental) The message to return when the guardrail blocks a model response.

        :default: "Sorry, I am unable to answer your question because of our usage policy."

        :stability: experimental
        '''
        result = self._values.get("blocked_outputs_messaging")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_filters(self) -> typing.Optional[typing.List[ContentFilter]]:
        '''(experimental) The content filters to apply to the guardrail.

        Note, if one of

        :stability: experimental
        '''
        result = self._values.get("content_filters")
        return typing.cast(typing.Optional[typing.List[ContentFilter]], result)

    @builtins.property
    def contextual_grounding_filters(
        self,
    ) -> typing.Optional[typing.List[ContextualGroundingFilter]]:
        '''(experimental) The contextual grounding filters to apply to the guardrail.

        :stability: experimental
        '''
        result = self._values.get("contextual_grounding_filters")
        return typing.cast(typing.Optional[typing.List[ContextualGroundingFilter]], result)

    @builtins.property
    def denied_topics(self) -> typing.Optional[typing.List["Topic"]]:
        '''(experimental) Up to 30 denied topics to block user inputs or model responses associated with the topic.

        :stability: experimental
        '''
        result = self._values.get("denied_topics")
        return typing.cast(typing.Optional[typing.List["Topic"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the guardrail.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) A custom KMS key to use for encrypting data.

        :default: "Your data is encrypted by default with a key that AWS owns and manages for you."

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def managed_word_list_filters(
        self,
    ) -> typing.Optional[typing.List["ManagedWordFilterType"]]:
        '''(experimental) The managed word filters to apply to the guardrail.

        :stability: experimental
        '''
        result = self._values.get("managed_word_list_filters")
        return typing.cast(typing.Optional[typing.List["ManagedWordFilterType"]], result)

    @builtins.property
    def pii_filters(self) -> typing.Optional[typing.List["PIIFilter"]]:
        '''(experimental) The PII filters to apply to the guardrail.

        :stability: experimental
        '''
        result = self._values.get("pii_filters")
        return typing.cast(typing.Optional[typing.List["PIIFilter"]], result)

    @builtins.property
    def regex_filters(self) -> typing.Optional[typing.List["RegexFilter"]]:
        '''(experimental) The regular expression (regex) filters to apply to the guardrail.

        :stability: experimental
        '''
        result = self._values.get("regex_filters")
        return typing.cast(typing.Optional[typing.List["RegexFilter"]], result)

    @builtins.property
    def word_filters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The word filters to apply to the guardrail.

        :stability: experimental
        '''
        result = self._values.get("word_filters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GuardrailProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.HierarchicalChunkingProps",
    jsii_struct_bases=[],
    name_mapping={
        "max_child_token_size": "maxChildTokenSize",
        "max_parent_token_size": "maxParentTokenSize",
        "overlap_tokens": "overlapTokens",
    },
)
class HierarchicalChunkingProps:
    def __init__(
        self,
        *,
        max_child_token_size: jsii.Number,
        max_parent_token_size: jsii.Number,
        overlap_tokens: jsii.Number,
    ) -> None:
        '''
        :param max_child_token_size: (experimental) Maximum number of tokens that a child chunk can contain. Keep in mind the maximum chunk size depends on the embedding model chosen.
        :param max_parent_token_size: (experimental) Maximum number of tokens that a parent chunk can contain. Keep in mind the maximum chunk size depends on the embedding model chosen.
        :param overlap_tokens: (experimental) The overlap tokens between adjacent chunks.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832a5183cc17b41fd7587d09a661c1bc3796489cafca2ed06677f49aa94a717d)
            check_type(argname="argument max_child_token_size", value=max_child_token_size, expected_type=type_hints["max_child_token_size"])
            check_type(argname="argument max_parent_token_size", value=max_parent_token_size, expected_type=type_hints["max_parent_token_size"])
            check_type(argname="argument overlap_tokens", value=overlap_tokens, expected_type=type_hints["overlap_tokens"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_child_token_size": max_child_token_size,
            "max_parent_token_size": max_parent_token_size,
            "overlap_tokens": overlap_tokens,
        }

    @builtins.property
    def max_child_token_size(self) -> jsii.Number:
        '''(experimental) Maximum number of tokens that a child chunk can contain.

        Keep in mind the maximum chunk size depends on the embedding model chosen.

        :stability: experimental
        '''
        result = self._values.get("max_child_token_size")
        assert result is not None, "Required property 'max_child_token_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_parent_token_size(self) -> jsii.Number:
        '''(experimental) Maximum number of tokens that a parent chunk can contain.

        Keep in mind the maximum chunk size depends on the embedding model chosen.

        :stability: experimental
        '''
        result = self._values.get("max_parent_token_size")
        assert result is not None, "Required property 'max_parent_token_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def overlap_tokens(self) -> jsii.Number:
        '''(experimental) The overlap tokens between adjacent chunks.

        :stability: experimental
        '''
        result = self._values.get("overlap_tokens")
        assert result is not None, "Required property 'overlap_tokens' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HierarchicalChunkingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IAgent")
class IAgent(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an Agent, either created with CDK or imported.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="agentArn")
    def agent_arn(self) -> builtins.str:
        '''(experimental) The ARN of the agent.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:agent/OKDSJOGKMO"@attributeundefined
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="agentId")
    def agent_id(self) -> builtins.str:
        '''(experimental) The ID of the Agent.

        :stability: experimental

        Example::

            "OKDSJOGKMO"@attributeundefined
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The IAM role associated to the agent.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this agent.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="lastUpdated")
    def last_updated(self) -> typing.Optional[builtins.str]:
        '''(experimental) When this agent was last updated.

        :stability: experimental
        '''
        ...


class _IAgentProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an Agent, either created with CDK or imported.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IAgent"

    @builtins.property
    @jsii.member(jsii_name="agentArn")
    def agent_arn(self) -> builtins.str:
        '''(experimental) The ARN of the agent.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:agent/OKDSJOGKMO"@attributeundefined
        '''
        return typing.cast(builtins.str, jsii.get(self, "agentArn"))

    @builtins.property
    @jsii.member(jsii_name="agentId")
    def agent_id(self) -> builtins.str:
        '''(experimental) The ID of the Agent.

        :stability: experimental

        Example::

            "OKDSJOGKMO"@attributeundefined
        '''
        return typing.cast(builtins.str, jsii.get(self, "agentId"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The IAM role associated to the agent.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this agent.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdated")
    def last_updated(self) -> typing.Optional[builtins.str]:
        '''(experimental) When this agent was last updated.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastUpdated"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAgent).__jsii_proxy_class__ = lambda : _IAgentProxy


@jsii.interface(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IAgentAlias")
class IAgentAlias(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an Agent Alias, either created with CDK or imported.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="agent")
    def agent(self) -> IAgent:
        '''(experimental) The underlying agent for this alias.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="aliasArn")
    def alias_arn(self) -> builtins.str:
        '''(experimental) The ARN of the agent alias.

        :stability: experimental

        Example::

            `arn:aws:bedrock:us-east-1:123456789012:agent-alias/DNCJJYQKSU/TCLCITFZTN`
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="aliasId")
    def alias_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the agent alias.

        :stability: experimental

        Example::

            `TCLCITFZTN`
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given principal identity permissions to perform actions on this agent alias.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to invoke the agent alias.

        :param grantee: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Define an EventBridge rule that triggers when something happens to this agent alias.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :stability: experimental
        '''
        ...


class _IAgentAliasProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an Agent Alias, either created with CDK or imported.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IAgentAlias"

    @builtins.property
    @jsii.member(jsii_name="agent")
    def agent(self) -> IAgent:
        '''(experimental) The underlying agent for this alias.

        :stability: experimental
        '''
        return typing.cast(IAgent, jsii.get(self, "agent"))

    @builtins.property
    @jsii.member(jsii_name="aliasArn")
    def alias_arn(self) -> builtins.str:
        '''(experimental) The ARN of the agent alias.

        :stability: experimental

        Example::

            `arn:aws:bedrock:us-east-1:123456789012:agent-alias/DNCJJYQKSU/TCLCITFZTN`
        '''
        return typing.cast(builtins.str, jsii.get(self, "aliasArn"))

    @builtins.property
    @jsii.member(jsii_name="aliasId")
    def alias_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the agent alias.

        :stability: experimental

        Example::

            `TCLCITFZTN`
        '''
        return typing.cast(builtins.str, jsii.get(self, "aliasId"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given principal identity permissions to perform actions on this agent alias.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7df59fa11db2053427ed6170c8adff35c1babc7d6257284c96c156295d88f9a1)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to invoke the agent alias.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a02c91625918402481c9f4e1e5c4423a8b43f91f76cc3c463edeeaaa0eae178e)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantInvoke", [grantee]))

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Define an EventBridge rule that triggers when something happens to this agent alias.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a0c02755094e6851a73cb8ab426a25166689912c7122d3c95b6ce963d214862)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onCloudTrailEvent", [id, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAgentAlias).__jsii_proxy_class__ = lambda : _IAgentAliasProxy


@jsii.interface(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IDataSource")
class IDataSource(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Specifies interface for resources created with CDK or imported into CDK.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        ...


class _IDataSourceProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Specifies interface for resources created with CDK or imported into CDK.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IDataSource"

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDataSource).__jsii_proxy_class__ = lambda : _IDataSourceProxy


@jsii.interface(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IGuardrail")
class IGuardrail(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents a Guardrail, either created with CDK or imported.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="guardrailArn")
    def guardrail_arn(self) -> builtins.str:
        '''(experimental) The ARN of the guardrail.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:guardrail/yympzo398ipq"@attributeundefined
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="guardrailId")
    def guardrail_id(self) -> builtins.str:
        '''(experimental) The ID of the guardrail.

        :stability: experimental

        Example::

            "yympzo398ipq"@attributeundefined
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this guardrail.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="lastUpdated")
    def last_updated(self) -> typing.Optional[builtins.str]:
        '''(experimental) When this guardrail was last updated.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="guardrailVersion")
    def guardrail_version(self) -> builtins.str:
        '''(experimental) The version of the guardrail.

        If no explicit version is created,
        this will default to "DRAFT"

        :stability: experimental
        '''
        ...

    @guardrail_version.setter
    def guardrail_version(self, value: builtins.str) -> None:
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given principal identity permissions to perform actions on this guardrail.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantApply")
    def grant_apply(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to apply the guardrail.

        :param grantee: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the given named metric for this guardrail.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricInvocationClientErrors")
    def metric_invocation_client_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocation client errors metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricInvocationLatency")
    def metric_invocation_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocation latency metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricInvocations")
    def metric_invocations(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocations metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricInvocationServerErrors")
    def metric_invocation_server_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocation server errors metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricInvocationsIntervened")
    def metric_invocations_intervened(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocations intervened metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricInvocationThrottles")
    def metric_invocation_throttles(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocation throttles metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricTextUnitCount")
    def metric_text_unit_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the text unit count metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...


class _IGuardrailProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents a Guardrail, either created with CDK or imported.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IGuardrail"

    @builtins.property
    @jsii.member(jsii_name="guardrailArn")
    def guardrail_arn(self) -> builtins.str:
        '''(experimental) The ARN of the guardrail.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:guardrail/yympzo398ipq"@attributeundefined
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailArn"))

    @builtins.property
    @jsii.member(jsii_name="guardrailId")
    def guardrail_id(self) -> builtins.str:
        '''(experimental) The ID of the guardrail.

        :stability: experimental

        Example::

            "yympzo398ipq"@attributeundefined
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailId"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this guardrail.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdated")
    def last_updated(self) -> typing.Optional[builtins.str]:
        '''(experimental) When this guardrail was last updated.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastUpdated"))

    @builtins.property
    @jsii.member(jsii_name="guardrailVersion")
    def guardrail_version(self) -> builtins.str:
        '''(experimental) The version of the guardrail.

        If no explicit version is created,
        this will default to "DRAFT"

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailVersion"))

    @guardrail_version.setter
    def guardrail_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa86b82cfa7566549e30a1d5b954f23d8c26046bfa7cc0af976bc3c76faa6d16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guardrailVersion", value) # pyright: ignore[reportArgumentType]

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given principal identity permissions to perform actions on this guardrail.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5125723d1fe4aed39d0c9ef21fda4887064605eb58037eb896c217af3572d08)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantApply")
    def grant_apply(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to apply the guardrail.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78ba62eccfee612703b786064d7f93d108f9f738d3af81886e81a1528ede7a98)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantApply", [grantee]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the given named metric for this guardrail.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a604164d87e46d6095394689572206d47548b4ca8f338519f76cb51ef2f735)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricInvocationClientErrors")
    def metric_invocation_client_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocation client errors metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricInvocationClientErrors", [props]))

    @jsii.member(jsii_name="metricInvocationLatency")
    def metric_invocation_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocation latency metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricInvocationLatency", [props]))

    @jsii.member(jsii_name="metricInvocations")
    def metric_invocations(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocations metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricInvocations", [props]))

    @jsii.member(jsii_name="metricInvocationServerErrors")
    def metric_invocation_server_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocation server errors metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricInvocationServerErrors", [props]))

    @jsii.member(jsii_name="metricInvocationsIntervened")
    def metric_invocations_intervened(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocations intervened metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricInvocationsIntervened", [props]))

    @jsii.member(jsii_name="metricInvocationThrottles")
    def metric_invocation_throttles(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocation throttles metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricInvocationThrottles", [props]))

    @jsii.member(jsii_name="metricTextUnitCount")
    def metric_text_unit_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the text unit count metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTextUnitCount", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGuardrail).__jsii_proxy_class__ = lambda : _IGuardrailProxy


@jsii.interface(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IInferenceProfile"
)
class IInferenceProfile(typing_extensions.Protocol):
    '''(experimental) Represents a ApplicationInferenceProfile, either created with CDK or imported.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileArn")
    def inference_profile_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application inference profile.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileId")
    def inference_profile_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the inference profile.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "InferenceProfileType":
        '''(experimental) The type of inference profile.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantProfileUsage")
    def grant_profile_usage(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grants appropriate permissions to use the inference profile.

        :param grantee: -

        :stability: experimental
        '''
        ...


class _IInferenceProfileProxy:
    '''(experimental) Represents a ApplicationInferenceProfile, either created with CDK or imported.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IInferenceProfile"

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileArn")
    def inference_profile_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application inference profile.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileArn"))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileId")
    def inference_profile_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the inference profile.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileId"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "InferenceProfileType":
        '''(experimental) The type of inference profile.

        :stability: experimental
        '''
        return typing.cast("InferenceProfileType", jsii.get(self, "type"))

    @jsii.member(jsii_name="grantProfileUsage")
    def grant_profile_usage(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grants appropriate permissions to use the inference profile.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e05b919b09e86b619e07b4ef364b84ec6c2406d5ea1bca6a3cc89fa68153ec7)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantProfileUsage", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInferenceProfile).__jsii_proxy_class__ = lambda : _IInferenceProfileProxy


@jsii.interface(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IInvokable")
class IInvokable(typing_extensions.Protocol):
    '''(experimental) Represents an Amazon Bedrock abstraction on which you can run the ``Invoke`` API.

    This can be a Foundational Model,
    a Custom Model, or an Inference Profile.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="invokableArn")
    def invokable_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Bedrock invokable abstraction.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Gives the appropriate policies to invoke and use the invokable abstraction.

        :param grantee: -

        :stability: experimental
        '''
        ...


class _IInvokableProxy:
    '''(experimental) Represents an Amazon Bedrock abstraction on which you can run the ``Invoke`` API.

    This can be a Foundational Model,
    a Custom Model, or an Inference Profile.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IInvokable"

    @builtins.property
    @jsii.member(jsii_name="invokableArn")
    def invokable_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Bedrock invokable abstraction.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "invokableArn"))

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Gives the appropriate policies to invoke and use the invokable abstraction.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29403dd1f5d63fdfa42529ed12671747a327e8f838334b096c8d604ee0871773)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantInvoke", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInvokable).__jsii_proxy_class__ = lambda : _IInvokableProxy


@jsii.interface(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IKnowledgeBase"
)
class IKnowledgeBase(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents a Knowledge Base, either created with CDK or imported, of any type.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseArn")
    def knowledge_base_arn(self) -> builtins.str:
        '''(experimental) The ARN of the knowledge base.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:knowledge-base/KB12345678"
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseId")
    def knowledge_base_id(self) -> builtins.str:
        '''(experimental) The ID of the knowledge base.

        :stability: experimental

        Example::

            "KB12345678"
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role associated with the knowledge base.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "KnowledgeBaseType":
        '''(experimental) The type of knowledge base.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the knowledge base.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="instruction")
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) A narrative instruction of the knowledge base.

        A Bedrock Agent can use this instruction to determine if it should
        query this Knowledge Base.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given principal identity permissions to perform actions on this knowledge base.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantQuery")
    def grant_query(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to query the knowledge base.

        :param grantee: -

        :stability: experimental
        '''
        ...


class _IKnowledgeBaseProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents a Knowledge Base, either created with CDK or imported, of any type.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IKnowledgeBase"

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseArn")
    def knowledge_base_arn(self) -> builtins.str:
        '''(experimental) The ARN of the knowledge base.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:knowledge-base/KB12345678"
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseArn"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseId")
    def knowledge_base_id(self) -> builtins.str:
        '''(experimental) The ID of the knowledge base.

        :stability: experimental

        Example::

            "KB12345678"
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseId"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role associated with the knowledge base.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "KnowledgeBaseType":
        '''(experimental) The type of knowledge base.

        :stability: experimental
        '''
        return typing.cast("KnowledgeBaseType", jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="instruction")
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) A narrative instruction of the knowledge base.

        A Bedrock Agent can use this instruction to determine if it should
        query this Knowledge Base.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instruction"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given principal identity permissions to perform actions on this knowledge base.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38eeedeba6ae1a17302d5c0d2af9c9f8fd714ba1ff9eae57010ac53606d94377)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantQuery")
    def grant_query(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to query the knowledge base.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f52b2243768badbd2bf4261a9b42e28734215c49e1318565708fb4cbdc5967a)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantQuery", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IKnowledgeBase).__jsii_proxy_class__ = lambda : _IKnowledgeBaseProxy


@jsii.interface(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IPrompt")
class IPrompt(typing_extensions.Protocol):
    '''(experimental) Represents a Prompt, either created with CDK or imported.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="promptArn")
    def prompt_arn(self) -> builtins.str:
        '''(experimental) The ARN of the prompt.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:prompt/PROMPT12345"
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="promptId")
    def prompt_id(self) -> builtins.str:
        '''(experimental) The ID of the prompt.

        :stability: experimental

        Example::

            "PROMPT12345"
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this prompt.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="promptVersion")
    def prompt_version(self) -> builtins.str:
        '''(experimental) The version of the prompt.

        :default: - "DRAFT"

        :stability: experimental
        '''
        ...

    @prompt_version.setter
    def prompt_version(self, value: builtins.str) -> None:
        ...


class _IPromptProxy:
    '''(experimental) Represents a Prompt, either created with CDK or imported.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IPrompt"

    @builtins.property
    @jsii.member(jsii_name="promptArn")
    def prompt_arn(self) -> builtins.str:
        '''(experimental) The ARN of the prompt.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:prompt/PROMPT12345"
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptArn"))

    @builtins.property
    @jsii.member(jsii_name="promptId")
    def prompt_id(self) -> builtins.str:
        '''(experimental) The ID of the prompt.

        :stability: experimental

        Example::

            "PROMPT12345"
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptId"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this prompt.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))

    @builtins.property
    @jsii.member(jsii_name="promptVersion")
    def prompt_version(self) -> builtins.str:
        '''(experimental) The version of the prompt.

        :default: - "DRAFT"

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptVersion"))

    @prompt_version.setter
    def prompt_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5960928d16109614db9d88a976b6813f338475a6d9bd76b0987c904ec8128c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "promptVersion", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPrompt).__jsii_proxy_class__ = lambda : _IPromptProxy


@jsii.interface(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IPromptRouter"
)
class IPromptRouter(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="promptRouterArn")
    def prompt_router_arn(self) -> builtins.str:
        '''(experimental) The ARN of the prompt router.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="promptRouterId")
    def prompt_router_id(self) -> builtins.str:
        '''(experimental) The Id of the prompt router.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="routingEndpoints")
    def routing_endpoints(self) -> typing.List[IInvokable]:
        '''(experimental) The foundation models / profiles this router will route to.

        :stability: experimental
        '''
        ...


class _IPromptRouterProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IPromptRouter"

    @builtins.property
    @jsii.member(jsii_name="promptRouterArn")
    def prompt_router_arn(self) -> builtins.str:
        '''(experimental) The ARN of the prompt router.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptRouterArn"))

    @builtins.property
    @jsii.member(jsii_name="promptRouterId")
    def prompt_router_id(self) -> builtins.str:
        '''(experimental) The Id of the prompt router.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptRouterId"))

    @builtins.property
    @jsii.member(jsii_name="routingEndpoints")
    def routing_endpoints(self) -> typing.List[IInvokable]:
        '''(experimental) The foundation models / profiles this router will route to.

        :stability: experimental
        '''
        return typing.cast(typing.List[IInvokable], jsii.get(self, "routingEndpoints"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPromptRouter).__jsii_proxy_class__ = lambda : _IPromptRouterProxy


@jsii.interface(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IVectorKnowledgeBase"
)
class IVectorKnowledgeBase(IKnowledgeBase, typing_extensions.Protocol):
    '''(experimental) Represents a Knowledge Base, either created with CDK or imported.

    :stability: experimental
    '''

    @jsii.member(jsii_name="addConfluenceDataSource")
    def add_confluence_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        confluence_url: builtins.str,
        auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
        filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "ConfluenceDataSource":
        '''(experimental) Add a Confluence data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Confluence instance URL. Secret must start with "AmazonBedrock-".
        :param confluence_url: (experimental) The Confluence host URL or instance URL.
        :param auth_type: (experimental) The supported authentication method to connect to the data source. Default: ConfluenceDataSourceAuthType.OAUTH2_CLIENT_CREDENTIALS
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addS3DataSource")
    def add_s3_data_source(
        self,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "S3DataSource":
        '''(experimental) Add an S3 data source to the knowledge base.

        :param bucket: (experimental) The bucket that contains the data source.
        :param inclusion_prefixes: (experimental) The prefixes of the objects in the bucket that should be included in the data source. Default: - All objects in the bucket.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addSalesforceDataSource")
    def add_salesforce_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        endpoint: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union["SalesforceCrawlingFilters", typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "SalesforceDataSource":
        '''(experimental) Add a Salesforce data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Salesforce instance URL. Secret must start with "AmazonBedrock-".
        :param endpoint: (experimental) The Salesforce host URL or instance URL.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addSharePointDataSource")
    def add_share_point_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        domain: builtins.str,
        site_urls: typing.Sequence[builtins.str],
        tenant_id: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union["SharePointCrawlingFilters", typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "SharePointDataSource":
        '''(experimental) Add a SharePoint data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Sharepoint instance URL. Secret must start with "AmazonBedrock-".
        :param domain: (experimental) The domain of your SharePoint instance or site URL/URLs.
        :param site_urls: (experimental) The SharePoint site URL/URLs. Must start with “https”. All URLs must start with same protocol.
        :param tenant_id: (experimental) The identifier of your Microsoft 365 tenant.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addWebCrawlerDataSource")
    def add_web_crawler_data_source(
        self,
        *,
        source_urls: typing.Sequence[builtins.str],
        crawling_rate: typing.Optional[jsii.Number] = None,
        crawling_scope: typing.Optional[CrawlingScope] = None,
        filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "WebCrawlerDataSource":
        '''(experimental) Add a web crawler data source to the knowledge base.

        :param source_urls: (experimental) The source urls in the format ``https://www.sitename.com``. Maximum of 100 URLs.
        :param crawling_rate: (experimental) The max rate at which pages are crawled, up to 300 per minute per host. Higher values will decrease sync time but increase the load on the host. Default: 300
        :param crawling_scope: (experimental) The scope of the crawling. Default: - CrawlingScope.DEFAULT
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRetrieve")
    def grant_retrieve(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to retrieve content from the knowledge base.

        :param grantee: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRetrieveAndGenerate")
    def grant_retrieve_and_generate(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to retrieve content from the knowledge base.

        :param grantee: -

        :stability: experimental
        '''
        ...


class _IVectorKnowledgeBaseProxy(
    jsii.proxy_for(IKnowledgeBase), # type: ignore[misc]
):
    '''(experimental) Represents a Knowledge Base, either created with CDK or imported.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IVectorKnowledgeBase"

    @jsii.member(jsii_name="addConfluenceDataSource")
    def add_confluence_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        confluence_url: builtins.str,
        auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
        filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "ConfluenceDataSource":
        '''(experimental) Add a Confluence data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Confluence instance URL. Secret must start with "AmazonBedrock-".
        :param confluence_url: (experimental) The Confluence host URL or instance URL.
        :param auth_type: (experimental) The supported authentication method to connect to the data source. Default: ConfluenceDataSourceAuthType.OAUTH2_CLIENT_CREDENTIALS
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = ConfluenceDataSourceAssociationProps(
            auth_secret=auth_secret,
            confluence_url=confluence_url,
            auth_type=auth_type,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("ConfluenceDataSource", jsii.invoke(self, "addConfluenceDataSource", [props]))

    @jsii.member(jsii_name="addS3DataSource")
    def add_s3_data_source(
        self,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "S3DataSource":
        '''(experimental) Add an S3 data source to the knowledge base.

        :param bucket: (experimental) The bucket that contains the data source.
        :param inclusion_prefixes: (experimental) The prefixes of the objects in the bucket that should be included in the data source. Default: - All objects in the bucket.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = S3DataSourceAssociationProps(
            bucket=bucket,
            inclusion_prefixes=inclusion_prefixes,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("S3DataSource", jsii.invoke(self, "addS3DataSource", [props]))

    @jsii.member(jsii_name="addSalesforceDataSource")
    def add_salesforce_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        endpoint: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union["SalesforceCrawlingFilters", typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "SalesforceDataSource":
        '''(experimental) Add a Salesforce data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Salesforce instance URL. Secret must start with "AmazonBedrock-".
        :param endpoint: (experimental) The Salesforce host URL or instance URL.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = SalesforceDataSourceAssociationProps(
            auth_secret=auth_secret,
            endpoint=endpoint,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("SalesforceDataSource", jsii.invoke(self, "addSalesforceDataSource", [props]))

    @jsii.member(jsii_name="addSharePointDataSource")
    def add_share_point_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        domain: builtins.str,
        site_urls: typing.Sequence[builtins.str],
        tenant_id: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union["SharePointCrawlingFilters", typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "SharePointDataSource":
        '''(experimental) Add a SharePoint data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Sharepoint instance URL. Secret must start with "AmazonBedrock-".
        :param domain: (experimental) The domain of your SharePoint instance or site URL/URLs.
        :param site_urls: (experimental) The SharePoint site URL/URLs. Must start with “https”. All URLs must start with same protocol.
        :param tenant_id: (experimental) The identifier of your Microsoft 365 tenant.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = SharePointDataSourceAssociationProps(
            auth_secret=auth_secret,
            domain=domain,
            site_urls=site_urls,
            tenant_id=tenant_id,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("SharePointDataSource", jsii.invoke(self, "addSharePointDataSource", [props]))

    @jsii.member(jsii_name="addWebCrawlerDataSource")
    def add_web_crawler_data_source(
        self,
        *,
        source_urls: typing.Sequence[builtins.str],
        crawling_rate: typing.Optional[jsii.Number] = None,
        crawling_scope: typing.Optional[CrawlingScope] = None,
        filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "WebCrawlerDataSource":
        '''(experimental) Add a web crawler data source to the knowledge base.

        :param source_urls: (experimental) The source urls in the format ``https://www.sitename.com``. Maximum of 100 URLs.
        :param crawling_rate: (experimental) The max rate at which pages are crawled, up to 300 per minute per host. Higher values will decrease sync time but increase the load on the host. Default: 300
        :param crawling_scope: (experimental) The scope of the crawling. Default: - CrawlingScope.DEFAULT
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = WebCrawlerDataSourceAssociationProps(
            source_urls=source_urls,
            crawling_rate=crawling_rate,
            crawling_scope=crawling_scope,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("WebCrawlerDataSource", jsii.invoke(self, "addWebCrawlerDataSource", [props]))

    @jsii.member(jsii_name="grantRetrieve")
    def grant_retrieve(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to retrieve content from the knowledge base.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb0ae116051d137f78de149c1f75f9b1baccacd6bacf105433c47f07dec8c50)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRetrieve", [grantee]))

    @jsii.member(jsii_name="grantRetrieveAndGenerate")
    def grant_retrieve_and_generate(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to retrieve content from the knowledge base.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__376dfa6a00d154d8a21d348f5ca5f0ae71a20f6e24f1a069048d3d2878532c9a)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRetrieveAndGenerate", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVectorKnowledgeBase).__jsii_proxy_class__ = lambda : _IVectorKnowledgeBaseProxy


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.InferenceConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "maximum_length": "maximumLength",
        "stop_sequences": "stopSequences",
        "temperature": "temperature",
        "top_k": "topK",
        "top_p": "topP",
    },
)
class InferenceConfiguration:
    def __init__(
        self,
        *,
        maximum_length: jsii.Number,
        stop_sequences: typing.Sequence[builtins.str],
        temperature: jsii.Number,
        top_k: jsii.Number,
        top_p: jsii.Number,
    ) -> None:
        '''(experimental) LLM inference configuration.

        :param maximum_length: (experimental) The maximum number of tokens to generate in the response. Integer min 0 max 4096
        :param stop_sequences: (experimental) A list of stop sequences. A stop sequence is a sequence of characters that causes the model to stop generating the response. length 0-4
        :param temperature: (experimental) The likelihood of the model selecting higher-probability options while generating a response. A lower value makes the model more likely to choose higher-probability options, while a higher value makes the model more likely to choose lower-probability options. Floating point min 0 max 1
        :param top_k: (experimental) While generating a response, the model determines the probability of the following token at each point of generation. The value that you set for topK is the number of most-likely candidates from which the model chooses the next token in the sequence. For example, if you set topK to 50, the model selects the next token from among the top 50 most likely choices. Integer min 0 max 500
        :param top_p: (experimental) While generating a response, the model determines the probability of the following token at each point of generation. The value that you set for Top P determines the number of most-likely candidates from which the model chooses the next token in the sequence. For example, if you set topP to 80, the model only selects the next token from the top 80% of the probability distribution of next tokens. Floating point min 0 max 1

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__befd502c2937a36c672491bd2695d4ec887944e821efe023f2dc44cff4137750)
            check_type(argname="argument maximum_length", value=maximum_length, expected_type=type_hints["maximum_length"])
            check_type(argname="argument stop_sequences", value=stop_sequences, expected_type=type_hints["stop_sequences"])
            check_type(argname="argument temperature", value=temperature, expected_type=type_hints["temperature"])
            check_type(argname="argument top_k", value=top_k, expected_type=type_hints["top_k"])
            check_type(argname="argument top_p", value=top_p, expected_type=type_hints["top_p"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "maximum_length": maximum_length,
            "stop_sequences": stop_sequences,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
        }

    @builtins.property
    def maximum_length(self) -> jsii.Number:
        '''(experimental) The maximum number of tokens to generate in the response.

        Integer

        min 0
        max 4096

        :stability: experimental
        '''
        result = self._values.get("maximum_length")
        assert result is not None, "Required property 'maximum_length' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def stop_sequences(self) -> typing.List[builtins.str]:
        '''(experimental) A list of stop sequences.

        A stop sequence is a sequence of characters that
        causes the model to stop generating the response.

        length 0-4

        :stability: experimental
        '''
        result = self._values.get("stop_sequences")
        assert result is not None, "Required property 'stop_sequences' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def temperature(self) -> jsii.Number:
        '''(experimental) The likelihood of the model selecting higher-probability options while generating a response.

        A lower value makes the model more likely to choose
        higher-probability options, while a higher value makes the model more
        likely to choose lower-probability options.

        Floating point

        min 0
        max 1

        :stability: experimental
        '''
        result = self._values.get("temperature")
        assert result is not None, "Required property 'temperature' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def top_k(self) -> jsii.Number:
        '''(experimental) While generating a response, the model determines the probability of the following token at each point of generation.

        The value that you set for
        topK is the number of most-likely candidates from which the model chooses
        the next token in the sequence. For example, if you set topK to 50, the
        model selects the next token from among the top 50 most likely choices.

        Integer

        min 0
        max 500

        :stability: experimental
        '''
        result = self._values.get("top_k")
        assert result is not None, "Required property 'top_k' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def top_p(self) -> jsii.Number:
        '''(experimental) While generating a response, the model determines the probability of the following token at each point of generation.

        The value that you set for
        Top P determines the number of most-likely candidates from which the model
        chooses the next token in the sequence. For example, if you set topP to
        80, the model only selects the next token from the top 80% of the
        probability distribution of next tokens.

        Floating point

        min 0
        max 1

        :stability: experimental
        '''
        result = self._values.get("top_p")
        assert result is not None, "Required property 'top_p' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InferenceConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IInferenceProfile, _aws_cdk_ceddda9d.IResource)
class InferenceProfileBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.InferenceProfileBase",
):
    '''(experimental) Abstract base class for a ApplicationInferenceProfile.

    Contains methods and attributes valid for ApplicationInferenceProfiles either created with CDK or imported.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47a0e32efc3020834d43d9c5523a26c5aa4f43e016164f6b0291a29938455be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantProfileUsage")
    def grant_profile_usage(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grants appropriate permissions to use the cross-region inference profile.

        Does not grant permissions to use the model in the profile.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43e018efd836bd4c5f724810d840738657b70936f17c80063e2affbcd56a59c5)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantProfileUsage", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileArn")
    @abc.abstractmethod
    def inference_profile_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application inference profile.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileId")
    @abc.abstractmethod
    def inference_profile_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the inference profile.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    @abc.abstractmethod
    def type(self) -> "InferenceProfileType":
        '''(experimental) The ID or Amazon Resource Name (ARN) of the inference profile.

        :stability: experimental
        '''
        ...


class _InferenceProfileBaseProxy(
    InferenceProfileBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="inferenceProfileArn")
    def inference_profile_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application inference profile.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileArn"))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileId")
    def inference_profile_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the inference profile.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileId"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "InferenceProfileType":
        '''(experimental) The ID or Amazon Resource Name (ARN) of the inference profile.

        :stability: experimental
        '''
        return typing.cast("InferenceProfileType", jsii.get(self, "type"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, InferenceProfileBase).__jsii_proxy_class__ = lambda : _InferenceProfileBaseProxy


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.InferenceProfileType"
)
class InferenceProfileType(enum.Enum):
    '''(experimental) These are the values used by the API when using aws bedrock get-inference-profile --inference-profile-identifier XXXXXXX.

    :stability: experimental
    '''

    SYSTEM_DEFINED = "SYSTEM_DEFINED"
    '''(experimental) An inference profile that is created by AWS.

    These are profiles such as cross-region
    which help you distributed traffic across a geographic region.

    :stability: experimental
    '''
    APPLICATION = "APPLICATION"
    '''(experimental) An inference profile that is user-created.

    These are profiles that help
    you track costs or metrics.

    :stability: experimental
    '''


class InlineApiSchema(
    ApiSchema,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.InlineApiSchema",
):
    '''
    :stability: experimental
    '''

    def __init__(self, schema: builtins.str) -> None:
        '''
        :param schema: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abeb00812cdcb551f5f688ee295d8f225db974111b8872709130c22fef51592f)
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        jsii.create(self.__class__, self, [schema])


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.KendraKnowledgeBaseAttributes",
    jsii_struct_bases=[CommonKnowledgeBaseAttributes],
    name_mapping={
        "execution_role_arn": "executionRoleArn",
        "knowledge_base_id": "knowledgeBaseId",
        "description": "description",
        "instruction": "instruction",
        "knowledge_base_state": "knowledgeBaseState",
        "kendra_index": "kendraIndex",
    },
)
class KendraKnowledgeBaseAttributes(CommonKnowledgeBaseAttributes):
    def __init__(
        self,
        *,
        execution_role_arn: builtins.str,
        knowledge_base_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        instruction: typing.Optional[builtins.str] = None,
        knowledge_base_state: typing.Optional[builtins.str] = None,
        kendra_index: _IKendraGenAiIndex_da04f105,
    ) -> None:
        '''(experimental) Properties for importing a knowledge base outside of this stack.

        :param execution_role_arn: (experimental) The Service Execution Role associated with the knowledge base.
        :param knowledge_base_id: (experimental) The ID of the knowledge base.
        :param description: (experimental) The description of the knowledge base. Default: - No description provided.
        :param instruction: (experimental) Instructions for agents based on the design and type of information of the Knowledge Base. This will impact how Agents interact with the Knowledge Base. Default: - No description provided.
        :param knowledge_base_state: (experimental) Specifies whether to use the knowledge base or not when sending an InvokeAgent request. Default: - ENABLED
        :param kendra_index: (experimental) The GenAI Kendra Index ARN.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d227560632c8cafe262d3765e0ad2d2b24c7478a3d874d75c9abfe763e731d8)
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument knowledge_base_id", value=knowledge_base_id, expected_type=type_hints["knowledge_base_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument instruction", value=instruction, expected_type=type_hints["instruction"])
            check_type(argname="argument knowledge_base_state", value=knowledge_base_state, expected_type=type_hints["knowledge_base_state"])
            check_type(argname="argument kendra_index", value=kendra_index, expected_type=type_hints["kendra_index"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execution_role_arn": execution_role_arn,
            "knowledge_base_id": knowledge_base_id,
            "kendra_index": kendra_index,
        }
        if description is not None:
            self._values["description"] = description
        if instruction is not None:
            self._values["instruction"] = instruction
        if knowledge_base_state is not None:
            self._values["knowledge_base_state"] = knowledge_base_state

    @builtins.property
    def execution_role_arn(self) -> builtins.str:
        '''(experimental) The Service Execution Role associated with the knowledge base.

        :stability: experimental

        Example::

            "arn:aws:iam::123456789012:role/AmazonBedrockExecutionRoleForKnowledgeBaseawscdkbdgeBaseKB12345678"
        '''
        result = self._values.get("execution_role_arn")
        assert result is not None, "Required property 'execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def knowledge_base_id(self) -> builtins.str:
        '''(experimental) The ID of the knowledge base.

        :stability: experimental

        Example::

            "KB12345678"
        '''
        result = self._values.get("knowledge_base_id")
        assert result is not None, "Required property 'knowledge_base_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the knowledge base.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) Instructions for agents based on the design and type of information of the Knowledge Base.

        This will impact how Agents interact with the Knowledge Base.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("instruction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def knowledge_base_state(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies whether to use the knowledge base or not when sending an InvokeAgent request.

        :default: - ENABLED

        :stability: experimental
        '''
        result = self._values.get("knowledge_base_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kendra_index(self) -> _IKendraGenAiIndex_da04f105:
        '''(experimental) The GenAI Kendra Index ARN.

        :stability: experimental
        '''
        result = self._values.get("kendra_index")
        assert result is not None, "Required property 'kendra_index' is missing"
        return typing.cast(_IKendraGenAiIndex_da04f105, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraKnowledgeBaseAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.KendraKnowledgeBaseProps",
    jsii_struct_bases=[CommonKnowledgeBaseProps],
    name_mapping={
        "description": "description",
        "existing_role": "existingRole",
        "instruction": "instruction",
        "name": "name",
        "kendra_index": "kendraIndex",
    },
)
class KendraKnowledgeBaseProps(CommonKnowledgeBaseProps):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        instruction: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        kendra_index: _IKendraGenAiIndex_da04f105,
    ) -> None:
        '''(experimental) Properties for creating a Kendra Index Knowledge Base.

        :param description: (experimental) The description of the knowledge base. Default: - No description provided.
        :param existing_role: (experimental) Existing IAM role with policy statements granting appropriate permissions to invoke the specific embeddings models. Any entity (e.g., an AWS service or application) that assumes this role will be able to invoke or use the specified embeddings model within the Bedrock service.
        :param instruction: (experimental) A narrative description of the knowledge base. A Bedrock Agent can use this instruction to determine if it should query this Knowledge Base. Default: - No description provided.
        :param name: (experimental) The name of the knowledge base.
        :param kendra_index: (experimental) The Kendra Index to use for the knowledge base.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df2891c8481d2110f8ef1227393069a9fb2102f7ea78c6d79011264ca11a179f)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument existing_role", value=existing_role, expected_type=type_hints["existing_role"])
            check_type(argname="argument instruction", value=instruction, expected_type=type_hints["instruction"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument kendra_index", value=kendra_index, expected_type=type_hints["kendra_index"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kendra_index": kendra_index,
        }
        if description is not None:
            self._values["description"] = description
        if existing_role is not None:
            self._values["existing_role"] = existing_role
        if instruction is not None:
            self._values["instruction"] = instruction
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the knowledge base.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def existing_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) Existing IAM role with policy statements granting appropriate permissions to invoke the specific embeddings models.

        Any entity (e.g., an AWS service or application) that assumes
        this role will be able to invoke or use the
        specified embeddings model within the Bedrock service.

        :stability: experimental
        '''
        result = self._values.get("existing_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) A narrative description of the knowledge base.

        A Bedrock Agent can use this instruction to determine if it should
        query this Knowledge Base.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("instruction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the knowledge base.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kendra_index(self) -> _IKendraGenAiIndex_da04f105:
        '''(experimental) The Kendra Index to use for the knowledge base.

        :stability: experimental
        '''
        result = self._values.get("kendra_index")
        assert result is not None, "Required property 'kendra_index' is missing"
        return typing.cast(_IKendraGenAiIndex_da04f105, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraKnowledgeBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IKnowledgeBase)
class KnowledgeBaseBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.KnowledgeBaseBase",
):
    '''(experimental) Abstract base class for Knowledge Base (regarless the type).

    Contains methods valid for KBs either created with CDK or imported and
    applicable to Knowledge Bases of any type.

    :stability: experimental
    '''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2018afba30c8a414072bbb105ab599acca2c6b6fbe157efe69349742ccbf99d6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given principal identity permissions to perform actions on this knowledge base.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffbd6f230e5a20f5fb83bf781858e4c477d1419b7b476b7e099e7abd31643846)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantQuery")
    def grant_query(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to query the knowledge base.

        This contains:

        - Retrieve
        - RetrieveAndGenerate

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4aa7e889359278217a09e6a1d1cdad6957d67358183f869750b18d467a82947)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantQuery", [grantee]))

    @jsii.member(jsii_name="grantRetrieve")
    def grant_retrieve(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to retrieve content from the knowledge base.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0248f7f07e8c1872e77085a6db35a628b2ede66df317215b0653aa6cba4a0377)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRetrieve", [grantee]))

    @jsii.member(jsii_name="grantRetrieveAndGenerate")
    def grant_retrieve_and_generate(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to retrieve content from the knowledge base.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24aab71d54c86fb197cc2fd20e38a72d68d2b34a4ded13e5260624512f27da7b)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRetrieveAndGenerate", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseArn")
    @abc.abstractmethod
    def knowledge_base_arn(self) -> builtins.str:
        '''(experimental) The ARN of the knowledge base.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseId")
    @abc.abstractmethod
    def knowledge_base_id(self) -> builtins.str:
        '''(experimental) The ID of the knowledge base.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="role")
    @abc.abstractmethod
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role associated with the knowledge base.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    @abc.abstractmethod
    def type(self) -> "KnowledgeBaseType":
        '''(experimental) The type of knowledge base.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="description")
    @abc.abstractmethod
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the knowledge base.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="instruction")
    @abc.abstractmethod
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) A narrative instruction of the knowledge base.

        A Bedrock Agent can use this instruction to determine if it should
        query this Knowledge Base.

        :stability: experimental
        '''
        ...


class _KnowledgeBaseBaseProxy(
    KnowledgeBaseBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseArn")
    def knowledge_base_arn(self) -> builtins.str:
        '''(experimental) The ARN of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseArn"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseId")
    def knowledge_base_id(self) -> builtins.str:
        '''(experimental) The ID of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseId"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role associated with the knowledge base.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "KnowledgeBaseType":
        '''(experimental) The type of knowledge base.

        :stability: experimental
        '''
        return typing.cast("KnowledgeBaseType", jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="instruction")
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) A narrative instruction of the knowledge base.

        A Bedrock Agent can use this instruction to determine if it should
        query this Knowledge Base.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instruction"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, KnowledgeBaseBase).__jsii_proxy_class__ = lambda : _KnowledgeBaseBaseProxy


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.KnowledgeBaseType")
class KnowledgeBaseType(enum.Enum):
    '''(experimental) Types of possible knowledge bases supported by Amazon Bedrock Knowledge Bases.

    :stability: experimental
    '''

    VECTOR = "VECTOR"
    '''(experimental) Vector database with emebeddings vectors.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/kb-how-it-works.html
    :stability: experimental
    '''
    KENDRA = "KENDRA"
    '''(experimental) Kendra GenAI Index.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-build-kendra-genai-index.html
    :stability: experimental
    '''
    SQL = "SQL"
    '''(experimental) Structured data store (e.g. REDSHIFT).

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-build-structured.html
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.LambdaCustomTransformationProps",
    jsii_struct_bases=[],
    name_mapping={"lambda_function": "lambdaFunction", "s3_bucket_uri": "s3BucketUri"},
)
class LambdaCustomTransformationProps:
    def __init__(
        self,
        *,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        s3_bucket_uri: builtins.str,
    ) -> None:
        '''(experimental) Properties for configuring a Lambda-based custom transformation.

        :param lambda_function: (experimental) The Lambda function to use for custom document processing.
        :param s3_bucket_uri: (experimental) An S3 bucket URL/path to store input documents for Lambda processing and to store the output of the processed documents.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762879178fd972fbfc85b23a5a96fe26104fbaf3791957f75d2f92316a91cc7a)
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
            check_type(argname="argument s3_bucket_uri", value=s3_bucket_uri, expected_type=type_hints["s3_bucket_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lambda_function": lambda_function,
            "s3_bucket_uri": s3_bucket_uri,
        }

    @builtins.property
    def lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''(experimental) The Lambda function to use for custom document processing.

        :stability: experimental
        '''
        result = self._values.get("lambda_function")
        assert result is not None, "Required property 'lambda_function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    @builtins.property
    def s3_bucket_uri(self) -> builtins.str:
        '''(experimental) An S3 bucket URL/path to store input documents for Lambda processing and to store the output of the processed documents.

        :stability: experimental

        Example::

            "s3://my-bucket/chunk-processor/"
        '''
        result = self._values.get("s3_bucket_uri")
        assert result is not None, "Required property 's3_bucket_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaCustomTransformationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ManagedWordFilterType"
)
class ManagedWordFilterType(enum.Enum):
    '''(experimental) The managed word type filter available for guardrails.

    :stability: experimental
    '''

    PROFANITY = "PROFANITY"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PIIFilter",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "type": "type"},
)
class PIIFilter:
    def __init__(
        self,
        *,
        action: GuardrailAction,
        type: typing.Union[_General_e613aa3a, _Finance_2430d674, _InformationTechnology_2f99a404, _USASpecific_fa88de63, _CanadaSpecific_f80239d8, _UKSpecific_c9314648],
    ) -> None:
        '''(experimental) Interface to define a PII Filter.

        :param action: (experimental) The action to take when PII is detected.
        :param type: (experimental) The type of PII to filter.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68aa36b0ead1124a53b5c01582eeed48828bdcc66f87d80565fddd7cc232b72e)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "type": type,
        }

    @builtins.property
    def action(self) -> GuardrailAction:
        '''(experimental) The action to take when PII is detected.

        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(GuardrailAction, result)

    @builtins.property
    def type(
        self,
    ) -> typing.Union[_General_e613aa3a, _Finance_2430d674, _InformationTechnology_2f99a404, _USASpecific_fa88de63, _CanadaSpecific_f80239d8, _UKSpecific_c9314648]:
        '''(experimental) The type of PII to filter.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(typing.Union[_General_e613aa3a, _Finance_2430d674, _InformationTechnology_2f99a404, _USASpecific_fa88de63, _CanadaSpecific_f80239d8, _UKSpecific_c9314648], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PIIFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ParentActionGroupSignature(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ParentActionGroupSignature",
):
    '''(experimental) AWS Defined signatures for enabling certain capabilities in your agent.

    :stability: experimental
    '''

    def __init__(self, value: builtins.str) -> None:
        '''(experimental) Constructor should be used as a temporary solution when a new signature is supported but its implementation in CDK hasn't been added yet.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98539d4744437cf3435827d76a26eec0c07d53390b769ffdeba9b651eabb38af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.create(self.__class__, self, [value])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CODE_INTERPRETER")
    def CODE_INTERPRETER(cls) -> "ParentActionGroupSignature":
        '''(experimental) Signature that allows your agent to generate, run, and troubleshoot code when trying to complete a task.

        :stability: experimental
        '''
        return typing.cast("ParentActionGroupSignature", jsii.sget(cls, "CODE_INTERPRETER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="USER_INPUT")
    def USER_INPUT(cls) -> "ParentActionGroupSignature":
        '''(experimental) Signature that allows your agent to request the user for additional information when trying to complete a task.

        :stability: experimental
        '''
        return typing.cast("ParentActionGroupSignature", jsii.sget(cls, "USER_INPUT"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "value"))


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ParsingModality")
class ParsingModality(enum.Enum):
    '''
    :stability: experimental
    '''

    MULTIMODAL = "MULTIMODAL"
    '''(experimental) Specifies whether to enable parsing of multimodal data, including both text and/or images.

    :stability: experimental
    '''


class ParsingStategy(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ParsingStategy",
):
    '''(experimental) Represents an advanced parsing strategy configuration for Knowledge Base ingestion.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking-parsing.html#kb-advanced-parsing
    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="foundationModel")
    @builtins.classmethod
    def foundation_model(
        cls,
        *,
        parsing_model: IInvokable,
        parsing_modality: typing.Optional[ParsingModality] = None,
        parsing_prompt: typing.Optional[builtins.str] = None,
    ) -> "ParsingStategy":
        '''(experimental) Creates a Foundation Model-based parsing strategy for extracting non-textual information from documents such as tables and charts.

        - Additional costs apply when using advanced parsing due to foundation model usage.
        - There are limits on file types (PDF) and total data that can be parsed using advanced parsing.

        :param parsing_model: (experimental) The Foundation Model to use for parsing non-textual information. Currently supported models are Claude 3 Sonnet and Claude 3 Haiku.
        :param parsing_modality: (experimental) Specifies whether to enable parsing of multimodal data, including both text and/or images. Default: undefined - Text only
        :param parsing_prompt: (experimental) Custom prompt to instruct the parser on how to interpret the document. Default: - Uses the default instruction prompt as provided in the AWS Console.

        :see: https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-ds.html#kb-ds-supported-doc-formats-limits
        :stability: experimental
        '''
        props = FoundationModelParsingStategyProps(
            parsing_model=parsing_model,
            parsing_modality=parsing_modality,
            parsing_prompt=parsing_prompt,
        )

        return typing.cast("ParsingStategy", jsii.sinvoke(cls, "foundationModel", [props]))

    @jsii.member(jsii_name="generatePolicyStatements")
    @abc.abstractmethod
    def generate_policy_statements(
        self,
    ) -> typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="configuration")
    @abc.abstractmethod
    def configuration(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ParsingConfigurationProperty:
        '''(experimental) The CloudFormation property representation of this configuration.

        :stability: experimental
        '''
        ...

    @configuration.setter
    @abc.abstractmethod
    def configuration(
        self,
        value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ParsingConfigurationProperty,
    ) -> None:
        ...


class _ParsingStategyProxy(ParsingStategy):
    @jsii.member(jsii_name="generatePolicyStatements")
    def generate_policy_statements(
        self,
    ) -> typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement], jsii.invoke(self, "generatePolicyStatements", []))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ParsingConfigurationProperty:
        '''(experimental) The CloudFormation property representation of this configuration.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ParsingConfigurationProperty, jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(
        self,
        value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ParsingConfigurationProperty,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c20f93031aefe7465a4c9b7b8cbf589b874a8c6abd25dd259847d7c99f2c292b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ParsingStategy).__jsii_proxy_class__ = lambda : _ParsingStategyProxy


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ParsingStategyType"
)
class ParsingStategyType(enum.Enum):
    '''(experimental) Enum representing the types of parsing strategies available for Amazon Bedrock Knowledge Bases.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/kb-advanced-parsing.html
    :stability: experimental
    '''

    FOUNDATION_MODEL = "FOUNDATION_MODEL"
    '''(experimental) Uses a Bedrock Foundation Model for advanced parsing of non-textual information from documents.

    :stability: experimental
    '''
    DATA_AUTOMATION = "DATA_AUTOMATION"
    '''(experimental) Processes multimodal data using Bedrock Data Automation (BDA).

    It leverages
    generative AI to automate the transformation of multi-modal data into structured formats.
    If you choose a foundation model or Amazon Bedrock Data Automation for parsing and it fails
    to parse a file, the Amazon Bedrock default parser is used instead.

    :stability: experimental
    '''


@jsii.implements(IPrompt)
class Prompt(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.Prompt",
):
    '''(experimental) Prompts are a specific set of inputs that guide FMs on Amazon Bedrock to generate an appropriate response or output for a given task or instruction.

    You can optimize the prompt for specific use cases and models.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html
    :stability: experimental
    :resource: AWS::Bedrock::Prompt
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        prompt_name: builtins.str,
        default_variant: typing.Optional["PromptVariant"] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        variants: typing.Optional[typing.Sequence["PromptVariant"]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param prompt_name: (experimental) The name of the prompt.
        :param default_variant: (experimental) The Prompt Variant that will be used by default. Default: - No default variant provided.
        :param description: (experimental) A description of what the prompt does. Default: - No description provided.
        :param kms_key: (experimental) The KMS key that the prompt is encrypted with. Default: - AWS owned and managed key.
        :param variants: (experimental) The variants of your prompt. Variants can use different messages, models, or configurations so that you can compare their outputs to decide the best variant for your use case. Maximum of 3 variants.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28412a5d8ac170fe3a64e61ef6ae3f19e2ab4831e4f173b4d9dd49819888b236)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PromptProps(
            prompt_name=prompt_name,
            default_variant=default_variant,
            description=description,
            kms_key=kms_key,
            variants=variants,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromPromptAttributes")
    @builtins.classmethod
    def from_prompt_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        prompt_arn: builtins.str,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        prompt_version: typing.Optional[builtins.str] = None,
    ) -> IPrompt:
        '''
        :param scope: -
        :param id: -
        :param prompt_arn: (experimental) The ARN of the prompt.
        :param kms_key: (experimental) Optional KMS encryption key associated with this prompt.
        :param prompt_version: (experimental) The version of the prompt. Default: - "DRAFT"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__493e34f209102ea802c9e52bb8d42086b43ec2f571efc98a8d11938b5c35926c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = PromptAttributes(
            prompt_arn=prompt_arn, kms_key=kms_key, prompt_version=prompt_version
        )

        return typing.cast(IPrompt, jsii.sinvoke(cls, "fromPromptAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addVariant")
    def add_variant(self, variant: "PromptVariant") -> None:
        '''(experimental) Adds a prompt variant.

        :param variant: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebfa6edec3745b41e32e786ccd9bf47e56b752a48a1204aefa620f6425599454)
            check_type(argname="argument variant", value=variant, expected_type=type_hints["variant"])
        return typing.cast(None, jsii.invoke(self, "addVariant", [variant]))

    @jsii.member(jsii_name="createVersion")
    def create_version(
        self,
        description: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) Creates a prompt version, a static snapshot of your prompt that can be deployed to production.

        :param description: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc07b4411e1c17474873d667b41d3c8be2fd1ca6adf765c3090c15136423d774)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        return typing.cast(builtins.str, jsii.invoke(self, "createVersion", [description]))

    @builtins.property
    @jsii.member(jsii_name="promptArn")
    def prompt_arn(self) -> builtins.str:
        '''(experimental) The ARN of the prompt.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:prompt/PROMPT12345"
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptArn"))

    @builtins.property
    @jsii.member(jsii_name="promptId")
    def prompt_id(self) -> builtins.str:
        '''(experimental) The ID of the prompt.

        :stability: experimental

        Example::

            "PROMPT12345"
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptId"))

    @builtins.property
    @jsii.member(jsii_name="promptName")
    def prompt_name(self) -> builtins.str:
        '''(experimental) The name of the prompt.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptName"))

    @builtins.property
    @jsii.member(jsii_name="variants")
    def variants(self) -> typing.List["PromptVariant"]:
        '''(experimental) The variants of the prompt.

        :stability: experimental
        '''
        return typing.cast(typing.List["PromptVariant"], jsii.get(self, "variants"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key that the prompt is encrypted with.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))

    @builtins.property
    @jsii.member(jsii_name="promptVersion")
    def prompt_version(self) -> builtins.str:
        '''(experimental) The version of the prompt.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptVersion"))

    @prompt_version.setter
    def prompt_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30a1a38bb8b0d638d069ad28bc55cbba27373d5af3489817853bd7e1dc88410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "promptVersion", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "prompt_arn": "promptArn",
        "kms_key": "kmsKey",
        "prompt_version": "promptVersion",
    },
)
class PromptAttributes:
    def __init__(
        self,
        *,
        prompt_arn: builtins.str,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        prompt_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) ****************************************************************************                     ATTRS FOR IMPORTED CONSTRUCT ***************************************************************************.

        :param prompt_arn: (experimental) The ARN of the prompt.
        :param kms_key: (experimental) Optional KMS encryption key associated with this prompt.
        :param prompt_version: (experimental) The version of the prompt. Default: - "DRAFT"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65cd66a5ef99991ddde61b718842ff11d482414cb8db73961c80294c681f3502)
            check_type(argname="argument prompt_arn", value=prompt_arn, expected_type=type_hints["prompt_arn"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument prompt_version", value=prompt_version, expected_type=type_hints["prompt_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prompt_arn": prompt_arn,
        }
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if prompt_version is not None:
            self._values["prompt_version"] = prompt_version

    @builtins.property
    def prompt_arn(self) -> builtins.str:
        '''(experimental) The ARN of the prompt.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:prompt/PROMPT12345"
        '''
        result = self._values.get("prompt_arn")
        assert result is not None, "Required property 'prompt_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this prompt.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def prompt_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the prompt.

        :default: - "DRAFT"

        :stability: experimental
        '''
        result = self._values.get("prompt_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PromptAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IPrompt)
class PromptBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptBase",
):
    '''(experimental) Abstract base class for a Prompt.

    Contains methods and attributes valid for Promtps either created with CDK or imported.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__416e615710246dc6fdddab19da69a2adde0b7094028409f64cc9e0c153344b57)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantGet")
    def grant_get(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to get the prompt.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6010854ea9d0c593f1187eff0dbb1c606b73ff1be68e89b0d245291215123a)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantGet", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="promptArn")
    @abc.abstractmethod
    def prompt_arn(self) -> builtins.str:
        '''(experimental) The ARN of the prompt.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="promptId")
    @abc.abstractmethod
    def prompt_id(self) -> builtins.str:
        '''(experimental) The ID of the prompt.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    @abc.abstractmethod
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this prompt.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="promptVersion")
    @abc.abstractmethod
    def prompt_version(self) -> builtins.str:
        '''(experimental) The version of the prompt.

        :stability: experimental
        '''
        ...

    @prompt_version.setter
    @abc.abstractmethod
    def prompt_version(self, value: builtins.str) -> None:
        ...


class _PromptBaseProxy(
    PromptBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="promptArn")
    def prompt_arn(self) -> builtins.str:
        '''(experimental) The ARN of the prompt.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptArn"))

    @builtins.property
    @jsii.member(jsii_name="promptId")
    def prompt_id(self) -> builtins.str:
        '''(experimental) The ID of the prompt.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptId"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this prompt.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))

    @builtins.property
    @jsii.member(jsii_name="promptVersion")
    def prompt_version(self) -> builtins.str:
        '''(experimental) The version of the prompt.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptVersion"))

    @prompt_version.setter
    def prompt_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2e18fab10acf8af328be25f79340aeb64cc011327127be967f99f267d6b6c92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "promptVersion", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, PromptBase).__jsii_proxy_class__ = lambda : _PromptBaseProxy


class PromptOverrideConfiguration(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptOverrideConfiguration",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="fromSteps")
    @builtins.classmethod
    def from_steps(
        cls,
        steps: typing.Optional[typing.Sequence[typing.Union["PromptStepConfiguration", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> "PromptOverrideConfiguration":
        '''
        :param steps: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff8b175dc775b29e053d126300ee889ac45a8923baf78518a02105c4a2534f75)
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
        return typing.cast("PromptOverrideConfiguration", jsii.sinvoke(cls, "fromSteps", [steps]))

    @jsii.member(jsii_name="withCustomParser")
    @builtins.classmethod
    def with_custom_parser(
        cls,
        *,
        parser: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction] = None,
        steps: typing.Optional[typing.Sequence[typing.Union["PromptStepConfigurationCustomParser", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> "PromptOverrideConfiguration":
        '''(experimental) Creates a PromptOverrideConfiguration with a custom Lambda parser function.

        :param parser: 
        :param steps: 

        :stability: experimental
        '''
        props = CustomParserProps(parser=parser, steps=steps)

        return typing.cast("PromptOverrideConfiguration", jsii.sinvoke(cls, "withCustomParser", [props]))

    @builtins.property
    @jsii.member(jsii_name="parser")
    def parser(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction]:
        '''(experimental) The custom Lambda parser function to use.

        The Lambda parser processes and interprets the raw foundation model output.
        It receives an input event with:

        - messageVersion: Version of message format (1.0)
        - agent: Info about the agent (name, id, alias, version)
        - invokeModelRawResponse: Raw model output to parse
        - promptType: Type of prompt being parsed
        - overrideType: Type of override (OUTPUT_PARSER)

        The Lambda must return a response that the agent uses for next actions.

        :see: https://docs.aws.amazon.com/bedrock/latest/userguide/lambda-parser.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction], jsii.get(self, "parser"))

    @builtins.property
    @jsii.member(jsii_name="steps")
    def steps(
        self,
    ) -> typing.Optional[typing.List["PromptStepConfigurationCustomParser"]]:
        '''(experimental) The prompt configurations to override the prompt templates in the agent sequence.

        :default: - No prompt configuration will be overridden.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List["PromptStepConfigurationCustomParser"]], jsii.get(self, "steps"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptProps",
    jsii_struct_bases=[],
    name_mapping={
        "prompt_name": "promptName",
        "default_variant": "defaultVariant",
        "description": "description",
        "kms_key": "kmsKey",
        "variants": "variants",
    },
)
class PromptProps:
    def __init__(
        self,
        *,
        prompt_name: builtins.str,
        default_variant: typing.Optional["PromptVariant"] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        variants: typing.Optional[typing.Sequence["PromptVariant"]] = None,
    ) -> None:
        '''(experimental) ****************************************************************************                       PROPS FOR NEW CONSTRUCT ***************************************************************************.

        :param prompt_name: (experimental) The name of the prompt.
        :param default_variant: (experimental) The Prompt Variant that will be used by default. Default: - No default variant provided.
        :param description: (experimental) A description of what the prompt does. Default: - No description provided.
        :param kms_key: (experimental) The KMS key that the prompt is encrypted with. Default: - AWS owned and managed key.
        :param variants: (experimental) The variants of your prompt. Variants can use different messages, models, or configurations so that you can compare their outputs to decide the best variant for your use case. Maximum of 3 variants.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed24724d2a2267a3662057e3f507a648a9688b88f50d099de8ac08580da8541)
            check_type(argname="argument prompt_name", value=prompt_name, expected_type=type_hints["prompt_name"])
            check_type(argname="argument default_variant", value=default_variant, expected_type=type_hints["default_variant"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument variants", value=variants, expected_type=type_hints["variants"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prompt_name": prompt_name,
        }
        if default_variant is not None:
            self._values["default_variant"] = default_variant
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if variants is not None:
            self._values["variants"] = variants

    @builtins.property
    def prompt_name(self) -> builtins.str:
        '''(experimental) The name of the prompt.

        :stability: experimental
        '''
        result = self._values.get("prompt_name")
        assert result is not None, "Required property 'prompt_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_variant(self) -> typing.Optional["PromptVariant"]:
        '''(experimental) The Prompt Variant that will be used by default.

        :default: - No default variant provided.

        :stability: experimental
        '''
        result = self._values.get("default_variant")
        return typing.cast(typing.Optional["PromptVariant"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of what the prompt does.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key that the prompt is encrypted with.

        :default: - AWS owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def variants(self) -> typing.Optional[typing.List["PromptVariant"]]:
        '''(experimental) The variants of your prompt.

        Variants can use different messages, models,
        or configurations so that you can compare their outputs to decide the best
        variant for your use case. Maximum of 3 variants.

        :stability: experimental
        '''
        result = self._values.get("variants")
        return typing.cast(typing.Optional[typing.List["PromptVariant"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PromptProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IInvokable, IPromptRouter)
class PromptRouter(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptRouter",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        props: typing.Union["PromptRouterProps", typing.Dict[builtins.str, typing.Any]],
        region: builtins.str,
    ) -> None:
        '''
        :param props: -
        :param region: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f2a0966faeb6dd9c7e135b2e783450d7792ed9243c747b5b8742493ba672ba7)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        jsii.create(self.__class__, self, [props, region])

    @jsii.member(jsii_name="fromDefaultId")
    @builtins.classmethod
    def from_default_id(
        cls,
        default_router: DefaultPromptRouterIdentifier,
        region: builtins.str,
    ) -> "PromptRouter":
        '''
        :param default_router: -
        :param region: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f20b9011e0f783fb6d55e2d1bcafcfaf570c09d7271f5b62d707a9d253cd566)
            check_type(argname="argument default_router", value=default_router, expected_type=type_hints["default_router"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        return typing.cast("PromptRouter", jsii.sinvoke(cls, "fromDefaultId", [default_router, region]))

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Gives the appropriate policies to invoke and use the invokable abstraction.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afc424676ecf4a95f0287e0a3f6ea4c6b6bfda8245f81a410a2256f615221690)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantInvoke", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="invokableArn")
    def invokable_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Bedrock invokable abstraction.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "invokableArn"))

    @builtins.property
    @jsii.member(jsii_name="promptRouterArn")
    def prompt_router_arn(self) -> builtins.str:
        '''(experimental) The ARN of the prompt router.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptRouterArn"))

    @builtins.property
    @jsii.member(jsii_name="promptRouterId")
    def prompt_router_id(self) -> builtins.str:
        '''(experimental) The Id of the prompt router.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptRouterId"))

    @builtins.property
    @jsii.member(jsii_name="routingEndpoints")
    def routing_endpoints(self) -> typing.List[IInvokable]:
        '''(experimental) The foundation models / profiles this router will route to.

        :stability: experimental
        '''
        return typing.cast(typing.List[IInvokable], jsii.get(self, "routingEndpoints"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptRouterProps",
    jsii_struct_bases=[],
    name_mapping={
        "prompt_router_id": "promptRouterId",
        "routing_models": "routingModels",
    },
)
class PromptRouterProps:
    def __init__(
        self,
        *,
        prompt_router_id: builtins.str,
        routing_models: typing.Sequence["BedrockFoundationModel"],
    ) -> None:
        '''
        :param prompt_router_id: (experimental) Prompt Router Id.
        :param routing_models: (experimental) The foundation models this router will route to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e4b730bc2659721f1a04223df16609ae329cd99215327a755ffdc68d924ca1)
            check_type(argname="argument prompt_router_id", value=prompt_router_id, expected_type=type_hints["prompt_router_id"])
            check_type(argname="argument routing_models", value=routing_models, expected_type=type_hints["routing_models"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prompt_router_id": prompt_router_id,
            "routing_models": routing_models,
        }

    @builtins.property
    def prompt_router_id(self) -> builtins.str:
        '''(experimental) Prompt Router Id.

        :stability: experimental
        '''
        result = self._values.get("prompt_router_id")
        assert result is not None, "Required property 'prompt_router_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def routing_models(self) -> typing.List["BedrockFoundationModel"]:
        '''(experimental) The foundation models this router will route to.

        :stability: experimental
        '''
        result = self._values.get("routing_models")
        assert result is not None, "Required property 'routing_models' is missing"
        return typing.cast(typing.List["BedrockFoundationModel"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PromptRouterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptStepConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "step_type": "stepType",
        "custom_prompt_template": "customPromptTemplate",
        "inference_config": "inferenceConfig",
        "step_enabled": "stepEnabled",
    },
)
class PromptStepConfiguration:
    def __init__(
        self,
        *,
        step_type: AgentStepType,
        custom_prompt_template: typing.Optional[builtins.str] = None,
        inference_config: typing.Optional[typing.Union[InferenceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        step_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Contains configurations to override a prompt template in one part of an agent sequence.

        :param step_type: (experimental) The step in the agent sequence where to set a specific prompt configuration.
        :param custom_prompt_template: (experimental) The custom prompt template to be used. Default: - The default prompt template will be used.
        :param inference_config: (experimental) The inference configuration parameters to use.
        :param step_enabled: (experimental) Whether to enable or skip this step in the agent sequence. Default: - The default state for each step type is as follows. PRE_PROCESSING – ENABLED ORCHESTRATION – ENABLED KNOWLEDGE_BASE_RESPONSE_GENERATION – ENABLED POST_PROCESSING – DISABLED

        :stability: experimental
        '''
        if isinstance(inference_config, dict):
            inference_config = InferenceConfiguration(**inference_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f9369143f88c7f634aa2f46b339696a36f19a0c3ed51f8df732360e157f4f6e)
            check_type(argname="argument step_type", value=step_type, expected_type=type_hints["step_type"])
            check_type(argname="argument custom_prompt_template", value=custom_prompt_template, expected_type=type_hints["custom_prompt_template"])
            check_type(argname="argument inference_config", value=inference_config, expected_type=type_hints["inference_config"])
            check_type(argname="argument step_enabled", value=step_enabled, expected_type=type_hints["step_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "step_type": step_type,
        }
        if custom_prompt_template is not None:
            self._values["custom_prompt_template"] = custom_prompt_template
        if inference_config is not None:
            self._values["inference_config"] = inference_config
        if step_enabled is not None:
            self._values["step_enabled"] = step_enabled

    @builtins.property
    def step_type(self) -> AgentStepType:
        '''(experimental) The step in the agent sequence where to set a specific prompt configuration.

        :stability: experimental
        '''
        result = self._values.get("step_type")
        assert result is not None, "Required property 'step_type' is missing"
        return typing.cast(AgentStepType, result)

    @builtins.property
    def custom_prompt_template(self) -> typing.Optional[builtins.str]:
        '''(experimental) The custom prompt template to be used.

        :default: - The default prompt template will be used.

        :see: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-placeholders.html
        :stability: experimental
        '''
        result = self._values.get("custom_prompt_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inference_config(self) -> typing.Optional[InferenceConfiguration]:
        '''(experimental) The inference configuration parameters to use.

        :stability: experimental
        '''
        result = self._values.get("inference_config")
        return typing.cast(typing.Optional[InferenceConfiguration], result)

    @builtins.property
    def step_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable or skip this step in the agent sequence.

        :default:

        - The default state for each step type is as follows.

        PRE_PROCESSING – ENABLED
        ORCHESTRATION – ENABLED
        KNOWLEDGE_BASE_RESPONSE_GENERATION – ENABLED
        POST_PROCESSING – DISABLED

        :stability: experimental
        '''
        result = self._values.get("step_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PromptStepConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptStepConfigurationCustomParser",
    jsii_struct_bases=[PromptStepConfiguration],
    name_mapping={
        "step_type": "stepType",
        "custom_prompt_template": "customPromptTemplate",
        "inference_config": "inferenceConfig",
        "step_enabled": "stepEnabled",
        "use_custom_parser": "useCustomParser",
    },
)
class PromptStepConfigurationCustomParser(PromptStepConfiguration):
    def __init__(
        self,
        *,
        step_type: AgentStepType,
        custom_prompt_template: typing.Optional[builtins.str] = None,
        inference_config: typing.Optional[typing.Union[InferenceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        step_enabled: typing.Optional[builtins.bool] = None,
        use_custom_parser: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param step_type: (experimental) The step in the agent sequence where to set a specific prompt configuration.
        :param custom_prompt_template: (experimental) The custom prompt template to be used. Default: - The default prompt template will be used.
        :param inference_config: (experimental) The inference configuration parameters to use.
        :param step_enabled: (experimental) Whether to enable or skip this step in the agent sequence. Default: - The default state for each step type is as follows. PRE_PROCESSING – ENABLED ORCHESTRATION – ENABLED KNOWLEDGE_BASE_RESPONSE_GENERATION – ENABLED POST_PROCESSING – DISABLED
        :param use_custom_parser: (experimental) Whether to use the custom Lambda parser defined for the sequence. Default: - false

        :stability: experimental
        '''
        if isinstance(inference_config, dict):
            inference_config = InferenceConfiguration(**inference_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed1da902ff6fd0d45695a80270445b8635df4af40f4e642b1dcb831867b294cb)
            check_type(argname="argument step_type", value=step_type, expected_type=type_hints["step_type"])
            check_type(argname="argument custom_prompt_template", value=custom_prompt_template, expected_type=type_hints["custom_prompt_template"])
            check_type(argname="argument inference_config", value=inference_config, expected_type=type_hints["inference_config"])
            check_type(argname="argument step_enabled", value=step_enabled, expected_type=type_hints["step_enabled"])
            check_type(argname="argument use_custom_parser", value=use_custom_parser, expected_type=type_hints["use_custom_parser"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "step_type": step_type,
        }
        if custom_prompt_template is not None:
            self._values["custom_prompt_template"] = custom_prompt_template
        if inference_config is not None:
            self._values["inference_config"] = inference_config
        if step_enabled is not None:
            self._values["step_enabled"] = step_enabled
        if use_custom_parser is not None:
            self._values["use_custom_parser"] = use_custom_parser

    @builtins.property
    def step_type(self) -> AgentStepType:
        '''(experimental) The step in the agent sequence where to set a specific prompt configuration.

        :stability: experimental
        '''
        result = self._values.get("step_type")
        assert result is not None, "Required property 'step_type' is missing"
        return typing.cast(AgentStepType, result)

    @builtins.property
    def custom_prompt_template(self) -> typing.Optional[builtins.str]:
        '''(experimental) The custom prompt template to be used.

        :default: - The default prompt template will be used.

        :see: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-placeholders.html
        :stability: experimental
        '''
        result = self._values.get("custom_prompt_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inference_config(self) -> typing.Optional[InferenceConfiguration]:
        '''(experimental) The inference configuration parameters to use.

        :stability: experimental
        '''
        result = self._values.get("inference_config")
        return typing.cast(typing.Optional[InferenceConfiguration], result)

    @builtins.property
    def step_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable or skip this step in the agent sequence.

        :default:

        - The default state for each step type is as follows.

        PRE_PROCESSING – ENABLED
        ORCHESTRATION – ENABLED
        KNOWLEDGE_BASE_RESPONSE_GENERATION – ENABLED
        POST_PROCESSING – DISABLED

        :stability: experimental
        '''
        result = self._values.get("step_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def use_custom_parser(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to use the custom Lambda parser defined for the sequence.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("use_custom_parser")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PromptStepConfigurationCustomParser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptTemplateType"
)
class PromptTemplateType(enum.Enum):
    '''
    :stability: experimental
    '''

    TEXT = "TEXT"
    '''
    :stability: experimental
    '''
    CHAT = "CHAT"
    '''
    :stability: experimental
    '''


class PromptVariant(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptVariant",
):
    '''(experimental) Variants are specific sets of inputs that guide FMs on Amazon Bedrock to generate an appropriate response or output for a given task or instruction.

    You can optimize the prompt for specific use cases and models.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="agent")
    @builtins.classmethod
    def agent(
        cls,
        *,
        agent_alias: IAgentAlias,
        prompt_text: builtins.str,
        model: IInvokable,
        variant_name: builtins.str,
        prompt_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> "PromptVariant":
        '''(experimental) Static method to create an agent prompt template.

        :param agent_alias: (experimental) An alias pointing to the agent version to be used.
        :param prompt_text: (experimental) The text prompt. Variables are used by enclosing its name with double curly braces as in ``{{variable_name}}``.
        :param model: (experimental) The model which is used to run the prompt. The model could be a foundation model, a custom model, or a provisioned model.
        :param variant_name: (experimental) The name of the prompt variant.
        :param prompt_variables: (experimental) The variables in the prompt template that can be filled in at runtime.

        :stability: experimental
        '''
        props = AgentPromptVariantProps(
            agent_alias=agent_alias,
            prompt_text=prompt_text,
            model=model,
            variant_name=variant_name,
            prompt_variables=prompt_variables,
        )

        return typing.cast("PromptVariant", jsii.sinvoke(cls, "agent", [props]))

    @jsii.member(jsii_name="chat")
    @builtins.classmethod
    def chat(
        cls,
        *,
        messages: typing.Sequence[ChatMessage],
        inference_configuration: typing.Optional[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        system: typing.Optional[builtins.str] = None,
        tool_configuration: typing.Optional[typing.Union["ToolConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        model: IInvokable,
        variant_name: builtins.str,
        prompt_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> "PromptVariant":
        '''(experimental) Static method to create a chat template.

        Use this template type when
        the model supports the Converse API or the AnthropicClaude Messages API.
        This allows you to include a System prompt and previous User messages
        and Assistant messages for context.

        :param messages: (experimental) Inference configuration for the Chat Prompt. Must include at least one User Message. The messages should alternate between User and Assistant.
        :param inference_configuration: (experimental) Inference configuration for the Text Prompt.
        :param system: (experimental) Context or instructions for the model to consider before generating a response.
        :param tool_configuration: (experimental) The configuration with available tools to the model and how it must use them.
        :param model: (experimental) The model which is used to run the prompt. The model could be a foundation model, a custom model, or a provisioned model.
        :param variant_name: (experimental) The name of the prompt variant.
        :param prompt_variables: (experimental) The variables in the prompt template that can be filled in at runtime.

        :stability: experimental
        '''
        props = ChatPromptVariantProps(
            messages=messages,
            inference_configuration=inference_configuration,
            system=system,
            tool_configuration=tool_configuration,
            model=model,
            variant_name=variant_name,
            prompt_variables=prompt_variables,
        )

        return typing.cast("PromptVariant", jsii.sinvoke(cls, "chat", [props]))

    @jsii.member(jsii_name="text")
    @builtins.classmethod
    def text(
        cls,
        *,
        prompt_text: builtins.str,
        inference_configuration: typing.Optional[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        model: IInvokable,
        variant_name: builtins.str,
        prompt_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> "PromptVariant":
        '''(experimental) Static method to create a text template.

        :param prompt_text: (experimental) The text prompt. Variables are used by enclosing its name with double curly braces as in ``{{variable_name}}``.
        :param inference_configuration: (experimental) Inference configuration for the Text Prompt.
        :param model: (experimental) The model which is used to run the prompt. The model could be a foundation model, a custom model, or a provisioned model.
        :param variant_name: (experimental) The name of the prompt variant.
        :param prompt_variables: (experimental) The variables in the prompt template that can be filled in at runtime.

        :stability: experimental
        '''
        props = TextPromptVariantProps(
            prompt_text=prompt_text,
            inference_configuration=inference_configuration,
            model=model,
            variant_name=variant_name,
            prompt_variables=prompt_variables,
        )

        return typing.cast("PromptVariant", jsii.sinvoke(cls, "text", [props]))

    @builtins.property
    @jsii.member(jsii_name="name")
    @abc.abstractmethod
    def name(self) -> builtins.str:
        '''(experimental) The name of the prompt variant.

        :stability: experimental
        '''
        ...

    @name.setter
    @abc.abstractmethod
    def name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="templateConfiguration")
    @abc.abstractmethod
    def template_configuration(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptTemplateConfigurationProperty:
        '''(experimental) The template configuration.

        :stability: experimental
        '''
        ...

    @template_configuration.setter
    @abc.abstractmethod
    def template_configuration(
        self,
        value: _aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptTemplateConfigurationProperty,
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="templateType")
    @abc.abstractmethod
    def template_type(self) -> PromptTemplateType:
        '''(experimental) The type of prompt template.

        :stability: experimental
        '''
        ...

    @template_type.setter
    @abc.abstractmethod
    def template_type(self, value: PromptTemplateType) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="genAiResource")
    @abc.abstractmethod
    def gen_ai_resource(
        self,
    ) -> typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptGenAiResourceProperty]:
        '''(experimental) The template configuration.

        :stability: experimental
        '''
        ...

    @gen_ai_resource.setter
    @abc.abstractmethod
    def gen_ai_resource(
        self,
        value: typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptGenAiResourceProperty],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="inferenceConfiguration")
    @abc.abstractmethod
    def inference_configuration(
        self,
    ) -> typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptInferenceConfigurationProperty]:
        '''(experimental) The inference configuration.

        :stability: experimental
        '''
        ...

    @inference_configuration.setter
    @abc.abstractmethod
    def inference_configuration(
        self,
        value: typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptInferenceConfigurationProperty],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="modelId")
    @abc.abstractmethod
    def model_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The unique identifier of the model with which to run inference on the prompt.

        :stability: experimental
        '''
        ...

    @model_id.setter
    @abc.abstractmethod
    def model_id(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _PromptVariantProxy(PromptVariant):
    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the prompt variant.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47858dac9c23ea6d5fe047093eb7c553df8379b538751a421229fcd6090a3d99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateConfiguration")
    def template_configuration(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptTemplateConfigurationProperty:
        '''(experimental) The template configuration.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptTemplateConfigurationProperty, jsii.get(self, "templateConfiguration"))

    @template_configuration.setter
    def template_configuration(
        self,
        value: _aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptTemplateConfigurationProperty,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfacc76ecbab5bd528fdafd1e6e9ea9558ae6b7f7404301dfde9e66ae3ed865c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateType")
    def template_type(self) -> PromptTemplateType:
        '''(experimental) The type of prompt template.

        :stability: experimental
        '''
        return typing.cast(PromptTemplateType, jsii.get(self, "templateType"))

    @template_type.setter
    def template_type(self, value: PromptTemplateType) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb21a09b18d3af2233c1a12de246544b29d61535df0d28d7f9fb947c1b2668d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="genAiResource")
    def gen_ai_resource(
        self,
    ) -> typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptGenAiResourceProperty]:
        '''(experimental) The template configuration.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptGenAiResourceProperty], jsii.get(self, "genAiResource"))

    @gen_ai_resource.setter
    def gen_ai_resource(
        self,
        value: typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptGenAiResourceProperty],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d836d8435ed72ee87ad020c0a9ebf265fc0986eaef8eb628703d17470a9ace0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "genAiResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inferenceConfiguration")
    def inference_configuration(
        self,
    ) -> typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptInferenceConfigurationProperty]:
        '''(experimental) The inference configuration.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptInferenceConfigurationProperty], jsii.get(self, "inferenceConfiguration"))

    @inference_configuration.setter
    def inference_configuration(
        self,
        value: typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptInferenceConfigurationProperty],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__868e405119ddf957e9771368dbe10acb67f0d6f0dc2fe35578128be175024448)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inferenceConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The unique identifier of the model with which to run inference on the prompt.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelId"))

    @model_id.setter
    def model_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94db700745c23c237379ad0e9208bfa80e98851952c0558325390455e764cd02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelId", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, PromptVariant).__jsii_proxy_class__ = lambda : _PromptVariantProxy


class PromptVersion(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptVersion",
):
    '''(experimental) Creates a version of the prompt.

    Use this to create a static snapshot of your prompt that can be deployed
    to production. Versions allow you to easily switch between different
    configurations for your prompt and update your application with the most
    appropriate version for your use-case.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-deploy.html
    :stability: experimental
    :resource: AWS::Bedrock::PromptVersion
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        prompt: Prompt,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param prompt: (experimental) The prompt to use for this version.
        :param description: (experimental) The description of the prompt version.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6daa6c79624257e31d9072fc0f20e2f2fc9397635524aa9d067fb36cc7cbbc53)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PromptVersionProps(prompt=prompt, description=description)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="prompt")
    def prompt(self) -> Prompt:
        '''(experimental) The prompt used by this version.

        :stability: experimental
        '''
        return typing.cast(Prompt, jsii.get(self, "prompt"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''(experimental) The version of the prompt that was created.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="versionArn")
    def version_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the prompt version.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:prompt/PROMPT12345:1"
        '''
        return typing.cast(builtins.str, jsii.get(self, "versionArn"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptVersionProps",
    jsii_struct_bases=[],
    name_mapping={"prompt": "prompt", "description": "description"},
)
class PromptVersionProps:
    def __init__(
        self,
        *,
        prompt: Prompt,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prompt: (experimental) The prompt to use for this version.
        :param description: (experimental) The description of the prompt version.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49af665e03ae5aea14b78e3aee6d9f0d78722f97c5b289cb5dc844a1cf90815)
            check_type(argname="argument prompt", value=prompt, expected_type=type_hints["prompt"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prompt": prompt,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def prompt(self) -> Prompt:
        '''(experimental) The prompt to use for this version.

        :stability: experimental
        '''
        result = self._values.get("prompt")
        assert result is not None, "Required property 'prompt' is missing"
        return typing.cast(Prompt, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the prompt version.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PromptVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.RegexFilter",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "name": "name",
        "pattern": "pattern",
        "description": "description",
    },
)
class RegexFilter:
    def __init__(
        self,
        *,
        action: GuardrailAction,
        name: builtins.str,
        pattern: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) A Regular expression (regex) filter for sensitive information.

        :param action: (experimental) The action to take when a regex match is detected.
        :param name: (experimental) The name of the regex filter.
        :param pattern: (experimental) The regular expression pattern to match.
        :param description: (experimental) The description of the regex filter.

        :stability: experimental

        Example::

            const regexFilter: RegexFilter = {
              name: "my-custom-filter",
              action: SensitiveInfoGuardrailAction.BLOCK,
              pattern: "\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b",
            };
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a46345c7df17f55020986d90b7ae90f85b55d19822b9b2574bc1ff9831b2d20)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "name": name,
            "pattern": pattern,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def action(self) -> GuardrailAction:
        '''(experimental) The action to take when a regex match is detected.

        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(GuardrailAction, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the regex filter.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''(experimental) The regular expression pattern to match.

        :stability: experimental
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the regex filter.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegexFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ApiSchema(
    ApiSchema,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.S3ApiSchema",
):
    '''(experimental) Class to define an API Schema from an S3 object.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        object_key: builtins.str,
        object_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: The name of the S3 Bucket the object is in.
        :param object_key: The path inside the Bucket where the object is located at.
        :param object_version: The S3 object version.

        :stability: experimental
        '''
        location = _aws_cdk_aws_s3_ceddda9d.Location(
            bucket_name=bucket_name,
            object_key=object_key,
            object_version=object_version,
        )

        jsii.create(self.__class__, self, [location])


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.S3DataSourceAssociationProps",
    jsii_struct_bases=[DataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "bucket": "bucket",
        "inclusion_prefixes": "inclusionPrefixes",
    },
)
class S3DataSourceAssociationProps(DataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Interface to add a new S3DataSource to an existing KB.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param bucket: (experimental) The bucket that contains the data source.
        :param inclusion_prefixes: (experimental) The prefixes of the objects in the bucket that should be included in the data source. Default: - All objects in the bucket.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937192d503ab06e7d72cb5fca8edb1e0959f925784ef831da357511f9247a9ec)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument inclusion_prefixes", value=inclusion_prefixes, expected_type=type_hints["inclusion_prefixes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if inclusion_prefixes is not None:
            self._values["inclusion_prefixes"] = inclusion_prefixes

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''(experimental) The bucket that contains the data source.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def inclusion_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The prefixes of the objects in the bucket that should be included in the data source.

        :default: - All objects in the bucket.

        :stability: experimental
        '''
        result = self._values.get("inclusion_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3DataSourceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.S3DataSourceProps",
    jsii_struct_bases=[S3DataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "bucket": "bucket",
        "inclusion_prefixes": "inclusionPrefixes",
        "knowledge_base": "knowledgeBase",
    },
)
class S3DataSourceProps(S3DataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        knowledge_base: IKnowledgeBase,
    ) -> None:
        '''(experimental) Interface to create a new S3 Data Source object.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param bucket: (experimental) The bucket that contains the data source.
        :param inclusion_prefixes: (experimental) The prefixes of the objects in the bucket that should be included in the data source. Default: - All objects in the bucket.
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__061fd79f5c6cc3fdad0a0fcccc8c2a083f5deeb769270d6795cc47edeeaecc0b)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument inclusion_prefixes", value=inclusion_prefixes, expected_type=type_hints["inclusion_prefixes"])
            check_type(argname="argument knowledge_base", value=knowledge_base, expected_type=type_hints["knowledge_base"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "knowledge_base": knowledge_base,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if inclusion_prefixes is not None:
            self._values["inclusion_prefixes"] = inclusion_prefixes

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''(experimental) The bucket that contains the data source.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def inclusion_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The prefixes of the objects in the bucket that should be included in the data source.

        :default: - All objects in the bucket.

        :stability: experimental
        '''
        result = self._values.get("inclusion_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        result = self._values.get("knowledge_base")
        assert result is not None, "Required property 'knowledge_base' is missing"
        return typing.cast(IKnowledgeBase, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3DataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SalesforceCrawlingFilters",
    jsii_struct_bases=[],
    name_mapping={
        "object_type": "objectType",
        "exclude_patterns": "excludePatterns",
        "include_patterns": "includePatterns",
    },
)
class SalesforceCrawlingFilters:
    def __init__(
        self,
        *,
        object_type: "SalesforceObjectType",
        exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Defines the crawling filters for Salesforce data ingestion.

        :param object_type: (experimental) The Salesforce object type to which this filter applies.
        :param exclude_patterns: (experimental) Regular expression patterns to exclude specific content.
        :param include_patterns: (experimental) Regular expression patterns to include specific content.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9ba2de3246503cef86100625445a5010d4594edc17ad5fe4ba4d35b9c066463)
            check_type(argname="argument object_type", value=object_type, expected_type=type_hints["object_type"])
            check_type(argname="argument exclude_patterns", value=exclude_patterns, expected_type=type_hints["exclude_patterns"])
            check_type(argname="argument include_patterns", value=include_patterns, expected_type=type_hints["include_patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_type": object_type,
        }
        if exclude_patterns is not None:
            self._values["exclude_patterns"] = exclude_patterns
        if include_patterns is not None:
            self._values["include_patterns"] = include_patterns

    @builtins.property
    def object_type(self) -> "SalesforceObjectType":
        '''(experimental) The Salesforce object type to which this filter applies.

        :stability: experimental
        '''
        result = self._values.get("object_type")
        assert result is not None, "Required property 'object_type' is missing"
        return typing.cast("SalesforceObjectType", result)

    @builtins.property
    def exclude_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Regular expression patterns to exclude specific content.

        :stability: experimental
        '''
        result = self._values.get("exclude_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Regular expression patterns to include specific content.

        :stability: experimental
        '''
        result = self._values.get("include_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SalesforceCrawlingFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SalesforceDataSourceAssociationProps",
    jsii_struct_bases=[DataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "auth_secret": "authSecret",
        "endpoint": "endpoint",
        "filters": "filters",
    },
)
class SalesforceDataSourceAssociationProps(DataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        endpoint: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union[SalesforceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Interface to add a new data source to an existing KB.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Salesforce instance URL. Secret must start with "AmazonBedrock-".
        :param endpoint: (experimental) The Salesforce host URL or instance URL.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce9630b4dd940c86a5fa5c47ae28d9a991c3d58e7b9c5432ba828cb2cb213d00)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument auth_secret", value=auth_secret, expected_type=type_hints["auth_secret"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_secret": auth_secret,
            "endpoint": endpoint,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Salesforce instance URL.

        Secret must start with "AmazonBedrock-".

        :stability: experimental
        '''
        result = self._values.get("auth_secret")
        assert result is not None, "Required property 'auth_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''(experimental) The Salesforce host URL or instance URL.

        :stability: experimental

        Example::

            "https://company.salesforce.com/"
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[SalesforceCrawlingFilters]]:
        '''(experimental) The filters (regular expression patterns) for the crawling.

        If there's a conflict, the exclude pattern takes precedence.

        :default: None - all your content is crawled.

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[SalesforceCrawlingFilters]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SalesforceDataSourceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SalesforceDataSourceAuthType"
)
class SalesforceDataSourceAuthType(enum.Enum):
    '''(experimental) Represents the authentication types available for connecting to a Salesforce data source.

    :stability: experimental
    '''

    OAUTH2_CLIENT_CREDENTIALS = "OAUTH2_CLIENT_CREDENTIALS"
    '''(experimental) Your secret authentication credentials in AWS Secrets Manager should include: - ``consumerKey`` (app client ID) - ``consumerSecret`` (client secret) - ``authenticationUrl``.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SalesforceDataSourceProps",
    jsii_struct_bases=[SalesforceDataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "auth_secret": "authSecret",
        "endpoint": "endpoint",
        "filters": "filters",
        "knowledge_base": "knowledgeBase",
    },
)
class SalesforceDataSourceProps(SalesforceDataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        endpoint: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union[SalesforceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        knowledge_base: IKnowledgeBase,
    ) -> None:
        '''(experimental) Interface to create a new standalone data source object.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Salesforce instance URL. Secret must start with "AmazonBedrock-".
        :param endpoint: (experimental) The Salesforce host URL or instance URL.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7dc3117cebd56970b3e49e262627a6133820bc4f98949e5002679327375f4f3)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument auth_secret", value=auth_secret, expected_type=type_hints["auth_secret"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument knowledge_base", value=knowledge_base, expected_type=type_hints["knowledge_base"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_secret": auth_secret,
            "endpoint": endpoint,
            "knowledge_base": knowledge_base,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Salesforce instance URL.

        Secret must start with "AmazonBedrock-".

        :stability: experimental
        '''
        result = self._values.get("auth_secret")
        assert result is not None, "Required property 'auth_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''(experimental) The Salesforce host URL or instance URL.

        :stability: experimental

        Example::

            "https://company.salesforce.com/"
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[SalesforceCrawlingFilters]]:
        '''(experimental) The filters (regular expression patterns) for the crawling.

        If there's a conflict, the exclude pattern takes precedence.

        :default: None - all your content is crawled.

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[SalesforceCrawlingFilters]], result)

    @builtins.property
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        result = self._values.get("knowledge_base")
        assert result is not None, "Required property 'knowledge_base' is missing"
        return typing.cast(IKnowledgeBase, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SalesforceDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SalesforceObjectType"
)
class SalesforceObjectType(enum.Enum):
    '''(experimental) Represents the Salesforce object types that can be accessed by the data source connector.

    :stability: experimental
    '''

    ACCOUNT = "ACCOUNT"
    '''
    :stability: experimental
    '''
    ATTACHMENT = "ATTACHMENT"
    '''
    :stability: experimental
    '''
    CAMPAIGN = "CAMPAIGN"
    '''
    :stability: experimental
    '''
    CONTENT_VERSION = "CONTENT_VERSION"
    '''
    :stability: experimental
    '''
    PARTNER = "PARTNER"
    '''
    :stability: experimental
    '''
    PRICEBOOK_2 = "PRICEBOOK_2"
    '''
    :stability: experimental
    '''
    CASE = "CASE"
    '''
    :stability: experimental
    '''
    CONTACT = "CONTACT"
    '''
    :stability: experimental
    '''
    CONTRACT = "CONTRACT"
    '''
    :stability: experimental
    '''
    DOCUMENT = "DOCUMENT"
    '''
    :stability: experimental
    '''
    IDEA = "IDEA"
    '''
    :stability: experimental
    '''
    LEAD = "LEAD"
    '''
    :stability: experimental
    '''
    OPPORTUNITY = "OPPORTUNITY"
    '''
    :stability: experimental
    '''
    PRODUCT_2 = "PRODUCT_2"
    '''
    :stability: experimental
    '''
    SOLUTION = "SOLUTION"
    '''
    :stability: experimental
    '''
    TASK = "TASK"
    '''
    :stability: experimental
    '''
    FEED_ITEM = "FEED_ITEM"
    '''
    :stability: experimental
    '''
    FEED_COMMENT = "FEED_COMMENT"
    '''
    :stability: experimental
    '''
    KNOWLEDGE_KAV = "KNOWLEDGE_KAV"
    '''
    :stability: experimental
    '''
    USER = "USER"
    '''
    :stability: experimental
    '''
    COLLABORATION_GROUP = "COLLABORATION_GROUP"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SharePointCrawlingFilters",
    jsii_struct_bases=[],
    name_mapping={
        "object_type": "objectType",
        "exclude_patterns": "excludePatterns",
        "include_patterns": "includePatterns",
    },
)
class SharePointCrawlingFilters:
    def __init__(
        self,
        *,
        object_type: "SharePointObjectType",
        exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Defines the crawling filters for SharePoint data ingestion.

        These filters allow
        you to specify which content should be included or excluded during the crawling process.
        If you specify an inclusion and exclusion filter and both match a document,
        the exclusion filter takes precedence and the document isn’t crawled.

        :param object_type: (experimental) The SharePoint object type this filter applies to.
        :param exclude_patterns: (experimental) Optional array of regular expression patterns to exclude specific content. Content matching these patterns will be skipped during crawling.
        :param include_patterns: (experimental) Optional array of regular expression patterns to include specific content. Only content matching these patterns will be crawled.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc66a84b3c3b22e2879cf44c3edf17abf1ec9c5fb2ebee76fab9d6455ad43867)
            check_type(argname="argument object_type", value=object_type, expected_type=type_hints["object_type"])
            check_type(argname="argument exclude_patterns", value=exclude_patterns, expected_type=type_hints["exclude_patterns"])
            check_type(argname="argument include_patterns", value=include_patterns, expected_type=type_hints["include_patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_type": object_type,
        }
        if exclude_patterns is not None:
            self._values["exclude_patterns"] = exclude_patterns
        if include_patterns is not None:
            self._values["include_patterns"] = include_patterns

    @builtins.property
    def object_type(self) -> "SharePointObjectType":
        '''(experimental) The SharePoint object type this filter applies to.

        :stability: experimental
        '''
        result = self._values.get("object_type")
        assert result is not None, "Required property 'object_type' is missing"
        return typing.cast("SharePointObjectType", result)

    @builtins.property
    def exclude_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Optional array of regular expression patterns to exclude specific content.

        Content matching these patterns will be skipped during crawling.

        :stability: experimental

        Example::

            ['.*private.*', '.*confidential.*']
        '''
        result = self._values.get("exclude_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Optional array of regular expression patterns to include specific content.

        Only content matching these patterns will be crawled.

        :stability: experimental

        Example::

            ['.*public.*', '.*shared.*']
        '''
        result = self._values.get("include_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SharePointCrawlingFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SharePointDataSourceAssociationProps",
    jsii_struct_bases=[DataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "auth_secret": "authSecret",
        "domain": "domain",
        "site_urls": "siteUrls",
        "tenant_id": "tenantId",
        "filters": "filters",
    },
)
class SharePointDataSourceAssociationProps(DataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        domain: builtins.str,
        site_urls: typing.Sequence[builtins.str],
        tenant_id: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union[SharePointCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Interface to add a new data source to an existing KB.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Sharepoint instance URL. Secret must start with "AmazonBedrock-".
        :param domain: (experimental) The domain of your SharePoint instance or site URL/URLs.
        :param site_urls: (experimental) The SharePoint site URL/URLs. Must start with “https”. All URLs must start with same protocol.
        :param tenant_id: (experimental) The identifier of your Microsoft 365 tenant.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c756d6075defa355f5293064dde03559d8f435bbe0f49037277d8587875a983f)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument auth_secret", value=auth_secret, expected_type=type_hints["auth_secret"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument site_urls", value=site_urls, expected_type=type_hints["site_urls"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_secret": auth_secret,
            "domain": domain,
            "site_urls": site_urls,
            "tenant_id": tenant_id,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Sharepoint instance URL.

        Secret must start with "AmazonBedrock-".

        :stability: experimental
        '''
        result = self._values.get("auth_secret")
        assert result is not None, "Required property 'auth_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def domain(self) -> builtins.str:
        '''(experimental) The domain of your SharePoint instance or site URL/URLs.

        :stability: experimental

        Example::

            "yourdomain"
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def site_urls(self) -> typing.List[builtins.str]:
        '''(experimental) The SharePoint site URL/URLs.

        Must start with “https”. All URLs must start with same protocol.

        :stability: experimental

        Example::

            ["https://yourdomain.sharepoint.com/sites/mysite"]
        '''
        result = self._values.get("site_urls")
        assert result is not None, "Required property 'site_urls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''(experimental) The identifier of your Microsoft 365 tenant.

        :stability: experimental

        Example::

            "d1c035a6-1dcf-457d-97e3"
        '''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[SharePointCrawlingFilters]]:
        '''(experimental) The filters (regular expression patterns) for the crawling.

        If there's a conflict, the exclude pattern takes precedence.

        :default: None - all your content is crawled.

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[SharePointCrawlingFilters]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SharePointDataSourceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SharePointDataSourceAuthType"
)
class SharePointDataSourceAuthType(enum.Enum):
    '''(experimental) Represents the authentication types available for connecting to a SharePoint data source.

    :stability: experimental
    '''

    OAUTH2_CLIENT_CREDENTIALS = "OAUTH2_CLIENT_CREDENTIALS"
    '''(experimental) OAuth 2.0 Client Credentials flow for authentication with SharePoint. Your secret authentication credentials in AWS Secrets Manager should include: - ``username``: The admin username for SharePoint authentication - ``password``: The admin password associated with the username - ``clientId``: The client ID (also known as application ID) - ``clientSecret``: The client secret.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SharePointDataSourceProps",
    jsii_struct_bases=[SharePointDataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "auth_secret": "authSecret",
        "domain": "domain",
        "site_urls": "siteUrls",
        "tenant_id": "tenantId",
        "filters": "filters",
        "knowledge_base": "knowledgeBase",
    },
)
class SharePointDataSourceProps(SharePointDataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        domain: builtins.str,
        site_urls: typing.Sequence[builtins.str],
        tenant_id: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union[SharePointCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        knowledge_base: IKnowledgeBase,
    ) -> None:
        '''(experimental) Interface to create a new standalone data source object.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Sharepoint instance URL. Secret must start with "AmazonBedrock-".
        :param domain: (experimental) The domain of your SharePoint instance or site URL/URLs.
        :param site_urls: (experimental) The SharePoint site URL/URLs. Must start with “https”. All URLs must start with same protocol.
        :param tenant_id: (experimental) The identifier of your Microsoft 365 tenant.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77cac4a3c20de6d6ae043e36137b1e8760f3e2ae41c065f2a00a80740ce91b38)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument auth_secret", value=auth_secret, expected_type=type_hints["auth_secret"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument site_urls", value=site_urls, expected_type=type_hints["site_urls"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument knowledge_base", value=knowledge_base, expected_type=type_hints["knowledge_base"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_secret": auth_secret,
            "domain": domain,
            "site_urls": site_urls,
            "tenant_id": tenant_id,
            "knowledge_base": knowledge_base,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Sharepoint instance URL.

        Secret must start with "AmazonBedrock-".

        :stability: experimental
        '''
        result = self._values.get("auth_secret")
        assert result is not None, "Required property 'auth_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def domain(self) -> builtins.str:
        '''(experimental) The domain of your SharePoint instance or site URL/URLs.

        :stability: experimental

        Example::

            "yourdomain"
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def site_urls(self) -> typing.List[builtins.str]:
        '''(experimental) The SharePoint site URL/URLs.

        Must start with “https”. All URLs must start with same protocol.

        :stability: experimental

        Example::

            ["https://yourdomain.sharepoint.com/sites/mysite"]
        '''
        result = self._values.get("site_urls")
        assert result is not None, "Required property 'site_urls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''(experimental) The identifier of your Microsoft 365 tenant.

        :stability: experimental

        Example::

            "d1c035a6-1dcf-457d-97e3"
        '''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[SharePointCrawlingFilters]]:
        '''(experimental) The filters (regular expression patterns) for the crawling.

        If there's a conflict, the exclude pattern takes precedence.

        :default: None - all your content is crawled.

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[SharePointCrawlingFilters]], result)

    @builtins.property
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        result = self._values.get("knowledge_base")
        assert result is not None, "Required property 'knowledge_base' is missing"
        return typing.cast(IKnowledgeBase, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SharePointDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SharePointObjectType"
)
class SharePointObjectType(enum.Enum):
    '''(experimental) Represents the SharePoint object types that can be accessed by the data source connector.

    :stability: experimental
    '''

    PAGE = "PAGE"
    '''(experimental) Represents a SharePoint page, which typically contains web parts and content.

    :stability: experimental
    '''
    EVENT = "EVENT"
    '''(experimental) Represents a calendar event in SharePoint.

    :stability: experimental
    '''
    FILE = "FILE"
    '''(experimental) Represents a file stored in SharePoint document libraries.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.TextPromptVariantProps",
    jsii_struct_bases=[CommonPromptVariantProps],
    name_mapping={
        "model": "model",
        "variant_name": "variantName",
        "prompt_variables": "promptVariables",
        "prompt_text": "promptText",
        "inference_configuration": "inferenceConfiguration",
    },
)
class TextPromptVariantProps(CommonPromptVariantProps):
    def __init__(
        self,
        *,
        model: IInvokable,
        variant_name: builtins.str,
        prompt_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
        prompt_text: builtins.str,
        inference_configuration: typing.Optional[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param model: (experimental) The model which is used to run the prompt. The model could be a foundation model, a custom model, or a provisioned model.
        :param variant_name: (experimental) The name of the prompt variant.
        :param prompt_variables: (experimental) The variables in the prompt template that can be filled in at runtime.
        :param prompt_text: (experimental) The text prompt. Variables are used by enclosing its name with double curly braces as in ``{{variable_name}}``.
        :param inference_configuration: (experimental) Inference configuration for the Text Prompt.

        :stability: experimental
        '''
        if isinstance(inference_configuration, dict):
            inference_configuration = _aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty(**inference_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd54adac2df83b870909830e4b8468b5d71a8b9dac001336a6076238c87d3c3d)
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
            check_type(argname="argument variant_name", value=variant_name, expected_type=type_hints["variant_name"])
            check_type(argname="argument prompt_variables", value=prompt_variables, expected_type=type_hints["prompt_variables"])
            check_type(argname="argument prompt_text", value=prompt_text, expected_type=type_hints["prompt_text"])
            check_type(argname="argument inference_configuration", value=inference_configuration, expected_type=type_hints["inference_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "model": model,
            "variant_name": variant_name,
            "prompt_text": prompt_text,
        }
        if prompt_variables is not None:
            self._values["prompt_variables"] = prompt_variables
        if inference_configuration is not None:
            self._values["inference_configuration"] = inference_configuration

    @builtins.property
    def model(self) -> IInvokable:
        '''(experimental) The model which is used to run the prompt.

        The model could be a foundation
        model, a custom model, or a provisioned model.

        :stability: experimental
        '''
        result = self._values.get("model")
        assert result is not None, "Required property 'model' is missing"
        return typing.cast(IInvokable, result)

    @builtins.property
    def variant_name(self) -> builtins.str:
        '''(experimental) The name of the prompt variant.

        :stability: experimental
        '''
        result = self._values.get("variant_name")
        assert result is not None, "Required property 'variant_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prompt_variables(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The variables in the prompt template that can be filled in at runtime.

        :stability: experimental
        '''
        result = self._values.get("prompt_variables")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def prompt_text(self) -> builtins.str:
        '''(experimental) The text prompt.

        Variables are used by enclosing its name with double curly braces
        as in ``{{variable_name}}``.

        :stability: experimental
        '''
        result = self._values.get("prompt_text")
        assert result is not None, "Required property 'prompt_text' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def inference_configuration(
        self,
    ) -> typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty]:
        '''(experimental) Inference configuration for the Text Prompt.

        :stability: experimental
        '''
        result = self._values.get("inference_configuration")
        return typing.cast(typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TextPromptVariantProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ToolChoice(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ToolChoice",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        any: typing.Any,
        auto: typing.Any,
        tool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param any: -
        :param auto: -
        :param tool: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9b5680e044cd8da5aa0920f581bea14656963b55a384dfacf04768640a80971)
            check_type(argname="argument any", value=any, expected_type=type_hints["any"])
            check_type(argname="argument auto", value=auto, expected_type=type_hints["auto"])
            check_type(argname="argument tool", value=tool, expected_type=type_hints["tool"])
        jsii.create(self.__class__, self, [any, auto, tool])

    @jsii.member(jsii_name="specificTool")
    @builtins.classmethod
    def specific_tool(cls, tool_name: builtins.str) -> "ToolChoice":
        '''(experimental) The Model must request the specified tool.

        Only supported by some models like Anthropic Claude 3 models.

        :param tool_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d688d553ece27b2a018e94fe57c53ee4011a209f98b79453dc65103b27cffc48)
            check_type(argname="argument tool_name", value=tool_name, expected_type=type_hints["tool_name"])
        return typing.cast("ToolChoice", jsii.sinvoke(cls, "specificTool", [tool_name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANY")
    def ANY(cls) -> "ToolChoice":
        '''(experimental) The model must request at least one tool (no text is generated).

        :stability: experimental
        '''
        return typing.cast("ToolChoice", jsii.sget(cls, "ANY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AUTO")
    def AUTO(cls) -> "ToolChoice":
        '''(experimental) (Default).

        The Model automatically decides if a tool should be called or whether to generate text instead.

        :stability: experimental
        '''
        return typing.cast("ToolChoice", jsii.sget(cls, "AUTO"))

    @builtins.property
    @jsii.member(jsii_name="any")
    def any(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "any"))

    @builtins.property
    @jsii.member(jsii_name="auto")
    def auto(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "auto"))

    @builtins.property
    @jsii.member(jsii_name="tool")
    def tool(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tool"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ToolConfiguration",
    jsii_struct_bases=[],
    name_mapping={"tool_choice": "toolChoice", "tools": "tools"},
)
class ToolConfiguration:
    def __init__(
        self,
        *,
        tool_choice: ToolChoice,
        tools: typing.Sequence[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.ToolProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param tool_choice: 
        :param tools: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88cee3238bc8434e4eade16ff3314f3a8bc41921f90329b1ba433d8293c63b71)
            check_type(argname="argument tool_choice", value=tool_choice, expected_type=type_hints["tool_choice"])
            check_type(argname="argument tools", value=tools, expected_type=type_hints["tools"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tool_choice": tool_choice,
            "tools": tools,
        }

    @builtins.property
    def tool_choice(self) -> ToolChoice:
        '''
        :stability: experimental
        '''
        result = self._values.get("tool_choice")
        assert result is not None, "Required property 'tool_choice' is missing"
        return typing.cast(ToolChoice, result)

    @builtins.property
    def tools(
        self,
    ) -> typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.ToolProperty]:
        '''
        :stability: experimental
        '''
        result = self._values.get("tools")
        assert result is not None, "Required property 'tools' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.ToolProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ToolConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Topic(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.Topic",
):
    '''(experimental) Defines a topic to deny.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        definition: builtins.str,
        examples: typing.Sequence[builtins.str],
        name: builtins.str,
    ) -> None:
        '''
        :param definition: (experimental) Provide a clear definition to detect and block user inputs and FM responses that fall into this topic. Avoid starting with "don't".
        :param examples: (experimental) Representative phrases that refer to the topic. These phrases can represent a user input or a model response. Add up to 5 phrases, up to 100 characters each.
        :param name: (experimental) The name of the topic to deny.

        :stability: experimental
        '''
        props = CustomTopicProps(definition=definition, examples=examples, name=name)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(
        cls,
        *,
        definition: builtins.str,
        examples: typing.Sequence[builtins.str],
        name: builtins.str,
    ) -> "Topic":
        '''
        :param definition: (experimental) Provide a clear definition to detect and block user inputs and FM responses that fall into this topic. Avoid starting with "don't".
        :param examples: (experimental) Representative phrases that refer to the topic. These phrases can represent a user input or a model response. Add up to 5 phrases, up to 100 characters each.
        :param name: (experimental) The name of the topic to deny.

        :stability: experimental
        '''
        props = CustomTopicProps(definition=definition, examples=examples, name=name)

        return typing.cast("Topic", jsii.sinvoke(cls, "custom", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FINANCIAL_ADVICE")
    def FINANCIAL_ADVICE(cls) -> "Topic":
        '''
        :stability: experimental
        '''
        return typing.cast("Topic", jsii.sget(cls, "FINANCIAL_ADVICE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="INAPPROPRIATE_CONTENT")
    def INAPPROPRIATE_CONTENT(cls) -> "Topic":
        '''
        :stability: experimental
        '''
        return typing.cast("Topic", jsii.sget(cls, "INAPPROPRIATE_CONTENT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LEGAL_ADVICE")
    def LEGAL_ADVICE(cls) -> "Topic":
        '''
        :stability: experimental
        '''
        return typing.cast("Topic", jsii.sget(cls, "LEGAL_ADVICE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MEDICAL_ADVICE")
    def MEDICAL_ADVICE(cls) -> "Topic":
        '''
        :stability: experimental
        '''
        return typing.cast("Topic", jsii.sget(cls, "MEDICAL_ADVICE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="POLITICAL_ADVICE")
    def POLITICAL_ADVICE(cls) -> "Topic":
        '''
        :stability: experimental
        '''
        return typing.cast("Topic", jsii.sget(cls, "POLITICAL_ADVICE"))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> builtins.str:
        '''(experimental) Definition of the topic.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "definition"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the topic to deny.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="examples")
    def examples(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Representative phrases that refer to the topic.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "examples"))


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.TransformationStep"
)
class TransformationStep(enum.Enum):
    '''(experimental) Defines the step in the ingestion process where the custom transformation is applied.

    :stability: experimental
    '''

    POST_CHUNKING = "POST_CHUNKING"
    '''(experimental) Processes documents after they have been converted into chunks.

    This allows for custom chunk-level metadata addition or custom post-chunking logic.

    :stability: experimental
    '''


@jsii.implements(IVectorKnowledgeBase)
class VectorKnowledgeBase(
    KnowledgeBaseBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.VectorKnowledgeBase",
):
    '''(experimental) Deploys a Bedrock Knowledge Base and configures a backend by OpenSearch Serverless, Pinecone, Redis Enterprise Cloud or Amazon Aurora PostgreSQL.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        embeddings_model: "BedrockFoundationModel",
        index_name: typing.Optional[builtins.str] = None,
        vector_field: typing.Optional[builtins.str] = None,
        vector_index: typing.Optional[_VectorIndex_e5d266e9] = None,
        vector_store: typing.Optional[typing.Union[_ExistingAmazonAuroraVectorStore_f7ccb819, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]] = None,
        vector_type: typing.Optional["VectorType"] = None,
        description: typing.Optional[builtins.str] = None,
        existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        instruction: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param embeddings_model: (experimental) The embeddings model for the knowledge base.
        :param index_name: (experimental) The name of the vector index. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - 'bedrock-knowledge-base-default-index'
        :param vector_field: (experimental) The name of the field in the vector index. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - 'bedrock-knowledge-base-default-vector'
        :param vector_index: (experimental) The vector index for the OpenSearch Serverless backed knowledge base. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - A new vector index is created on the Vector Collection if vector store is of ``VectorCollection`` type.
        :param vector_store: (experimental) The vector store for the knowledge base. Must be either of type ``VectorCollection``, ``RedisEnterpriseVectorStore``, ``PineconeVectorStore`` or ``AmazonAuroraVectorStore``. Default: - A new OpenSearch Serverless vector collection is created.
        :param vector_type: (experimental) The vector type to store vector embeddings. Default: - VectorType.FLOATING_POINT
        :param description: (experimental) The description of the knowledge base. Default: - No description provided.
        :param existing_role: (experimental) Existing IAM role with policy statements granting appropriate permissions to invoke the specific embeddings models. Any entity (e.g., an AWS service or application) that assumes this role will be able to invoke or use the specified embeddings model within the Bedrock service.
        :param instruction: (experimental) A narrative description of the knowledge base. A Bedrock Agent can use this instruction to determine if it should query this Knowledge Base. Default: - No description provided.
        :param name: (experimental) The name of the knowledge base.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d431125f578eeb429055e5151ba6ee8f25bf86af603577323e147b9307afaa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VectorKnowledgeBaseProps(
            embeddings_model=embeddings_model,
            index_name=index_name,
            vector_field=vector_field,
            vector_index=vector_index,
            vector_store=vector_store,
            vector_type=vector_type,
            description=description,
            existing_role=existing_role,
            instruction=instruction,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromKnowledgeBaseAttributes")
    @builtins.classmethod
    def from_knowledge_base_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        execution_role_arn: builtins.str,
        knowledge_base_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        instruction: typing.Optional[builtins.str] = None,
        knowledge_base_state: typing.Optional[builtins.str] = None,
    ) -> IVectorKnowledgeBase:
        '''
        :param scope: -
        :param id: -
        :param execution_role_arn: (experimental) The Service Execution Role associated with the knowledge base.
        :param knowledge_base_id: (experimental) The ID of the knowledge base.
        :param description: (experimental) The description of the knowledge base. Default: - No description provided.
        :param instruction: (experimental) Instructions for agents based on the design and type of information of the Knowledge Base. This will impact how Agents interact with the Knowledge Base. Default: - No description provided.
        :param knowledge_base_state: (experimental) Specifies whether to use the knowledge base or not when sending an InvokeAgent request. Default: - ENABLED

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__071f6f3bd86a8b545dbba812f435c0f6d53fb8c691d0150900edad95da48759b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = VectorKnowledgeBaseAttributes(
            execution_role_arn=execution_role_arn,
            knowledge_base_id=knowledge_base_id,
            description=description,
            instruction=instruction,
            knowledge_base_state=knowledge_base_state,
        )

        return typing.cast(IVectorKnowledgeBase, jsii.sinvoke(cls, "fromKnowledgeBaseAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addConfluenceDataSource")
    def add_confluence_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        confluence_url: builtins.str,
        auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
        filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
    ) -> "ConfluenceDataSource":
        '''(experimental) Add a Confluence data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Confluence instance URL. Secret must start with "AmazonBedrock-".
        :param confluence_url: (experimental) The Confluence host URL or instance URL.
        :param auth_type: (experimental) The supported authentication method to connect to the data source. Default: ConfluenceDataSourceAuthType.OAUTH2_CLIENT_CREDENTIALS
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = ConfluenceDataSourceAssociationProps(
            auth_secret=auth_secret,
            confluence_url=confluence_url,
            auth_type=auth_type,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("ConfluenceDataSource", jsii.invoke(self, "addConfluenceDataSource", [props]))

    @jsii.member(jsii_name="addS3DataSource")
    def add_s3_data_source(
        self,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
    ) -> "S3DataSource":
        '''(experimental) Add an S3 data source to the knowledge base.

        :param bucket: (experimental) The bucket that contains the data source.
        :param inclusion_prefixes: (experimental) The prefixes of the objects in the bucket that should be included in the data source. Default: - All objects in the bucket.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = S3DataSourceAssociationProps(
            bucket=bucket,
            inclusion_prefixes=inclusion_prefixes,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("S3DataSource", jsii.invoke(self, "addS3DataSource", [props]))

    @jsii.member(jsii_name="addSalesforceDataSource")
    def add_salesforce_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        endpoint: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union[SalesforceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
    ) -> "SalesforceDataSource":
        '''(experimental) Add a Salesforce data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Salesforce instance URL. Secret must start with "AmazonBedrock-".
        :param endpoint: (experimental) The Salesforce host URL or instance URL.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = SalesforceDataSourceAssociationProps(
            auth_secret=auth_secret,
            endpoint=endpoint,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("SalesforceDataSource", jsii.invoke(self, "addSalesforceDataSource", [props]))

    @jsii.member(jsii_name="addSharePointDataSource")
    def add_share_point_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        domain: builtins.str,
        site_urls: typing.Sequence[builtins.str],
        tenant_id: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union[SharePointCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
    ) -> "SharePointDataSource":
        '''(experimental) Add a SharePoint data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Sharepoint instance URL. Secret must start with "AmazonBedrock-".
        :param domain: (experimental) The domain of your SharePoint instance or site URL/URLs.
        :param site_urls: (experimental) The SharePoint site URL/URLs. Must start with “https”. All URLs must start with same protocol.
        :param tenant_id: (experimental) The identifier of your Microsoft 365 tenant.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = SharePointDataSourceAssociationProps(
            auth_secret=auth_secret,
            domain=domain,
            site_urls=site_urls,
            tenant_id=tenant_id,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("SharePointDataSource", jsii.invoke(self, "addSharePointDataSource", [props]))

    @jsii.member(jsii_name="addWebCrawlerDataSource")
    def add_web_crawler_data_source(
        self,
        *,
        source_urls: typing.Sequence[builtins.str],
        crawling_rate: typing.Optional[jsii.Number] = None,
        crawling_scope: typing.Optional[CrawlingScope] = None,
        filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
    ) -> "WebCrawlerDataSource":
        '''(experimental) Add a web crawler data source to the knowledge base.

        :param source_urls: (experimental) The source urls in the format ``https://www.sitename.com``. Maximum of 100 URLs.
        :param crawling_rate: (experimental) The max rate at which pages are crawled, up to 300 per minute per host. Higher values will decrease sync time but increase the load on the host. Default: 300
        :param crawling_scope: (experimental) The scope of the crawling. Default: - CrawlingScope.DEFAULT
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = WebCrawlerDataSourceAssociationProps(
            source_urls=source_urls,
            crawling_rate=crawling_rate,
            crawling_scope=crawling_scope,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("WebCrawlerDataSource", jsii.invoke(self, "addWebCrawlerDataSource", [props]))

    @jsii.member(jsii_name="associateToAgent")
    def associate_to_agent(self, agent: "Agent") -> None:
        '''(experimental) Associate knowledge base with an agent.

        :param agent: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b6c29b0f94928797fa2fcc3e89d70bd0cd52190b237c122af7142338e6d0e3c)
            check_type(argname="argument agent", value=agent, expected_type=type_hints["agent"])
        return typing.cast(None, jsii.invoke(self, "associateToAgent", [agent]))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseArn")
    def knowledge_base_arn(self) -> builtins.str:
        '''(experimental) The ARN of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseArn"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseId")
    def knowledge_base_id(self) -> builtins.str:
        '''(experimental) The ID of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseId"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseInstance")
    def knowledge_base_instance(self) -> _aws_cdk_aws_bedrock_ceddda9d.CfnKnowledgeBase:
        '''(experimental) Instance of knowledge base.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnKnowledgeBase, jsii.get(self, "knowledgeBaseInstance"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role the Knowledge Base uses to access the vector store and data source.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> KnowledgeBaseType:
        '''(experimental) The type of knowledge base.

        :stability: experimental
        '''
        return typing.cast(KnowledgeBaseType, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="vectorStore")
    def vector_store(
        self,
    ) -> typing.Union[_ExistingAmazonAuroraVectorStore_f7ccb819, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]:
        '''(experimental) The vector store for the knowledge base.

        :stability: experimental
        '''
        return typing.cast(typing.Union[_ExistingAmazonAuroraVectorStore_f7ccb819, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196], jsii.get(self, "vectorStore"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="instruction")
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) Instructions for agents based on the design and type of information of the Knowledge Base.

        This will impact how Agents interact with the Knowledge Base.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instruction"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.VectorKnowledgeBaseAttributes",
    jsii_struct_bases=[CommonKnowledgeBaseAttributes],
    name_mapping={
        "execution_role_arn": "executionRoleArn",
        "knowledge_base_id": "knowledgeBaseId",
        "description": "description",
        "instruction": "instruction",
        "knowledge_base_state": "knowledgeBaseState",
    },
)
class VectorKnowledgeBaseAttributes(CommonKnowledgeBaseAttributes):
    def __init__(
        self,
        *,
        execution_role_arn: builtins.str,
        knowledge_base_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        instruction: typing.Optional[builtins.str] = None,
        knowledge_base_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for importing a knowledge base outside of this stack.

        :param execution_role_arn: (experimental) The Service Execution Role associated with the knowledge base.
        :param knowledge_base_id: (experimental) The ID of the knowledge base.
        :param description: (experimental) The description of the knowledge base. Default: - No description provided.
        :param instruction: (experimental) Instructions for agents based on the design and type of information of the Knowledge Base. This will impact how Agents interact with the Knowledge Base. Default: - No description provided.
        :param knowledge_base_state: (experimental) Specifies whether to use the knowledge base or not when sending an InvokeAgent request. Default: - ENABLED

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f9534cd4670aae2be069501f0039e758de585b8fd9859df103e55a26458438)
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument knowledge_base_id", value=knowledge_base_id, expected_type=type_hints["knowledge_base_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument instruction", value=instruction, expected_type=type_hints["instruction"])
            check_type(argname="argument knowledge_base_state", value=knowledge_base_state, expected_type=type_hints["knowledge_base_state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execution_role_arn": execution_role_arn,
            "knowledge_base_id": knowledge_base_id,
        }
        if description is not None:
            self._values["description"] = description
        if instruction is not None:
            self._values["instruction"] = instruction
        if knowledge_base_state is not None:
            self._values["knowledge_base_state"] = knowledge_base_state

    @builtins.property
    def execution_role_arn(self) -> builtins.str:
        '''(experimental) The Service Execution Role associated with the knowledge base.

        :stability: experimental

        Example::

            "arn:aws:iam::123456789012:role/AmazonBedrockExecutionRoleForKnowledgeBaseawscdkbdgeBaseKB12345678"
        '''
        result = self._values.get("execution_role_arn")
        assert result is not None, "Required property 'execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def knowledge_base_id(self) -> builtins.str:
        '''(experimental) The ID of the knowledge base.

        :stability: experimental

        Example::

            "KB12345678"
        '''
        result = self._values.get("knowledge_base_id")
        assert result is not None, "Required property 'knowledge_base_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the knowledge base.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) Instructions for agents based on the design and type of information of the Knowledge Base.

        This will impact how Agents interact with the Knowledge Base.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("instruction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def knowledge_base_state(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies whether to use the knowledge base or not when sending an InvokeAgent request.

        :default: - ENABLED

        :stability: experimental
        '''
        result = self._values.get("knowledge_base_state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VectorKnowledgeBaseAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.VectorKnowledgeBaseProps",
    jsii_struct_bases=[CommonKnowledgeBaseProps],
    name_mapping={
        "description": "description",
        "existing_role": "existingRole",
        "instruction": "instruction",
        "name": "name",
        "embeddings_model": "embeddingsModel",
        "index_name": "indexName",
        "vector_field": "vectorField",
        "vector_index": "vectorIndex",
        "vector_store": "vectorStore",
        "vector_type": "vectorType",
    },
)
class VectorKnowledgeBaseProps(CommonKnowledgeBaseProps):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        instruction: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        embeddings_model: "BedrockFoundationModel",
        index_name: typing.Optional[builtins.str] = None,
        vector_field: typing.Optional[builtins.str] = None,
        vector_index: typing.Optional[_VectorIndex_e5d266e9] = None,
        vector_store: typing.Optional[typing.Union[_ExistingAmazonAuroraVectorStore_f7ccb819, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]] = None,
        vector_type: typing.Optional["VectorType"] = None,
    ) -> None:
        '''(experimental) Properties for a knowledge base.

        :param description: (experimental) The description of the knowledge base. Default: - No description provided.
        :param existing_role: (experimental) Existing IAM role with policy statements granting appropriate permissions to invoke the specific embeddings models. Any entity (e.g., an AWS service or application) that assumes this role will be able to invoke or use the specified embeddings model within the Bedrock service.
        :param instruction: (experimental) A narrative description of the knowledge base. A Bedrock Agent can use this instruction to determine if it should query this Knowledge Base. Default: - No description provided.
        :param name: (experimental) The name of the knowledge base.
        :param embeddings_model: (experimental) The embeddings model for the knowledge base.
        :param index_name: (experimental) The name of the vector index. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - 'bedrock-knowledge-base-default-index'
        :param vector_field: (experimental) The name of the field in the vector index. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - 'bedrock-knowledge-base-default-vector'
        :param vector_index: (experimental) The vector index for the OpenSearch Serverless backed knowledge base. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - A new vector index is created on the Vector Collection if vector store is of ``VectorCollection`` type.
        :param vector_store: (experimental) The vector store for the knowledge base. Must be either of type ``VectorCollection``, ``RedisEnterpriseVectorStore``, ``PineconeVectorStore`` or ``AmazonAuroraVectorStore``. Default: - A new OpenSearch Serverless vector collection is created.
        :param vector_type: (experimental) The vector type to store vector embeddings. Default: - VectorType.FLOATING_POINT

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47fae20f2001bac9670b6ad45b66ff9f8fe8e075e4d4f97b9f3130e153d3ea79)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument existing_role", value=existing_role, expected_type=type_hints["existing_role"])
            check_type(argname="argument instruction", value=instruction, expected_type=type_hints["instruction"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument embeddings_model", value=embeddings_model, expected_type=type_hints["embeddings_model"])
            check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
            check_type(argname="argument vector_field", value=vector_field, expected_type=type_hints["vector_field"])
            check_type(argname="argument vector_index", value=vector_index, expected_type=type_hints["vector_index"])
            check_type(argname="argument vector_store", value=vector_store, expected_type=type_hints["vector_store"])
            check_type(argname="argument vector_type", value=vector_type, expected_type=type_hints["vector_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "embeddings_model": embeddings_model,
        }
        if description is not None:
            self._values["description"] = description
        if existing_role is not None:
            self._values["existing_role"] = existing_role
        if instruction is not None:
            self._values["instruction"] = instruction
        if name is not None:
            self._values["name"] = name
        if index_name is not None:
            self._values["index_name"] = index_name
        if vector_field is not None:
            self._values["vector_field"] = vector_field
        if vector_index is not None:
            self._values["vector_index"] = vector_index
        if vector_store is not None:
            self._values["vector_store"] = vector_store
        if vector_type is not None:
            self._values["vector_type"] = vector_type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the knowledge base.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def existing_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) Existing IAM role with policy statements granting appropriate permissions to invoke the specific embeddings models.

        Any entity (e.g., an AWS service or application) that assumes
        this role will be able to invoke or use the
        specified embeddings model within the Bedrock service.

        :stability: experimental
        '''
        result = self._values.get("existing_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) A narrative description of the knowledge base.

        A Bedrock Agent can use this instruction to determine if it should
        query this Knowledge Base.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("instruction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the knowledge base.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def embeddings_model(self) -> "BedrockFoundationModel":
        '''(experimental) The embeddings model for the knowledge base.

        :stability: experimental
        '''
        result = self._values.get("embeddings_model")
        assert result is not None, "Required property 'embeddings_model' is missing"
        return typing.cast("BedrockFoundationModel", result)

    @builtins.property
    def index_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the vector index.

        If vectorStore is not of type ``VectorCollection``,
        do not include this property as it will throw error.

        :default: - 'bedrock-knowledge-base-default-index'

        :stability: experimental
        '''
        result = self._values.get("index_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vector_field(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the field in the vector index.

        If vectorStore is not of type ``VectorCollection``,
        do not include this property as it will throw error.

        :default: - 'bedrock-knowledge-base-default-vector'

        :stability: experimental
        '''
        result = self._values.get("vector_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vector_index(self) -> typing.Optional[_VectorIndex_e5d266e9]:
        '''(experimental) The vector index for the OpenSearch Serverless backed knowledge base.

        If vectorStore is not of type ``VectorCollection``, do not include
        this property as it will throw error.

        :default:

        - A new vector index is created on the Vector Collection
        if vector store is of ``VectorCollection`` type.

        :stability: experimental
        '''
        result = self._values.get("vector_index")
        return typing.cast(typing.Optional[_VectorIndex_e5d266e9], result)

    @builtins.property
    def vector_store(
        self,
    ) -> typing.Optional[typing.Union[_ExistingAmazonAuroraVectorStore_f7ccb819, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]]:
        '''(experimental) The vector store for the knowledge base.

        Must be either of
        type ``VectorCollection``, ``RedisEnterpriseVectorStore``,
        ``PineconeVectorStore`` or ``AmazonAuroraVectorStore``.

        :default: - A new OpenSearch Serverless vector collection is created.

        :stability: experimental
        '''
        result = self._values.get("vector_store")
        return typing.cast(typing.Optional[typing.Union[_ExistingAmazonAuroraVectorStore_f7ccb819, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]], result)

    @builtins.property
    def vector_type(self) -> typing.Optional["VectorType"]:
        '''(experimental) The vector type to store vector embeddings.

        :default: - VectorType.FLOATING_POINT

        :stability: experimental
        '''
        result = self._values.get("vector_type")
        return typing.cast(typing.Optional["VectorType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VectorKnowledgeBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.VectorType")
class VectorType(enum.Enum):
    '''(experimental) The data type for the vectors when using a model to convert text into vector embeddings.

    The model must support the specified data type for vector embeddings. Floating-point (float32)
    is the default data type, and is supported by most models for vector embeddings. See Supported
    embeddings models for information on the available models and their vector data types.

    :stability: experimental
    '''

    FLOATING_POINT = "FLOATING_POINT"
    '''(experimental) ``FLOATING_POINT`` convert the data to floating-point (float32) vector embeddings (more precise, but more costly).

    :stability: experimental
    '''
    BINARY = "BINARY"
    '''(experimental) ``BINARY`` convert the data to binary vector embeddings (less precise, but less costly).

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.WebCrawlerDataSourceAssociationProps",
    jsii_struct_bases=[DataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "source_urls": "sourceUrls",
        "crawling_rate": "crawlingRate",
        "crawling_scope": "crawlingScope",
        "filters": "filters",
    },
)
class WebCrawlerDataSourceAssociationProps(DataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        source_urls: typing.Sequence[builtins.str],
        crawling_rate: typing.Optional[jsii.Number] = None,
        crawling_scope: typing.Optional[CrawlingScope] = None,
        filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Interface to add a new data source to an existing KB.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param source_urls: (experimental) The source urls in the format ``https://www.sitename.com``. Maximum of 100 URLs.
        :param crawling_rate: (experimental) The max rate at which pages are crawled, up to 300 per minute per host. Higher values will decrease sync time but increase the load on the host. Default: 300
        :param crawling_scope: (experimental) The scope of the crawling. Default: - CrawlingScope.DEFAULT
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None

        :stability: experimental
        '''
        if isinstance(filters, dict):
            filters = CrawlingFilters(**filters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f2d4384933474c1f544b514a9796e0d1ce1eea63851d2a0cbad594f4b1d4830)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument source_urls", value=source_urls, expected_type=type_hints["source_urls"])
            check_type(argname="argument crawling_rate", value=crawling_rate, expected_type=type_hints["crawling_rate"])
            check_type(argname="argument crawling_scope", value=crawling_scope, expected_type=type_hints["crawling_scope"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_urls": source_urls,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if crawling_rate is not None:
            self._values["crawling_rate"] = crawling_rate
        if crawling_scope is not None:
            self._values["crawling_scope"] = crawling_scope
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def source_urls(self) -> typing.List[builtins.str]:
        '''(experimental) The source urls in the format ``https://www.sitename.com``. Maximum of 100 URLs.

        :stability: experimental
        '''
        result = self._values.get("source_urls")
        assert result is not None, "Required property 'source_urls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def crawling_rate(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The max rate at which pages are crawled, up to 300 per minute per host.

        Higher values will decrease sync time but increase the load on the host.

        :default: 300

        :stability: experimental
        '''
        result = self._values.get("crawling_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def crawling_scope(self) -> typing.Optional[CrawlingScope]:
        '''(experimental) The scope of the crawling.

        :default: - CrawlingScope.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("crawling_scope")
        return typing.cast(typing.Optional[CrawlingScope], result)

    @builtins.property
    def filters(self) -> typing.Optional[CrawlingFilters]:
        '''(experimental) The filters (regular expression patterns) for the crawling.

        If there's a conflict, the exclude pattern takes precedence.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[CrawlingFilters], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebCrawlerDataSourceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.WebCrawlerDataSourceProps",
    jsii_struct_bases=[WebCrawlerDataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "source_urls": "sourceUrls",
        "crawling_rate": "crawlingRate",
        "crawling_scope": "crawlingScope",
        "filters": "filters",
        "knowledge_base": "knowledgeBase",
    },
)
class WebCrawlerDataSourceProps(WebCrawlerDataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        source_urls: typing.Sequence[builtins.str],
        crawling_rate: typing.Optional[jsii.Number] = None,
        crawling_scope: typing.Optional[CrawlingScope] = None,
        filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
        knowledge_base: IKnowledgeBase,
    ) -> None:
        '''(experimental) Interface to create a new standalone data source object.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param source_urls: (experimental) The source urls in the format ``https://www.sitename.com``. Maximum of 100 URLs.
        :param crawling_rate: (experimental) The max rate at which pages are crawled, up to 300 per minute per host. Higher values will decrease sync time but increase the load on the host. Default: 300
        :param crawling_scope: (experimental) The scope of the crawling. Default: - CrawlingScope.DEFAULT
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        if isinstance(filters, dict):
            filters = CrawlingFilters(**filters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc7f1066a3d54b5b87f6d6542c10949f6480a3b99f641342456db80c76a73a8c)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument source_urls", value=source_urls, expected_type=type_hints["source_urls"])
            check_type(argname="argument crawling_rate", value=crawling_rate, expected_type=type_hints["crawling_rate"])
            check_type(argname="argument crawling_scope", value=crawling_scope, expected_type=type_hints["crawling_scope"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument knowledge_base", value=knowledge_base, expected_type=type_hints["knowledge_base"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_urls": source_urls,
            "knowledge_base": knowledge_base,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if crawling_rate is not None:
            self._values["crawling_rate"] = crawling_rate
        if crawling_scope is not None:
            self._values["crawling_scope"] = crawling_scope
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def source_urls(self) -> typing.List[builtins.str]:
        '''(experimental) The source urls in the format ``https://www.sitename.com``. Maximum of 100 URLs.

        :stability: experimental
        '''
        result = self._values.get("source_urls")
        assert result is not None, "Required property 'source_urls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def crawling_rate(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The max rate at which pages are crawled, up to 300 per minute per host.

        Higher values will decrease sync time but increase the load on the host.

        :default: 300

        :stability: experimental
        '''
        result = self._values.get("crawling_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def crawling_scope(self) -> typing.Optional[CrawlingScope]:
        '''(experimental) The scope of the crawling.

        :default: - CrawlingScope.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("crawling_scope")
        return typing.cast(typing.Optional[CrawlingScope], result)

    @builtins.property
    def filters(self) -> typing.Optional[CrawlingFilters]:
        '''(experimental) The filters (regular expression patterns) for the crawling.

        If there's a conflict, the exclude pattern takes precedence.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[CrawlingFilters], result)

    @builtins.property
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        result = self._values.get("knowledge_base")
        assert result is not None, "Required property 'knowledge_base' is missing"
        return typing.cast(IKnowledgeBase, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebCrawlerDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IAgentAlias)
class AgentAliasBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentAliasBase",
):
    '''(experimental) Abstract base class for an Agent.

    Contains methods and attributes valid for Agents either created with CDK or imported.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d536a97c14b9ec306362ef2e875029959b8f84ade2155154aed19edb293431e4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given principal identity permissions to perform actions on this agent alias.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa6bd6a42c3fe8b4e86fa23e7ace7c0b0c85484f76e3f333524490377b8a4863)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to invoke the agent alias.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827dee60e296765d8e60eb0f1309cd9e89e299b3b2433b78b0a788426ea1010c)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantInvoke", [grantee]))

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Define an EventBridge rule that triggers when something happens to this agent alias.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b448e39f322730fa1e625ecc3696ed24683045df5d66fa9df27b36a524a5c262)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onCloudTrailEvent", [id, options]))

    @builtins.property
    @jsii.member(jsii_name="agent")
    @abc.abstractmethod
    def agent(self) -> IAgent:
        '''(experimental) The underlying agent for this alias.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="aliasArn")
    @abc.abstractmethod
    def alias_arn(self) -> builtins.str:
        '''(experimental) The ARN of the agent alias.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="aliasId")
    @abc.abstractmethod
    def alias_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the agent alias.

        :stability: experimental
        '''
        ...


class _AgentAliasBaseProxy(
    AgentAliasBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="agent")
    def agent(self) -> IAgent:
        '''(experimental) The underlying agent for this alias.

        :stability: experimental
        '''
        return typing.cast(IAgent, jsii.get(self, "agent"))

    @builtins.property
    @jsii.member(jsii_name="aliasArn")
    def alias_arn(self) -> builtins.str:
        '''(experimental) The ARN of the agent alias.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "aliasArn"))

    @builtins.property
    @jsii.member(jsii_name="aliasId")
    def alias_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the agent alias.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "aliasId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, AgentAliasBase).__jsii_proxy_class__ = lambda : _AgentAliasBaseProxy


@jsii.implements(IAgent)
class AgentBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentBase",
):
    '''(experimental) Abstract base class for an Agent.

    Contains methods and attributes valid for Agents either created with CDK or imported.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41c3a5d0cda4ce4456eb176ad1c07357a39d7fe3af20e3e68687067f16c8c7aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="agentArn")
    @abc.abstractmethod
    def agent_arn(self) -> builtins.str:
        '''(experimental) The ARN of the agent.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="agentId")
    @abc.abstractmethod
    def agent_id(self) -> builtins.str:
        '''(experimental) The ID of the Agent.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="role")
    @abc.abstractmethod
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The IAM role associated to the agent.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    @abc.abstractmethod
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this agent.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="lastUpdated")
    @abc.abstractmethod
    def last_updated(self) -> typing.Optional[builtins.str]:
        '''(experimental) When this agent was last updated.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="agentVersion")
    @abc.abstractmethod
    def agent_version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @agent_version.setter
    @abc.abstractmethod
    def agent_version(self, value: builtins.str) -> None:
        ...


class _AgentBaseProxy(
    AgentBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="agentArn")
    def agent_arn(self) -> builtins.str:
        '''(experimental) The ARN of the agent.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "agentArn"))

    @builtins.property
    @jsii.member(jsii_name="agentId")
    def agent_id(self) -> builtins.str:
        '''(experimental) The ID of the Agent.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "agentId"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The IAM role associated to the agent.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this agent.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdated")
    def last_updated(self) -> typing.Optional[builtins.str]:
        '''(experimental) When this agent was last updated.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastUpdated"))

    @builtins.property
    @jsii.member(jsii_name="agentVersion")
    def agent_version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "agentVersion"))

    @agent_version.setter
    def agent_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__483f422cc7a4f217d1c995fd9ee49bffdd94d76795a73ccb19ca6a05a2917aaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentVersion", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, AgentBase).__jsii_proxy_class__ = lambda : _AgentBaseProxy


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentPromptVariantProps",
    jsii_struct_bases=[CommonPromptVariantProps],
    name_mapping={
        "model": "model",
        "variant_name": "variantName",
        "prompt_variables": "promptVariables",
        "agent_alias": "agentAlias",
        "prompt_text": "promptText",
    },
)
class AgentPromptVariantProps(CommonPromptVariantProps):
    def __init__(
        self,
        *,
        model: IInvokable,
        variant_name: builtins.str,
        prompt_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
        agent_alias: IAgentAlias,
        prompt_text: builtins.str,
    ) -> None:
        '''
        :param model: (experimental) The model which is used to run the prompt. The model could be a foundation model, a custom model, or a provisioned model.
        :param variant_name: (experimental) The name of the prompt variant.
        :param prompt_variables: (experimental) The variables in the prompt template that can be filled in at runtime.
        :param agent_alias: (experimental) An alias pointing to the agent version to be used.
        :param prompt_text: (experimental) The text prompt. Variables are used by enclosing its name with double curly braces as in ``{{variable_name}}``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdd09e55bb476582351ebba4821a32d4d2805cc94cd42116b015f968efff63ee)
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
            check_type(argname="argument variant_name", value=variant_name, expected_type=type_hints["variant_name"])
            check_type(argname="argument prompt_variables", value=prompt_variables, expected_type=type_hints["prompt_variables"])
            check_type(argname="argument agent_alias", value=agent_alias, expected_type=type_hints["agent_alias"])
            check_type(argname="argument prompt_text", value=prompt_text, expected_type=type_hints["prompt_text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "model": model,
            "variant_name": variant_name,
            "agent_alias": agent_alias,
            "prompt_text": prompt_text,
        }
        if prompt_variables is not None:
            self._values["prompt_variables"] = prompt_variables

    @builtins.property
    def model(self) -> IInvokable:
        '''(experimental) The model which is used to run the prompt.

        The model could be a foundation
        model, a custom model, or a provisioned model.

        :stability: experimental
        '''
        result = self._values.get("model")
        assert result is not None, "Required property 'model' is missing"
        return typing.cast(IInvokable, result)

    @builtins.property
    def variant_name(self) -> builtins.str:
        '''(experimental) The name of the prompt variant.

        :stability: experimental
        '''
        result = self._values.get("variant_name")
        assert result is not None, "Required property 'variant_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prompt_variables(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The variables in the prompt template that can be filled in at runtime.

        :stability: experimental
        '''
        result = self._values.get("prompt_variables")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def agent_alias(self) -> IAgentAlias:
        '''(experimental) An alias pointing to the agent version to be used.

        :stability: experimental
        '''
        result = self._values.get("agent_alias")
        assert result is not None, "Required property 'agent_alias' is missing"
        return typing.cast(IAgentAlias, result)

    @builtins.property
    def prompt_text(self) -> builtins.str:
        '''(experimental) The text prompt.

        Variables are used by enclosing its name with double curly braces
        as in ``{{variable_name}}``.

        :stability: experimental
        '''
        result = self._values.get("prompt_text")
        assert result is not None, "Required property 'prompt_text' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentPromptVariantProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IInvokable)
class ApplicationInferenceProfile(
    InferenceProfileBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ApplicationInferenceProfile",
):
    '''(experimental) Class to create a ApplicationInferenceProfile with CDK.

    These are inference profiles created by users (user defined).
    This helps to track costs and model usage.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-create.html
    :stability: experimental
    :resource: AWS::Bedrock::ApplicationInferenceProfile
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        inference_profile_name: builtins.str,
        model_source: IInvokable,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param inference_profile_name: (experimental) The name of the inference profile.
        :param model_source: (experimental) To create an application inference profile for one Region, specify a foundation model. Usage and costs for requests made to that Region with that model will be tracked. To create an application inference profile for multiple Regions, specify a cross region (system-defined) inference profile. The inference profile will route requests to the Regions defined in the cross region (system-defined) inference profile that you choose. Usage and costs for requests made to the Regions in the inference profile will be tracked.
        :param description: (experimental) Description of the inference profile.
        :param tags: (experimental) A list of tags associated with the inference profile.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9295fc37ecfd5ba15c3b4b32661816cc911d30425b0457d6d9e73aab82dc7f58)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApplicationInferenceProfileProps(
            inference_profile_name=inference_profile_name,
            model_source=model_source,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromApplicationInferenceProfileAttributes")
    @builtins.classmethod
    def from_application_inference_profile_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        inference_profile_arn: builtins.str,
        inference_profile_identifier: builtins.str,
    ) -> IInferenceProfile:
        '''(experimental) Import a ApplicationInferenceProfile given its attributes.

        :param scope: -
        :param id: -
        :param inference_profile_arn: (experimental) The ARN of the application inference profile.
        :param inference_profile_identifier: (experimental) The ID or Amazon Resource Name (ARN) of the inference profile.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08499f882d34a991b6ff994ce67891aa81aad629aea208a0d363fe07aa2d8b5d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = ApplicationInferenceProfileAttributes(
            inference_profile_arn=inference_profile_arn,
            inference_profile_identifier=inference_profile_identifier,
        )

        return typing.cast(IInferenceProfile, jsii.sinvoke(cls, "fromApplicationInferenceProfileAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromCfnApplicationInferenceProfile")
    @builtins.classmethod
    def from_cfn_application_inference_profile(
        cls,
        cfn_application_inference_profile: _aws_cdk_aws_bedrock_ceddda9d.CfnApplicationInferenceProfile,
    ) -> IInferenceProfile:
        '''(experimental) Import a low-level L1 Cfn ApplicationInferenceProfile.

        :param cfn_application_inference_profile: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4756b25b5d6740797b0f293da1e552a81883343f282122c5ff5fadb11eeb76b3)
            check_type(argname="argument cfn_application_inference_profile", value=cfn_application_inference_profile, expected_type=type_hints["cfn_application_inference_profile"])
        return typing.cast(IInferenceProfile, jsii.sinvoke(cls, "fromCfnApplicationInferenceProfile", [cfn_application_inference_profile]))

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Gives the appropriate policies to invoke and use the application inference profile.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7315621579f5e4f7d30f4502f1eeff997dba6cf3f1b3fa9f44a777ac8142ef07)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantInvoke", [grantee]))

    @jsii.member(jsii_name="grantProfileUsage")
    def grant_profile_usage(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grants appropriate permissions to use the application inference profile (AIP).

        Does not grant permissions to use the model/cross-region profile in the AIP.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cee844d1aa1c3aa02aa8a059e448586063f79d5157d71fc62c9035f258d4a04)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantProfileUsage", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        '''(experimental) Time Stamp for ApplicationInferenceProfile creation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileArn")
    def inference_profile_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application application inference profile.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileArn"))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileId")
    def inference_profile_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the application inference profile.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileId"))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileModel")
    def inference_profile_model(self) -> IInvokable:
        '''(experimental) The underlying model/cross-region model used by the application inference profile.

        :stability: experimental
        '''
        return typing.cast(IInvokable, jsii.get(self, "inferenceProfileModel"))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileName")
    def inference_profile_name(self) -> builtins.str:
        '''(experimental) The name of the application inference profile.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileName"))

    @builtins.property
    @jsii.member(jsii_name="invokableArn")
    def invokable_arn(self) -> builtins.str:
        '''(experimental) This equals to the inferenceProfileArn property, useful just to implement IInvokable interface.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "invokableArn"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        '''(experimental) The status of the application inference profile.

        ACTIVE means that the inference profile is ready to be used.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> InferenceProfileType:
        '''(experimental) The type of the inference profile.

        The following types are possible:
        SYSTEM_DEFINED – The inference profile is defined by Amazon Bedrock.
        You can route inference requests across regions with these inference profiles.
        APPLICATION – The inference profile was created by a user.
        This type of inference profile can track metrics and costs when invoking the model in it.
        The inference profile may route requests to one or multiple regions.

        :stability: experimental
        '''
        return typing.cast(InferenceProfileType, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        '''(experimental) Time Stamp for ApplicationInferenceProfile update.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))


@jsii.implements(IInvokable)
class BedrockFoundationModel(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.BedrockFoundationModel",
):
    '''(experimental) Bedrock models.

    If you need to use a model name that doesn't exist as a static member, you
    can instantiate a ``BedrockFoundationModel`` object, e.g: ``new BedrockFoundationModel('my-model')``.

    :stability: experimental
    '''

    def __init__(
        self,
        value: builtins.str,
        *,
        supported_vector_type: typing.Optional[typing.Sequence[VectorType]] = None,
        supports_agents: typing.Optional[builtins.bool] = None,
        supports_cross_region: typing.Optional[builtins.bool] = None,
        supports_knowledge_base: typing.Optional[builtins.bool] = None,
        vector_dimensions: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param value: -
        :param supported_vector_type: (experimental) Embeddings models have different supported vector types.
        :param supports_agents: (experimental) Bedrock Agents can use this model. Default: - false
        :param supports_cross_region: (experimental) Can be used with a Cross-Region Inference Profile. Default: - false
        :param supports_knowledge_base: (experimental) Bedrock Knowledge Base can use this model. Default: - false
        :param vector_dimensions: (experimental) Embedding models have different vector dimensions. Only applicable for embedding models.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a81fd58f8932cf2d8dbd47ee14e3d74d82d0d0245523bd77f54c7a3ebe2a31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        props = BedrockFoundationModelProps(
            supported_vector_type=supported_vector_type,
            supports_agents=supports_agents,
            supports_cross_region=supports_cross_region,
            supports_knowledge_base=supports_knowledge_base,
            vector_dimensions=vector_dimensions,
        )

        jsii.create(self.__class__, self, [value, props])

    @jsii.member(jsii_name="fromCdkFoundationModel")
    @builtins.classmethod
    def from_cdk_foundation_model(
        cls,
        model_id: _aws_cdk_aws_bedrock_ceddda9d.FoundationModel,
        *,
        supported_vector_type: typing.Optional[typing.Sequence[VectorType]] = None,
        supports_agents: typing.Optional[builtins.bool] = None,
        supports_cross_region: typing.Optional[builtins.bool] = None,
        supports_knowledge_base: typing.Optional[builtins.bool] = None,
        vector_dimensions: typing.Optional[jsii.Number] = None,
    ) -> "BedrockFoundationModel":
        '''
        :param model_id: -
        :param supported_vector_type: (experimental) Embeddings models have different supported vector types.
        :param supports_agents: (experimental) Bedrock Agents can use this model. Default: - false
        :param supports_cross_region: (experimental) Can be used with a Cross-Region Inference Profile. Default: - false
        :param supports_knowledge_base: (experimental) Bedrock Knowledge Base can use this model. Default: - false
        :param vector_dimensions: (experimental) Embedding models have different vector dimensions. Only applicable for embedding models.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e574ebd23afcb2cd940b46095855d515345af1851202b2050e4beae0b61b0797)
            check_type(argname="argument model_id", value=model_id, expected_type=type_hints["model_id"])
        props = BedrockFoundationModelProps(
            supported_vector_type=supported_vector_type,
            supports_agents=supports_agents,
            supports_cross_region=supports_cross_region,
            supports_knowledge_base=supports_knowledge_base,
            vector_dimensions=vector_dimensions,
        )

        return typing.cast("BedrockFoundationModel", jsii.sinvoke(cls, "fromCdkFoundationModel", [model_id, props]))

    @jsii.member(jsii_name="fromCdkFoundationModelId")
    @builtins.classmethod
    def from_cdk_foundation_model_id(
        cls,
        model_id: _aws_cdk_aws_bedrock_ceddda9d.FoundationModelIdentifier,
        *,
        supported_vector_type: typing.Optional[typing.Sequence[VectorType]] = None,
        supports_agents: typing.Optional[builtins.bool] = None,
        supports_cross_region: typing.Optional[builtins.bool] = None,
        supports_knowledge_base: typing.Optional[builtins.bool] = None,
        vector_dimensions: typing.Optional[jsii.Number] = None,
    ) -> "BedrockFoundationModel":
        '''
        :param model_id: -
        :param supported_vector_type: (experimental) Embeddings models have different supported vector types.
        :param supports_agents: (experimental) Bedrock Agents can use this model. Default: - false
        :param supports_cross_region: (experimental) Can be used with a Cross-Region Inference Profile. Default: - false
        :param supports_knowledge_base: (experimental) Bedrock Knowledge Base can use this model. Default: - false
        :param vector_dimensions: (experimental) Embedding models have different vector dimensions. Only applicable for embedding models.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e6ba9edf9949ffdb893690a97303140d822c69b491d2f36a23884f599a2c01)
            check_type(argname="argument model_id", value=model_id, expected_type=type_hints["model_id"])
        props = BedrockFoundationModelProps(
            supported_vector_type=supported_vector_type,
            supports_agents=supports_agents,
            supports_cross_region=supports_cross_region,
            supports_knowledge_base=supports_knowledge_base,
            vector_dimensions=vector_dimensions,
        )

        return typing.cast("BedrockFoundationModel", jsii.sinvoke(cls, "fromCdkFoundationModelId", [model_id, props]))

    @jsii.member(jsii_name="asArn")
    def as_arn(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.str:
        '''(experimental) Returns the ARN of the foundation model in the following format: ``arn:${Partition}:bedrock:${Region}::foundation-model/${ResourceId}``.

        :param construct: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0736a1f1795a1917c49125732e66d2d15e2a25a6b98ac778b58a6ed32dc0df7b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.str, jsii.invoke(self, "asArn", [construct]))

    @jsii.member(jsii_name="asIModel")
    def as_i_model(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.IModel:
        '''
        :param construct: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da72b0f5ffa432a07504325247590f94f501d9e78a5f834d66e81cfc7e0273f1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.IModel, jsii.invoke(self, "asIModel", [construct]))

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Gives the appropriate policies to invoke and use the Foundation Model in the stack region.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f51a4f667d4d649aafa9ba1bacf7d35b00909caf39e4001910a74850fc7131df)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantInvoke", [grantee]))

    @jsii.member(jsii_name="grantInvokeAllRegions")
    def grant_invoke_all_regions(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Gives the appropriate policies to invoke and use the Foundation Model in all regions.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d3c75724e9e59d672c6ddd0ebf03051252caf48c764eeff6f38c9dbc5d4750)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantInvokeAllRegions", [grantee]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_NOVA_LITE_V1")
    def AMAZON_NOVA_LITE_V1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "AMAZON_NOVA_LITE_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_NOVA_MICRO_V1")
    def AMAZON_NOVA_MICRO_V1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "AMAZON_NOVA_MICRO_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_NOVA_PRO_V1")
    def AMAZON_NOVA_PRO_V1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "AMAZON_NOVA_PRO_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_PREMIER_V1_0")
    def AMAZON_TITAN_PREMIER_V1_0(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "AMAZON_TITAN_PREMIER_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_TEXT_EXPRESS_V1")
    def AMAZON_TITAN_TEXT_EXPRESS_V1(cls) -> "BedrockFoundationModel":
        '''(experimental) **************************************************************************                           AMAZON *************************************************************************.

        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "AMAZON_TITAN_TEXT_EXPRESS_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_3_5_HAIKU_V1_0")
    def ANTHROPIC_CLAUDE_3_5_HAIKU_V1_0(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_3_5_HAIKU_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_3_5_SONNET_V1_0")
    def ANTHROPIC_CLAUDE_3_5_SONNET_V1_0(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_3_5_SONNET_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_3_5_SONNET_V2_0")
    def ANTHROPIC_CLAUDE_3_5_SONNET_V2_0(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_3_5_SONNET_V2_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_3_7_SONNET_V1_0")
    def ANTHROPIC_CLAUDE_3_7_SONNET_V1_0(cls) -> "BedrockFoundationModel":
        '''(experimental) **************************************************************************                           ANTHROPIC *************************************************************************.

        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_3_7_SONNET_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_HAIKU_V1_0")
    def ANTHROPIC_CLAUDE_HAIKU_V1_0(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_HAIKU_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_INSTANT_V1_2")
    def ANTHROPIC_CLAUDE_INSTANT_V1_2(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_INSTANT_V1_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_OPUS_V1_0")
    def ANTHROPIC_CLAUDE_OPUS_V1_0(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_OPUS_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_SONNET_V1_0")
    def ANTHROPIC_CLAUDE_SONNET_V1_0(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_SONNET_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_V2")
    def ANTHROPIC_CLAUDE_V2(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_V2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_V2_1")
    def ANTHROPIC_CLAUDE_V2_1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_V2_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="COHERE_EMBED_ENGLISH_V3")
    def COHERE_EMBED_ENGLISH_V3(cls) -> "BedrockFoundationModel":
        '''(experimental) **************************************************************************                           COHERE *************************************************************************.

        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "COHERE_EMBED_ENGLISH_V3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="COHERE_EMBED_MULTILINGUAL_V3")
    def COHERE_EMBED_MULTILINGUAL_V3(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "COHERE_EMBED_MULTILINGUAL_V3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_3_1_70B_INSTRUCT_V1")
    def META_LLAMA_3_1_70_B_INSTRUCT_V1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "META_LLAMA_3_1_70B_INSTRUCT_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_3_1_8B_INSTRUCT_V1")
    def META_LLAMA_3_1_8_B_INSTRUCT_V1(cls) -> "BedrockFoundationModel":
        '''(experimental) **************************************************************************                           META *************************************************************************.

        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "META_LLAMA_3_1_8B_INSTRUCT_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_3_2_11B_INSTRUCT_V1")
    def META_LLAMA_3_2_11_B_INSTRUCT_V1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "META_LLAMA_3_2_11B_INSTRUCT_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_3_2_1B_INSTRUCT_V1")
    def META_LLAMA_3_2_1_B_INSTRUCT_V1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "META_LLAMA_3_2_1B_INSTRUCT_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_3_2_3B_INSTRUCT_V1")
    def META_LLAMA_3_2_3_B_INSTRUCT_V1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "META_LLAMA_3_2_3B_INSTRUCT_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TITAN_EMBED_TEXT_V1")
    def TITAN_EMBED_TEXT_V1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "TITAN_EMBED_TEXT_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TITAN_EMBED_TEXT_V2_1024")
    def TITAN_EMBED_TEXT_V2_1024(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "TITAN_EMBED_TEXT_V2_1024"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TITAN_EMBED_TEXT_V2_256")
    def TITAN_EMBED_TEXT_V2_256(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "TITAN_EMBED_TEXT_V2_256"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TITAN_EMBED_TEXT_V2_512")
    def TITAN_EMBED_TEXT_V2_512(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "TITAN_EMBED_TEXT_V2_512"))

    @builtins.property
    @jsii.member(jsii_name="invokableArn")
    def invokable_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Bedrock invokable abstraction.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "invokableArn"))

    @builtins.property
    @jsii.member(jsii_name="modelArn")
    def model_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "modelArn"))

    @builtins.property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> builtins.str:
        '''(experimental) **************************************************************************                           Constructor *************************************************************************.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "modelId"))

    @builtins.property
    @jsii.member(jsii_name="supportsAgents")
    def supports_agents(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "supportsAgents"))

    @builtins.property
    @jsii.member(jsii_name="supportsCrossRegion")
    def supports_cross_region(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "supportsCrossRegion"))

    @builtins.property
    @jsii.member(jsii_name="supportsKnowledgeBase")
    def supports_knowledge_base(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "supportsKnowledgeBase"))

    @builtins.property
    @jsii.member(jsii_name="supportedVectorType")
    def supported_vector_type(self) -> typing.Optional[typing.List[VectorType]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[VectorType]], jsii.get(self, "supportedVectorType"))

    @builtins.property
    @jsii.member(jsii_name="vectorDimensions")
    def vector_dimensions(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vectorDimensions"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ChatPromptVariantProps",
    jsii_struct_bases=[CommonPromptVariantProps],
    name_mapping={
        "model": "model",
        "variant_name": "variantName",
        "prompt_variables": "promptVariables",
        "messages": "messages",
        "inference_configuration": "inferenceConfiguration",
        "system": "system",
        "tool_configuration": "toolConfiguration",
    },
)
class ChatPromptVariantProps(CommonPromptVariantProps):
    def __init__(
        self,
        *,
        model: IInvokable,
        variant_name: builtins.str,
        prompt_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
        messages: typing.Sequence[ChatMessage],
        inference_configuration: typing.Optional[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        system: typing.Optional[builtins.str] = None,
        tool_configuration: typing.Optional[typing.Union[ToolConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param model: (experimental) The model which is used to run the prompt. The model could be a foundation model, a custom model, or a provisioned model.
        :param variant_name: (experimental) The name of the prompt variant.
        :param prompt_variables: (experimental) The variables in the prompt template that can be filled in at runtime.
        :param messages: (experimental) Inference configuration for the Chat Prompt. Must include at least one User Message. The messages should alternate between User and Assistant.
        :param inference_configuration: (experimental) Inference configuration for the Text Prompt.
        :param system: (experimental) Context or instructions for the model to consider before generating a response.
        :param tool_configuration: (experimental) The configuration with available tools to the model and how it must use them.

        :stability: experimental
        '''
        if isinstance(inference_configuration, dict):
            inference_configuration = _aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty(**inference_configuration)
        if isinstance(tool_configuration, dict):
            tool_configuration = ToolConfiguration(**tool_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15c2d071889b362ccec61b0fabb43bd263896b68f536a4efb599bdbee9c6282d)
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
            check_type(argname="argument variant_name", value=variant_name, expected_type=type_hints["variant_name"])
            check_type(argname="argument prompt_variables", value=prompt_variables, expected_type=type_hints["prompt_variables"])
            check_type(argname="argument messages", value=messages, expected_type=type_hints["messages"])
            check_type(argname="argument inference_configuration", value=inference_configuration, expected_type=type_hints["inference_configuration"])
            check_type(argname="argument system", value=system, expected_type=type_hints["system"])
            check_type(argname="argument tool_configuration", value=tool_configuration, expected_type=type_hints["tool_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "model": model,
            "variant_name": variant_name,
            "messages": messages,
        }
        if prompt_variables is not None:
            self._values["prompt_variables"] = prompt_variables
        if inference_configuration is not None:
            self._values["inference_configuration"] = inference_configuration
        if system is not None:
            self._values["system"] = system
        if tool_configuration is not None:
            self._values["tool_configuration"] = tool_configuration

    @builtins.property
    def model(self) -> IInvokable:
        '''(experimental) The model which is used to run the prompt.

        The model could be a foundation
        model, a custom model, or a provisioned model.

        :stability: experimental
        '''
        result = self._values.get("model")
        assert result is not None, "Required property 'model' is missing"
        return typing.cast(IInvokable, result)

    @builtins.property
    def variant_name(self) -> builtins.str:
        '''(experimental) The name of the prompt variant.

        :stability: experimental
        '''
        result = self._values.get("variant_name")
        assert result is not None, "Required property 'variant_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prompt_variables(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The variables in the prompt template that can be filled in at runtime.

        :stability: experimental
        '''
        result = self._values.get("prompt_variables")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def messages(self) -> typing.List[ChatMessage]:
        '''(experimental) Inference configuration for the Chat Prompt.

        Must include at least one User Message.
        The messages should alternate between User and Assistant.

        :stability: experimental
        '''
        result = self._values.get("messages")
        assert result is not None, "Required property 'messages' is missing"
        return typing.cast(typing.List[ChatMessage], result)

    @builtins.property
    def inference_configuration(
        self,
    ) -> typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty]:
        '''(experimental) Inference configuration for the Text Prompt.

        :stability: experimental
        '''
        result = self._values.get("inference_configuration")
        return typing.cast(typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty], result)

    @builtins.property
    def system(self) -> typing.Optional[builtins.str]:
        '''(experimental) Context or instructions for the model to consider before generating a response.

        :stability: experimental
        '''
        result = self._values.get("system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tool_configuration(self) -> typing.Optional[ToolConfiguration]:
        '''(experimental) The configuration with available tools to the model and how it must use them.

        :stability: experimental
        '''
        result = self._values.get("tool_configuration")
        return typing.cast(typing.Optional[ToolConfiguration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChatPromptVariantProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ConfluenceDataSourceAssociationProps",
    jsii_struct_bases=[DataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "auth_secret": "authSecret",
        "confluence_url": "confluenceUrl",
        "auth_type": "authType",
        "filters": "filters",
    },
)
class ConfluenceDataSourceAssociationProps(DataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        confluence_url: builtins.str,
        auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
        filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Interface to add a new data source to an existing KB.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Confluence instance URL. Secret must start with "AmazonBedrock-".
        :param confluence_url: (experimental) The Confluence host URL or instance URL.
        :param auth_type: (experimental) The supported authentication method to connect to the data source. Default: ConfluenceDataSourceAuthType.OAUTH2_CLIENT_CREDENTIALS
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825542cfcf1e14b8a9bbb49badd630cea24320a1c93de247ce04dade6510a396)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument auth_secret", value=auth_secret, expected_type=type_hints["auth_secret"])
            check_type(argname="argument confluence_url", value=confluence_url, expected_type=type_hints["confluence_url"])
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_secret": auth_secret,
            "confluence_url": confluence_url,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Confluence instance URL.

        Secret must start with "AmazonBedrock-".

        :stability: experimental
        '''
        result = self._values.get("auth_secret")
        assert result is not None, "Required property 'auth_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def confluence_url(self) -> builtins.str:
        '''(experimental) The Confluence host URL or instance URL.

        :stability: experimental

        Example::

            https://example.atlassian.net
        '''
        result = self._values.get("confluence_url")
        assert result is not None, "Required property 'confluence_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_type(self) -> typing.Optional[ConfluenceDataSourceAuthType]:
        '''(experimental) The supported authentication method to connect to the data source.

        :default: ConfluenceDataSourceAuthType.OAUTH2_CLIENT_CREDENTIALS

        :stability: experimental
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[ConfluenceDataSourceAuthType], result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[ConfluenceCrawlingFilters]]:
        '''(experimental) The filters (regular expression patterns) for the crawling.

        If there's a conflict, the exclude pattern takes precedence.

        :default: None - all your content is crawled.

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[ConfluenceCrawlingFilters]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfluenceDataSourceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ConfluenceDataSourceProps",
    jsii_struct_bases=[ConfluenceDataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "auth_secret": "authSecret",
        "confluence_url": "confluenceUrl",
        "auth_type": "authType",
        "filters": "filters",
        "knowledge_base": "knowledgeBase",
    },
)
class ConfluenceDataSourceProps(ConfluenceDataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        confluence_url: builtins.str,
        auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
        filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        knowledge_base: IKnowledgeBase,
    ) -> None:
        '''(experimental) Interface to create a new standalone data source object.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Confluence instance URL. Secret must start with "AmazonBedrock-".
        :param confluence_url: (experimental) The Confluence host URL or instance URL.
        :param auth_type: (experimental) The supported authentication method to connect to the data source. Default: ConfluenceDataSourceAuthType.OAUTH2_CLIENT_CREDENTIALS
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b14df6d19dffd71a4d3ac18b026e201bc33f4eabb05690ed07f68835b4c37b32)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument auth_secret", value=auth_secret, expected_type=type_hints["auth_secret"])
            check_type(argname="argument confluence_url", value=confluence_url, expected_type=type_hints["confluence_url"])
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument knowledge_base", value=knowledge_base, expected_type=type_hints["knowledge_base"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_secret": auth_secret,
            "confluence_url": confluence_url,
            "knowledge_base": knowledge_base,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Confluence instance URL.

        Secret must start with "AmazonBedrock-".

        :stability: experimental
        '''
        result = self._values.get("auth_secret")
        assert result is not None, "Required property 'auth_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def confluence_url(self) -> builtins.str:
        '''(experimental) The Confluence host URL or instance URL.

        :stability: experimental

        Example::

            https://example.atlassian.net
        '''
        result = self._values.get("confluence_url")
        assert result is not None, "Required property 'confluence_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_type(self) -> typing.Optional[ConfluenceDataSourceAuthType]:
        '''(experimental) The supported authentication method to connect to the data source.

        :default: ConfluenceDataSourceAuthType.OAUTH2_CLIENT_CREDENTIALS

        :stability: experimental
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[ConfluenceDataSourceAuthType], result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[ConfluenceCrawlingFilters]]:
        '''(experimental) The filters (regular expression patterns) for the crawling.

        If there's a conflict, the exclude pattern takes precedence.

        :default: None - all your content is crawled.

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[ConfluenceCrawlingFilters]], result)

    @builtins.property
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        result = self._values.get("knowledge_base")
        assert result is not None, "Required property 'knowledge_base' is missing"
        return typing.cast(IKnowledgeBase, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfluenceDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IInvokable, IInferenceProfile)
class CrossRegionInferenceProfile(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CrossRegionInferenceProfile",
):
    '''(experimental) Cross-region inference enables you to seamlessly manage unplanned traffic bursts by utilizing compute across different AWS Regions.

    With cross-region
    inference, you can distribute traffic across multiple AWS Regions, enabling
    higher throughput and enhanced resilience during periods of peak demands.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html
    :stability: experimental
    '''

    @jsii.member(jsii_name="fromConfig")
    @builtins.classmethod
    def from_config(
        cls,
        *,
        geo_region: CrossRegionInferenceProfileRegion,
        model: BedrockFoundationModel,
    ) -> "CrossRegionInferenceProfile":
        '''
        :param geo_region: (experimental) The geographic region where the traffic is going to be distributed. Routing factors in user traffic, demand and utilization of resources.
        :param model: (experimental) A model supporting cross-region inference.

        :stability: experimental
        '''
        config = CrossRegionInferenceProfileProps(geo_region=geo_region, model=model)

        return typing.cast("CrossRegionInferenceProfile", jsii.sinvoke(cls, "fromConfig", [config]))

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Gives the appropriate policies to invoke and use the Foundation Model.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f472f27b5fa3d24da2ba8a7f195c5e15bd841db7f86b5c297fc541b722f61ac6)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantInvoke", [grantee]))

    @jsii.member(jsii_name="grantProfileUsage")
    def grant_profile_usage(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grants appropriate permissions to use the cross-region inference profile.

        Does not grant permissions to use the model in the profile.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93fff43e7d1f97fa19dd910168fe2f7ff3f51b42c62d60e9b28f154c02abdf57)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantProfileUsage", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileArn")
    def inference_profile_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application inference profile.

        :stability: experimental

        Example::

            'arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-3-5-sonnet-20240620-v1:0'
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileArn"))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileId")
    def inference_profile_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the inference profile.

        :stability: experimental

        Example::

            'us.anthropic.claude-3-5-sonnet-20240620-v1:0'
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileId"))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileModel")
    def inference_profile_model(self) -> BedrockFoundationModel:
        '''(experimental) The underlying model supporting cross-region inference.

        :stability: experimental
        '''
        return typing.cast(BedrockFoundationModel, jsii.get(self, "inferenceProfileModel"))

    @builtins.property
    @jsii.member(jsii_name="invokableArn")
    def invokable_arn(self) -> builtins.str:
        '''(experimental) This equals to the inferenceProfileArn property, useful just to implement IInvokable interface.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "invokableArn"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> InferenceProfileType:
        '''(experimental) The type of inference profile.

        :stability: experimental

        Example::

            InferenceProfileType.SYSTEM_DEFINED
        '''
        return typing.cast(InferenceProfileType, jsii.get(self, "type"))


@jsii.implements(IDataSource)
class DataSourceBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.DataSourceBase",
):
    '''(experimental) Specifies the base class for all data source resources (imported and new).

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd33be0b5b715618515a9e14205bd91556c356258bedc630996b5ce10baf76f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    @abc.abstractmethod
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        ...


class _DataSourceBaseProxy(
    DataSourceBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, DataSourceBase).__jsii_proxy_class__ = lambda : _DataSourceBaseProxy


class DataSourceNew(
    DataSourceBase,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.DataSourceNew",
):
    '''(experimental) Specifies the base class for all NEW data source resources of ANY type.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fd726166f60d1f4704e8a674b6b10ffb8ada8138d51b0fb6cd7ff76f8b98644)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="formatAsCfnProps")
    def format_as_cfn_props(
        self,
        props: typing.Union[DataSourceAssociationProps, typing.Dict[builtins.str, typing.Any]],
        *,
        type: builtins.str,
        confluence_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ConfluenceDataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.S3DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        salesforce_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.SalesforceDataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        share_point_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.SharePointDataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        web_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.WebDataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnDataSourceProps:
        '''(experimental) Formats the data source configuration properties for CloudFormation.

        :param props: -
        :param type: The type of data source.
        :param confluence_configuration: The configuration information to connect to Confluence as your data source. .. epigraph:: Confluence data source connector is in preview release and is subject to change.
        :param s3_configuration: The configuration information to connect to Amazon S3 as your data source.
        :param salesforce_configuration: The configuration information to connect to Salesforce as your data source. .. epigraph:: Salesforce data source connector is in preview release and is subject to change.
        :param share_point_configuration: The configuration information to connect to SharePoint as your data source. .. epigraph:: SharePoint data source connector is in preview release and is subject to change.
        :param web_configuration: The configuration of web URLs to crawl for your data source. You should be authorized to crawl the URLs. .. epigraph:: Crawling web URLs as your data source is in preview release and is subject to change.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff20dd4f9a8695235fc5ad3f8044d1b2ab4c308a247f269a7667225817ffa47f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        data_source_configuration = _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.DataSourceConfigurationProperty(
            type=type,
            confluence_configuration=confluence_configuration,
            s3_configuration=s3_configuration,
            salesforce_configuration=salesforce_configuration,
            share_point_configuration=share_point_configuration,
            web_configuration=web_configuration,
        )

        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnDataSourceProps, jsii.invoke(self, "formatAsCfnProps", [props, data_source_configuration]))

    @jsii.member(jsii_name="handleCommonPermissions")
    def handle_common_permissions(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
    ) -> None:
        '''(experimental) Adds appropriate permissions to the KB execution role needed by the data source.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = DataSourceAssociationProps(
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast(None, jsii.invoke(self, "handleCommonPermissions", [props]))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    @abc.abstractmethod
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    @abc.abstractmethod
    def data_source_name(self) -> builtins.str:
        '''(experimental) The name of the data source.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="dataSourceType")
    @abc.abstractmethod
    def data_source_type(self) -> DataSourceType:
        '''(experimental) The type of data source.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="knowledgeBase")
    @abc.abstractmethod
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base associated with the data source.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    @abc.abstractmethod
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :stability: experimental
        '''
        ...


class _DataSourceNewProxy(
    DataSourceNew,
    jsii.proxy_for(DataSourceBase), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> builtins.str:
        '''(experimental) The name of the data source.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceName"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceType")
    def data_source_type(self) -> DataSourceType:
        '''(experimental) The type of data source.

        :stability: experimental
        '''
        return typing.cast(DataSourceType, jsii.get(self, "dataSourceType"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBase")
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base associated with the data source.

        :stability: experimental
        '''
        return typing.cast(IKnowledgeBase, jsii.get(self, "knowledgeBase"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, DataSourceNew).__jsii_proxy_class__ = lambda : _DataSourceNewProxy


@jsii.implements(IGuardrail)
class GuardrailBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.GuardrailBase",
):
    '''(experimental) Abstract base class for a Guardrail.

    Contains methods and attributes valid for Guardrails either created with CDK or imported.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd3735db5e3fe2e0ab1bdcc83a66314e304f7420d3c02093aaa2f59d0c028ef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="metricAll")
    @builtins.classmethod
    def metric_all(
        cls,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the given named metric for all guardrails.

        By default, the metric will be calculated as a sum over a period of 5 minutes.
        You can customize this by using the ``statistic`` and ``period`` properties.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ffd62f94a075285352644796900ec1cbbc174ef702181d1d0731d60a2b44690)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.sinvoke(cls, "metricAll", [metric_name, props]))

    @jsii.member(jsii_name="metricAllInvocationLatency")
    @builtins.classmethod
    def metric_all_invocation_latency(
        cls,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocation latency metric for all guardrails.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.sinvoke(cls, "metricAllInvocationLatency", [props]))

    @jsii.member(jsii_name="metricAllInvocations")
    @builtins.classmethod
    def metric_all_invocations(
        cls,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocations metric for all guardrails.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.sinvoke(cls, "metricAllInvocations", [props]))

    @jsii.member(jsii_name="metricAllInvocationsIntervened")
    @builtins.classmethod
    def metric_all_invocations_intervened(
        cls,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocations intervened metric for all guardrails.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.sinvoke(cls, "metricAllInvocationsIntervened", [props]))

    @jsii.member(jsii_name="metricAllTextUnitCount")
    @builtins.classmethod
    def metric_all_text_unit_count(
        cls,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the text unit count metric for all guardrails.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.sinvoke(cls, "metricAllTextUnitCount", [props]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given principal identity permissions to perform actions on this agent alias.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df7159e78ce120fa250f1ffec06780e7e9794db74027afd73494579443efb1b0)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantApply")
    def grant_apply(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to apply the guardrail.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96bf842a81e21fd1954424599cbfcd6aa0d8d29978b87d0221427d57ac30a99a)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantApply", [grantee]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the given named metric for this guardrail.

        By default, the metric will be calculated as a sum over a period of 5 minutes.
        You can customize this by using the ``statistic`` and ``period`` properties.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29a8aa8ec53e9d8a3927f7d99acea5795fe62a6615a19aba1057ba5b5e2bb02)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricInvocationClientErrors")
    def metric_invocation_client_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocation client errors metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricInvocationClientErrors", [props]))

    @jsii.member(jsii_name="metricInvocationLatency")
    def metric_invocation_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocation latency metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricInvocationLatency", [props]))

    @jsii.member(jsii_name="metricInvocations")
    def metric_invocations(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocations metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricInvocations", [props]))

    @jsii.member(jsii_name="metricInvocationServerErrors")
    def metric_invocation_server_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocation server errors metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricInvocationServerErrors", [props]))

    @jsii.member(jsii_name="metricInvocationsIntervened")
    def metric_invocations_intervened(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocations intervened metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricInvocationsIntervened", [props]))

    @jsii.member(jsii_name="metricInvocationThrottles")
    def metric_invocation_throttles(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the invocation throttles metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricInvocationThrottles", [props]))

    @jsii.member(jsii_name="metricTextUnitCount")
    def metric_text_unit_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the text unit count metric for this guardrail.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTextUnitCount", [props]))

    @builtins.property
    @jsii.member(jsii_name="guardrailArn")
    @abc.abstractmethod
    def guardrail_arn(self) -> builtins.str:
        '''(experimental) The ARN of the guardrail.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="guardrailId")
    @abc.abstractmethod
    def guardrail_id(self) -> builtins.str:
        '''(experimental) The ID of the guardrail.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    @abc.abstractmethod
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key of the guardrail if custom encryption is configured.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="lastUpdated")
    @abc.abstractmethod
    def last_updated(self) -> typing.Optional[builtins.str]:
        '''(experimental) When this guardrail was last updated.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="guardrailVersion")
    @abc.abstractmethod
    def guardrail_version(self) -> builtins.str:
        '''(experimental) The ID of the guardrail.

        :stability: experimental
        '''
        ...

    @guardrail_version.setter
    @abc.abstractmethod
    def guardrail_version(self, value: builtins.str) -> None:
        ...


class _GuardrailBaseProxy(
    GuardrailBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="guardrailArn")
    def guardrail_arn(self) -> builtins.str:
        '''(experimental) The ARN of the guardrail.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailArn"))

    @builtins.property
    @jsii.member(jsii_name="guardrailId")
    def guardrail_id(self) -> builtins.str:
        '''(experimental) The ID of the guardrail.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailId"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key of the guardrail if custom encryption is configured.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdated")
    def last_updated(self) -> typing.Optional[builtins.str]:
        '''(experimental) When this guardrail was last updated.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastUpdated"))

    @builtins.property
    @jsii.member(jsii_name="guardrailVersion")
    def guardrail_version(self) -> builtins.str:
        '''(experimental) The ID of the guardrail.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailVersion"))

    @guardrail_version.setter
    def guardrail_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3213cd2c4a16450e0a0e2f790d34031e9f57737b870372668dd1026cdbc75470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guardrailVersion", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, GuardrailBase).__jsii_proxy_class__ = lambda : _GuardrailBaseProxy


@jsii.interface(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IKendraKnowledgeBase"
)
class IKendraKnowledgeBase(IKnowledgeBase, typing_extensions.Protocol):
    '''(experimental) ****************************************************************************                            COMMON INTERFACES ***************************************************************************.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="kendraIndex")
    def kendra_index(self) -> _IKendraGenAiIndex_da04f105:
        '''(experimental) The GenAI Kendra Index.

        :stability: experimental
        '''
        ...


class _IKendraKnowledgeBaseProxy(
    jsii.proxy_for(IKnowledgeBase), # type: ignore[misc]
):
    '''(experimental) ****************************************************************************                            COMMON INTERFACES ***************************************************************************.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IKendraKnowledgeBase"

    @builtins.property
    @jsii.member(jsii_name="kendraIndex")
    def kendra_index(self) -> _IKendraGenAiIndex_da04f105:
        '''(experimental) The GenAI Kendra Index.

        :stability: experimental
        '''
        return typing.cast(_IKendraGenAiIndex_da04f105, jsii.get(self, "kendraIndex"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IKendraKnowledgeBase).__jsii_proxy_class__ = lambda : _IKendraKnowledgeBaseProxy


class KendraKnowledgeBaseBase(
    KnowledgeBaseBase,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.KendraKnowledgeBaseBase",
):
    '''(experimental) ****************************************************************************                             ABSTRACT CLASS ***************************************************************************.

    :stability: experimental
    '''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b02cf0eea625902c4343704976c208b4fd02d51cbe3f630137ba3ccecb55886)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @builtins.property
    @jsii.member(jsii_name="kendraIndex")
    @abc.abstractmethod
    def kendra_index(self) -> _IKendraGenAiIndex_da04f105:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseArn")
    @abc.abstractmethod
    def knowledge_base_arn(self) -> builtins.str:
        '''(experimental) The ARN of the knowledge base.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseId")
    @abc.abstractmethod
    def knowledge_base_id(self) -> builtins.str:
        '''(experimental) The ID of the knowledge base.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="role")
    @abc.abstractmethod
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role associated with the knowledge base.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> KnowledgeBaseType:
        '''(experimental) The type of knowledge base.

        :stability: experimental
        '''
        return typing.cast(KnowledgeBaseType, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="description")
    @abc.abstractmethod
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the knowledge base.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="instruction")
    @abc.abstractmethod
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) A narrative instruction of the knowledge base.

        A Bedrock Agent can use this instruction to determine if it should
        query this Knowledge Base.

        :stability: experimental
        '''
        ...


class _KendraKnowledgeBaseBaseProxy(
    KendraKnowledgeBaseBase,
    jsii.proxy_for(KnowledgeBaseBase), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="kendraIndex")
    def kendra_index(self) -> _IKendraGenAiIndex_da04f105:
        '''
        :stability: experimental
        '''
        return typing.cast(_IKendraGenAiIndex_da04f105, jsii.get(self, "kendraIndex"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseArn")
    def knowledge_base_arn(self) -> builtins.str:
        '''(experimental) The ARN of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseArn"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseId")
    def knowledge_base_id(self) -> builtins.str:
        '''(experimental) The ID of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseId"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role associated with the knowledge base.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="instruction")
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) A narrative instruction of the knowledge base.

        A Bedrock Agent can use this instruction to determine if it should
        query this Knowledge Base.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instruction"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, KendraKnowledgeBaseBase).__jsii_proxy_class__ = lambda : _KendraKnowledgeBaseBaseProxy


class S3DataSource(
    DataSourceNew,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.S3DataSource",
):
    '''(experimental) Sets up an S3 Data Source to be added to a knowledge base.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        knowledge_base: IKnowledgeBase,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.
        :param bucket: (experimental) The bucket that contains the data source.
        :param inclusion_prefixes: (experimental) The prefixes of the objects in the bucket that should be included in the data source. Default: - All objects in the bucket.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48fbbb836e75c99d63b1aecb8d429a451f727eaf6d350fa9c8a3e73f4932c719)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S3DataSourceProps(
            knowledge_base=knowledge_base,
            bucket=bucket,
            inclusion_prefixes=inclusion_prefixes,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''(experimental) The bucket associated with the data source.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> builtins.str:
        '''(experimental) The name of the data source.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceName"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceType")
    def data_source_type(self) -> DataSourceType:
        '''(experimental) The type of data source.

        :stability: experimental
        '''
        return typing.cast(DataSourceType, jsii.get(self, "dataSourceType"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBase")
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base associated with the data source.

        :stability: experimental
        '''
        return typing.cast(IKnowledgeBase, jsii.get(self, "knowledgeBase"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))


class SalesforceDataSource(
    DataSourceNew,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SalesforceDataSource",
):
    '''(experimental) Sets up an data source to be added to a knowledge base.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        knowledge_base: IKnowledgeBase,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        endpoint: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union[SalesforceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Salesforce instance URL. Secret must start with "AmazonBedrock-".
        :param endpoint: (experimental) The Salesforce host URL or instance URL.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b24d143c738c77349d9a94ed93b630e764b1d3c773aec262ad85df95b6be2129)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SalesforceDataSourceProps(
            knowledge_base=knowledge_base,
            auth_secret=auth_secret,
            endpoint=endpoint,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="authSecret")
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "authSecret"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> builtins.str:
        '''(experimental) The name of the data source.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceName"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceType")
    def data_source_type(self) -> DataSourceType:
        '''(experimental) The type of data source.

        :stability: experimental
        '''
        return typing.cast(DataSourceType, jsii.get(self, "dataSourceType"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        '''(experimental) The Salesforce host URL or instance URL.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBase")
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base associated with the data source.

        :stability: experimental
        '''
        return typing.cast(IKnowledgeBase, jsii.get(self, "knowledgeBase"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))


class SharePointDataSource(
    DataSourceNew,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SharePointDataSource",
):
    '''(experimental) Sets up an data source to be added to a knowledge base.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        knowledge_base: IKnowledgeBase,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        domain: builtins.str,
        site_urls: typing.Sequence[builtins.str],
        tenant_id: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union[SharePointCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Sharepoint instance URL. Secret must start with "AmazonBedrock-".
        :param domain: (experimental) The domain of your SharePoint instance or site URL/URLs.
        :param site_urls: (experimental) The SharePoint site URL/URLs. Must start with “https”. All URLs must start with same protocol.
        :param tenant_id: (experimental) The identifier of your Microsoft 365 tenant.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a767e627d5bb3db391024a83258857573d524cc605c090521fdd3266c3253351)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SharePointDataSourceProps(
            knowledge_base=knowledge_base,
            auth_secret=auth_secret,
            domain=domain,
            site_urls=site_urls,
            tenant_id=tenant_id,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="authSecret")
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "authSecret"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> builtins.str:
        '''(experimental) The name of the data source.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceName"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceType")
    def data_source_type(self) -> DataSourceType:
        '''(experimental) The type of data source.

        :stability: experimental
        '''
        return typing.cast(DataSourceType, jsii.get(self, "dataSourceType"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        '''(experimental) The domain name of your SharePoint instance.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBase")
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base associated with the data source.

        :stability: experimental
        '''
        return typing.cast(IKnowledgeBase, jsii.get(self, "knowledgeBase"))

    @builtins.property
    @jsii.member(jsii_name="siteUrls")
    def site_urls(self) -> typing.List[builtins.str]:
        '''(experimental) The SharePoint site URL/URLs.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "siteUrls"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))


class WebCrawlerDataSource(
    DataSourceNew,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.WebCrawlerDataSource",
):
    '''(experimental) Sets up a web crawler data source to be added to a knowledge base.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        knowledge_base: IKnowledgeBase,
        source_urls: typing.Sequence[builtins.str],
        crawling_rate: typing.Optional[jsii.Number] = None,
        crawling_scope: typing.Optional[CrawlingScope] = None,
        filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.
        :param source_urls: (experimental) The source urls in the format ``https://www.sitename.com``. Maximum of 100 URLs.
        :param crawling_rate: (experimental) The max rate at which pages are crawled, up to 300 per minute per host. Higher values will decrease sync time but increase the load on the host. Default: 300
        :param crawling_scope: (experimental) The scope of the crawling. Default: - CrawlingScope.DEFAULT
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e8107d76623400258117634288819beb4c9790e20e7ae484c9025d9dded738)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WebCrawlerDataSourceProps(
            knowledge_base=knowledge_base,
            source_urls=source_urls,
            crawling_rate=crawling_rate,
            crawling_scope=crawling_scope,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="crawlingRate")
    def crawling_rate(self) -> jsii.Number:
        '''(experimental) The max rate at which pages are crawled.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "crawlingRate"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> builtins.str:
        '''(experimental) The name of the data source.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceName"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceType")
    def data_source_type(self) -> DataSourceType:
        '''(experimental) The type of data source.

        :stability: experimental
        '''
        return typing.cast(DataSourceType, jsii.get(self, "dataSourceType"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBase")
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base associated with the data source.

        :stability: experimental
        '''
        return typing.cast(IKnowledgeBase, jsii.get(self, "knowledgeBase"))

    @builtins.property
    @jsii.member(jsii_name="siteUrls")
    def site_urls(self) -> typing.List[builtins.str]:
        '''(experimental) The max rate at which pages are crawled.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "siteUrls"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))


class Agent(
    AgentBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.Agent",
):
    '''(experimental) Class to create (or import) an Agent with CDK.

    :stability: experimental
    :cloudformationResource: AWS::Bedrock::Agent
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        foundation_model: IInvokable,
        instruction: builtins.str,
        action_groups: typing.Optional[typing.Sequence[AgentActionGroup]] = None,
        code_interpreter_enabled: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        force_delete: typing.Optional[builtins.bool] = None,
        guardrail: typing.Optional[IGuardrail] = None,
        idle_session_ttl: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        knowledge_bases: typing.Optional[typing.Sequence[IKnowledgeBase]] = None,
        name: typing.Optional[builtins.str] = None,
        prompt_override_configuration: typing.Optional[PromptOverrideConfiguration] = None,
        should_prepare_agent: typing.Optional[builtins.bool] = None,
        user_input_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param foundation_model: (experimental) The foundation model used for orchestration by the agent.
        :param instruction: (experimental) The instruction used by the agent. This determines how the agent will perform his task. This instruction must have a minimum of 40 characters.
        :param action_groups: (experimental) The Action Groups associated with the agent.
        :param code_interpreter_enabled: (experimental) Select whether the agent can generate, run, and troubleshoot code when trying to complete a task. Default: - false
        :param description: (experimental) A description of the agent. Default: - No description is provided.
        :param existing_role: (experimental) The existing IAM Role for the agent to use. Ensure the role has a trust policy that allows the Bedrock service to assume the role. Default: - A new role is created for you.
        :param force_delete: (experimental) Whether to delete the resource even if it's in use. Default: - true
        :param guardrail: (experimental) The guardrail that will be associated with the agent.
        :param idle_session_ttl: (experimental) How long sessions should be kept open for the agent. If no conversation occurs during this time, the session expires and Amazon Bedrock deletes any data provided before the timeout. Default: - 1 hour
        :param kms_key: (experimental) The KMS key of the agent if custom encryption is configured. Default: - An AWS managed key is used.
        :param knowledge_bases: (experimental) The KnowledgeBases associated with the agent.
        :param name: (experimental) The name of the agent. Default: - A name is generated by CDK.
        :param prompt_override_configuration: (experimental) Overrides some prompt templates in different parts of an agent sequence configuration. Default: - No overrides are provided.
        :param should_prepare_agent: (experimental) Specifies whether to automatically update the ``DRAFT`` version of the agent after making changes to the agent. The ``DRAFT`` version can be continually iterated upon during internal development. Default: - false
        :param user_input_enabled: (experimental) Select whether the agent can prompt additional information from the user when it does not have enough information to respond to an utterance. Default: - false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__627af24bb5e1ca4b3ebb82ecbd7a3f01cb1f5177248afdccbc1d0ffab70726de)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AgentProps(
            foundation_model=foundation_model,
            instruction=instruction,
            action_groups=action_groups,
            code_interpreter_enabled=code_interpreter_enabled,
            description=description,
            existing_role=existing_role,
            force_delete=force_delete,
            guardrail=guardrail,
            idle_session_ttl=idle_session_ttl,
            kms_key=kms_key,
            knowledge_bases=knowledge_bases,
            name=name,
            prompt_override_configuration=prompt_override_configuration,
            should_prepare_agent=should_prepare_agent,
            user_input_enabled=user_input_enabled,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAgentAttrs")
    @builtins.classmethod
    def from_agent_attrs(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        agent_arn: builtins.str,
        role_arn: builtins.str,
        agent_version: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        last_updated: typing.Optional[builtins.str] = None,
    ) -> IAgent:
        '''(experimental) Static Method for importing an existing Bedrock Agent.

        :param scope: -
        :param id: -
        :param agent_arn: (experimental) The ARN of the agent.
        :param role_arn: (experimental) The ARN of the IAM role associated to the agent.
        :param agent_version: (experimental) The agent version. If no explicit versions have been created, leave this empty to use the DRAFT version. Otherwise, use the version number (e.g. 1).
        :param kms_key_arn: (experimental) Optional KMS encryption key associated with this agent.
        :param last_updated: (experimental) When this agent was last updated.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ddfd67114f779bb1081ff73c6fe6d8d34c791f11bde1dea5b4e7f8983c46c0a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = AgentAttributes(
            agent_arn=agent_arn,
            role_arn=role_arn,
            agent_version=agent_version,
            kms_key_arn=kms_key_arn,
            last_updated=last_updated,
        )

        return typing.cast(IAgent, jsii.sinvoke(cls, "fromAgentAttrs", [scope, id, attrs]))

    @jsii.member(jsii_name="addActionGroup")
    def add_action_group(self, action_group: AgentActionGroup) -> None:
        '''(experimental) Add an action group to the agent.

        :param action_group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417f1714f331f713e989d70b6417dbb800ceedf7de8245c42ba72cde605b3504)
            check_type(argname="argument action_group", value=action_group, expected_type=type_hints["action_group"])
        return typing.cast(None, jsii.invoke(self, "addActionGroup", [action_group]))

    @jsii.member(jsii_name="addActionGroups")
    def add_action_groups(self, *action_groups: AgentActionGroup) -> None:
        '''(experimental) Add multiple action groups to the agent.

        :param action_groups: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd86fd4e92aa0f8ee4a2b95a5ad405d539c55043eec94bf739fcc7fc1455d7a4)
            check_type(argname="argument action_groups", value=action_groups, expected_type=typing.Tuple[type_hints["action_groups"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addActionGroups", [*action_groups]))

    @jsii.member(jsii_name="addGuardrail")
    def add_guardrail(self, guardrail: IGuardrail) -> None:
        '''(experimental) Add guardrail to the agent.

        :param guardrail: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11c85531cb630c4447db8a8385837856811c9de1f8891137d8afe73a3e03cd62)
            check_type(argname="argument guardrail", value=guardrail, expected_type=type_hints["guardrail"])
        return typing.cast(None, jsii.invoke(self, "addGuardrail", [guardrail]))

    @jsii.member(jsii_name="addKnowledgeBase")
    def add_knowledge_base(self, knowledge_base: IKnowledgeBase) -> None:
        '''(experimental) Add knowledge base to the agent.

        :param knowledge_base: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0ea7a1a86c29879ce5949318dae4e0d40df1772332d09e26ac0eebfde38479d)
            check_type(argname="argument knowledge_base", value=knowledge_base, expected_type=type_hints["knowledge_base"])
        return typing.cast(None, jsii.invoke(self, "addKnowledgeBase", [knowledge_base]))

    @builtins.property
    @jsii.member(jsii_name="agentArn")
    def agent_arn(self) -> builtins.str:
        '''(experimental) The ARN of the agent.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "agentArn"))

    @builtins.property
    @jsii.member(jsii_name="agentId")
    def agent_id(self) -> builtins.str:
        '''(experimental) The unique identifier for the agent.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "agentId"))

    @builtins.property
    @jsii.member(jsii_name="codeInterpreterEnabled")
    def code_interpreter_enabled(self) -> builtins.bool:
        '''(experimental) Whether the agent can generate, run, and troubleshoot code when trying to complete a task.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "codeInterpreterEnabled"))

    @builtins.property
    @jsii.member(jsii_name="forceDelete")
    def force_delete(self) -> builtins.bool:
        '''(experimental) Whether the resource will be deleted even if it's in use.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "forceDelete"))

    @builtins.property
    @jsii.member(jsii_name="foundationModel")
    def foundation_model(self) -> IInvokable:
        '''(experimental) The foundation model used for orchestration by the agent.

        :stability: experimental
        '''
        return typing.cast(IInvokable, jsii.get(self, "foundationModel"))

    @builtins.property
    @jsii.member(jsii_name="idleSessionTTL")
    def idle_session_ttl(self) -> _aws_cdk_ceddda9d.Duration:
        '''(experimental) How long sessions should be kept open for the agent.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_ceddda9d.Duration, jsii.get(self, "idleSessionTTL"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the agent.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The IAM role associated to the agent.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="shouldPrepareAgent")
    def should_prepare_agent(self) -> builtins.bool:
        '''(experimental) Whether the agent will automatically update the DRAFT version of the agent after making changes to the agent.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "shouldPrepareAgent"))

    @builtins.property
    @jsii.member(jsii_name="testAlias")
    def test_alias(self) -> IAgentAlias:
        '''(experimental) The default test alias for this agent.

        This corresponds to the test alias
        (``TSTALIASID``) that points to the working (``DRAFT``) version.

        :stability: experimental
        '''
        return typing.cast(IAgentAlias, jsii.get(self, "testAlias"))

    @builtins.property
    @jsii.member(jsii_name="userInputEnabled")
    def user_input_enabled(self) -> builtins.bool:
        '''(experimental) Whether the agent can prompt additional information from the user when it does not have enough information to respond to an utterance.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "userInputEnabled"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description for the agent.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="instruction")
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) The instruction used by the agent.

        This determines how the agent will perform his task.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instruction"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this agent.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdated")
    def last_updated(self) -> typing.Optional[builtins.str]:
        '''(experimental) When this agent was last updated.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastUpdated"))

    @builtins.property
    @jsii.member(jsii_name="promptOverrideConfiguration")
    def prompt_override_configuration(
        self,
    ) -> typing.Optional[PromptOverrideConfiguration]:
        '''(experimental) Overrides some prompt templates in different parts of an agent sequence configuration.

        :default: - No overrides are provided.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[PromptOverrideConfiguration], jsii.get(self, "promptOverrideConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="actionGroups")
    def action_groups(self) -> typing.List[AgentActionGroup]:
        '''(experimental) The action groups associated with the agent.

        :stability: experimental
        '''
        return typing.cast(typing.List[AgentActionGroup], jsii.get(self, "actionGroups"))

    @action_groups.setter
    def action_groups(self, value: typing.List[AgentActionGroup]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__362bb8b9135358d9388689544abcd0d0c9e8e45ae46a6dc95b075f20007b92ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agentVersion")
    def agent_version(self) -> builtins.str:
        '''(experimental) The version of the agent.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "agentVersion"))

    @agent_version.setter
    def agent_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91cb459048547f306b5430fddeea34ffad532f3833878a8a84eb26b35cc9b3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="knowledgeBases")
    def knowledge_bases(self) -> typing.List[IKnowledgeBase]:
        '''(experimental) The KnowledgeBases associated with the agent.

        :stability: experimental
        '''
        return typing.cast(typing.List[IKnowledgeBase], jsii.get(self, "knowledgeBases"))

    @knowledge_bases.setter
    def knowledge_bases(self, value: typing.List[IKnowledgeBase]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8a2ba31fca57d8bfcd42f9f0c012e95f4a9a95f52fe008b4777fe99b12b466)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "knowledgeBases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="guardrail")
    def guardrail(self) -> typing.Optional[IGuardrail]:
        '''(experimental) The guardrail associated with the agent.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IGuardrail], jsii.get(self, "guardrail"))

    @guardrail.setter
    def guardrail(self, value: typing.Optional[IGuardrail]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f09fbddef471377c79a6446f42ca661654094bc2fd1c09c71dd4e5a7f49173)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guardrail", value) # pyright: ignore[reportArgumentType]


class AgentAlias(
    AgentAliasBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentAlias",
):
    '''(experimental) Class to create an Agent Alias with CDK.

    :stability: experimental
    :cloudformationResource: AWS::Bedrock::AgentAlias
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        agent: IAgent,
        agent_version: typing.Optional[builtins.str] = None,
        alias_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param agent: (experimental) The agent associated to this alias.
        :param agent_version: (experimental) The version of the agent to associate with the agent alias. Default: - Creates a new version of the agent.
        :param alias_name: (experimental) The name for the agent alias. Default: - "latest-{hash}"
        :param description: (experimental) Description for the agent alias.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d5252a70a25f0e579966376a7e29bb2527a503dda1a1fed24527d3559affff2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AgentAliasProps(
            agent=agent,
            agent_version=agent_version,
            alias_name=alias_name,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAttributes")
    @builtins.classmethod
    def from_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        agent: IAgent,
        agent_version: builtins.str,
        alias_id: builtins.str,
        alias_name: typing.Optional[builtins.str] = None,
    ) -> IAgentAlias:
        '''(experimental) Brings an Agent Alias from an existing one created outside of CDK.

        :param scope: -
        :param id: -
        :param agent: (experimental) The underlying agent for this alias.
        :param agent_version: (experimental) The agent version for this alias.
        :param alias_id: (experimental) The Id of the agent alias.
        :param alias_name: (experimental) The name of the agent alias.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4d42b60834bc6764b4f77bd27f582ed437f065fd0784141a6193e99b7543ef6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = AgentAliasAttributes(
            agent=agent,
            agent_version=agent_version,
            alias_id=alias_id,
            alias_name=alias_name,
        )

        return typing.cast(IAgentAlias, jsii.sinvoke(cls, "fromAttributes", [scope, id, attrs]))

    @builtins.property
    @jsii.member(jsii_name="agent")
    def agent(self) -> IAgent:
        '''(experimental) The underlying agent for this alias.

        :stability: experimental
        '''
        return typing.cast(IAgent, jsii.get(self, "agent"))

    @builtins.property
    @jsii.member(jsii_name="aliasArn")
    def alias_arn(self) -> builtins.str:
        '''(experimental) The ARN of the agent alias.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "aliasArn"))

    @builtins.property
    @jsii.member(jsii_name="aliasId")
    def alias_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the agent alias.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "aliasId"))

    @builtins.property
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "aliasName"))


class ConfluenceDataSource(
    DataSourceNew,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ConfluenceDataSource",
):
    '''(experimental) Sets up a Confluence Data Source to be added to a knowledge base.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/confluence-data-source-connector.html
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        knowledge_base: IKnowledgeBase,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        confluence_url: builtins.str,
        auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
        filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Confluence instance URL. Secret must start with "AmazonBedrock-".
        :param confluence_url: (experimental) The Confluence host URL or instance URL.
        :param auth_type: (experimental) The supported authentication method to connect to the data source. Default: ConfluenceDataSourceAuthType.OAUTH2_CLIENT_CREDENTIALS
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b38f8a816fb7d23775a4ed11b9b014cd4c8776d9580e4dae986abe72268d6d4b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ConfluenceDataSourceProps(
            knowledge_base=knowledge_base,
            auth_secret=auth_secret,
            confluence_url=confluence_url,
            auth_type=auth_type,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="authSecret")
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "authSecret"))

    @builtins.property
    @jsii.member(jsii_name="confluenceUrl")
    def confluence_url(self) -> builtins.str:
        '''(experimental) The Confluence host URL or instance URL.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "confluenceUrl"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> builtins.str:
        '''(experimental) The name of the data source.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceName"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceType")
    def data_source_type(self) -> DataSourceType:
        '''(experimental) The type of data source.

        :stability: experimental
        '''
        return typing.cast(DataSourceType, jsii.get(self, "dataSourceType"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBase")
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base associated with the data source.

        :stability: experimental
        '''
        return typing.cast(IKnowledgeBase, jsii.get(self, "knowledgeBase"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))


class DataSource(
    DataSourceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.DataSource",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="fromDataSourceId")
    @builtins.classmethod
    def from_data_source_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        data_source_id: builtins.str,
    ) -> IDataSource:
        '''
        :param scope: -
        :param id: -
        :param data_source_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91bb2023285f784980074a6bd9353d73694f701da8c5417daa958a6ed92e7c61)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument data_source_id", value=data_source_id, expected_type=type_hints["data_source_id"])
        return typing.cast(IDataSource, jsii.sinvoke(cls, "fromDataSourceId", [scope, id, data_source_id]))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))


class Guardrail(
    GuardrailBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.Guardrail",
):
    '''(experimental) Class to create a Guardrail with CDK.

    :stability: experimental
    :cloudformationResource: AWS::Bedrock::Guardrail
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        blocked_input_messaging: typing.Optional[builtins.str] = None,
        blocked_outputs_messaging: typing.Optional[builtins.str] = None,
        content_filters: typing.Optional[typing.Sequence[typing.Union[ContentFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
        contextual_grounding_filters: typing.Optional[typing.Sequence[typing.Union[ContextualGroundingFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
        denied_topics: typing.Optional[typing.Sequence[Topic]] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        managed_word_list_filters: typing.Optional[typing.Sequence[ManagedWordFilterType]] = None,
        pii_filters: typing.Optional[typing.Sequence[typing.Union[PIIFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
        regex_filters: typing.Optional[typing.Sequence[typing.Union[RegexFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
        word_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: (experimental) The name of the guardrail.
        :param blocked_input_messaging: (experimental) The message to return when the guardrail blocks a prompt. Default: "Sorry, your query violates our usage policy."
        :param blocked_outputs_messaging: (experimental) The message to return when the guardrail blocks a model response. Default: "Sorry, I am unable to answer your question because of our usage policy."
        :param content_filters: (experimental) The content filters to apply to the guardrail. Note, if one of
        :param contextual_grounding_filters: (experimental) The contextual grounding filters to apply to the guardrail.
        :param denied_topics: (experimental) Up to 30 denied topics to block user inputs or model responses associated with the topic.
        :param description: (experimental) The description of the guardrail.
        :param kms_key: (experimental) A custom KMS key to use for encrypting data. Default: "Your data is encrypted by default with a key that AWS owns and manages for you."
        :param managed_word_list_filters: (experimental) The managed word filters to apply to the guardrail.
        :param pii_filters: (experimental) The PII filters to apply to the guardrail.
        :param regex_filters: (experimental) The regular expression (regex) filters to apply to the guardrail.
        :param word_filters: (experimental) The word filters to apply to the guardrail.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd0388fb62544574fdce33c495357bb3e4ab10d5b21f074fb9b6bce8f730e44)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GuardrailProps(
            name=name,
            blocked_input_messaging=blocked_input_messaging,
            blocked_outputs_messaging=blocked_outputs_messaging,
            content_filters=content_filters,
            contextual_grounding_filters=contextual_grounding_filters,
            denied_topics=denied_topics,
            description=description,
            kms_key=kms_key,
            managed_word_list_filters=managed_word_list_filters,
            pii_filters=pii_filters,
            regex_filters=regex_filters,
            word_filters=word_filters,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromCfnGuardrail")
    @builtins.classmethod
    def from_cfn_guardrail(
        cls,
        cfn_guardrail: _aws_cdk_aws_bedrock_ceddda9d.CfnGuardrail,
    ) -> IGuardrail:
        '''(experimental) Import a low-level L1 Cfn Guardrail.

        :param cfn_guardrail: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b6644b9376e16a02bd94086914855232ac81bd6c18fc520f8750a4a6a15cff)
            check_type(argname="argument cfn_guardrail", value=cfn_guardrail, expected_type=type_hints["cfn_guardrail"])
        return typing.cast(IGuardrail, jsii.sinvoke(cls, "fromCfnGuardrail", [cfn_guardrail]))

    @jsii.member(jsii_name="fromGuardrailAttributes")
    @builtins.classmethod
    def from_guardrail_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        guardrail_arn: builtins.str,
        guardrail_version: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> IGuardrail:
        '''(experimental) Import a guardrail given its attributes.

        :param scope: -
        :param id: -
        :param guardrail_arn: (experimental) The ARN of the guardrail. At least one of guardrailArn or guardrailId must be defined in order to initialize a guardrail ref.
        :param guardrail_version: (experimental) The version of the guardrail. Default: "DRAFT"
        :param kms_key: (experimental) The KMS key of the guardrail if custom encryption is configured. Default: undefined - Means data is encrypted by default with a AWS-managed key

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac4fce8c7366950317863b5de6e9ccb7926adb829fd43d67af111921b6fe60a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = GuardrailAttributes(
            guardrail_arn=guardrail_arn,
            guardrail_version=guardrail_version,
            kms_key=kms_key,
        )

        return typing.cast(IGuardrail, jsii.sinvoke(cls, "fromGuardrailAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addContentFilter")
    def add_content_filter(
        self,
        *,
        input_strength: ContentFilterStrength,
        output_strength: ContentFilterStrength,
        type: ContentFilterType,
    ) -> None:
        '''(experimental) Adds a content filter to the guardrail.

        :param input_strength: (experimental) The strength of the content filter to apply to prompts / user input.
        :param output_strength: (experimental) The strength of the content filter to apply to model responses.
        :param type: (experimental) The type of harmful category that the content filter is applied to.

        :stability: experimental
        '''
        filter = ContentFilter(
            input_strength=input_strength, output_strength=output_strength, type=type
        )

        return typing.cast(None, jsii.invoke(self, "addContentFilter", [filter]))

    @jsii.member(jsii_name="addContextualGroundingFilter")
    def add_contextual_grounding_filter(
        self,
        *,
        threshold: jsii.Number,
        type: ContextualGroundingFilterType,
    ) -> None:
        '''(experimental) Adds a contextual grounding filter to the guardrail.

        :param threshold: (experimental) The threshold for the contextual grounding filter. - ``0`` (blocks nothing) - ``0.99`` (blocks almost everything)
        :param type: (experimental) The type of contextual grounding filter.

        :stability: experimental
        '''
        filter = ContextualGroundingFilter(threshold=threshold, type=type)

        return typing.cast(None, jsii.invoke(self, "addContextualGroundingFilter", [filter]))

    @jsii.member(jsii_name="addDeniedTopicFilter")
    def add_denied_topic_filter(self, filter: Topic) -> None:
        '''(experimental) Adds a denied topic filter to the guardrail.

        :param filter: The denied topic filter to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692157e64cb60b32896dffcc96ff8ad03d713b97963615da507d483b512c865e)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        return typing.cast(None, jsii.invoke(self, "addDeniedTopicFilter", [filter]))

    @jsii.member(jsii_name="addManagedWordListFilter")
    def add_managed_word_list_filter(self, filter: ManagedWordFilterType) -> None:
        '''(experimental) Adds a managed word list filter to the guardrail.

        :param filter: The managed word list filter to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1550b5555345ccffe24c169c8da1cf1ecf54d33d7d26c1a8e1558a75eaa04299)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        return typing.cast(None, jsii.invoke(self, "addManagedWordListFilter", [filter]))

    @jsii.member(jsii_name="addPIIFilter")
    def add_pii_filter(
        self,
        *,
        action: GuardrailAction,
        type: typing.Union[_General_e613aa3a, _Finance_2430d674, _InformationTechnology_2f99a404, _USASpecific_fa88de63, _CanadaSpecific_f80239d8, _UKSpecific_c9314648],
    ) -> None:
        '''(experimental) Adds a PII filter to the guardrail.

        :param action: (experimental) The action to take when PII is detected.
        :param type: (experimental) The type of PII to filter.

        :stability: experimental
        '''
        filter = PIIFilter(action=action, type=type)

        return typing.cast(None, jsii.invoke(self, "addPIIFilter", [filter]))

    @jsii.member(jsii_name="addRegexFilter")
    def add_regex_filter(
        self,
        *,
        action: GuardrailAction,
        name: builtins.str,
        pattern: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Adds a regex filter to the guardrail.

        :param action: (experimental) The action to take when a regex match is detected.
        :param name: (experimental) The name of the regex filter.
        :param pattern: (experimental) The regular expression pattern to match.
        :param description: (experimental) The description of the regex filter.

        :stability: experimental
        '''
        filter = RegexFilter(
            action=action, name=name, pattern=pattern, description=description
        )

        return typing.cast(None, jsii.invoke(self, "addRegexFilter", [filter]))

    @jsii.member(jsii_name="addWordFilter")
    def add_word_filter(self, filter: builtins.str) -> None:
        '''(experimental) Adds a word filter to the guardrail.

        :param filter: The word filter to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b12e8cf2ba55857bc5666a519e1ecd649c5d3b91bef66f1347adeefa1aa890)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        return typing.cast(None, jsii.invoke(self, "addWordFilter", [filter]))

    @jsii.member(jsii_name="addWordFilterFromFile")
    def add_word_filter_from_file(self, file_path: builtins.str) -> None:
        '''(experimental) Adds a word filter to the guardrail.

        :param file_path: The location of the word filter file.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a0c18147e5b1c9acba7a307ef8418fbd3d0c93d1b437ebddea0c1bf85d022a)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        return typing.cast(None, jsii.invoke(self, "addWordFilterFromFile", [file_path]))

    @jsii.member(jsii_name="createVersion")
    def create_version(
        self,
        description: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) Create a version for the guardrail.

        :param description: The description of the version.

        :return: The guardrail version.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__369d6b13c2eb78c16c6cc80e126b921de08cc17315fb782cbeff1efc9a981bfc)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        return typing.cast(builtins.str, jsii.invoke(self, "createVersion", [description]))

    @builtins.property
    @jsii.member(jsii_name="contentFilters")
    def content_filters(self) -> typing.List[ContentFilter]:
        '''(experimental) The content filters applied by the guardrail.

        :stability: experimental
        '''
        return typing.cast(typing.List[ContentFilter], jsii.get(self, "contentFilters"))

    @builtins.property
    @jsii.member(jsii_name="contextualGroundingFilters")
    def contextual_grounding_filters(self) -> typing.List[ContextualGroundingFilter]:
        '''(experimental) The contextual grounding filters applied by the guardrail.

        :stability: experimental
        '''
        return typing.cast(typing.List[ContextualGroundingFilter], jsii.get(self, "contextualGroundingFilters"))

    @builtins.property
    @jsii.member(jsii_name="deniedTopics")
    def denied_topics(self) -> typing.List[Topic]:
        '''(experimental) The denied topic filters applied by the guardrail.

        :stability: experimental
        '''
        return typing.cast(typing.List[Topic], jsii.get(self, "deniedTopics"))

    @builtins.property
    @jsii.member(jsii_name="guardrailArn")
    def guardrail_arn(self) -> builtins.str:
        '''(experimental) The ARN of the guardrail.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailArn"))

    @builtins.property
    @jsii.member(jsii_name="guardrailId")
    def guardrail_id(self) -> builtins.str:
        '''(experimental) The ID of the guardrail.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailId"))

    @builtins.property
    @jsii.member(jsii_name="hash")
    def hash(self) -> builtins.str:
        '''(experimental) The computed hash of the guardrail properties.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "hash"))

    @builtins.property
    @jsii.member(jsii_name="managedWordListFilters")
    def managed_word_list_filters(self) -> typing.List[ManagedWordFilterType]:
        '''(experimental) The managed word list filters applied by the guardrail.

        :stability: experimental
        '''
        return typing.cast(typing.List[ManagedWordFilterType], jsii.get(self, "managedWordListFilters"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the guardrail.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="piiFilters")
    def pii_filters(self) -> typing.List[PIIFilter]:
        '''(experimental) The PII filters applied by the guardrail.

        :stability: experimental
        '''
        return typing.cast(typing.List[PIIFilter], jsii.get(self, "piiFilters"))

    @builtins.property
    @jsii.member(jsii_name="regexFilters")
    def regex_filters(self) -> typing.List[RegexFilter]:
        '''(experimental) The regex filters applied by the guardrail.

        :stability: experimental
        '''
        return typing.cast(typing.List[RegexFilter], jsii.get(self, "regexFilters"))

    @builtins.property
    @jsii.member(jsii_name="wordFilters")
    def word_filters(self) -> typing.List[builtins.str]:
        '''(experimental) The word filters applied by the guardrail.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "wordFilters"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key used to encrypt data.

        :default: undefined - "Data is encrypted by default with a key that AWS owns and manages for you"

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdated")
    def last_updated(self) -> typing.Optional[builtins.str]:
        '''(experimental) When this guardrail was last updated.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastUpdated"))

    @builtins.property
    @jsii.member(jsii_name="guardrailVersion")
    def guardrail_version(self) -> builtins.str:
        '''(experimental) The version of the guardrail.

        By default, this value will always be ``DRAFT`` unless an explicit version is created.
        For an explicit version created, this will usually be a number (e.g. for Version 1 just enter "1")

        :default: - "DRAFT"

        :stability: experimental

        Example::

            "1"
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailVersion"))

    @guardrail_version.setter
    def guardrail_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__587892fea6ede7e5e05e003ef091d1b5fc420c347657acd1011cba3e2b3ee75d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guardrailVersion", value) # pyright: ignore[reportArgumentType]


class KendraKnowledgeBase(
    KendraKnowledgeBaseBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.KendraKnowledgeBase",
):
    '''(experimental) ****************************************************************************                       		  CONSTRUCT ***************************************************************************.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        kendra_index: _IKendraGenAiIndex_da04f105,
        description: typing.Optional[builtins.str] = None,
        existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        instruction: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param kendra_index: (experimental) The Kendra Index to use for the knowledge base.
        :param description: (experimental) The description of the knowledge base. Default: - No description provided.
        :param existing_role: (experimental) Existing IAM role with policy statements granting appropriate permissions to invoke the specific embeddings models. Any entity (e.g., an AWS service or application) that assumes this role will be able to invoke or use the specified embeddings model within the Bedrock service.
        :param instruction: (experimental) A narrative description of the knowledge base. A Bedrock Agent can use this instruction to determine if it should query this Knowledge Base. Default: - No description provided.
        :param name: (experimental) The name of the knowledge base.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864b66087a28ee98dc8d27b89a31b7dc5970fa2857f171a98b2fe87508bcbb97)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = KendraKnowledgeBaseProps(
            kendra_index=kendra_index,
            description=description,
            existing_role=existing_role,
            instruction=instruction,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromKnowledgeBaseAttributes")
    @builtins.classmethod
    def from_knowledge_base_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        kendra_index: _IKendraGenAiIndex_da04f105,
        execution_role_arn: builtins.str,
        knowledge_base_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        instruction: typing.Optional[builtins.str] = None,
        knowledge_base_state: typing.Optional[builtins.str] = None,
    ) -> IKendraKnowledgeBase:
        '''
        :param scope: -
        :param id: -
        :param kendra_index: (experimental) The GenAI Kendra Index ARN.
        :param execution_role_arn: (experimental) The Service Execution Role associated with the knowledge base.
        :param knowledge_base_id: (experimental) The ID of the knowledge base.
        :param description: (experimental) The description of the knowledge base. Default: - No description provided.
        :param instruction: (experimental) Instructions for agents based on the design and type of information of the Knowledge Base. This will impact how Agents interact with the Knowledge Base. Default: - No description provided.
        :param knowledge_base_state: (experimental) Specifies whether to use the knowledge base or not when sending an InvokeAgent request. Default: - ENABLED

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e2407f1aecc6ae0f25c95ddfa4073eb78c8f1ca8847ac51c018cfbc974921b0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = KendraKnowledgeBaseAttributes(
            kendra_index=kendra_index,
            execution_role_arn=execution_role_arn,
            knowledge_base_id=knowledge_base_id,
            description=description,
            instruction=instruction,
            knowledge_base_state=knowledge_base_state,
        )

        return typing.cast(IKendraKnowledgeBase, jsii.sinvoke(cls, "fromKnowledgeBaseAttributes", [scope, id, attrs]))

    @builtins.property
    @jsii.member(jsii_name="kendraIndex")
    def kendra_index(self) -> _IKendraGenAiIndex_da04f105:
        '''(experimental) The GenAI Kendra Index.

        :stability: experimental
        '''
        return typing.cast(_IKendraGenAiIndex_da04f105, jsii.get(self, "kendraIndex"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseArn")
    def knowledge_base_arn(self) -> builtins.str:
        '''(experimental) The ARN of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseArn"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseId")
    def knowledge_base_id(self) -> builtins.str:
        '''(experimental) The ID of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseId"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role associated with the knowledge base.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> KnowledgeBaseType:
        '''(experimental) The type of Knowledge Base.

        :stability: experimental
        '''
        return typing.cast(KnowledgeBaseType, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="instruction")
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) A narrative instruction of the knowledge base.

        A Bedrock Agent can use this instruction to determine if it should
        query this Knowledge Base.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instruction"))


__all__ = [
    "ActionGroupExecutor",
    "Agent",
    "AgentActionGroup",
    "AgentActionGroupProps",
    "AgentAlias",
    "AgentAliasAttributes",
    "AgentAliasBase",
    "AgentAliasProps",
    "AgentAttributes",
    "AgentBase",
    "AgentPromptVariantProps",
    "AgentProps",
    "AgentStepType",
    "ApiSchema",
    "ApplicationInferenceProfile",
    "ApplicationInferenceProfileAttributes",
    "ApplicationInferenceProfileProps",
    "BedrockFoundationModel",
    "BedrockFoundationModelProps",
    "ChatMessage",
    "ChatMessageRole",
    "ChatPromptVariantProps",
    "ChunkingStrategy",
    "CommonKnowledgeBaseAttributes",
    "CommonKnowledgeBaseProps",
    "CommonPromptVariantProps",
    "ConfluenceCrawlingFilters",
    "ConfluenceDataSource",
    "ConfluenceDataSourceAssociationProps",
    "ConfluenceDataSourceAuthType",
    "ConfluenceDataSourceProps",
    "ConfluenceObjectType",
    "ContentFilter",
    "ContentFilterStrength",
    "ContentFilterType",
    "ContextualGroundingFilter",
    "ContextualGroundingFilterType",
    "CrawlingFilters",
    "CrawlingScope",
    "CrossRegionInferenceProfile",
    "CrossRegionInferenceProfileProps",
    "CrossRegionInferenceProfileRegion",
    "CustomParserProps",
    "CustomTopicProps",
    "CustomTransformation",
    "DataDeletionPolicy",
    "DataSource",
    "DataSourceAssociationProps",
    "DataSourceBase",
    "DataSourceNew",
    "DataSourceType",
    "DefaultPromptRouterIdentifier",
    "FoundationModelParsingStategyProps",
    "Guardrail",
    "GuardrailAction",
    "GuardrailAttributes",
    "GuardrailBase",
    "GuardrailProps",
    "HierarchicalChunkingProps",
    "IAgent",
    "IAgentAlias",
    "IDataSource",
    "IGuardrail",
    "IInferenceProfile",
    "IInvokable",
    "IKendraKnowledgeBase",
    "IKnowledgeBase",
    "IPrompt",
    "IPromptRouter",
    "IVectorKnowledgeBase",
    "InferenceConfiguration",
    "InferenceProfileBase",
    "InferenceProfileType",
    "InlineApiSchema",
    "KendraKnowledgeBase",
    "KendraKnowledgeBaseAttributes",
    "KendraKnowledgeBaseBase",
    "KendraKnowledgeBaseProps",
    "KnowledgeBaseBase",
    "KnowledgeBaseType",
    "LambdaCustomTransformationProps",
    "ManagedWordFilterType",
    "PIIFilter",
    "ParentActionGroupSignature",
    "ParsingModality",
    "ParsingStategy",
    "ParsingStategyType",
    "Prompt",
    "PromptAttributes",
    "PromptBase",
    "PromptOverrideConfiguration",
    "PromptProps",
    "PromptRouter",
    "PromptRouterProps",
    "PromptStepConfiguration",
    "PromptStepConfigurationCustomParser",
    "PromptTemplateType",
    "PromptVariant",
    "PromptVersion",
    "PromptVersionProps",
    "RegexFilter",
    "S3ApiSchema",
    "S3DataSource",
    "S3DataSourceAssociationProps",
    "S3DataSourceProps",
    "SalesforceCrawlingFilters",
    "SalesforceDataSource",
    "SalesforceDataSourceAssociationProps",
    "SalesforceDataSourceAuthType",
    "SalesforceDataSourceProps",
    "SalesforceObjectType",
    "SharePointCrawlingFilters",
    "SharePointDataSource",
    "SharePointDataSourceAssociationProps",
    "SharePointDataSourceAuthType",
    "SharePointDataSourceProps",
    "SharePointObjectType",
    "TextPromptVariantProps",
    "ToolChoice",
    "ToolConfiguration",
    "Topic",
    "TransformationStep",
    "VectorKnowledgeBase",
    "VectorKnowledgeBaseAttributes",
    "VectorKnowledgeBaseProps",
    "VectorType",
    "WebCrawlerDataSource",
    "WebCrawlerDataSourceAssociationProps",
    "WebCrawlerDataSourceProps",
    "pii_type",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import pii_type

def _typecheckingstub__1d66975a777761af2c2afa135a0c71acee1d35ee3de96016c47f3c26f3d1d382(
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4482a2286d1aa9365ffd4769d5c935c3786542f444b664ea9da29cb2b875990(
    enabled: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f35ff4a8218c89e3d2dece2516fdae627f224c02993b718a265d95f3b21a74a9(
    enabled: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47b674f810daa9a7bde371ad21ea6944cc41d81e91b4c04fca71b8f52c01288(
    *,
    name: builtins.str,
    api_schema: typing.Optional[ApiSchema] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    executor: typing.Optional[ActionGroupExecutor] = None,
    force_delete: typing.Optional[builtins.bool] = None,
    function_schema: typing.Optional[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.FunctionSchemaProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    parent_action_group_signature: typing.Optional[ParentActionGroupSignature] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c673a16aeefb1b29db08c60a2c30c29e637ee706bdb0fd7a8cfe1a1fc9a2c2c8(
    *,
    agent: IAgent,
    agent_version: builtins.str,
    alias_id: builtins.str,
    alias_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cae66eefc5f4c5599e0686171b63cba4b3c09493c31167b8afaa8bff00da6cc(
    *,
    agent: IAgent,
    agent_version: typing.Optional[builtins.str] = None,
    alias_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae1875c8eb70cd3926525174ad613e977ffed1dda090873c972d973ad219927c(
    *,
    agent_arn: builtins.str,
    role_arn: builtins.str,
    agent_version: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    last_updated: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5254c1c0482eaa66699188ff0467d936350a386bbe823d4ef46c9ba982f91c(
    *,
    foundation_model: IInvokable,
    instruction: builtins.str,
    action_groups: typing.Optional[typing.Sequence[AgentActionGroup]] = None,
    code_interpreter_enabled: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    force_delete: typing.Optional[builtins.bool] = None,
    guardrail: typing.Optional[IGuardrail] = None,
    idle_session_ttl: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    knowledge_bases: typing.Optional[typing.Sequence[IKnowledgeBase]] = None,
    name: typing.Optional[builtins.str] = None,
    prompt_override_configuration: typing.Optional[PromptOverrideConfiguration] = None,
    should_prepare_agent: typing.Optional[builtins.bool] = None,
    user_input_enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e9990488025ce0d3337500e926f885584cf0e74d3bd85a5bb26807188ae82a(
    s3_file: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.Location, typing.Dict[builtins.str, typing.Any]]] = None,
    inline_schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c2792cc1fa0f16747e3820d17877eef4b648c9b158bc65527d5d5c852652166(
    schema: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054b5777af191a7d5068e3619e43fd80fa172483666692ce34f8e2f5ed6246f3(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e985add44eef93f1230fa0ea2845a5132786479af068992c0d8ab98020ad9c58(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    object_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ea34e402b2535f2082177ac38775e1034896579d3693772035c4f45ca2d654(
    *,
    inference_profile_arn: builtins.str,
    inference_profile_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c9200d651e22ff89688db78ff2bdec2a56b7d93a7d2cb347b49efafe13b581c(
    *,
    inference_profile_name: builtins.str,
    model_source: IInvokable,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e1a21a71ca2d85f4b0cb18a5ce955b8c59bb0c4403b3d6f750c90739061d548(
    *,
    supported_vector_type: typing.Optional[typing.Sequence[VectorType]] = None,
    supports_agents: typing.Optional[builtins.bool] = None,
    supports_cross_region: typing.Optional[builtins.bool] = None,
    supports_knowledge_base: typing.Optional[builtins.bool] = None,
    vector_dimensions: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134f5f0222c6822adcdaa44fe72c823a3907b61a0e4f1dc0a388befd7e412755(
    role: ChatMessageRole,
    text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5063cf1ecc7fe858c159acb9c143817eaaf014910bfb9cc7c9f7cfdbb225227(
    text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e85bd735be93f1bf58d001d28c9e0b750bc2a7477c6bb774c806f0be1b6c8fa(
    text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8c95b7bfa78b1915cee9f049873d2af67238c73953179ae4f9479b54751ebf(
    value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ChunkingConfigurationProperty,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e39ca943fffc8eee1fd4bcb58c8e99b2ceda8714caf2e11e757c97dc51b4a9e(
    *,
    execution_role_arn: builtins.str,
    knowledge_base_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    instruction: typing.Optional[builtins.str] = None,
    knowledge_base_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b338369fcf3800b974be16fc9d16c5bbb6e844c94ab39431bdb5db8741f5f7a(
    *,
    description: typing.Optional[builtins.str] = None,
    existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    instruction: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2752ca933595bdb580dc70b29b9d7fea9196785967ed1f46d44fff8b435477(
    *,
    model: IInvokable,
    variant_name: builtins.str,
    prompt_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba4b91ab5b955d9d72d8af6f07cdc07ac568ef117419de41dca7871ad32d6b8(
    *,
    object_type: ConfluenceObjectType,
    exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a9140c0049260b2d312c4a80d1b958e9761476560ef6b565d603fce991e815(
    *,
    input_strength: ContentFilterStrength,
    output_strength: ContentFilterStrength,
    type: ContentFilterType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e4288f485be62d723f6fe133287e8c88a90f455b2dec35e5c4095e4ba4cd69(
    *,
    threshold: jsii.Number,
    type: ContextualGroundingFilterType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf8789f899b4cf122996f24d6718a644cc2bc6a74788ac86472a28afaba4e33f(
    *,
    exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0779b391b71e321d48d3445f56e45aa413e6050e51f0b7161ca653bdbdd424ab(
    *,
    geo_region: CrossRegionInferenceProfileRegion,
    model: BedrockFoundationModel,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75718aff5128dcd74c4fa51ae85d75a9e02a9beda7f7d3f7170e5d1d876dd73(
    *,
    parser: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction] = None,
    steps: typing.Optional[typing.Sequence[typing.Union[PromptStepConfigurationCustomParser, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7afa8690bf8def1351745b409bf75b1c9388f7690948642485ab500130f04eab(
    *,
    definition: builtins.str,
    examples: typing.Sequence[builtins.str],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__898a06e70f7f1a8abcf9e8433317e047be3a6f52316351b0d22de8a49154fb6c(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ea7d98a453ed23a6d13ca01317dfc8f56bd010bb3d771347e4898118887260(
    value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.CustomTransformationConfigurationProperty,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3370fd8035498a3339649efe16f36fa523a3b651e8f4e3f2f7cc83f1af7f2c0(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed85f0ccfdf38b650635f35650195519e14f924af93233cef46e2fd5af61295(
    *,
    parsing_model: IInvokable,
    parsing_modality: typing.Optional[ParsingModality] = None,
    parsing_prompt: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b140b7ab54824449cb92973af6b36eb6cf61ab0c9257fdf79c5d510e1f60ff(
    *,
    guardrail_arn: builtins.str,
    guardrail_version: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9d19859a6750c938be49617894f02e36de79c2e5a05a9cb6d6eac91e68d0ea(
    *,
    name: builtins.str,
    blocked_input_messaging: typing.Optional[builtins.str] = None,
    blocked_outputs_messaging: typing.Optional[builtins.str] = None,
    content_filters: typing.Optional[typing.Sequence[typing.Union[ContentFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    contextual_grounding_filters: typing.Optional[typing.Sequence[typing.Union[ContextualGroundingFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    denied_topics: typing.Optional[typing.Sequence[Topic]] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    managed_word_list_filters: typing.Optional[typing.Sequence[ManagedWordFilterType]] = None,
    pii_filters: typing.Optional[typing.Sequence[typing.Union[PIIFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    regex_filters: typing.Optional[typing.Sequence[typing.Union[RegexFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    word_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832a5183cc17b41fd7587d09a661c1bc3796489cafca2ed06677f49aa94a717d(
    *,
    max_child_token_size: jsii.Number,
    max_parent_token_size: jsii.Number,
    overlap_tokens: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df59fa11db2053427ed6170c8adff35c1babc7d6257284c96c156295d88f9a1(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02c91625918402481c9f4e1e5c4423a8b43f91f76cc3c463edeeaaa0eae178e(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a0c02755094e6851a73cb8ab426a25166689912c7122d3c95b6ce963d214862(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa86b82cfa7566549e30a1d5b954f23d8c26046bfa7cc0af976bc3c76faa6d16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5125723d1fe4aed39d0c9ef21fda4887064605eb58037eb896c217af3572d08(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ba62eccfee612703b786064d7f93d108f9f738d3af81886e81a1528ede7a98(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a604164d87e46d6095394689572206d47548b4ca8f338519f76cb51ef2f735(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    stack_account: typing.Optional[builtins.str] = None,
    stack_region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e05b919b09e86b619e07b4ef364b84ec6c2406d5ea1bca6a3cc89fa68153ec7(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29403dd1f5d63fdfa42529ed12671747a327e8f838334b096c8d604ee0871773(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38eeedeba6ae1a17302d5c0d2af9c9f8fd714ba1ff9eae57010ac53606d94377(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f52b2243768badbd2bf4261a9b42e28734215c49e1318565708fb4cbdc5967a(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5960928d16109614db9d88a976b6813f338475a6d9bd76b0987c904ec8128c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb0ae116051d137f78de149c1f75f9b1baccacd6bacf105433c47f07dec8c50(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__376dfa6a00d154d8a21d348f5ca5f0ae71a20f6e24f1a069048d3d2878532c9a(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__befd502c2937a36c672491bd2695d4ec887944e821efe023f2dc44cff4137750(
    *,
    maximum_length: jsii.Number,
    stop_sequences: typing.Sequence[builtins.str],
    temperature: jsii.Number,
    top_k: jsii.Number,
    top_p: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47a0e32efc3020834d43d9c5523a26c5aa4f43e016164f6b0291a29938455be(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e018efd836bd4c5f724810d840738657b70936f17c80063e2affbcd56a59c5(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abeb00812cdcb551f5f688ee295d8f225db974111b8872709130c22fef51592f(
    schema: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d227560632c8cafe262d3765e0ad2d2b24c7478a3d874d75c9abfe763e731d8(
    *,
    execution_role_arn: builtins.str,
    knowledge_base_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    instruction: typing.Optional[builtins.str] = None,
    knowledge_base_state: typing.Optional[builtins.str] = None,
    kendra_index: _IKendraGenAiIndex_da04f105,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2891c8481d2110f8ef1227393069a9fb2102f7ea78c6d79011264ca11a179f(
    *,
    description: typing.Optional[builtins.str] = None,
    existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    instruction: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    kendra_index: _IKendraGenAiIndex_da04f105,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2018afba30c8a414072bbb105ab599acca2c6b6fbe157efe69349742ccbf99d6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffbd6f230e5a20f5fb83bf781858e4c477d1419b7b476b7e099e7abd31643846(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4aa7e889359278217a09e6a1d1cdad6957d67358183f869750b18d467a82947(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0248f7f07e8c1872e77085a6db35a628b2ede66df317215b0653aa6cba4a0377(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24aab71d54c86fb197cc2fd20e38a72d68d2b34a4ded13e5260624512f27da7b(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762879178fd972fbfc85b23a5a96fe26104fbaf3791957f75d2f92316a91cc7a(
    *,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    s3_bucket_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68aa36b0ead1124a53b5c01582eeed48828bdcc66f87d80565fddd7cc232b72e(
    *,
    action: GuardrailAction,
    type: typing.Union[_General_e613aa3a, _Finance_2430d674, _InformationTechnology_2f99a404, _USASpecific_fa88de63, _CanadaSpecific_f80239d8, _UKSpecific_c9314648],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98539d4744437cf3435827d76a26eec0c07d53390b769ffdeba9b651eabb38af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20f93031aefe7465a4c9b7b8cbf589b874a8c6abd25dd259847d7c99f2c292b(
    value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ParsingConfigurationProperty,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28412a5d8ac170fe3a64e61ef6ae3f19e2ab4831e4f173b4d9dd49819888b236(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    prompt_name: builtins.str,
    default_variant: typing.Optional[PromptVariant] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    variants: typing.Optional[typing.Sequence[PromptVariant]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493e34f209102ea802c9e52bb8d42086b43ec2f571efc98a8d11938b5c35926c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    prompt_arn: builtins.str,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    prompt_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebfa6edec3745b41e32e786ccd9bf47e56b752a48a1204aefa620f6425599454(
    variant: PromptVariant,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc07b4411e1c17474873d667b41d3c8be2fd1ca6adf765c3090c15136423d774(
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30a1a38bb8b0d638d069ad28bc55cbba27373d5af3489817853bd7e1dc88410(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65cd66a5ef99991ddde61b718842ff11d482414cb8db73961c80294c681f3502(
    *,
    prompt_arn: builtins.str,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    prompt_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416e615710246dc6fdddab19da69a2adde0b7094028409f64cc9e0c153344b57(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6010854ea9d0c593f1187eff0dbb1c606b73ff1be68e89b0d245291215123a(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e18fab10acf8af328be25f79340aeb64cc011327127be967f99f267d6b6c92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8b175dc775b29e053d126300ee889ac45a8923baf78518a02105c4a2534f75(
    steps: typing.Optional[typing.Sequence[typing.Union[PromptStepConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed24724d2a2267a3662057e3f507a648a9688b88f50d099de8ac08580da8541(
    *,
    prompt_name: builtins.str,
    default_variant: typing.Optional[PromptVariant] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    variants: typing.Optional[typing.Sequence[PromptVariant]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2a0966faeb6dd9c7e135b2e783450d7792ed9243c747b5b8742493ba672ba7(
    props: typing.Union[PromptRouterProps, typing.Dict[builtins.str, typing.Any]],
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f20b9011e0f783fb6d55e2d1bcafcfaf570c09d7271f5b62d707a9d253cd566(
    default_router: DefaultPromptRouterIdentifier,
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc424676ecf4a95f0287e0a3f6ea4c6b6bfda8245f81a410a2256f615221690(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e4b730bc2659721f1a04223df16609ae329cd99215327a755ffdc68d924ca1(
    *,
    prompt_router_id: builtins.str,
    routing_models: typing.Sequence[BedrockFoundationModel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9369143f88c7f634aa2f46b339696a36f19a0c3ed51f8df732360e157f4f6e(
    *,
    step_type: AgentStepType,
    custom_prompt_template: typing.Optional[builtins.str] = None,
    inference_config: typing.Optional[typing.Union[InferenceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    step_enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed1da902ff6fd0d45695a80270445b8635df4af40f4e642b1dcb831867b294cb(
    *,
    step_type: AgentStepType,
    custom_prompt_template: typing.Optional[builtins.str] = None,
    inference_config: typing.Optional[typing.Union[InferenceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    step_enabled: typing.Optional[builtins.bool] = None,
    use_custom_parser: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47858dac9c23ea6d5fe047093eb7c553df8379b538751a421229fcd6090a3d99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfacc76ecbab5bd528fdafd1e6e9ea9558ae6b7f7404301dfde9e66ae3ed865c(
    value: _aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptTemplateConfigurationProperty,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb21a09b18d3af2233c1a12de246544b29d61535df0d28d7f9fb947c1b2668d(
    value: PromptTemplateType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d836d8435ed72ee87ad020c0a9ebf265fc0986eaef8eb628703d17470a9ace0(
    value: typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptGenAiResourceProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868e405119ddf957e9771368dbe10acb67f0d6f0dc2fe35578128be175024448(
    value: typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptInferenceConfigurationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94db700745c23c237379ad0e9208bfa80e98851952c0558325390455e764cd02(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6daa6c79624257e31d9072fc0f20e2f2fc9397635524aa9d067fb36cc7cbbc53(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    prompt: Prompt,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49af665e03ae5aea14b78e3aee6d9f0d78722f97c5b289cb5dc844a1cf90815(
    *,
    prompt: Prompt,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a46345c7df17f55020986d90b7ae90f85b55d19822b9b2574bc1ff9831b2d20(
    *,
    action: GuardrailAction,
    name: builtins.str,
    pattern: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937192d503ab06e7d72cb5fca8edb1e0959f925784ef831da357511f9247a9ec(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061fd79f5c6cc3fdad0a0fcccc8c2a083f5deeb769270d6795cc47edeeaecc0b(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    knowledge_base: IKnowledgeBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ba2de3246503cef86100625445a5010d4594edc17ad5fe4ba4d35b9c066463(
    *,
    object_type: SalesforceObjectType,
    exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9630b4dd940c86a5fa5c47ae28d9a991c3d58e7b9c5432ba828cb2cb213d00(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    endpoint: builtins.str,
    filters: typing.Optional[typing.Sequence[typing.Union[SalesforceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7dc3117cebd56970b3e49e262627a6133820bc4f98949e5002679327375f4f3(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    endpoint: builtins.str,
    filters: typing.Optional[typing.Sequence[typing.Union[SalesforceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    knowledge_base: IKnowledgeBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc66a84b3c3b22e2879cf44c3edf17abf1ec9c5fb2ebee76fab9d6455ad43867(
    *,
    object_type: SharePointObjectType,
    exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c756d6075defa355f5293064dde03559d8f435bbe0f49037277d8587875a983f(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    domain: builtins.str,
    site_urls: typing.Sequence[builtins.str],
    tenant_id: builtins.str,
    filters: typing.Optional[typing.Sequence[typing.Union[SharePointCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77cac4a3c20de6d6ae043e36137b1e8760f3e2ae41c065f2a00a80740ce91b38(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    domain: builtins.str,
    site_urls: typing.Sequence[builtins.str],
    tenant_id: builtins.str,
    filters: typing.Optional[typing.Sequence[typing.Union[SharePointCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    knowledge_base: IKnowledgeBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd54adac2df83b870909830e4b8468b5d71a8b9dac001336a6076238c87d3c3d(
    *,
    model: IInvokable,
    variant_name: builtins.str,
    prompt_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
    prompt_text: builtins.str,
    inference_configuration: typing.Optional[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b5680e044cd8da5aa0920f581bea14656963b55a384dfacf04768640a80971(
    any: typing.Any,
    auto: typing.Any,
    tool: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d688d553ece27b2a018e94fe57c53ee4011a209f98b79453dc65103b27cffc48(
    tool_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88cee3238bc8434e4eade16ff3314f3a8bc41921f90329b1ba433d8293c63b71(
    *,
    tool_choice: ToolChoice,
    tools: typing.Sequence[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.ToolProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d431125f578eeb429055e5151ba6ee8f25bf86af603577323e147b9307afaa(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    embeddings_model: BedrockFoundationModel,
    index_name: typing.Optional[builtins.str] = None,
    vector_field: typing.Optional[builtins.str] = None,
    vector_index: typing.Optional[_VectorIndex_e5d266e9] = None,
    vector_store: typing.Optional[typing.Union[_ExistingAmazonAuroraVectorStore_f7ccb819, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]] = None,
    vector_type: typing.Optional[VectorType] = None,
    description: typing.Optional[builtins.str] = None,
    existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    instruction: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__071f6f3bd86a8b545dbba812f435c0f6d53fb8c691d0150900edad95da48759b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    execution_role_arn: builtins.str,
    knowledge_base_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    instruction: typing.Optional[builtins.str] = None,
    knowledge_base_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6c29b0f94928797fa2fcc3e89d70bd0cd52190b237c122af7142338e6d0e3c(
    agent: Agent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f9534cd4670aae2be069501f0039e758de585b8fd9859df103e55a26458438(
    *,
    execution_role_arn: builtins.str,
    knowledge_base_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    instruction: typing.Optional[builtins.str] = None,
    knowledge_base_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47fae20f2001bac9670b6ad45b66ff9f8fe8e075e4d4f97b9f3130e153d3ea79(
    *,
    description: typing.Optional[builtins.str] = None,
    existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    instruction: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    embeddings_model: BedrockFoundationModel,
    index_name: typing.Optional[builtins.str] = None,
    vector_field: typing.Optional[builtins.str] = None,
    vector_index: typing.Optional[_VectorIndex_e5d266e9] = None,
    vector_store: typing.Optional[typing.Union[_ExistingAmazonAuroraVectorStore_f7ccb819, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]] = None,
    vector_type: typing.Optional[VectorType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2d4384933474c1f544b514a9796e0d1ce1eea63851d2a0cbad594f4b1d4830(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    source_urls: typing.Sequence[builtins.str],
    crawling_rate: typing.Optional[jsii.Number] = None,
    crawling_scope: typing.Optional[CrawlingScope] = None,
    filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7f1066a3d54b5b87f6d6542c10949f6480a3b99f641342456db80c76a73a8c(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    source_urls: typing.Sequence[builtins.str],
    crawling_rate: typing.Optional[jsii.Number] = None,
    crawling_scope: typing.Optional[CrawlingScope] = None,
    filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
    knowledge_base: IKnowledgeBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d536a97c14b9ec306362ef2e875029959b8f84ade2155154aed19edb293431e4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6bd6a42c3fe8b4e86fa23e7ace7c0b0c85484f76e3f333524490377b8a4863(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827dee60e296765d8e60eb0f1309cd9e89e299b3b2433b78b0a788426ea1010c(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b448e39f322730fa1e625ecc3696ed24683045df5d66fa9df27b36a524a5c262(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c3a5d0cda4ce4456eb176ad1c07357a39d7fe3af20e3e68687067f16c8c7aa(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__483f422cc7a4f217d1c995fd9ee49bffdd94d76795a73ccb19ca6a05a2917aaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd09e55bb476582351ebba4821a32d4d2805cc94cd42116b015f968efff63ee(
    *,
    model: IInvokable,
    variant_name: builtins.str,
    prompt_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
    agent_alias: IAgentAlias,
    prompt_text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9295fc37ecfd5ba15c3b4b32661816cc911d30425b0457d6d9e73aab82dc7f58(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    inference_profile_name: builtins.str,
    model_source: IInvokable,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08499f882d34a991b6ff994ce67891aa81aad629aea208a0d363fe07aa2d8b5d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    inference_profile_arn: builtins.str,
    inference_profile_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4756b25b5d6740797b0f293da1e552a81883343f282122c5ff5fadb11eeb76b3(
    cfn_application_inference_profile: _aws_cdk_aws_bedrock_ceddda9d.CfnApplicationInferenceProfile,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7315621579f5e4f7d30f4502f1eeff997dba6cf3f1b3fa9f44a777ac8142ef07(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cee844d1aa1c3aa02aa8a059e448586063f79d5157d71fc62c9035f258d4a04(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a81fd58f8932cf2d8dbd47ee14e3d74d82d0d0245523bd77f54c7a3ebe2a31(
    value: builtins.str,
    *,
    supported_vector_type: typing.Optional[typing.Sequence[VectorType]] = None,
    supports_agents: typing.Optional[builtins.bool] = None,
    supports_cross_region: typing.Optional[builtins.bool] = None,
    supports_knowledge_base: typing.Optional[builtins.bool] = None,
    vector_dimensions: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e574ebd23afcb2cd940b46095855d515345af1851202b2050e4beae0b61b0797(
    model_id: _aws_cdk_aws_bedrock_ceddda9d.FoundationModel,
    *,
    supported_vector_type: typing.Optional[typing.Sequence[VectorType]] = None,
    supports_agents: typing.Optional[builtins.bool] = None,
    supports_cross_region: typing.Optional[builtins.bool] = None,
    supports_knowledge_base: typing.Optional[builtins.bool] = None,
    vector_dimensions: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e6ba9edf9949ffdb893690a97303140d822c69b491d2f36a23884f599a2c01(
    model_id: _aws_cdk_aws_bedrock_ceddda9d.FoundationModelIdentifier,
    *,
    supported_vector_type: typing.Optional[typing.Sequence[VectorType]] = None,
    supports_agents: typing.Optional[builtins.bool] = None,
    supports_cross_region: typing.Optional[builtins.bool] = None,
    supports_knowledge_base: typing.Optional[builtins.bool] = None,
    vector_dimensions: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0736a1f1795a1917c49125732e66d2d15e2a25a6b98ac778b58a6ed32dc0df7b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da72b0f5ffa432a07504325247590f94f501d9e78a5f834d66e81cfc7e0273f1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f51a4f667d4d649aafa9ba1bacf7d35b00909caf39e4001910a74850fc7131df(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d3c75724e9e59d672c6ddd0ebf03051252caf48c764eeff6f38c9dbc5d4750(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c2d071889b362ccec61b0fabb43bd263896b68f536a4efb599bdbee9c6282d(
    *,
    model: IInvokable,
    variant_name: builtins.str,
    prompt_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
    messages: typing.Sequence[ChatMessage],
    inference_configuration: typing.Optional[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    system: typing.Optional[builtins.str] = None,
    tool_configuration: typing.Optional[typing.Union[ToolConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825542cfcf1e14b8a9bbb49badd630cea24320a1c93de247ce04dade6510a396(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    confluence_url: builtins.str,
    auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
    filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14df6d19dffd71a4d3ac18b026e201bc33f4eabb05690ed07f68835b4c37b32(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    confluence_url: builtins.str,
    auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
    filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    knowledge_base: IKnowledgeBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f472f27b5fa3d24da2ba8a7f195c5e15bd841db7f86b5c297fc541b722f61ac6(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93fff43e7d1f97fa19dd910168fe2f7ff3f51b42c62d60e9b28f154c02abdf57(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd33be0b5b715618515a9e14205bd91556c356258bedc630996b5ce10baf76f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd726166f60d1f4704e8a674b6b10ffb8ada8138d51b0fb6cd7ff76f8b98644(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff20dd4f9a8695235fc5ad3f8044d1b2ab4c308a247f269a7667225817ffa47f(
    props: typing.Union[DataSourceAssociationProps, typing.Dict[builtins.str, typing.Any]],
    *,
    type: builtins.str,
    confluence_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ConfluenceDataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.S3DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    salesforce_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.SalesforceDataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    share_point_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.SharePointDataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    web_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.WebDataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd3735db5e3fe2e0ab1bdcc83a66314e304f7420d3c02093aaa2f59d0c028ef(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ffd62f94a075285352644796900ec1cbbc174ef702181d1d0731d60a2b44690(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    stack_account: typing.Optional[builtins.str] = None,
    stack_region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7159e78ce120fa250f1ffec06780e7e9794db74027afd73494579443efb1b0(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96bf842a81e21fd1954424599cbfcd6aa0d8d29978b87d0221427d57ac30a99a(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29a8aa8ec53e9d8a3927f7d99acea5795fe62a6615a19aba1057ba5b5e2bb02(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    stack_account: typing.Optional[builtins.str] = None,
    stack_region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3213cd2c4a16450e0a0e2f790d34031e9f57737b870372668dd1026cdbc75470(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b02cf0eea625902c4343704976c208b4fd02d51cbe3f630137ba3ccecb55886(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48fbbb836e75c99d63b1aecb8d429a451f727eaf6d350fa9c8a3e73f4932c719(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    knowledge_base: IKnowledgeBase,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24d143c738c77349d9a94ed93b630e764b1d3c773aec262ad85df95b6be2129(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    knowledge_base: IKnowledgeBase,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    endpoint: builtins.str,
    filters: typing.Optional[typing.Sequence[typing.Union[SalesforceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a767e627d5bb3db391024a83258857573d524cc605c090521fdd3266c3253351(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    knowledge_base: IKnowledgeBase,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    domain: builtins.str,
    site_urls: typing.Sequence[builtins.str],
    tenant_id: builtins.str,
    filters: typing.Optional[typing.Sequence[typing.Union[SharePointCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e8107d76623400258117634288819beb4c9790e20e7ae484c9025d9dded738(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    knowledge_base: IKnowledgeBase,
    source_urls: typing.Sequence[builtins.str],
    crawling_rate: typing.Optional[jsii.Number] = None,
    crawling_scope: typing.Optional[CrawlingScope] = None,
    filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627af24bb5e1ca4b3ebb82ecbd7a3f01cb1f5177248afdccbc1d0ffab70726de(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    foundation_model: IInvokable,
    instruction: builtins.str,
    action_groups: typing.Optional[typing.Sequence[AgentActionGroup]] = None,
    code_interpreter_enabled: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    force_delete: typing.Optional[builtins.bool] = None,
    guardrail: typing.Optional[IGuardrail] = None,
    idle_session_ttl: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    knowledge_bases: typing.Optional[typing.Sequence[IKnowledgeBase]] = None,
    name: typing.Optional[builtins.str] = None,
    prompt_override_configuration: typing.Optional[PromptOverrideConfiguration] = None,
    should_prepare_agent: typing.Optional[builtins.bool] = None,
    user_input_enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ddfd67114f779bb1081ff73c6fe6d8d34c791f11bde1dea5b4e7f8983c46c0a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    agent_arn: builtins.str,
    role_arn: builtins.str,
    agent_version: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    last_updated: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417f1714f331f713e989d70b6417dbb800ceedf7de8245c42ba72cde605b3504(
    action_group: AgentActionGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd86fd4e92aa0f8ee4a2b95a5ad405d539c55043eec94bf739fcc7fc1455d7a4(
    *action_groups: AgentActionGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11c85531cb630c4447db8a8385837856811c9de1f8891137d8afe73a3e03cd62(
    guardrail: IGuardrail,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ea7a1a86c29879ce5949318dae4e0d40df1772332d09e26ac0eebfde38479d(
    knowledge_base: IKnowledgeBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362bb8b9135358d9388689544abcd0d0c9e8e45ae46a6dc95b075f20007b92ec(
    value: typing.List[AgentActionGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91cb459048547f306b5430fddeea34ffad532f3833878a8a84eb26b35cc9b3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8a2ba31fca57d8bfcd42f9f0c012e95f4a9a95f52fe008b4777fe99b12b466(
    value: typing.List[IKnowledgeBase],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f09fbddef471377c79a6446f42ca661654094bc2fd1c09c71dd4e5a7f49173(
    value: typing.Optional[IGuardrail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5252a70a25f0e579966376a7e29bb2527a503dda1a1fed24527d3559affff2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    agent: IAgent,
    agent_version: typing.Optional[builtins.str] = None,
    alias_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d42b60834bc6764b4f77bd27f582ed437f065fd0784141a6193e99b7543ef6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    agent: IAgent,
    agent_version: builtins.str,
    alias_id: builtins.str,
    alias_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38f8a816fb7d23775a4ed11b9b014cd4c8776d9580e4dae986abe72268d6d4b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    knowledge_base: IKnowledgeBase,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    confluence_url: builtins.str,
    auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
    filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91bb2023285f784980074a6bd9353d73694f701da8c5417daa958a6ed92e7c61(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    data_source_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd0388fb62544574fdce33c495357bb3e4ab10d5b21f074fb9b6bce8f730e44(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    blocked_input_messaging: typing.Optional[builtins.str] = None,
    blocked_outputs_messaging: typing.Optional[builtins.str] = None,
    content_filters: typing.Optional[typing.Sequence[typing.Union[ContentFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    contextual_grounding_filters: typing.Optional[typing.Sequence[typing.Union[ContextualGroundingFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    denied_topics: typing.Optional[typing.Sequence[Topic]] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    managed_word_list_filters: typing.Optional[typing.Sequence[ManagedWordFilterType]] = None,
    pii_filters: typing.Optional[typing.Sequence[typing.Union[PIIFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    regex_filters: typing.Optional[typing.Sequence[typing.Union[RegexFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    word_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b6644b9376e16a02bd94086914855232ac81bd6c18fc520f8750a4a6a15cff(
    cfn_guardrail: _aws_cdk_aws_bedrock_ceddda9d.CfnGuardrail,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac4fce8c7366950317863b5de6e9ccb7926adb829fd43d67af111921b6fe60a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    guardrail_arn: builtins.str,
    guardrail_version: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692157e64cb60b32896dffcc96ff8ad03d713b97963615da507d483b512c865e(
    filter: Topic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1550b5555345ccffe24c169c8da1cf1ecf54d33d7d26c1a8e1558a75eaa04299(
    filter: ManagedWordFilterType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b12e8cf2ba55857bc5666a519e1ecd649c5d3b91bef66f1347adeefa1aa890(
    filter: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a0c18147e5b1c9acba7a307ef8418fbd3d0c93d1b437ebddea0c1bf85d022a(
    file_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__369d6b13c2eb78c16c6cc80e126b921de08cc17315fb782cbeff1efc9a981bfc(
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__587892fea6ede7e5e05e003ef091d1b5fc420c347657acd1011cba3e2b3ee75d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864b66087a28ee98dc8d27b89a31b7dc5970fa2857f171a98b2fe87508bcbb97(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    kendra_index: _IKendraGenAiIndex_da04f105,
    description: typing.Optional[builtins.str] = None,
    existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    instruction: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e2407f1aecc6ae0f25c95ddfa4073eb78c8f1ca8847ac51c018cfbc974921b0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    kendra_index: _IKendraGenAiIndex_da04f105,
    execution_role_arn: builtins.str,
    knowledge_base_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    instruction: typing.Optional[builtins.str] = None,
    knowledge_base_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
