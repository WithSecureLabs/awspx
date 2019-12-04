# Contributing to awspx

The easiest way you can contribute to awspx is by using the tool and reporting bugs you encounter through the Github issue tracker. But if you'd like to do a bit more than that, the project has two naturally expandable components: service ingestors and attack patterns. This file provides a couple of brief tutorials on how to add those.

<br/>
<br/>

## Adding a new service ingestor

Depending on the service you want to add support for, you may need to write a Resources-based ingestor, or you may need to write a custom ingestor.

### Adding a new service with boto3 Resources

The base Ingestor class uses [boto3's Resources](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/resources.html) interface to ingest resources and infer relationships between them. Currently, this interface is implemented for the following services.

* cloudformation
* cloudwatch
* dynamodb
* ec2
* glacier
* iam
* opsworks
* s3
* sns
* sqs

Currently, awspx's EC2 and S3 ingestors use this architecture. If you would like to add one of the other services in this list (for example, CloudFormation), you can start with the following class declaration:

```
class CloudFormation:
    pass
```

To test your ingestor, run `awspx ingest` with the following arguments:

```
awspice ingest --profile your-profile --services CloudFormation
```

It is likely that the first run will crash with an error. These errors usually result from the ingestor failing to determine a `Name` or `Arn` property for one or more resources in the service. With verbose output, you will be able to see the structure of the data the ingestor fails on. Using this output, you will need to amend the methods `_get_resource_arn` and `_get_resource_name` in the `Ingestor` base class. Continue until all ingested resources have both a `Name` and an `Arn`.

Once you've fixed these bugs, you can start considering which resources you want to ingest and which relationships are worth showing. These two aspects of ingestion are represented by `run` and `associates` respectively.

An ingestor's `run` attribute is a list of resources it will ingest by default. These are formatted as plurals of the final part of each resource name in `lib/aws/resources.py`. Thus `AWS::S3::Bucket` becomes `buckets` and `AWS::Ec2::Vpc` becomes `vpcs`.

An ingestor's `associates` attribute is a list of tuples, representing relationships between types to map. The ingestor will infer relationships between resources based on boto3's Resource model, e.g. if an `instance` object has an attribute called `snapshots`, there is a relationship between instances and snapshots. If `associates` is not defined, all inferred relationships will be mapped. Thus, `associates` is a good way to prune excessive edges. See the EC2 ingestor for a good example.

### Adding a new service without boto3 Resources

When adding services not supported by boto3 Resources, you will have to fall back to using boto3 service clients, which are thin wrappers over AWS cli commands. You will need to manually discover the different resource types and their associations. The Lambda service ingestor is an example of such an ingestor.

You can start with code like the following, which inherits from the base Ingestor but tells the initializer not to run the default ingestion while still accounting for type and ARN selection.

```python
class MyService(Ingestor):
    run = [ '...' ]

    def __init__(self, session, account="0000000000000",
                 only_types=[], except_types=[], only_arns=[], except_arns=[]):

        super().__init__(session=session, default=False)
        if not (super()._resolve_type_selection(only_types, except_types)
                and super()._resolve_arn_selection(only_arns, except_arns)):
            return

        self.client = self.session.client(self.__class__.__name__.lower())

        for rt in self.run:

            print(f"{self.__class__.__name__}: Loading {rt}")


```

### Enriching services

While the above methods will ingest a large amount of data about resources and their relationships, many AWS services require additional enrichment for us to get all the information that's useful for mapping out the environment and drawing attack paths. For these cases, we need to do some ingestor enrichment.

The S3 ingestor provides a good example of this. Because bucket policies and ACLs are not pulled by the standard ingestor logic, we have two additional methods to pull this information for each bucket. Consider the method for getting bucket policies:


```python
def get_bucket_policies(self):

    sr = self.session.resource(self.__class__.__name__.lower())

    for bucket in self.get("AWS::S3::Bucket").get("Resource"):
        try:

            bucket.set("Policy", json.loads(sr.BucketPolicy(
                bucket.get('Name')).policy))
        except:  # no policy for this bucket
            pass
```

This method uses additional, S3-specific methods to get the policy for each ingested bucket, which are enumerated using methods provided by `Ingestor`'s parent class, `Elements` (see `lib/graph/base.py`). The same procedure is followed to get bucket ACLs, and to get instance user data in EC2.

<br/>
<br/>

## Adding a new attack pattern

A dictionary of attacks is defined in `lib/aws/attacks.py`. An overview of the thinking behind attack resolution in awspx can be found [on the F-Secure Labs blog](https://labs.f-secure.com/blog/awspx).
