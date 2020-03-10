export const queries = [
    {
        name: "Inventory",
        description: "List all resources in your account",
        value: [
            "MATCH (Source:Resource)",
            "RETURN Source.Name AS Name,",
            "Source.Arn AS ARN"
        ]
    },
    {
        name: "Administrators",
        description: "List resources that effectively have full access to your account",
        value: [
            "MATCH Path=(Source:Resource)-[:TRANSITIVE|ATTACK*1..]->(Target:Admin)",
            "RETURN Source.Name AS Name, Source.Arn AS Arn"
        ]
    },
    {
        name: "Public access",
        description: "Shows actions that can be performed by anyone",
        value: [
            "MATCH Actions=(Source:`AWS::Account`)-[Action:ACTION]->(Target:Resource)",
            "WHERE Source.Name = 'All AWS Accounts'",
            "AND Action.Effect = 'Allow'",
            "RETURN Actions"
        ]
    },
    {
        name: "Public buckets (read access)",
        description: "Shows buckets that can be read anonymously",
        value: [
            "MATCH Actions=(Source:`AWS::Account`)-[Action:ACTION]->(Target:`AWS::S3::Bucket`)",
            "WHERE Source.Name = 'All AWS Accounts'",
            "AND Action.Access = 'Read'",
            "AND Action.Effect = 'Allow'",
            "RETURN Actions"
        ]
    },
    {
        name: "Public roles (assumable)",
        description: "Shows roles that can be assumed anonymously",
        value: [
            "MATCH Actions=(Source:`AWS::Account`)-[Action:ACTION]->(Target:`AWS::Iam::Role`)",
            "WHERE Source.Name = 'All AWS Accounts'",
            "AND Action.Effect = 'Allow'",
            "AND Action.Name =~ '.*sts:Assume.*'",
            "RETURN Actions"
        ]
    }
];
