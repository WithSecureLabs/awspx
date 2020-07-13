ACTIONS = {
  "ec2:AcceptReservedInstancesExchangeQuote": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to accept a Convertible Reserved Instance exchange quote",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AcceptReservedInstancesExchangeQuote.html"
  },
  "ec2:AcceptTransitGatewayPeeringAttachment": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to accept a transit gateway peering attachment request",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AcceptTransitGatewayPeeringAttachment.html"
  },
  "ec2:AcceptTransitGatewayVpcAttachment": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to accept a request to attach a VPC to a transit gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AcceptTransitGatewayVpcAttachment.html"
  },
  "ec2:AcceptVpcEndpointConnections": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to accept one or more interface VPC endpoint connections to your VPC endpoint service",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AcceptVpcEndpointConnections.html"
  },
  "ec2:AcceptVpcPeeringConnection": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Vpc": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcFlowLog": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcPeeringConnection": {
        "Condition Keys": [
          "ec2:AccepterVpc",
          "ec2:Region",
          "ec2:RequesterVpc",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to accept a VPC peering connection request",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AcceptVpcPeeringConnection.html"
  },
  "ec2:AdvertiseByoipCidr": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to advertise an IP address range that is provisioned for use in AWS through bring your own IP addresses (BYOIP)",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AdvertiseByoipCidr.html"
  },
  "ec2:AllocateAddress": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to allocate an Elastic IP address (EIP) to your account",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AllocateAddress.html"
  },
  "ec2:AllocateHosts": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::DedicatedHost": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to allocate a Dedicated Host to your account",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AllocateHosts.html"
  },
  "ec2:ApplySecurityGroupsToClientVpnTargetNetwork": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::ClientVpnEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::SecurityGroup": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Vpc": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcFlowLog": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcPeeringConnection": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to apply a security group to the association between a Client VPN endpoint and a target network",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ApplySecurityGroupsToClientVpnTargetNetwork.html"
  },
  "ec2:AssignIpv6Addresses": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to assign one or more IPv6 addresses to a network interface",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AssignIpv6Addresses.html"
  },
  "ec2:AssignPrivateIpAddresses": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to assign one or more secondary private IP addresses to a network interface",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AssignPrivateIpAddresses.html"
  },
  "ec2:AssociateAddress": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to associate an Elastic IP address (EIP) with an instance or a network interface",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AssociateAddress.html"
  },
  "ec2:AssociateClientVpnTargetNetwork": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::ClientVpnEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Subnet": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to associate a target network with a Client VPN endpoint",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AssociateClientVpnTargetNetwork.html"
  },
  "ec2:AssociateDhcpOptions": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to associate or disassociate a set of DHCP options with a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AssociateDhcpOptions.html"
  },
  "ec2:AssociateIamInstanceProfile": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": [
          "iam:PassRole"
        ]
      },
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": [
          "iam:PassRole"
        ]
      }
    },
    "Description": "Grants permission to associate an IAM instance profile with a running or stopped instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AssociateIamInstanceProfile.html"
  },
  "ec2:AssociateRouteTable": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to associate a subnet or gateway with a route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AssociateRouteTable.html"
  },
  "ec2:AssociateSubnetCidrBlock": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to associate a CIDR block with a subnet",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AssociateSubnetCidrBlock.html"
  },
  "ec2:AssociateTransitGatewayMulticastDomain": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Subnet": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayMulticastDomain": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to associate an attachment and list of subnets with a transit gateway multicast domain",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AssociateTransitGatewayMulticastDomain.html"
  },
  "ec2:AssociateTransitGatewayRouteTable": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayRouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to associate an attachment with a transit gateway route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AssociateTransitGatewayRouteTable.html"
  },
  "ec2:AssociateVpcCidrBlock": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to associate a CIDR block with a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AssociateVpcCidrBlock.html"
  },
  "ec2:AttachClassicLinkVpc": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::SecurityGroup": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Vpc": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcFlowLog": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcPeeringConnection": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to link an EC2-Classic instance to a ClassicLink-enabled VPC through one or more of the VPC's security groups",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AttachClassicLinkVpc.html"
  },
  "ec2:AttachInternetGateway": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to attach an internet gateway to a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AttachInternetGateway.html"
  },
  "ec2:AttachNetworkInterface": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to attach a network interface to an instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AttachNetworkInterface.html"
  },
  "ec2:AttachVolume": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Volume": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:Encrypted",
          "ec2:ParentSnapshot",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:VolumeIops",
          "ec2:VolumeSize",
          "ec2:VolumeType"
        ],
        "Dependant Actions": []
      },
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to attach an EBS volume to a running or stopped instance and expose it to the instance with the specified device name",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AttachVolume.html"
  },
  "ec2:AttachVpnGateway": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to attach a virtual private gateway to a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AttachVpnGateway.html"
  },
  "ec2:AuthorizeClientVpnIngress": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::ClientVpnEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to add an inbound authorization rule to a Client VPN endpoint",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AuthorizeClientVpnIngress.html"
  },
  "ec2:AuthorizeSecurityGroupEgress": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::SecurityGroup": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to add one or more outbound rules to a VPC security group",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AuthorizeSecurityGroupEgress.html"
  },
  "ec2:AuthorizeSecurityGroupIngress": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::SecurityGroup": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to add one or more inbound rules to a security group",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AuthorizeSecurityGroupIngress.html"
  },
  "ec2:BundleInstance": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to bundle an instance store-backed Windows instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_BundleInstance.html"
  },
  "ec2:CancelBundleTask": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to cancel a bundling operation",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CancelBundleTask.html"
  },
  "ec2:CancelCapacityReservation": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::CapacityReservation": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to cancel a Capacity Reservation and release the reserved capacity",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CancelCapacityReservation.html"
  },
  "ec2:CancelConversionTask": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to cancel an active conversion task",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CancelConversionTask.html"
  },
  "ec2:CancelExportTask": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to cancel an active export task",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CancelExportTask.html"
  },
  "ec2:CancelImportTask": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to cancel an in-process import virtual machine or import snapshot task",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CancelImportTask.html"
  },
  "ec2:CancelReservedInstancesListing": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to cancel a Reserved Instance listing on the Reserved Instance Marketplace",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CancelReservedInstancesListing.html"
  },
  "ec2:CancelSpotFleetRequests": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to cancel one or more Spot Fleet requests",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CancelSpotFleetRequests.html"
  },
  "ec2:CancelSpotInstanceRequests": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to cancel one or more Spot Instance requests",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CancelSpotInstanceRequests.html"
  },
  "ec2:ConfirmProductInstance": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to determine whether an owned product code is associated with an instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ConfirmProductInstance.html"
  },
  "ec2:CopyFpgaImage": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to copy a source Amazon FPGA image (AFI) to the current Region",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CopyFpgaImage.html"
  },
  "ec2:CopyImage": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to copy an Amazon Machine Image (AMI) from a source Region to the current Region",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CopyImage.html"
  },
  "ec2:CopySnapshot": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Snapshot": {
        "Condition Keys": [
          "aws:TagKeys",
          "aws:RequestTag/${TagKey}",
          "ec2:Region"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to copy a point-in-time snapshot of an EBS volume and store it in Amazon S3",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CopySnapshot.html"
  },
  "ec2:CreateCapacityReservation": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a Capacity Reservation",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateCapacityReservation.html"
  },
  "ec2:CreateClientVpnEndpoint": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::ClientVpnEndpoint": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a Client VPN endpoint",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateClientVpnEndpoint.html"
  },
  "ec2:CreateClientVpnRoute": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::ClientVpnEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Subnet": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to add a network route to a Client VPN endpoint's route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateClientVpnRoute.html"
  },
  "ec2:CreateCustomerGateway": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a customer gateway, which provides information to AWS about your customer gateway device",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateCustomerGateway.html"
  },
  "ec2:CreateDefaultSubnet": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a default subnet in a specified Availability Zone in a default VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateDefaultSubnet.html"
  },
  "ec2:CreateDefaultVpc": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a default VPC with a default subnet in each Availability Zone",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateDefaultVpc.html"
  },
  "ec2:CreateDhcpOptions": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a set of DHCP options for a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateDhcpOptions.html"
  },
  "ec2:CreateEgressOnlyInternetGateway": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create an egress-only internet gateway for a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateEgressOnlyInternetGateway.html"
  },
  "ec2:CreateFleet": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to launch an EC2 Fleet",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateFleet.html"
  },
  "ec2:CreateFlowLogs": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::NetworkInterface": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:Subnet",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Subnet": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Vpc": {
        "Condition Keys": [
          "ec2:Region"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcFlowLog": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region"
        ],
        "Dependant Actions": [
          "iam:PassRole"
        ]
      }
    },
    "Description": "Grants permission to create one or more flow logs to capture IP traffic for a network interface",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateFlowLogs.html"
  },
  "ec2:CreateFpgaImage": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create an Amazon FPGA Image (AFI) from a design checkpoint (DCP)",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateFpgaImage.html"
  },
  "ec2:CreateImage": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create an Amazon EBS-backed AMI from a stopped or running Amazon EBS-backed instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateImage.html"
  },
  "ec2:CreateInstanceExportTask": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to export a running or stopped instance to an Amazon S3 bucket",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateInstanceExportTask.html"
  },
  "ec2:CreateInternetGateway": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create an internet gateway for a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateInternetGateway.html"
  },
  "ec2:CreateKeyPair": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a 2048-bit RSA key pair",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateKeyPair.html"
  },
  "ec2:CreateLaunchTemplate": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a launch template",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateLaunchTemplate.html"
  },
  "ec2:CreateLaunchTemplateVersion": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::LaunchTemplate": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a new version of a launch template",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateLaunchTemplateVersion.html"
  },
  "ec2:CreateLocalGatewayRoute": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::LocalGatewayRouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGatewayRouteTableVirtualInterfaceGroupAssociation": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGatewayRouteTableVpcAssociation": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGatewayVirtualInterfaceGroup": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a static route for a local gateway route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateLocalGatewayRoute.html"
  },
  "ec2:CreateLocalGatewayRouteTableVpcAssociation": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::LocalGatewayRouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGatewayRouteTableVirtualInterfaceGroupAssociation": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGatewayRouteTableVpcAssociation": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Vpc": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcFlowLog": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcPeeringConnection": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to associate a VPC with a local gateway route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateLocalGatewayRouteTableVpcAssociation.html"
  },
  "ec2:CreateNatGateway": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a NAT gateway in a subnet",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateNatGateway.html"
  },
  "ec2:CreateNetworkAcl": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a network ACL in a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateNetworkAcl.html"
  },
  "ec2:CreateNetworkAclEntry": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a numbered entry (a rule) in a network ACL",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateNetworkAclEntry.html"
  },
  "ec2:CreateNetworkInterface": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a network interface in a subnet",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateNetworkInterface.html"
  },
  "ec2:CreateNetworkInterfacePermission": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Ec2::NetworkInterface": {
        "Condition Keys": [
          "ec2:AuthorizedUser",
          "ec2:AvailabilityZone",
          "ec2:Permission",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Subnet",
          "ec2:Vpc",
          "ec2:AuthorizedService"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a permission for an AWS-authorized user to perform certain operations on a network interface",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateNetworkInterfacePermission.html"
  },
  "ec2:CreatePlacementGroup": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a placement group",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreatePlacementGroup.html"
  },
  "ec2:CreateReservedInstancesListing": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a listing for Standard Reserved Instances to be sold in the Reserved Instance Marketplace",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateReservedInstancesListing.html"
  },
  "ec2:CreateRoute": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::RouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a route in a VPC route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateRoute.html"
  },
  "ec2:CreateRouteTable": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a route table for a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateRouteTable.html"
  },
  "ec2:CreateSecurityGroup": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a security group",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateSecurityGroup.html"
  },
  "ec2:CreateSnapshot": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Snapshot": {
        "Condition Keys": [
          "aws:TagKeys",
          "aws:RequestTag/${TagKey}",
          "ec2:ParentVolume",
          "ec2:Region"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Volume": {
        "Condition Keys": [
          "ec2:Encrypted",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:VolumeIops",
          "ec2:VolumeSize",
          "ec2:VolumeType"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a snapshot of an EBS volume and store it in Amazon S3",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateSnapshot.html"
  },
  "ec2:CreateSnapshots": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Snapshot": {
        "Condition Keys": [
          "aws:TagKeys",
          "aws:RequestTag/${TagKey}",
          "ec2:ParentVolume",
          "ec2:Region"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Volume": {
        "Condition Keys": [
          "ec2:Encrypted",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:VolumeIops",
          "ec2:VolumeSize",
          "ec2:VolumeType"
        ],
        "Dependant Actions": []
      },
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create crash-consistent snapshots of multiple EBS volumes and store them in Amazon S3",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateSnapshots.html"
  },
  "ec2:CreateSpotDatafeedSubscription": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a data feed for Spot Instances to view Spot Instance usage logs",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateSpotDatafeedSubscription.html"
  },
  "ec2:CreateSubnet": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a subnet in a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateSubnet.html"
  },
  "ec2:CreateTags": {
    "Access": "Tagging",
    "Affects": {
      "AWS::Ec2::CapacityReservation": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::ClientVpnEndpoint": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::DedicatedHost": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Ec2::DhcpOptions": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::FpgaImage": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Owner",
          "ec2:Public",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Image": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:ImageType",
          "ec2:Owner",
          "ec2:Public",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::InternetGateway": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGateway": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGatewayRouteTable": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGatewayRouteTableVirtualInterfaceGroupAssociation": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGatewayRouteTableVpcAssociation": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGatewayVirtualInterface": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGatewayVirtualInterfaceGroup": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Ec2::NetworkAcl": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::NetworkInterface": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:AvailabilityZone",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Subnet",
          "ec2:Vpc",
          "ec2:AssociatePublicIpAddress"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::ReservedInstances": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:AvailabilityZone",
          "ec2:InstanceType",
          "ec2:Region",
          "ec2:ReservedInstancesOfferingType",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::RouteTable": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::SecurityGroup": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Snapshot": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Owner",
          "ec2:ParentVolume",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:SnapshotTime",
          "ec2:VolumeSize"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::SpotInstanceRequest": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Subnet": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:AvailabilityZone",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TrafficMirrorFilter": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TrafficMirrorSession": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TrafficMirrorTarget": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGateway": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayMulticastDomain": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayRouteTable": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Volume": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:AvailabilityZone",
          "ec2:Encrypted",
          "ec2:ParentSnapshot",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:VolumeIops",
          "ec2:VolumeSize",
          "ec2:VolumeType"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Vpc": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpoint": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcFlowLog": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpnConnection": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpnGateway": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to add or overwrite one or more tags for Amazon EC2 resources",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateTags.html"
  },
  "ec2:CreateTrafficMirrorFilter": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TrafficMirrorFilter": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TrafficMirrorFilterRule": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a traffic mirror filter",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateTrafficMirrorFilter.html"
  },
  "ec2:CreateTrafficMirrorFilterRule": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TrafficMirrorFilter": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TrafficMirrorFilterRule": {
        "Condition Keys": [
          "ec2:Region"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a traffic mirror filter rule",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateTrafficMirrorFilterRule.html"
  },
  "ec2:CreateTrafficMirrorSession": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::NetworkInterface": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TrafficMirrorFilter": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TrafficMirrorFilterRule": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TrafficMirrorSession": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TrafficMirrorTarget": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a traffic mirror session",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateTrafficMirrorSession.html"
  },
  "ec2:CreateTrafficMirrorTarget": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::NetworkInterface": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TrafficMirrorTarget": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a traffic mirror target",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateTrafficMirrorTarget.html"
  },
  "ec2:CreateTransitGateway": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGateway": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayMulticastDomain": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayRouteTable": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a transit gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateTransitGateway.html"
  },
  "ec2:CreateTransitGatewayMulticastDomain": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGateway": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayMulticastDomain": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayRouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a multicast domain for a transit gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateTransitGatewayMulticastDomain.html"
  },
  "ec2:CreateTransitGatewayPeeringAttachment": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGateway": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayMulticastDomain": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayRouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to request a transit gateway peering attachment between a requester and accepter transit gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateTransitGatewayPeeringAttachment.html"
  },
  "ec2:CreateTransitGatewayRoute": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayRouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a static route for a transit gateway route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateTransitGatewayRoute.html"
  },
  "ec2:CreateTransitGatewayRouteTable": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGateway": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayMulticastDomain": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayRouteTable": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a route table for a transit gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateTransitGatewayRouteTable.html"
  },
  "ec2:CreateTransitGatewayVpcAttachment": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Subnet": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGateway": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayMulticastDomain": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayRouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Vpc": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcFlowLog": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcPeeringConnection": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to attach a VPC to a transit gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateTransitGatewayVpcAttachment.html"
  },
  "ec2:CreateVolume": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Volume": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:AvailabilityZone",
          "ec2:Encrypted",
          "ec2:ParentSnapshot",
          "ec2:Region",
          "ec2:VolumeIops",
          "ec2:VolumeSize",
          "ec2:VolumeType"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create an EBS volume",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateVolume.html"
  },
  "ec2:CreateVpc": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a VPC with a specified CIDR block",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateVpc.html"
  },
  "ec2:CreateVpcEndpoint": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::RouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::SecurityGroup": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Subnet": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Vpc": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": [
          "route53:AssociateVPCWithHostedZone"
        ]
      },
      "AWS::Ec2::VpcEndpoint": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:VpceServiceName",
          "ec2:VpceServiceOwner"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:VpceServiceName",
          "ec2:VpceServiceOwner"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcFlowLog": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": [
          "route53:AssociateVPCWithHostedZone"
        ]
      },
      "AWS::Ec2::VpcPeeringConnection": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": [
          "route53:AssociateVPCWithHostedZone"
        ]
      }
    },
    "Description": "Grants permission to create a VPC endpoint for an AWS service",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateVpcEndpoint.html"
  },
  "ec2:CreateVpcEndpointConnectionNotification": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a connection notification for a VPC endpoint or VPC endpoint service",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateVpcEndpointConnectionNotification.html"
  },
  "ec2:CreateVpcEndpointServiceConfiguration": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:VpceServicePrivateDnsName"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a VPC endpoint service configuration to which service consumers (AWS accounts, IAM users, and IAM roles) can connect",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateVpcEndpointServiceConfiguration.html"
  },
  "ec2:CreateVpcPeeringConnection": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Vpc": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcFlowLog": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcPeeringConnection": {
        "Condition Keys": [
          "ec2:AccepterVpc",
          "ec2:Region",
          "ec2:RequesterVpc"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to request a VPC peering connection between two VPCs",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateVpcPeeringConnection.html"
  },
  "ec2:CreateVpnConnection": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::VpnConnection": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:AuthenticationType",
          "ec2:DPDTimeoutSeconds",
          "ec2:GatewayType",
          "ec2:IKEVersions",
          "ec2:InsideTunnelCidr",
          "ec2:Phase1DHGroupNumbers",
          "ec2:Phase2DHGroupNumbers",
          "ec2:Phase1EncryptionAlgorithms",
          "ec2:Phase2EncryptionAlgorithms",
          "ec2:Phase1IntegrityAlgorithms",
          "ec2:Phase2IntegrityAlgorithms",
          "ec2:Phase1LifetimeSeconds",
          "ec2:Phase2LifetimeSeconds",
          "ec2:PresharedKeys",
          "ec2:RekeyFuzzPercentage",
          "ec2:RekeyMarginTimeSeconds",
          "ec2:RoutingType"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a VPN connection between a virtual private gateway or transit gateway and a customer gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateVpnConnection.html"
  },
  "ec2:CreateVpnConnectionRoute": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a static route for a VPN connection between a virtual private gateway and a customer gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateVpnConnectionRoute.html"
  },
  "ec2:CreateVpnGateway": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a virtual private gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateVpnGateway.html"
  },
  "ec2:DeleteClientVpnEndpoint": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::ClientVpnEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a Client VPN endpoint",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteClientVpnEndpoint.html"
  },
  "ec2:DeleteClientVpnRoute": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::ClientVpnEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Subnet": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a route from a Client VPN endpoint",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteClientVpnRoute.html"
  },
  "ec2:DeleteCustomerGateway": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::CustomerGateway": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a customer gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteCustomerGateway.html"
  },
  "ec2:DeleteDhcpOptions": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::DhcpOptions": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a set of DHCP options",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteDhcpOptions.html"
  },
  "ec2:DeleteEgressOnlyInternetGateway": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to delete an egress-only internet gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteEgressOnlyInternetGateway.html"
  },
  "ec2:DeleteFleets": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to delete one or more EC2 Fleets",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteFleets.html"
  },
  "ec2:DeleteFlowLogs": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to delete one or more flow logs",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteFlowLogs.html"
  },
  "ec2:DeleteFpgaImage": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to delete an Amazon FPGA Image (AFI)",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteFpgaImage.html"
  },
  "ec2:DeleteInternetGateway": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::InternetGateway": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete an internet gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteInternetGateway.html"
  },
  "ec2:DeleteKeyPair": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to delete a key pair by removing the public key from Amazon EC2",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteKeyPair.html"
  },
  "ec2:DeleteLaunchTemplate": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::LaunchTemplate": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a launch template and its associated versions",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteLaunchTemplate.html"
  },
  "ec2:DeleteLaunchTemplateVersions": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::LaunchTemplate": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete one or more versions of a launch template",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteLaunchTemplateVersions.html"
  },
  "ec2:DeleteLocalGatewayRoute": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::LocalGatewayRouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGatewayRouteTableVirtualInterfaceGroupAssociation": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGatewayRouteTableVpcAssociation": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a route from a local gateway route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteLocalGatewayRoute.html"
  },
  "ec2:DeleteLocalGatewayRouteTableVpcAssociation": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::LocalGatewayRouteTableVpcAssociation": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete an association between a VPC and local gateway route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteLocalGatewayRouteTableVpcAssociation.html"
  },
  "ec2:DeleteNatGateway": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to delete a NAT gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteNatGateway.html"
  },
  "ec2:DeleteNetworkAcl": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::NetworkAcl": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a network ACL",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteNetworkAcl.html"
  },
  "ec2:DeleteNetworkAclEntry": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::NetworkAcl": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete an inbound or outbound entry (rule) from a network ACL",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteNetworkAclEntry.html"
  },
  "ec2:DeleteNetworkInterface": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to delete a detached network interface",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteNetworkInterface.html"
  },
  "ec2:DeleteNetworkInterfacePermission": {
    "Access": "Permissions Management",
    "Affects": {},
    "Description": "Grants permission to delete a permission that is associated with a network interface",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteNetworkInterfacePermission.html"
  },
  "ec2:DeletePlacementGroup": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to delete a placement group",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeletePlacementGroup.html"
  },
  "ec2:DeleteRoute": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::RouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a route from a route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteRoute.html"
  },
  "ec2:DeleteRouteTable": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::RouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteRouteTable.html"
  },
  "ec2:DeleteSecurityGroup": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::SecurityGroup": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a security group",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteSecurityGroup.html"
  },
  "ec2:DeleteSnapshot": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Snapshot": {
        "Condition Keys": [
          "ec2:Owner",
          "ec2:ParentVolume",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:SnapshotTime",
          "ec2:VolumeSize"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a snapshot of an EBS volume",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteSnapshot.html"
  },
  "ec2:DeleteSpotDatafeedSubscription": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to delete a data feed for Spot Instances",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteSpotDatafeedSubscription.html"
  },
  "ec2:DeleteSubnet": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to delete a subnet",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteSubnet.html"
  },
  "ec2:DeleteTags": {
    "Access": "Tagging",
    "Affects": {
      "AWS::Ec2::CapacityReservation": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::ClientVpnEndpoint": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::DedicatedHost": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Ec2::DhcpOptions": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::FpgaImage": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Image": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::InternetGateway": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGateway": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGatewayRouteTable": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGatewayRouteTableVirtualInterfaceGroupAssociation": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGatewayRouteTableVpcAssociation": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGatewayVirtualInterface": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Ec2::LocalGatewayVirtualInterfaceGroup": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Ec2::NetworkAcl": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::NetworkInterface": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::ReservedInstances": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::RouteTable": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::SecurityGroup": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Snapshot": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::SpotInstanceRequest": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Subnet": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGateway": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayMulticastDomain": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayRouteTable": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Volume": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Vpc": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpoint": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcFlowLog": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpnConnection": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpnGateway": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete one or more tags from Amazon EC2 resources",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteTags.html"
  },
  "ec2:DeleteTrafficMirrorFilter": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TrafficMirrorFilter": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TrafficMirrorFilterRule": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a traffic mirror filter",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteTrafficMirrorFilter.html"
  },
  "ec2:DeleteTrafficMirrorFilterRule": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TrafficMirrorFilter": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TrafficMirrorFilterRule": {
        "Condition Keys": [
          "ec2:Region"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a traffic mirror filter rule",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteTrafficMirrorFilterRule.html"
  },
  "ec2:DeleteTrafficMirrorSession": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TrafficMirrorSession": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a traffic mirror session",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteTrafficMirrorSession.html"
  },
  "ec2:DeleteTrafficMirrorTarget": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TrafficMirrorTarget": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a traffic mirror target",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteTrafficMirrorTarget.html"
  },
  "ec2:DeleteTransitGateway": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGateway": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayMulticastDomain": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayRouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a transit gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteTransitGateway.html"
  },
  "ec2:DeleteTransitGatewayMulticastDomain": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGatewayMulticastDomain": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permissions to delete a transit gateway multicast domain",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteTransitGatewayMulticastDomain.html"
  },
  "ec2:DeleteTransitGatewayPeeringAttachment": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a peering attachment from a transit gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteTransitGatewayPeeringAttachment.html"
  },
  "ec2:DeleteTransitGatewayRoute": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGatewayRouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a route from a transit gateway route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteTransitGatewayRoute.html"
  },
  "ec2:DeleteTransitGatewayRouteTable": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGatewayRouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a transit gateway route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteTransitGatewayRouteTable.html"
  },
  "ec2:DeleteTransitGatewayVpcAttachment": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a VPC attachment from a transit gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteTransitGatewayVpcAttachment.html"
  },
  "ec2:DeleteVolume": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Volume": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:Encrypted",
          "ec2:ParentSnapshot",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:VolumeIops",
          "ec2:VolumeSize",
          "ec2:VolumeType"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete an EBS volume",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteVolume.html"
  },
  "ec2:DeleteVpc": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to delete a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteVpc.html"
  },
  "ec2:DeleteVpcEndpointConnectionNotifications": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to delete one or more VPC endpoint connection notifications",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteVpcEndpointConnectionNotifications.html"
  },
  "ec2:DeleteVpcEndpointServiceConfigurations": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete one or more VPC endpoint service configurations",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteVpcEndpointServiceConfigurations.html"
  },
  "ec2:DeleteVpcEndpoints": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::VpcEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete one or more VPC endpoints",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteVpcEndpoints.html"
  },
  "ec2:DeleteVpcPeeringConnection": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::VpcPeeringConnection": {
        "Condition Keys": [
          "ec2:AccepterVpc",
          "ec2:Region",
          "ec2:RequesterVpc",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a VPC peering connection",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteVpcPeeringConnection.html"
  },
  "ec2:DeleteVpnConnection": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to delete a VPN connection",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteVpnConnection.html"
  },
  "ec2:DeleteVpnConnectionRoute": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to delete a static route for a VPN connection between a virtual private gateway and a customer gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteVpnConnectionRoute.html"
  },
  "ec2:DeleteVpnGateway": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to delete a virtual private gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteVpnGateway.html"
  },
  "ec2:DeprovisionByoipCidr": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to release an IP address range that was provisioned through bring your own IP addresses (BYOIP), and to delete the corresponding address pool",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeprovisionByoipCidr.html"
  },
  "ec2:DeregisterImage": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to deregister an Amazon Machine Image (AMI)",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeregisterImage.html"
  },
  "ec2:DeregisterTransitGatewayMulticastGroupMembers": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::NetworkInterface": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayMulticastDomain": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to deregister one or more network interface members from a group IP address in a transit gateway multicast domain",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeregisterTransitGatewayMulticastGroupMembers.html"
  },
  "ec2:DeregisterTransitGatewayMulticastGroupSources": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::NetworkInterface": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayMulticastDomain": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to deregister one or more network interface sources from a group IP address in a transit gateway multicast domain",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeregisterTransitGatewayMulticastGroupSources.html"
  },
  "ec2:DescribeAccountAttributes": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the attributes of the AWS account",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeAccountAttributes.html"
  },
  "ec2:DescribeAddresses": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more Elastic IP addresses",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeAddresses.html"
  },
  "ec2:DescribeAggregateIdFormat": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the longer ID format settings for all resource types",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeAggregateIdFormat.html"
  },
  "ec2:DescribeAvailabilityZones": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more of the Availability Zones that are available to you",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeAvailabilityZones.html"
  },
  "ec2:DescribeBundleTasks": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more bundling tasks",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeBundleTasks.html"
  },
  "ec2:DescribeByoipCidrs": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the IP address ranges that were provisioned through bring your own IP addresses (BYOIP)",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeByoipCidrs.html"
  },
  "ec2:DescribeCapacityReservations": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more Capacity Reservations",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeCapacityReservations.html"
  },
  "ec2:DescribeClassicLinkInstances": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more linked EC2-Classic instances",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeClassicLinkInstances.html"
  },
  "ec2:DescribeClientVpnAuthorizationRules": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the authorization rules for a Client VPN endpoint",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeClientVpnAuthorizationRules.html"
  },
  "ec2:DescribeClientVpnConnections": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe active client connections and connections that have been terminated within the last 60 minutes for a Client VPN endpoint",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeClientVpnConnections.html"
  },
  "ec2:DescribeClientVpnEndpoints": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more Client VPN endpoints",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeClientVpnEndpoints.html"
  },
  "ec2:DescribeClientVpnRoutes": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the routes for a Client VPN endpoint",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeClientVpnRoutes.html"
  },
  "ec2:DescribeClientVpnTargetNetworks": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the target networks that are associated with a Client VPN endpoint",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeClientVpnTargetNetworks.html"
  },
  "ec2:DescribeConversionTasks": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more conversion tasks",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeConversionTasks.html"
  },
  "ec2:DescribeCustomerGateways": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more customer gateways",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeCustomerGateways.html"
  },
  "ec2:DescribeDhcpOptions": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more DHCP options sets",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeDhcpOptions.html"
  },
  "ec2:DescribeEgressOnlyInternetGateways": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more egress-only internet gateways",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeEgressOnlyInternetGateways.html"
  },
  "ec2:DescribeElasticGpus": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to describe an Elastic Graphics accelerator that is associated with an instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeElasticGpus.html"
  },
  "ec2:DescribeExportImageTasks": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more export image tasks",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeExportImageTasks.html"
  },
  "ec2:DescribeExportTasks": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more export instance tasks",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeExportTasks.html"
  },
  "ec2:DescribeFastSnapshotRestores": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to describe the state of fast snapshot restores for snapshots",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeFastSnapshotRestores.html"
  },
  "ec2:DescribeFleetHistory": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the events for an EC2 Fleet during a specified time",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeFleetHistory.html"
  },
  "ec2:DescribeFleetInstances": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the running instances for an EC2 Fleet",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeFleetInstances.html"
  },
  "ec2:DescribeFleets": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more EC2 Fleets",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeFleets.html"
  },
  "ec2:DescribeFlowLogs": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more flow logs",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeFlowLogs.html"
  },
  "ec2:DescribeFpgaImageAttribute": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the attributes of an Amazon FPGA Image (AFI)",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeFpgaImageAttribute.html"
  },
  "ec2:DescribeFpgaImages": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more Amazon FPGA Images (AFIs)",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeFpgaImages.html"
  },
  "ec2:DescribeHostReservationOfferings": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the Dedicated Host Reservations that are available to purchase",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeHostReservationOfferings.html"
  },
  "ec2:DescribeHostReservations": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the Dedicated Host Reservations that are associated with Dedicated Hosts in the AWS account",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeHostReservations.html"
  },
  "ec2:DescribeHosts": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more Dedicated Hosts",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeHosts.html"
  },
  "ec2:DescribeIamInstanceProfileAssociations": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the IAM instance profile associations",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeIamInstanceProfileAssociations.html"
  },
  "ec2:DescribeIdFormat": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the ID format settings for resources",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeIdFormat.html"
  },
  "ec2:DescribeIdentityIdFormat": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the ID format settings for resources for an IAM user, IAM role, or root user",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeIdentityIdFormat.html"
  },
  "ec2:DescribeImageAttribute": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe an attribute of an Amazon Machine Image (AMI)",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeImageAttribute.html"
  },
  "ec2:DescribeImages": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more images (AMIs, AKIs, and ARIs)",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeImages.html"
  },
  "ec2:DescribeImportImageTasks": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe import virtual machine or import snapshot tasks",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeImportImageTasks.html"
  },
  "ec2:DescribeImportSnapshotTasks": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe import snapshot tasks",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeImportSnapshotTasks.html"
  },
  "ec2:DescribeInstanceAttribute": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the attributes of an instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeInstanceAttribute.html"
  },
  "ec2:DescribeInstanceCreditSpecifications": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the credit option for CPU usage of one or more burstable performance instances",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeInstanceCreditSpecifications.html"
  },
  "ec2:DescribeInstanceStatus": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the status of one or more instances",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeInstanceStatus.html"
  },
  "ec2:DescribeInstanceTypes": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe all instance types that are offered in an AWS Region",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeInstanceTypes.html"
  },
  "ec2:DescribeInstances": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more instances",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeInstances.html"
  },
  "ec2:DescribeInternetGateways": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more internet gateways",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeInternetGateways.html"
  },
  "ec2:DescribeKeyPairs": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more key pairs",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeKeyPairs.html"
  },
  "ec2:DescribeLaunchTemplateVersions": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more launch template versions",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeLaunchTemplateVersions.html"
  },
  "ec2:DescribeLaunchTemplates": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more launch templates",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeLaunchTemplates.html"
  },
  "ec2:DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociations": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the associations between virtual interface groups and local gateway route tables",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociations.html"
  },
  "ec2:DescribeLocalGatewayRouteTableVpcAssociations": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe an association between VPCs and local gateway route tables",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeLocalGatewayRouteTableVpcAssociations.html"
  },
  "ec2:DescribeLocalGatewayRouteTables": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more local gateway route tables",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeLocalGatewayRouteTables.html"
  },
  "ec2:DescribeLocalGatewayVirtualInterfaceGroups": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe local gateway virtual interface groups",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeLocalGatewayVirtualInterfaceGroups.html"
  },
  "ec2:DescribeLocalGatewayVirtualInterfaces": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe local gateway virtual interfaces",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeLocalGatewayVirtualInterfaces.html"
  },
  "ec2:DescribeLocalGateways": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more local gateways",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeLocalGateways.html"
  },
  "ec2:DescribeMovingAddresses": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe Elastic IP addresses that are being moved to the EC2-VPC platform",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeMovingAddresses.html"
  },
  "ec2:DescribeNatGateways": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more NAT gateways",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeNatGateways.html"
  },
  "ec2:DescribeNetworkAcls": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more network ACLs",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeNetworkAcls.html"
  },
  "ec2:DescribeNetworkInterfaceAttribute": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe a network interface attribute",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeNetworkInterfaceAttribute.html"
  },
  "ec2:DescribeNetworkInterfacePermissions": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the permissions that are associated with a network interface",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeNetworkInterfacePermissions.html"
  },
  "ec2:DescribeNetworkInterfaces": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more network interfaces",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeNetworkInterfaces.html"
  },
  "ec2:DescribePlacementGroups": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more placement groups",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribePlacementGroups.html"
  },
  "ec2:DescribePrefixLists": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe available AWS services in a prefix list format",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribePrefixLists.html"
  },
  "ec2:DescribePrincipalIdFormat": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the ID format settings for the root user and all IAM roles and IAM users that have explicitly specified a longer ID (17-character ID) preference",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribePrincipalIdFormat.html"
  },
  "ec2:DescribePublicIpv4Pools": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more IPv4 address pools",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribePublicIpv4Pools.html"
  },
  "ec2:DescribeRegions": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more AWS Regions that are currently available in your account",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeRegions.html"
  },
  "ec2:DescribeReservedInstances": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more purchased Reserved Instances in your account",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeReservedInstances.html"
  },
  "ec2:DescribeReservedInstancesListings": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe your account's Reserved Instance listings in the Reserved Instance Marketplace",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeReservedInstancesListings.html"
  },
  "ec2:DescribeReservedInstancesModifications": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the modifications made to one or more Reserved Instances",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeReservedInstancesModifications.html"
  },
  "ec2:DescribeReservedInstancesOfferings": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the Reserved Instance offerings that are available for purchase",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeReservedInstancesOfferings.html"
  },
  "ec2:DescribeRouteTables": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more route tables",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeRouteTables.html"
  },
  "ec2:DescribeScheduledInstanceAvailability": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to find available schedules for Scheduled Instances",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeScheduledInstanceAvailability.html"
  },
  "ec2:DescribeScheduledInstances": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to describe one or more Scheduled Instances in your account",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeScheduledInstances.html"
  },
  "ec2:DescribeSecurityGroupReferences": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the VPCs on the other side of a VPC peering connection that are referencing specified VPC security groups",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeSecurityGroupReferences.html"
  },
  "ec2:DescribeSecurityGroups": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more security groups",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeSecurityGroups.html"
  },
  "ec2:DescribeSnapshotAttribute": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe an attribute of a snapshot",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeSnapshotAttribute.html"
  },
  "ec2:DescribeSnapshots": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more EBS snapshots",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeSnapshots.html"
  },
  "ec2:DescribeSpotDatafeedSubscription": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the data feed for Spot Instances",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeSpotDatafeedSubscription.html"
  },
  "ec2:DescribeSpotFleetInstances": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the running instances for a Spot Fleet",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeSpotFleetInstances.html"
  },
  "ec2:DescribeSpotFleetRequestHistory": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the events for a Spot Fleet request during a specified time",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeSpotFleetRequestHistory.html"
  },
  "ec2:DescribeSpotFleetRequests": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more Spot Fleet requests",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeSpotFleetRequests.html"
  },
  "ec2:DescribeSpotInstanceRequests": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more Spot Instance requests",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeSpotInstanceRequests.html"
  },
  "ec2:DescribeSpotPriceHistory": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the Spot Instance price history",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeSpotPriceHistory.html"
  },
  "ec2:DescribeStaleSecurityGroups": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the stale security group rules for security groups in a specified VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeStaleSecurityGroups.html"
  },
  "ec2:DescribeSubnets": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more subnets",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeSubnets.html"
  },
  "ec2:DescribeTags": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to describe one or more tags for an Amazon EC2 resource",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeTags.html"
  },
  "ec2:DescribeTrafficMirrorFilters": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more traffic mirror filters",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeTrafficMirrorFilters.html"
  },
  "ec2:DescribeTrafficMirrorSessions": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more traffic mirror sessions",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeTrafficMirrorSessions.html"
  },
  "ec2:DescribeTrafficMirrorTargets": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more traffic mirror targets",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeTrafficMirrorTargets.html"
  },
  "ec2:DescribeTransitGatewayAttachments": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more attachments between resources and transit gateways",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeTransitGatewayAttachments.html"
  },
  "ec2:DescribeTransitGatewayMulticastDomains": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more transit gateway multicast domains",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeTransitGatewayMulticastDomains.html"
  },
  "ec2:DescribeTransitGatewayPeeringAttachments": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more transit gateway peering attachments",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeTransitGatewayPeeringAttachments.html"
  },
  "ec2:DescribeTransitGatewayRouteTables": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more transit gateway route tables",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeTransitGatewayRouteTables.html"
  },
  "ec2:DescribeTransitGatewayVpcAttachments": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more VPC attachments on a transit gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeTransitGatewayVpcAttachments.html"
  },
  "ec2:DescribeTransitGateways": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more transit gateways",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeTransitGateways.html"
  },
  "ec2:DescribeVolumeAttribute": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe an attribute of an EBS volume",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVolumeAttribute.html"
  },
  "ec2:DescribeVolumeStatus": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the status of one or more EBS volumes",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVolumeStatus.html"
  },
  "ec2:DescribeVolumes": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more EBS volumes",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVolumes.html"
  },
  "ec2:DescribeVolumesModifications": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to describe the current modification status of one or more EBS volumes",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVolumesModifications.html"
  },
  "ec2:DescribeVpcAttribute": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe an attribute of a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcAttribute.html"
  },
  "ec2:DescribeVpcClassicLink": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the ClassicLink status of one or more VPCs",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcClassicLink.html"
  },
  "ec2:DescribeVpcClassicLinkDnsSupport": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the ClassicLink DNS support status of one or more VPCs",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcClassicLinkDnsSupport.html"
  },
  "ec2:DescribeVpcEndpointConnectionNotifications": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the connection notifications for VPC endpoints and VPC endpoint services",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcEndpointConnectionNotifications.html"
  },
  "ec2:DescribeVpcEndpointConnections": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the VPC endpoint connections to your VPC endpoint services",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcEndpointConnections.html"
  },
  "ec2:DescribeVpcEndpointServiceConfigurations": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe VPC endpoint service configurations (your services)",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcEndpointServiceConfigurations.html"
  },
  "ec2:DescribeVpcEndpointServicePermissions": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe the principals (service consumers) that are permitted to discover your VPC endpoint service",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcEndpointServicePermissions.html"
  },
  "ec2:DescribeVpcEndpointServices": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe all supported AWS services that can be specified when creating a VPC endpoint",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcEndpointServices.html"
  },
  "ec2:DescribeVpcEndpoints": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more VPC endpoints",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcEndpoints.html"
  },
  "ec2:DescribeVpcPeeringConnections": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more VPC peering connections",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcPeeringConnections.html"
  },
  "ec2:DescribeVpcs": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more VPCs",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcs.html"
  },
  "ec2:DescribeVpnConnections": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to describe one or more VPN connections",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpnConnections.html"
  },
  "ec2:DescribeVpnGateways": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to describe one or more virtual private gateways",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpnGateways.html"
  },
  "ec2:DetachClassicLinkVpc": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Vpc": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcFlowLog": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcPeeringConnection": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to unlink (detach) a linked EC2-Classic instance from a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DetachClassicLinkVpc.html"
  },
  "ec2:DetachInternetGateway": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to detach an internet gateway from a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DetachInternetGateway.html"
  },
  "ec2:DetachNetworkInterface": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to detach a network interface from an instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DetachNetworkInterface.html"
  },
  "ec2:DetachVolume": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Volume": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:Encrypted",
          "ec2:ParentSnapshot",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:VolumeIops",
          "ec2:VolumeSize",
          "ec2:VolumeType"
        ],
        "Dependant Actions": []
      },
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to detach an EBS volume from an instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DetachVolume.html"
  },
  "ec2:DetachVpnGateway": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to detach a virtual private gateway from a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DetachVpnGateway.html"
  },
  "ec2:DisableEbsEncryptionByDefault": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to disable EBS encryption by default for your account",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DisableEbsEncryptionByDefault.html"
  },
  "ec2:DisableFastSnapshotRestores": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Snapshot": {
        "Condition Keys": [
          "ec2:Owner",
          "ec2:ParentVolume",
          "ec2:Region",
          "ec2:AvailabilityZone",
          "ec2:SnapshotTime",
          "ec2:Encrypted",
          "ec2:VolumeSize",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to disable fast snapshot restores for one or more snapshots in specified Availability Zones",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DisableFastSnapshotRestores.html"
  },
  "ec2:DisableTransitGatewayRouteTablePropagation": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayRouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to disable a resource attachment from propagating routes to the specified propagation route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DisableTransitGatewayRouteTablePropagation.html"
  },
  "ec2:DisableVgwRoutePropagation": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to disable a virtual private gateway from propagating routes to a specified route table of a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DisableVgwRoutePropagation.html"
  },
  "ec2:DisableVpcClassicLink": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Vpc": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcFlowLog": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcPeeringConnection": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to disable ClassicLink for a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DisableVpcClassicLink.html"
  },
  "ec2:DisableVpcClassicLinkDnsSupport": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to disable ClassicLink DNS support for a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DisableVpcClassicLinkDnsSupport.html"
  },
  "ec2:DisassociateAddress": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to disassociate an Elastic IP address from an instance or network interface",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DisassociateAddress.html"
  },
  "ec2:DisassociateClientVpnTargetNetwork": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::ClientVpnEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to disassociate a target network from a Client VPN endpoint",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DisassociateClientVpnTargetNetwork.html"
  },
  "ec2:DisassociateIamInstanceProfile": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to disassociate an IAM instance profile from a running or stopped instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DisassociateIamInstanceProfile.html"
  },
  "ec2:DisassociateRouteTable": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to disassociate a subnet from a route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DisassociateRouteTable.html"
  },
  "ec2:DisassociateSubnetCidrBlock": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to disassociate a CIDR block from a subnet",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DisassociateSubnetCidrBlock.html"
  },
  "ec2:DisassociateTransitGatewayMulticastDomain": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Subnet": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayMulticastDomain": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to disassociate one or more subnets from a transit gateway multicast domain",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DisassociateTransitGatewayMulticastDomain.html"
  },
  "ec2:DisassociateTransitGatewayRouteTable": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayRouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to disassociate a resource attachment from a transit gateway route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DisassociateTransitGatewayRouteTable.html"
  },
  "ec2:DisassociateVpcCidrBlock": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to disassociate a CIDR block from a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DisassociateVpcCidrBlock.html"
  },
  "ec2:EnableEbsEncryptionByDefault": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to enable EBS encryption by default for your account",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_EnableEbsEncryptionByDefault.html"
  },
  "ec2:EnableFastSnapshotRestores": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Snapshot": {
        "Condition Keys": [
          "ec2:Owner",
          "ec2:ParentVolume",
          "ec2:Region",
          "ec2:AvailabilityZone",
          "ec2:SnapshotTime",
          "ec2:Encrypted",
          "ec2:VolumeSize",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to enable fast snapshot restores for one or more snapshots in specified Availability Zones",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_EnableFastSnapshotRestores.html"
  },
  "ec2:EnableTransitGatewayRouteTablePropagation": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayRouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to enable an attachment to propagate routes to a propagation route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_EnableTransitGatewayRouteTablePropagation.html"
  },
  "ec2:EnableVgwRoutePropagation": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to enable a virtual private gateway to propagate routes to a VPC route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_EnableVgwRoutePropagation.html"
  },
  "ec2:EnableVolumeIO": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to enable I/O operations for a volume that had I/O operations disabled",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_EnableVolumeIO.html"
  },
  "ec2:EnableVpcClassicLink": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Vpc": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcFlowLog": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcPeeringConnection": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to enable a VPC for ClassicLink",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_EnableVpcClassicLink.html"
  },
  "ec2:EnableVpcClassicLinkDnsSupport": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to enable a VPC to support DNS hostname resolution for ClassicLink",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_EnableVpcClassicLinkDnsSupport.html"
  },
  "ec2:ExportClientVpnClientCertificateRevocationList": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to download the client certificate revocation list for a Client VPN endpoint",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ExportClientVpnClientCertificateRevocationList.html"
  },
  "ec2:ExportClientVpnClientConfiguration": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to download the contents of the Client VPN endpoint configuration file for a Client VPN endpoint",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ExportClientVpnClientConfiguration.html"
  },
  "ec2:ExportImage": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to export an Amazon Machine Image (AMI) to a VM file",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ExportImage.html"
  },
  "ec2:ExportTransitGatewayRoutes": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to export routes from a transit gateway route table to an Amazon S3 bucket",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ExportTransitGatewayRoutes.html"
  },
  "ec2:GetCapacityReservationUsage": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to get usage information about a Capacity Reservation",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetCapacityReservationUsage.html"
  },
  "ec2:GetConsoleOutput": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to get the console output for an instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetConsoleOutput.html"
  },
  "ec2:GetConsoleScreenshot": {
    "Access": "Read",
    "Affects": {
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve a JPG-format screenshot of a running instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetConsoleScreenshot.html"
  },
  "ec2:GetDefaultCreditSpecification": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to get the default credit option for CPU usage of a burstable performance instance family",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetDefaultCreditSpecification.html"
  },
  "ec2:GetEbsDefaultKmsKeyId": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to get the ID of the default customer master key (CMK) for EBS encryption by default",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetEbsDefaultKmsKeyId.html"
  },
  "ec2:GetEbsEncryptionByDefault": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to describe whether EBS encryption by default is enabled for your account",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetEbsEncryptionByDefault.html"
  },
  "ec2:GetHostReservationPurchasePreview": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to preview a reservation purchase with configurations that match those of a Dedicated Host",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetHostReservationPurchasePreview.html"
  },
  "ec2:GetLaunchTemplateData": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to get the configuration data of the specified instance for use with a new launch template or launch template version",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetLaunchTemplateData.html"
  },
  "ec2:GetPasswordData": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to retrieve the encrypted administrator password for a running Windows instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetPasswordData.html"
  },
  "ec2:GetReservedInstancesExchangeQuote": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to return a quote and exchange information for exchanging one or more Convertible Reserved Instances for a new Convertible Reserved Instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetReservedInstancesExchangeQuote.html"
  },
  "ec2:GetTransitGatewayAttachmentPropagations": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to list the route tables to which a resource attachment propagates routes",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetTransitGatewayAttachmentPropagations.html"
  },
  "ec2:GetTransitGatewayMulticastDomainAssociations": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to get information about the associations for a transit gateway multicast domain",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetTransitGatewayMulticastDomainAssociations.html"
  },
  "ec2:GetTransitGatewayRouteTableAssociations": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to get information about associations for a transit gateway route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetTransitGatewayRouteTableAssociations.html"
  },
  "ec2:GetTransitGatewayRouteTablePropagations": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to get information about the route table propagations for a transit gateway route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetTransitGatewayRouteTablePropagations.html"
  },
  "ec2:ImportClientVpnClientCertificateRevocationList": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::ClientVpnEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to upload a client certificate revocation list to a Client VPN endpoint",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ImportClientVpnClientCertificateRevocationList.html"
  },
  "ec2:ImportImage": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to import single or multi-volume disk images or EBS snapshots into an Amazon Machine Image (AMI)",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ImportImage.html"
  },
  "ec2:ImportInstance": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create an import instance task using metadata from a disk image",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ImportInstance.html"
  },
  "ec2:ImportKeyPair": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to import a public key from an RSA key pair that was created with a third-party tool",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ImportKeyPair.html"
  },
  "ec2:ImportSnapshot": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to import a disk into an EBS snapshot",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ImportSnapshot.html"
  },
  "ec2:ImportVolume": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create an import volume task using metadata from a disk image",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ImportVolume.html"
  },
  "ec2:ModifyCapacityReservation": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::CapacityReservation": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to modify a Capacity Reservation's capacity and the conditions under which it is to be released",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyCapacityReservation.html"
  },
  "ec2:ModifyClientVpnEndpoint": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::ClientVpnEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to modify a Client VPN endpoint",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyClientVpnEndpoint.html"
  },
  "ec2:ModifyDefaultCreditSpecification": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to change the account level default credit option for CPU usage of burstable performance instances",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyDefaultCreditSpecification.html"
  },
  "ec2:ModifyEbsDefaultKmsKeyId": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to change the default customer master key (CMK) for EBS encryption by default for your account",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyEbsDefaultKmsKeyId.html"
  },
  "ec2:ModifyFleet": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify an EC2 Fleet",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyFleet.html"
  },
  "ec2:ModifyFpgaImageAttribute": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify an attribute of an Amazon FPGA Image (AFI)",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyFpgaImageAttribute.html"
  },
  "ec2:ModifyHosts": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify a Dedicated Host",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyHosts.html"
  },
  "ec2:ModifyIdFormat": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify the ID format for a resource",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyIdFormat.html"
  },
  "ec2:ModifyIdentityIdFormat": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify the ID format of a resource for a specific principal in your account",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyIdentityIdFormat.html"
  },
  "ec2:ModifyImageAttribute": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify an attribute of an Amazon Machine Image (AMI)",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyImageAttribute.html"
  },
  "ec2:ModifyInstanceAttribute": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify an attribute of an instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyInstanceAttribute.html"
  },
  "ec2:ModifyInstanceCapacityReservationAttributes": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify the Capacity Reservation settings for a stopped instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyInstanceCapacityReservationAttributes.html"
  },
  "ec2:ModifyInstanceCreditSpecification": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Instance": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to modify the credit option for CPU usage on an instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyInstanceCreditSpecification.html"
  },
  "ec2:ModifyInstanceEventStartTime": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "ec2:Region"
        ],
        "Dependant Actions": []
      },
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [
          "ec2:Region"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to modify the start time for a scheduled EC2 instance event",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyInstanceEventStartTime.html"
  },
  "ec2:ModifyInstanceMetadataOptions": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify the metadata options for an instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyInstanceMetadataOptions.html"
  },
  "ec2:ModifyInstancePlacement": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify the placement attributes for an instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyInstancePlacement.html"
  },
  "ec2:ModifyLaunchTemplate": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::LaunchTemplate": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to modify a launch template",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyLaunchTemplate.html"
  },
  "ec2:ModifyNetworkInterfaceAttribute": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify an attribute of a network interface",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyNetworkInterfaceAttribute.html"
  },
  "ec2:ModifyReservedInstances": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify attributes of one or more Reserved Instances",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyReservedInstances.html"
  },
  "ec2:ModifySnapshotAttribute": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Ec2::Snapshot": {
        "Condition Keys": [
          "ec2:Owner",
          "ec2:ParentVolume",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:SnapshotTime",
          "ec2:VolumeSize"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to add or remove permission settings for a snapshot",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifySnapshotAttribute.html"
  },
  "ec2:ModifySpotFleetRequest": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify a Spot Fleet request",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifySpotFleetRequest.html"
  },
  "ec2:ModifySubnetAttribute": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify an attribute of a subnet",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifySubnetAttribute.html"
  },
  "ec2:ModifyTrafficMirrorFilterNetworkServices": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TrafficMirrorFilter": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TrafficMirrorFilterRule": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to allow or restrict mirroring network services",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyTrafficMirrorFilterNetworkServices.html"
  },
  "ec2:ModifyTrafficMirrorFilterRule": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TrafficMirrorFilter": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TrafficMirrorFilterRule": {
        "Condition Keys": [
          "ec2:Region"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to modify a traffic mirror rule",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyTrafficMirrorFilterRule.html"
  },
  "ec2:ModifyTrafficMirrorSession": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TrafficMirrorFilter": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TrafficMirrorSession": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TrafficMirrorTarget": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to modify a traffic mirror session",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyTrafficMirrorSession.html"
  },
  "ec2:ModifyTransitGatewayVpcAttachment": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Subnet": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to modify a VPC attachment on a transit gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyTransitGatewayVpcAttachment.html"
  },
  "ec2:ModifyVolume": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify the parameters of an EBS volume",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVolume.html"
  },
  "ec2:ModifyVolumeAttribute": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify an attribute of a volume",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVolumeAttribute.html"
  },
  "ec2:ModifyVpcAttribute": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify an attribute of a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVpcAttribute.html"
  },
  "ec2:ModifyVpcEndpoint": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::RouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::SecurityGroup": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Subnet": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to modify an attribute of a VPC endpoint",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVpcEndpoint.html"
  },
  "ec2:ModifyVpcEndpointConnectionNotification": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify a connection notification for a VPC endpoint or VPC endpoint service",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVpcEndpointConnectionNotification.html"
  },
  "ec2:ModifyVpcEndpointServiceConfiguration": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:VpceServicePrivateDnsName",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to modify the attributes of a VPC endpoint service configuration",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVpcEndpointServiceConfiguration.html"
  },
  "ec2:ModifyVpcEndpointServicePermissions": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to modify the permissions for a VPC endpoint service",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVpcEndpointServicePermissions.html"
  },
  "ec2:ModifyVpcPeeringConnectionOptions": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify the VPC peering connection options on one side of a VPC peering connection",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVpcPeeringConnectionOptions.html"
  },
  "ec2:ModifyVpcTenancy": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify the instance tenancy attribute of a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVpcTenancy.html"
  },
  "ec2:ModifyVpnConnection": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::VpnConnection": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:GatewayType"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to modify the target gateway of a Site-to-Site VPN connection",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVpnConnection.html"
  },
  "ec2:ModifyVpnTunnelCertificate": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to modify the certificate for a Site-to-Site VPN connection",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVpnTunnelCertificate"
  },
  "ec2:ModifyVpnTunnelOptions": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::VpnConnection": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:AuthenticationType",
          "ec2:DPDTimeoutSeconds",
          "ec2:IKEVersions",
          "ec2:InsideTunnelCidr",
          "ec2:Phase1DHGroupNumbers",
          "ec2:Phase2DHGroupNumbers",
          "ec2:Phase1EncryptionAlgorithms",
          "ec2:Phase2EncryptionAlgorithms",
          "ec2:Phase1IntegrityAlgorithms",
          "ec2:Phase2IntegrityAlgorithms",
          "ec2:Phase1LifetimeSeconds",
          "ec2:Phase2LifetimeSeconds",
          "ec2:PresharedKeys",
          "ec2:RekeyFuzzPercentage",
          "ec2:RekeyMarginTimeSeconds",
          "ec2:RoutingType"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to modify the options for a Site-to-Site VPN connection",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVpnTunnelOptions.html"
  },
  "ec2:MonitorInstances": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to enable detailed monitoring for a running instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_MonitorInstances.html"
  },
  "ec2:MoveAddressToVpc": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to move an Elastic IP address from the EC2-Classic platform to the EC2-VPC platform",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_MoveAddressToVpc.html"
  },
  "ec2:ProvisionByoipCidr": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to provision an address range for use in AWS through bring your own IP addresses (BYOIP), and to create a corresponding address pool",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ProvisionByoipCidr.html"
  },
  "ec2:PurchaseHostReservation": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to purchase a reservation with configurations that match those of a Dedicated Host",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_PurchaseHostReservation.html"
  },
  "ec2:PurchaseReservedInstancesOffering": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to purchase a Reserved Instance offering",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_PurchaseReservedInstancesOffering.html"
  },
  "ec2:PurchaseScheduledInstances": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to purchase one or more Scheduled Instances with a specified schedule",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_PurchaseScheduledInstances.html"
  },
  "ec2:RebootInstances": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to request a reboot of one or more instances",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RebootInstances.html"
  },
  "ec2:RegisterImage": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to register an Amazon Machine Image (AMI)",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RegisterImage.html"
  },
  "ec2:RegisterTransitGatewayMulticastGroupMembers": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::NetworkInterface": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayMulticastDomain": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to register one or more network interfaces as a member of a group IP address in a transit gateway multicast domain",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RegisterTransitGatewayMulticastGroupMembers.html"
  },
  "ec2:RegisterTransitGatewayMulticastGroupSources": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::NetworkInterface": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayMulticastDomain": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to register one or more network interfaces as a source of a group IP address in a transit gateway multicast domain",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RegisterTransitGatewayMulticastGroupSources.html"
  },
  "ec2:RejectTransitGatewayPeeringAttachment": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to reject a transit gateway peering attachment request",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RejectTransitGatewayPeeringAttachment.html"
  },
  "ec2:RejectTransitGatewayVpcAttachment": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to reject a request to attach a VPC to a transit gateway",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RejectTransitGatewayVpcAttachment.html"
  },
  "ec2:RejectVpcEndpointConnections": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to reject one or more VPC endpoint connection requests to a VPC endpoint service",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RejectVpcEndpointConnections.html"
  },
  "ec2:RejectVpcPeeringConnection": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::VpcPeeringConnection": {
        "Condition Keys": [
          "ec2:AccepterVpc",
          "ec2:Region",
          "ec2:RequesterVpc",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to reject a VPC peering connection request",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RejectVpcPeeringConnection.html"
  },
  "ec2:ReleaseAddress": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to release an Elastic IP address",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ReleaseAddress.html"
  },
  "ec2:ReleaseHosts": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to release one or more On-Demand Dedicated Hosts",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ReleaseHosts.html"
  },
  "ec2:ReplaceIamInstanceProfileAssociation": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": [
          "iam:PassRole"
        ]
      },
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": [
          "iam:PassRole"
        ]
      }
    },
    "Description": "Grants permission to replace an IAM instance profile for an instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ReplaceIamInstanceProfileAssociation.html"
  },
  "ec2:ReplaceNetworkAclAssociation": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to change which network ACL a subnet is associated with",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ReplaceNetworkAclAssociation.html"
  },
  "ec2:ReplaceNetworkAclEntry": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to replace an entry (rule) in a network ACL",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ReplaceNetworkAclEntry.html"
  },
  "ec2:ReplaceRoute": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::RouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to replace a route within a route table in a VPC",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ReplaceRoute.html"
  },
  "ec2:ReplaceRouteTableAssociation": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to change the route table that is associated with a subnet",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ReplaceRouteTableAssociation.html"
  },
  "ec2:ReplaceTransitGatewayRoute": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::TransitGatewayAttachment": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::TransitGatewayRouteTable": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to replace a route in a transit gateway route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ReplaceTransitGatewayRoute.html"
  },
  "ec2:ReportInstanceStatus": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to submit feedback about the status of an instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ReportInstanceStatus.html"
  },
  "ec2:RequestSpotFleet": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a Spot Fleet request",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RequestSpotFleet.html"
  },
  "ec2:RequestSpotInstances": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a Spot Instance request",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RequestSpotInstances.html"
  },
  "ec2:ResetEbsDefaultKmsKeyId": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to reset the default customer master key (CMK) for EBS encryption for your account to use the AWS-managed CMK for EBS",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ResetEbsDefaultKmsKeyId.html"
  },
  "ec2:ResetFpgaImageAttribute": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to reset an attribute of an Amazon FPGA Image (AFI) to its default value",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ResetFpgaImageAttribute.html"
  },
  "ec2:ResetImageAttribute": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to reset an attribute of an Amazon Machine Image (AMI) to its default value",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ResetImageAttribute.html"
  },
  "ec2:ResetInstanceAttribute": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to reset an attribute of an instance to its default value",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ResetInstanceAttribute.html"
  },
  "ec2:ResetNetworkInterfaceAttribute": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to reset an attribute of a network interface",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ResetNetworkInterfaceAttribute.html"
  },
  "ec2:ResetSnapshotAttribute": {
    "Access": "Permissions Management",
    "Affects": {},
    "Description": "Grants permission to reset permission settings for a snapshot",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ResetSnapshotAttribute.html"
  },
  "ec2:RestoreAddressToClassic": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to restore an Elastic IP address that was previously moved to the EC2-VPC platform back to the EC2-Classic platform",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RestoreAddressToClassic.html"
  },
  "ec2:RevokeClientVpnIngress": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::ClientVpnEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to remove an inbound authorization rule from a Client VPN endpoint",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RevokeClientVpnIngress.html"
  },
  "ec2:RevokeSecurityGroupEgress": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::SecurityGroup": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to remove one or more outbound rules from a VPC security group",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RevokeSecurityGroupEgress.html"
  },
  "ec2:RevokeSecurityGroupIngress": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::SecurityGroup": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to remove one or more inbound rules from a security group",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RevokeSecurityGroupIngress.html"
  },
  "ec2:RunInstances": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::ElasticGpu": {
        "Condition Keys": [
          "ec2:ElasticGpuType"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Image": {
        "Condition Keys": [
          "ec2:ImageType",
          "ec2:IsLaunchTemplateResource",
          "ec2:LaunchTemplate",
          "ec2:Owner",
          "ec2:Public",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:IsLaunchTemplateResource",
          "ec2:LaunchTemplate",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:RootDeviceType",
          "ec2:Tenancy",
          "ec2:MetadataHttpEndpoint",
          "ec2:MetadataHttpTokens",
          "ec2:MetadataHttpPutResponseHopLimit"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::KeyPair": {
        "Condition Keys": [
          "ec2:IsLaunchTemplateResource",
          "ec2:LaunchTemplate",
          "ec2:Region"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::LaunchTemplate": {
        "Condition Keys": [
          "ec2:IsLaunchTemplateResource",
          "ec2:LaunchTemplate",
          "ec2:Region"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::NetworkInterface": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:IsLaunchTemplateResource",
          "ec2:LaunchTemplate",
          "ec2:Region",
          "ec2:ResourceTag/",
          "ec2:Subnet",
          "ec2:Vpc",
          "ec2:AssociatePublicIpAddress"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::PlacementGroup": {
        "Condition Keys": [
          "ec2:IsLaunchTemplateResource",
          "ec2:LaunchTemplate",
          "ec2:PlacementGroupStrategy",
          "ec2:Region"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::SecurityGroup": {
        "Condition Keys": [
          "ec2:IsLaunchTemplateResource",
          "ec2:LaunchTemplate",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Snapshot": {
        "Condition Keys": [
          "ec2:IsLaunchTemplateResource",
          "ec2:LaunchTemplate",
          "ec2:Owner",
          "ec2:ParentVolume",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:SnapshotTime",
          "ec2:VolumeSize"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Subnet": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:IsLaunchTemplateResource",
          "ec2:LaunchTemplate",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      },
      "AWS::Ec2::Volume": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:AvailabilityZone",
          "ec2:Encrypted",
          "ec2:IsLaunchTemplateResource",
          "ec2:LaunchTemplate",
          "ec2:ParentSnapshot",
          "ec2:Region",
          "ec2:VolumeIops",
          "ec2:VolumeSize",
          "ec2:VolumeType"
        ],
        "Dependant Actions": []
      },
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [
          "aws:RequestTag/${TagKey}",
          "aws:TagKeys",
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:IsLaunchTemplateResource",
          "ec2:LaunchTemplate",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:RootDeviceType",
          "ec2:Tenancy",
          "ec2:MetadataHttpEndpoint",
          "ec2:MetadataHttpTokens",
          "ec2:MetadataHttpPutResponseHopLimit"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to launch one or more instances",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RunInstances.html"
  },
  "ec2:RunScheduledInstances": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to launch one or more Scheduled Instances",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RunScheduledInstances.html"
  },
  "ec2:SearchLocalGatewayRoutes": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to search for routes in a local gateway route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_SearchLocalGatewayRoutes.html"
  },
  "ec2:SearchTransitGatewayMulticastGroups": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to search for groups, sources, and members in a transit gateway multicast domain",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_SearchTransitGatewayMulticastGroups.html"
  },
  "ec2:SearchTransitGatewayRoutes": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to search for routes in a transit gateway route table",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_SearchTransitGatewayRoutes.html"
  },
  "ec2:SendDiagnosticInterrupt": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to send a diagnostic interrupt to an Amazon EC2 instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_SendDiagnosticInterrupt.html"
  },
  "ec2:StartInstances": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to start a stopped instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_StartInstances.html"
  },
  "ec2:StartVpcEndpointServicePrivateDnsVerification": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::VpcEndpointService": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to start the private DNS verification process for a VPC endpoint service",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_StartVpcEndpointServicePrivateDnsVerification.html"
  },
  "ec2:StopInstances": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to stop an Amazon EBS-backed instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_StopInstances.html"
  },
  "ec2:TerminateClientVpnConnections": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::ClientVpnEndpoint": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to terminate active Client VPN endpoint connections",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_TerminateClientVpnConnections.html"
  },
  "ec2:TerminateInstances": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::Instance": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      },
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [
          "ec2:AvailabilityZone",
          "ec2:EbsOptimized",
          "ec2:InstanceProfile",
          "ec2:InstanceType",
          "ec2:PlacementGroup",
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:RootDeviceType",
          "ec2:Tenancy"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to shut down one or more instances",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_TerminateInstances.html"
  },
  "ec2:UnassignIpv6Addresses": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to unassign one or more IPv6 addresses from a network interface",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_UnassignIpv6Addresses.html"
  },
  "ec2:UnassignPrivateIpAddresses": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to unassign one or more secondary private IP addresses from a network interface",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_UnassignPrivateIpAddresses.html"
  },
  "ec2:UnmonitorInstances": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to disable detailed monitoring for a running instance",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_UnmonitorInstances.html"
  },
  "ec2:UpdateSecurityGroupRuleDescriptionsEgress": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::SecurityGroup": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to update descriptions for one or more outbound rules in a VPC security group",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_UpdateSecurityGroupRuleDescriptionsEgress.html"
  },
  "ec2:UpdateSecurityGroupRuleDescriptionsIngress": {
    "Access": "Write",
    "Affects": {
      "AWS::Ec2::SecurityGroup": {
        "Condition Keys": [
          "ec2:Region",
          "ec2:ResourceTag/${TagKey}",
          "ec2:Vpc"
        ],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to update descriptions for one or more inbound rules in a security group",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_UpdateSecurityGroupRuleDescriptionsIngress.html"
  },
  "ec2:WithdrawByoipCidr": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to stop advertising an address range that was provisioned for use in AWS through bring your own IP addresses (BYOIP)",
    "Reference": "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_WithdrawByoipCidr.html"
  },
  "iam:AddClientIDToOpenIDConnectProvider": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::OidcProvider": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to add a new client ID (audience) to the list of registered IDs for the specified IAM OpenID Connect (OIDC) provider resource",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_AddClientIDToOpenIDConnectProvider.html"
  },
  "iam:AddRoleToInstanceProfile": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to add an IAM role to the specified instance profile",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_AddRoleToInstanceProfile.html"
  },
  "iam:AddUserToGroup": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::Group": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to add an IAM user to the specified IAM group",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_AddUserToGroup.html"
  },
  "iam:AttachGroupPolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::Group": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to attach a managed policy to the specified IAM group",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_AttachGroupPolicy.html"
  },
  "iam:AttachRolePolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to attach a managed policy to the specified IAM role",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_AttachRolePolicy.html"
  },
  "iam:AttachUserPolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to attach a managed policy to the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_AttachUserPolicy.html"
  },
  "iam:ChangePassword": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission for an IAM user to to change their own password",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ChangePassword.html"
  },
  "iam:CreateAccessKey": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create access key and secret access key for the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateAccessKey.html"
  },
  "iam:CreateAccountAlias": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create an alias for your AWS account",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateAccountAlias.html"
  },
  "iam:CreateGroup": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::Group": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a new group",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateGroup.html"
  },
  "iam:CreateInstanceProfile": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a new instance profile",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateInstanceProfile.html"
  },
  "iam:CreateLoginProfile": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a password for the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateLoginProfile.html"
  },
  "iam:CreateOpenIDConnectProvider": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::OidcProvider": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create an IAM resource that describes an identity provider (IdP) that supports OpenID Connect (OIDC)",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html"
  },
  "iam:CreatePolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::Policy": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a new managed policy",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreatePolicy.html"
  },
  "iam:CreatePolicyVersion": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::Policy": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a new version of the specified managed policy",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreatePolicyVersion.html"
  },
  "iam:CreateRole": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a new role",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateRole.html"
  },
  "iam:CreateSAMLProvider": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::SamlProvider": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create an IAM resource that describes an identity provider (IdP) that supports SAML 2.0",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateSAMLProvider.html"
  },
  "iam:CreateServiceLinkedRole": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create an IAM role that allows an AWS service to perform actions on your behalf",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateServiceLinkedRole.html"
  },
  "iam:CreateServiceSpecificCredential": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a new service-specific credential for an IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateServiceSpecificCredential.html"
  },
  "iam:CreateUser": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a new IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateUser.html"
  },
  "iam:CreateVirtualMFADevice": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::VirtualMfaDevice": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create a new virtual MFA device",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateVirtualMFADevice.html"
  },
  "iam:DeactivateMFADevice": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to deactivate the specified MFA device and remove its association with the IAM user for which it was originally enabled",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeactivateMFADevice.html"
  },
  "iam:DeleteAccessKey": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete the access key pair that is associated with the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteAccessKey.html"
  },
  "iam:DeleteAccountAlias": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to delete the specified AWS account alias",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteAccountAlias.html"
  },
  "iam:DeleteAccountPasswordPolicy": {
    "Access": "Permissions Management",
    "Affects": {},
    "Description": "Grants permission to delete the password policy for the AWS account",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteAccountPasswordPolicy.html"
  },
  "iam:DeleteGroup": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::Group": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete the specified IAM group",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteGroup.html"
  },
  "iam:DeleteGroupPolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::Group": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete the specified inline policy from its group",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteGroupPolicy.html"
  },
  "iam:DeleteInstanceProfile": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete the specified instance profile",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteInstanceProfile.html"
  },
  "iam:DeleteLoginProfile": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete the password for the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteLoginProfile.html"
  },
  "iam:DeleteOpenIDConnectProvider": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::OidcProvider": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete an OpenID Connect identity provider (IdP) resource object in IAM",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteOpenIDConnectProvider.html"
  },
  "iam:DeletePolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::Policy": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete the specified managed policy and remove it from any IAM entities (users, groups, or roles) to which it is attached",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeletePolicy.html"
  },
  "iam:DeletePolicyVersion": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::Policy": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a version from the specified managed policy",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeletePolicyVersion.html"
  },
  "iam:DeleteRole": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete the specified role",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteRole.html"
  },
  "iam:DeleteRolePermissionsBoundary": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to remove the permissions boundary from a role",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteRolePermissionsBoundary.html"
  },
  "iam:DeleteRolePolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete the specified inline policy from the specified role",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteRolePolicy.html"
  },
  "iam:DeleteSAMLProvider": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::SamlProvider": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a SAML provider resource in IAM",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteSAMLProvider.html"
  },
  "iam:DeleteSSHPublicKey": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete the specified SSH public key",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteSSHPublicKey.html"
  },
  "iam:DeleteServerCertificate": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::ServerCertificate": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete the specified server certificate",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteServerCertificate.html"
  },
  "iam:DeleteServiceLinkedRole": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete an IAM role that is linked to a specific AWS service, if the service is no longer using it",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteServiceLinkedRole.html"
  },
  "iam:DeleteServiceSpecificCredential": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete the specified service-specific credential for an IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteServiceSpecificCredential.html"
  },
  "iam:DeleteSigningCertificate": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a signing certificate that is associated with the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteSigningCertificate.html"
  },
  "iam:DeleteUser": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteUser.html"
  },
  "iam:DeleteUserPermissionsBoundary": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to remove the permissions boundary from the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteUserPermissionsBoundary.html"
  },
  "iam:DeleteUserPolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete the specified inline policy from an IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteUserPolicy.html"
  },
  "iam:DeleteVirtualMFADevice": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::VirtualMfaDevice": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Iam::SmsMfa": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a virtual MFA device",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeleteVirtualMFADevice.html"
  },
  "iam:DetachGroupPolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::Group": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to detach a managed policy from the specified IAM group",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DetachGroupPolicy.html"
  },
  "iam:DetachRolePolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to detach a managed policy from the specified role",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DetachRolePolicy.html"
  },
  "iam:DetachUserPolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to detach a managed policy from the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_DetachUserPolicy.html"
  },
  "iam:EnableMFADevice": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to enable an MFA device and associate it with the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_EnableMFADevice.html"
  },
  "iam:GenerateCredentialReport": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to generate a credential report for the AWS account",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GenerateCredentialReport.html"
  },
  "iam:GenerateOrganizationsAccessReport": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::AccessReport": {
        "Condition Keys": [],
        "Dependant Actions": [
          "organizations:DescribePolicy",
          "organizations:ListChildren",
          "organizations:ListParents",
          "organizations:ListPoliciesForTarget",
          "organizations:ListRoots",
          "organizations:ListTargetsForPolicy"
        ]
      }
    },
    "Description": "Grants permission to generate an access report for an AWS Organizations entity",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GenerateOrganizationsAccessReport.html"
  },
  "iam:GenerateServiceLastAccessedDetails": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to generate a service last accessed data report for an IAM resource",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GenerateServiceLastAccessedDetails.html"
  },
  "iam:GetAccessKeyLastUsed": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve information about when the specified access key was last used",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetAccessKeyLastUsed.html"
  },
  "iam:GetAccountAuthorizationDetails": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to retrieve information about all IAM users, groups, roles, and policies in your AWS account, including their relationships to one another",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetAccountAuthorizationDetails.html"
  },
  "iam:GetAccountPasswordPolicy": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to retrieve the password policy for the AWS account",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetAccountPasswordPolicy.html"
  },
  "iam:GetAccountSummary": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to retrieve information about IAM entity usage and IAM quotas in the AWS account",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetAccountSummary.html"
  },
  "iam:GetContextKeysForCustomPolicy": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to retrieve a list of all of the context keys that are referenced in the specified policy",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetContextKeysForCustomPolicy.html"
  },
  "iam:GetContextKeysForPrincipalPolicy": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::Group": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve a list of all context keys that are referenced in all IAM policies that are attached to the specified IAM identity (user, group, or role)",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetContextKeysForPrincipalPolicy.html"
  },
  "iam:GetCredentialReport": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to retrieve a credential report for the AWS account",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetCredentialReport.html"
  },
  "iam:GetGroup": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::Group": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve a list of IAM users in the specified IAM group",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetGroup.html"
  },
  "iam:GetGroupPolicy": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::Group": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve an inline policy document that is embedded in the specified IAM group",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetGroupPolicy.html"
  },
  "iam:GetInstanceProfile": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve information about the specified instance profile, including the instance profile's path, GUID, ARN, and role",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetInstanceProfile.html"
  },
  "iam:GetLoginProfile": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve the user name and password creation date for the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetLoginProfile.html"
  },
  "iam:GetOpenIDConnectProvider": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::OidcProvider": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve information about the specified OpenID Connect (OIDC) provider resource in IAM",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetOpenIDConnectProvider.html"
  },
  "iam:GetOrganizationsAccessReport": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to retrieve an AWS Organizations access report",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetOrganizationsAccessReport.html"
  },
  "iam:GetPolicy": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::Policy": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve information about the specified managed policy, including the policy's default version and the total number of identities to which the policy is attached",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetPolicy.html"
  },
  "iam:GetPolicyVersion": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::Policy": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve information about a version of the specified managed policy, including the policy document",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetPolicyVersion.html"
  },
  "iam:GetRole": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve information about the specified role, including the role's path, GUID, ARN, and the role's trust policy",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetRole.html"
  },
  "iam:GetRolePolicy": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve an inline policy document that is embedded with the specified IAM role",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetRolePolicy.html"
  },
  "iam:GetSAMLProvider": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::SamlProvider": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve the SAML provider metadocument that was uploaded when the IAM SAML provider resource was created or updated",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetSAMLProvider.html"
  },
  "iam:GetSSHPublicKey": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve the specified SSH public key, including metadata about the key",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetSSHPublicKey.html"
  },
  "iam:GetServerCertificate": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::ServerCertificate": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve information about the specified server certificate stored in IAM",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetServerCertificate.html"
  },
  "iam:GetServiceLastAccessedDetails": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to retrieve information about the service last accessed data report",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetServiceLastAccessedDetails.html"
  },
  "iam:GetServiceLastAccessedDetailsWithEntities": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to retrieve information about the entities from the service last accessed data report",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetServiceLastAccessedDetailsWithEntities.html"
  },
  "iam:GetServiceLinkedRoleDeletionStatus": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve an IAM service-linked role deletion status",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetServiceLinkedRoleDeletionStatus.html"
  },
  "iam:GetUser": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve information about the specified IAM user, including the user's creation date, path, unique ID, and ARN",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetUser.html"
  },
  "iam:GetUserPolicy": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve an inline policy document that is embedded in the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetUserPolicy.html"
  },
  "iam:ListAccessKeys": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list information about the access key IDs that are associated with the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListAccessKeys.html"
  },
  "iam:ListAccountAliases": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to list the account alias that is associated with the AWS account",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListAccountAliases.html"
  },
  "iam:ListAttachedGroupPolicies": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::Group": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list all managed policies that are attached to the specified IAM group",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListAttachedGroupPolicies.html"
  },
  "iam:ListAttachedRolePolicies": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list all managed policies that are attached to the specified IAM role",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListAttachedRolePolicies.html"
  },
  "iam:ListAttachedUserPolicies": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list all managed policies that are attached to the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListAttachedUserPolicies.html"
  },
  "iam:ListEntitiesForPolicy": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::Policy": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list all IAM identities to which the specified managed policy is attached",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListEntitiesForPolicy.html"
  },
  "iam:ListGroupPolicies": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::Group": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list the names of the inline policies that are embedded in the specified IAM group",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListGroupPolicies.html"
  },
  "iam:ListGroups": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to list the IAM groups that have the specified path prefix",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListGroups.html"
  },
  "iam:ListGroupsForUser": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list the IAM groups that the specified IAM user belongs to",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListGroupsForUser.html"
  },
  "iam:ListInstanceProfiles": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list the instance profiles that have the specified path prefix",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListInstanceProfiles.html"
  },
  "iam:ListInstanceProfilesForRole": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list the instance profiles that have the specified associated IAM role",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListInstanceProfilesForRole.html"
  },
  "iam:ListMFADevices": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list the MFA devices for an IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListMFADevices.html"
  },
  "iam:ListOpenIDConnectProviders": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to list information about the IAM OpenID Connect (OIDC) provider resource objects that are defined in the AWS account",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListOpenIDConnectProviders.html"
  },
  "iam:ListPolicies": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to list all managed policies",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListPolicies.html"
  },
  "iam:ListPoliciesGrantingServiceAccess": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to list information about the policies that grant an entity access to a specific service",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListPoliciesGrantingServiceAccess.html"
  },
  "iam:ListPolicyVersions": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::Policy": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list information about the versions of the specified managed policy, including the version that is currently set as the policy's default version",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListPolicyVersions.html"
  },
  "iam:ListRolePolicies": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list the names of the inline policies that are embedded in the specified IAM role",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListRolePolicies.html"
  },
  "iam:ListRoleTags": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list the tags that are attached to the specified IAM role.",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListRoleTags.html"
  },
  "iam:ListRoles": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to list the IAM roles that have the specified path prefix",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListRoles.html"
  },
  "iam:ListSAMLProviders": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to list the SAML provider resources in IAM",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListSAMLProviders.html"
  },
  "iam:ListSSHPublicKeys": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list information about the SSH public keys that are associated with the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListSSHPublicKeys.html"
  },
  "iam:ListServerCertificates": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to list the server certificates that have the specified path prefix",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListServerCertificates.html"
  },
  "iam:ListServiceSpecificCredentials": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list the service-specific credentials that are associated with the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListServiceSpecificCredentials.html"
  },
  "iam:ListSigningCertificates": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list information about the signing certificates that are associated with the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListSigningCertificates.html"
  },
  "iam:ListUserPolicies": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list the names of the inline policies that are embedded in the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListUserPolicies.html"
  },
  "iam:ListUserTags": {
    "Access": "List",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to list the tags that are attached to the specified IAM user.",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListUserTags.html"
  },
  "iam:ListUsers": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to list the IAM users that have the specified path prefix",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListUsers.html"
  },
  "iam:ListVirtualMFADevices": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to list virtual MFA devices by assignment status",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListVirtualMFADevices.html"
  },
  "iam:PassRole": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to pass a role to a service",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html"
  },
  "iam:PutGroupPolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::Group": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create or update an inline policy document that is embedded in the specified IAM group",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_PutGroupPolicy.html"
  },
  "iam:PutRolePermissionsBoundary": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to set a managed policy as a permissions boundary for a role",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_PutRolePermissionsBoundary.html"
  },
  "iam:PutRolePolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create or update an inline policy document that is embedded in the specified IAM role",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_PutRolePolicy.html"
  },
  "iam:PutUserPermissionsBoundary": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to set a managed policy as a permissions boundary for an IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_PutUserPermissionsBoundary.html"
  },
  "iam:PutUserPolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create or update an inline policy document that is embedded in the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_PutUserPolicy.html"
  },
  "iam:RemoveClientIDFromOpenIDConnectProvider": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::OidcProvider": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to remove the client ID (audience) from the list of client IDs in the specified IAM OpenID Connect (OIDC) provider resource",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_RemoveClientIDFromOpenIDConnectProvider.html"
  },
  "iam:RemoveRoleFromInstanceProfile": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::InstanceProfile": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to remove an IAM role from the specified EC2 instance profile",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_RemoveRoleFromInstanceProfile.html"
  },
  "iam:RemoveUserFromGroup": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::Group": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to remove an IAM user from the specified group",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_RemoveUserFromGroup.html"
  },
  "iam:ResetServiceSpecificCredential": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to reset the password for an existing service-specific credential for an IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ResetServiceSpecificCredential.html"
  },
  "iam:ResyncMFADevice": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to synchronize the specified MFA device with its IAM entity (user or role)",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_ResyncMFADevice.html"
  },
  "iam:SetDefaultPolicyVersion": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::Policy": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to set the version of the specified policy as the policy's default version",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_SetDefaultPolicyVersion.html"
  },
  "iam:SetSecurityTokenServicePreferences": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to set the STS global endpoint token version",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_SetSecurityTokenServicePreferences.html"
  },
  "iam:SimulateCustomPolicy": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to simulate whether an identity-based policy or resource-based policy provides permissions for specific API operations and resources",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_SimulateCustomPolicy.html"
  },
  "iam:SimulatePrincipalPolicy": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::Group": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to simulate whether an identity-based policy that is attached to a specified IAM entity (user or role) provides permissions for specific API operations and resources",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_SimulatePrincipalPolicy.html"
  },
  "iam:TagRole": {
    "Access": "Tagging",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to add tags to an IAM role.",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_TagRole.html"
  },
  "iam:TagUser": {
    "Access": "Tagging",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to add tags to an IAM user.",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_TagUser.html"
  },
  "iam:UntagRole": {
    "Access": "Tagging",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to remove the specified tags from the role.",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UntagRole.html"
  },
  "iam:UntagUser": {
    "Access": "Tagging",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to remove the specified tags from the user.",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UntagUser.html"
  },
  "iam:UpdateAccessKey": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to update the status of the specified access key as Active or Inactive",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateAccessKey.html"
  },
  "iam:UpdateAccountPasswordPolicy": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to update the password policy settings for the AWS account",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateAccountPasswordPolicy.html"
  },
  "iam:UpdateAssumeRolePolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to update the policy that grants an IAM entity permission to assume a role",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateAssumeRolePolicy.html"
  },
  "iam:UpdateGroup": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::Group": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to update the name or path of the specified IAM group",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateGroup.html"
  },
  "iam:UpdateLoginProfile": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to change the password for the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateLoginProfile.html"
  },
  "iam:UpdateOpenIDConnectProviderThumbprint": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::OidcProvider": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to update the entire list of server certificate thumbprints that are associated with an OpenID Connect (OIDC) provider resource",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateOpenIDConnectProviderThumbprint.html"
  },
  "iam:UpdateRole": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to update the description or maximum session duration setting of a role",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateRole.html"
  },
  "iam:UpdateRoleDescription": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to update only the description of a role",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateRoleDescription.html"
  },
  "iam:UpdateSAMLProvider": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::SamlProvider": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to update the metadata document for an existing SAML provider resource",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateSAMLProvider.html"
  },
  "iam:UpdateSSHPublicKey": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to update the status of an IAM user's SSH public key to active or inactive",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateSSHPublicKey.html"
  },
  "iam:UpdateServerCertificate": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::ServerCertificate": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to update the name or the path of the specified server certificate stored in IAM",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateServerCertificate.html"
  },
  "iam:UpdateServiceSpecificCredential": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to update the status of a service-specific credential to active or inactive for an IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateServiceSpecificCredential.html"
  },
  "iam:UpdateSigningCertificate": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to update the status of the specified user signing certificate to active or disabled",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateSigningCertificate.html"
  },
  "iam:UpdateUser": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to update the name or the path of the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateUser.html"
  },
  "iam:UploadSSHPublicKey": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to upload an SSH public key and associate it with the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UploadSSHPublicKey.html"
  },
  "iam:UploadServerCertificate": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::ServerCertificate": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to upload a server certificate entity for the AWS account",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UploadServerCertificate.html"
  },
  "iam:UploadSigningCertificate": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to upload an X.509 signing certificate and associate it with the specified IAM user",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/APIReference/API_UploadSigningCertificate.html"
  },
  "lambda:AddLayerVersionPermission": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Lambda::LayerVersion": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to add permissions to the resource-based policy of a version of an AWS Lambda layer",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_AddLayerVersionPermission.html"
  },
  "lambda:AddPermission": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to give an AWS service or another account permission to use an AWS Lambda function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_AddPermission.html"
  },
  "lambda:CreateAlias": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create an alias for a Lambda function version",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_CreateAlias.html"
  },
  "lambda:CreateEventSourceMapping": {
    "Access": "Write",
    "Affects": {},
    "Description": "Grants permission to create a mapping between an event source and an AWS Lambda function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_CreateEventSourceMapping.html"
  },
  "lambda:CreateFunction": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create an AWS Lambda function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_CreateFunction.html"
  },
  "lambda:DeleteAlias": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete an AWS Lambda function alias",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_DeleteAlias.html"
  },
  "lambda:DeleteEventSourceMapping": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::EventSourceMapping": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete an AWS Lambda event source mapping",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_DeleteEventSourceMapping.html"
  },
  "lambda:DeleteFunction": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete an AWS Lambda function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_DeleteFunction.html"
  },
  "lambda:DeleteFunctionConcurrency": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to remove a concurrent execution limit from an AWS Lambda function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_DeleteFunctionConcurrency.html"
  },
  "lambda:DeleteFunctionEventInvokeConfig": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete the configuration for asynchronous invocation for an AWS Lambda function, version, or alias",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_DeleteFunctionEventInvokeConfig.html"
  },
  "lambda:DeleteLayerVersion": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::LayerVersion": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete a version of an AWS Lambda layer",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_DeleteLayerVersion.html"
  },
  "lambda:DeleteProvisionedConcurrencyConfig": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to delete the provisioned concurrency configuration for an AWS Lambda function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_DeleteProvisionedConcurrencyConfig.html"
  },
  "lambda:DisableReplication": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to disable replication for a Lambda@Edge function",
    "Reference": ""
  },
  "lambda:EnableReplication": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to enable replication for a Lambda@Edge function",
    "Reference": ""
  },
  "lambda:GetAccountSettings": {
    "Access": "Read",
    "Affects": {},
    "Description": "Grants permission to view details about an account's limits and usage in an AWS Region",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_GetAccountSettings.html"
  },
  "lambda:GetAlias": {
    "Access": "Read",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to view details about an AWS Lambda function alias",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_GetAlias.html"
  },
  "lambda:GetEventSourceMapping": {
    "Access": "Read",
    "Affects": {
      "AWS::Lambda::EventSourceMapping": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to view details about an AWS Lambda event source mapping",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_GetEventSourceMapping.html"
  },
  "lambda:GetFunction": {
    "Access": "Read",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to view details about an AWS Lambda function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_GetFunction.html"
  },
  "lambda:GetFunctionConcurrency": {
    "Access": "Read",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to view details about the reserved concurrency configuration for a function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_GetFunctionConcurrency.html"
  },
  "lambda:GetFunctionConfiguration": {
    "Access": "Read",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to view details about the version-specific settings of an AWS Lambda function or version",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_GetFunctionConfiguration.html"
  },
  "lambda:GetFunctionEventInvokeConfig": {
    "Access": "Read",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to view the configuration for asynchronous invocation for a function, version, or alias",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_GetFunctionEventInvokeConfig.html"
  },
  "lambda:GetLayerVersion": {
    "Access": "Read",
    "Affects": {
      "AWS::Lambda::LayerVersion": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to view details about a version of an AWS Lambda layer",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_GetLayerVersion.html"
  },
  "lambda:GetLayerVersionByArn": {
    "Access": "Read",
    "Affects": {
      "AWS::Lambda::LayerVersion": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to view details about a version of an AWS Lambda layer",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_GetLayerVersionByArn.html"
  },
  "lambda:GetLayerVersionPolicy": {
    "Access": "Read",
    "Affects": {
      "AWS::Lambda::LayerVersion": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to view the resource-based policy for a version of an AWS Lambda layer",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_GetLayerVersionPolicy.html"
  },
  "lambda:GetPolicy": {
    "Access": "Read",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to view the resource-based policy for an AWS Lambda function, version, or alias",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_GetPolicy.html"
  },
  "lambda:GetProvisionedConcurrencyConfig": {
    "Access": "Read",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to view the provisioned concurrency configuration for an AWS Lambda function's alias or version",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_GetProvisionedConcurrencyConfig.html"
  },
  "lambda:InvokeAsync": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "(Deprecated) Grants permission to invoke a function asynchronously",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_InvokeAsync.html"
  },
  "lambda:InvokeFunction": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to invoke an AWS Lambda function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html"
  },
  "lambda:ListAliases": {
    "Access": "List",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve a list of aliases for an AWS Lambda function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_ListAliases.html"
  },
  "lambda:ListEventSourceMappings": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to retrieve a list of AWS Lambda event source mappings",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_ListEventSourceMappings.html"
  },
  "lambda:ListFunctionEventInvokeConfigs": {
    "Access": "List",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve a list of configurations for asynchronous invocation for a function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_ListFunctionEventInvokeConfigs.html"
  },
  "lambda:ListFunctions": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to retrieve a list of AWS Lambda functions, with the version-specific configuration of each function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_ListFunctions.html"
  },
  "lambda:ListLayerVersions": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to retrieve a list of versions of an AWS Lambda layer",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_ListLayerVersions.html"
  },
  "lambda:ListLayers": {
    "Access": "List",
    "Affects": {},
    "Description": "Grants permission to retrieve a list of AWS Lambda layers, with details about the latest version of each layer",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_ListLayers.html"
  },
  "lambda:ListProvisionedConcurrencyConfigs": {
    "Access": "List",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve a list of provisioned concurrency configurations for an AWS Lambda function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_ListProvisionedConcurrencyConfigs.html"
  },
  "lambda:ListTags": {
    "Access": "Read",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve a list of tags for an AWS Lambda function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_ListTags.html"
  },
  "lambda:ListVersionsByFunction": {
    "Access": "List",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to retrieve a list of versions for an AWS Lambda function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_ListVersionsByFunction.html"
  },
  "lambda:PublishLayerVersion": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Layer": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Lambda::LayerVersion": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create an AWS Lambda layer",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_PublishLayerVersion.html"
  },
  "lambda:PublishVersion": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to create an AWS Lambda function version",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_PublishVersion.html"
  },
  "lambda:PutFunctionConcurrency": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to configure reserved concurrency for an AWS Lambda function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_PutFunctionConcurrency.html"
  },
  "lambda:PutFunctionEventInvokeConfig": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to configures options for asynchronous invocation on an AWS Lambda function, version, or alias",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_PutFunctionEventInvokeConfig.html"
  },
  "lambda:PutProvisionedConcurrencyConfig": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to configure provisioned concurrency for an AWS Lambda function's alias or version",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_PutProvisionedConcurrencyConfig.html"
  },
  "lambda:RemoveLayerVersionPermission": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Lambda::LayerVersion": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to remove a statement from the permissions policy for a version of an AWS Lambda layer",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_RemoveLayerVersionPermission.html"
  },
  "lambda:RemovePermission": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to revoke function-use permission from an AWS service or another account",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_RemovePermission.html"
  },
  "lambda:TagResource": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to add tags to an AWS Lambda function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_TagResources.html"
  },
  "lambda:UntagResource": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to remove tags from an AWS Lambda function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_UntagResource.html"
  },
  "lambda:UpdateAlias": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to update the configuration of an AWS Lambda function's alias",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_UpdateAlias.html"
  },
  "lambda:UpdateEventSourceMapping": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::EventSourceMapping": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to update the configuration of an AWS Lambda event source mapping",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_UpdateEventSourceMapping.html"
  },
  "lambda:UpdateFunctionCode": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to update the code of an AWS Lambda function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_UpdateFunctionCode.html"
  },
  "lambda:UpdateFunctionConfiguration": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to modify the version-specific settings of an AWS Lambda function",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_UpdateFunctionConfiguration.html"
  },
  "lambda:UpdateFunctionEventInvokeConfig": {
    "Access": "Write",
    "Affects": {
      "AWS::Lambda::Function": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to modify the configuration for asynchronous invocation for an AWS Lambda function, version, or alias",
    "Reference": "https://docs.aws.amazon.com/lambda/latest/dg/API_UpdateFunctionEventInvokeConfig.html"
  },
  "s3:AbortMultipartUpload": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Aborts a multipart upload.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_AbortMultipartUpload.html"
  },
  "s3:BypassGovernanceRetention": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Allows circumvention of governance-mode object retention settings",
    "Reference": ""
  },
  "s3:CreateAccessPoint": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::AccessPoint": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Creates a new access point.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_CreateAccessPoint.html"
  },
  "s3:CreateBucket": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Creates a new bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_CreateBucket.html"
  },
  "s3:CreateJob": {
    "Access": "Write",
    "Affects": {},
    "Description": "Creates a new Amazon S3 Batch Operations job.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_CreateJob.html"
  },
  "s3:DeleteAccessPoint": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::AccessPoint": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Deletes the access point named in the URI",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_DeleteAccessPoint.html"
  },
  "s3:DeleteAccessPointPolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::S3::AccessPoint": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Delete the policy on a specified access point",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_DeleteAccessPointPolicy.html"
  },
  "s3:DeleteBucket": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Deletes the bucket named in the URI",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteBucket.html"
  },
  "s3:DeleteBucketPolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Delete the policy on a specified bucket",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteBucketPolicy.html"
  },
  "s3:DeleteBucketWebsite": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Removes the website configuration for a bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteBucketWebsite.html"
  },
  "s3:DeleteObject": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Removes the null version (if there is one) of an object and inserts a delete marker, which becomes the current version of the object.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteObject.html"
  },
  "s3:DeleteObjectTagging": {
    "Access": "Tagging",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "This implementation of the DELETE operation uses the tagging subresource to remove the entire tag set from the specified object.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteObjectTagging.html"
  },
  "s3:DeleteObjectVersion": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "To remove a specific version of a object, you must be the bucket owner and you must use the versionId subresource.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteObject.html"
  },
  "s3:DeleteObjectVersionTagging": {
    "Access": "Tagging",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "DELETE Object tagging (for a Specific Version of the Object)",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteObjectTagging.html"
  },
  "s3:DescribeJob": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Job": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Retrieves the configuration parameters and status for an Amazon S3 batch operations job.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_DescribeJob.html"
  },
  "s3:GetAccelerateConfiguration": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "This implementation of the GET operation uses the accelerate subresource to return the Transfer Acceleration state of a bucket, which is either Enabled or Suspended.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketAccelerateConfiguration.html"
  },
  "s3:GetAccessPoint": {
    "Access": "Read",
    "Affects": {},
    "Description": "Retrieve access point metadata",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_GetAccessPoint.html"
  },
  "s3:GetAccessPointPolicy": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::AccessPoint": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Return the policy of a specified access point.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_GetAccessPointPolicy.html"
  },
  "s3:GetAccessPointPolicyStatus": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::AccessPoint": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Retrieve the policy status for an specific access point's policy",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_GetAccessPointPolicyStatus.html"
  },
  "s3:GetAccountPublicAccessBlock": {
    "Access": "Read",
    "Affects": {},
    "Description": "Retrieve the PublicAccessBlock configuration for an AWS account",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_GetPublicAccessBlock.html"
  },
  "s3:GetAnalyticsConfiguration": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "This implementation of the GET operation returns an analytics configuration (identified by the analytics configuration ID) from the bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketAnalyticsConfiguration.html"
  },
  "s3:GetBucketAcl": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Return the access control list (ACL) of a bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketAcl.html"
  },
  "s3:GetBucketCORS": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Returns the CORS configuration information set for the bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketCors.html"
  },
  "s3:GetBucketLocation": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Return a bucket's region.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketLocation.html"
  },
  "s3:GetBucketLogging": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Return the logging status of a bucket and the permissions users have to view and modify that status.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketLogging.html"
  },
  "s3:GetBucketNotification": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Return the notification configuration of a bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketNotification.html"
  },
  "s3:GetBucketObjectLockConfiguration": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "GET Object Lock configuration for a specific bucket",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObjectLockConfiguration.html"
  },
  "s3:GetBucketPolicy": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Return the policy of a specified bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketPolicy.html"
  },
  "s3:GetBucketPolicyStatus": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Retrieve the policy status for an specific S3 bucket, indicating whether the bucket is public.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketPolicyStatus.html"
  },
  "s3:GetBucketPublicAccessBlock": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Retrieve the PublicAccessBlock configuration for a specific S3 bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetPublicAccessBlock.html"
  },
  "s3:GetBucketRequestPayment": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Return the request payment configuration of a bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketRequestPayment.html"
  },
  "s3:GetBucketTagging": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Return the tag set associated with the bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketTagging.html"
  },
  "s3:GetBucketVersioning": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Return the versioning state of a bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketVersioning.html"
  },
  "s3:GetBucketWebsite": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Returns the website configuration associated with a bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketWebsite.html"
  },
  "s3:GetEncryptionConfiguration": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Returns the encryption configuration information set on the bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketEncryption.html"
  },
  "s3:GetInventoryConfiguration": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "This implementation of the GET operation returns an inventory configuration (identified by the inventory configuration ID) from the bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketInventoryConfiguration.html"
  },
  "s3:GetLifecycleConfiguration": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Returns the lifecycle configuration information set on the bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketLifecycleConfiguration.html"
  },
  "s3:GetMetricsConfiguration": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Gets a metrics configuration for the CloudWatch request metrics (specified by the metrics configuration ID) from the bucket. Note that this doesn't include the daily storage metrics.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketMetricsConfiguration.html"
  },
  "s3:GetObject": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Retrieves objects from Amazon S3.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html"
  },
  "s3:GetObjectAcl": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Return the access control list (ACL) of an object.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObjectAcl.html"
  },
  "s3:GetObjectLegalHold": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "GET Object Legal Hold for a specific object",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObjectLegalHold.html"
  },
  "s3:GetObjectRetention": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "GET Object Legal Hold for a specific object",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObjectRetention.html"
  },
  "s3:GetObjectTagging": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "This implementation of the GET operation returns the tags associated with an object. You send the GET request against the tagging subresource associated with the object.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObjectTagging.html"
  },
  "s3:GetObjectTorrent": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "return torrent files from a bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObjectTorrent.html"
  },
  "s3:GetObjectVersion": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "To return a different version, use the versionId subresource.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html"
  },
  "s3:GetObjectVersionAcl": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "To return ACL information about a different version, use the versionId subresource.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObjectAcl.html"
  },
  "s3:GetObjectVersionForReplication": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Permission exercised by S3 replication",
    "Reference": ""
  },
  "s3:GetObjectVersionTagging": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "GET Object tagging (for a Specific Version of the Object)",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObjectTagging.html"
  },
  "s3:GetObjectVersionTorrent": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "To return Torrent files about a different version, use the versionId subresource.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObjectTorrent.html"
  },
  "s3:GetReplicationConfiguration": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Returns the replication configuration information set on the bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketReplication.html"
  },
  "s3:ListAccessPoints": {
    "Access": "Read",
    "Affects": {},
    "Description": "Lists access points.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_ListAccessPoints.html"
  },
  "s3:ListAllMyBuckets": {
    "Access": "List",
    "Affects": {},
    "Description": "Returns a list of all buckets owned by the authenticated sender of the request.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListBuckets.html"
  },
  "s3:ListBucket": {
    "Access": "List",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Returns some or all (up to 1000) of the objects in a bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListBuckets.html"
  },
  "s3:ListBucketMultipartUploads": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Lists in-progress multipart uploads.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListMultipartUploads.html"
  },
  "s3:ListBucketVersions": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Use the versions subresource to list metadata about all of the versions of objects in a bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListBuckets.html"
  },
  "s3:ListJobs": {
    "Access": "Read",
    "Affects": {},
    "Description": "Lists current jobs and jobs that have ended recently.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_ListJobs.html"
  },
  "s3:ListMultipartUploadParts": {
    "Access": "Read",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Lists the parts that have been uploaded for a specific multipart upload.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListParts.html"
  },
  "s3:ObjectOwnerOverrideToBucketOwner": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Permission exercised by S3 replication",
    "Reference": ""
  },
  "s3:PutAccelerateConfiguration": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "This implementation of the PUT operation uses the accelerate subresource to set the Transfer Acceleration state of an existing bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketAccelerateConfiguration.html"
  },
  "s3:PutAccessPointPolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::S3::AccessPoint": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Add to or replace a data policy on a access point.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_PutAccessPointPolicy.html"
  },
  "s3:PutAccountPublicAccessBlock": {
    "Access": "Permissions Management",
    "Affects": {},
    "Description": "Create or modify the PublicAccessBlock configuration for an AWS account.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_PutPublicAccessBlock.html"
  },
  "s3:PutAnalyticsConfiguration": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "This implementation of the PUT operation adds an analytics configuration (identified by the analytics ID) to the bucket. You can have up to 1,000 analytics configurations per bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketAnalyticsConfiguration.html"
  },
  "s3:PutBucketAcl": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Set the permissions on an existing bucket using access control lists (ACL).",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketAcl.html"
  },
  "s3:PutBucketCORS": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Sets the CORS configuration for your bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketCors.html"
  },
  "s3:PutBucketLogging": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Set the logging parameters for a bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketLogging.html"
  },
  "s3:PutBucketNotification": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Enables you to receive notifications when certain events happen in your bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketNotification.html"
  },
  "s3:PutBucketObjectLockConfiguration": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "PUT Object Lock configuration on a specific bucket",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObjectLockConfiguration.html"
  },
  "s3:PutBucketPolicy": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Add to or replace a policy on a bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketPolicy.html"
  },
  "s3:PutBucketPublicAccessBlock": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Create or modify the PublicAccessBlock configuration for an specific S3 bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutPublicAccessBlock.html"
  },
  "s3:PutBucketRequestPayment": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Set the request payment configuration of a bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketRequestPayment.html"
  },
  "s3:PutBucketTagging": {
    "Access": "Tagging",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Add a set of tags to an existing bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketTagging.html"
  },
  "s3:PutBucketVersioning": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Set the versioning state of an existing bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketVersioning.html"
  },
  "s3:PutBucketWebsite": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Sets the configuration of the website that is specified in the website subresource.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketWebsite.html"
  },
  "s3:PutEncryptionConfiguration": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Sets the encryption configuration for the bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketEncryption.html"
  },
  "s3:PutInventoryConfiguration": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "This implementation of the PUT operation adds an inventory configuration (identified by the inventory ID) to the bucket. You can have up to 1,000 inventory configurations per bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketInventoryConfiguration.html"
  },
  "s3:PutLifecycleConfiguration": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Creates a new lifecycle configuration for the bucket or replaces an existing lifecycle configuration.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketLifecycleConfiguration.html"
  },
  "s3:PutMetricsConfiguration": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Sets or updates a metrics configuration for the CloudWatch request metrics (specified by the metrics configuration ID) from the bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketMetricsConfiguration.html"
  },
  "s3:PutObject": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Adds an object to a bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObject.html"
  },
  "s3:PutObjectAcl": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Set the access control list (ACL) permissions for an object that already exists in a bucket.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObjectAcl.html"
  },
  "s3:PutObjectLegalHold": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "PUT Object Legal Hold on a specific object",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObjectLegalHold.html"
  },
  "s3:PutObjectRetention": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "PUT Object Retention on a specific object",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObjectRetention.html"
  },
  "s3:PutObjectTagging": {
    "Access": "Tagging",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "This implementation of the PUT operation uses the tagging subresource to add a set of tags to an existing object.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObjectTagging.html"
  },
  "s3:PutObjectVersionAcl": {
    "Access": "Permissions Management",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "The ACL of an object is set at the object version level.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObjectAcl.html"
  },
  "s3:PutObjectVersionTagging": {
    "Access": "Tagging",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "PUT Object tagging (for a Specific Version of the Object)",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObjectTagging.html"
  },
  "s3:PutReplicationConfiguration": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Bucket": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "In a versioning-enabled bucket, this operation creates a new replication configuration (or replaces an existing one, if present).",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketReplication.html"
  },
  "s3:ReplicateDelete": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Permission exercised by S3 replication",
    "Reference": ""
  },
  "s3:ReplicateObject": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Permission exercised by S3 replication",
    "Reference": ""
  },
  "s3:ReplicateTags": {
    "Access": "Tagging",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Permission exercised by S3 replication",
    "Reference": ""
  },
  "s3:RestoreObject": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Object": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Restores a temporary copy of an archived object.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_RestoreObject.html"
  },
  "s3:UpdateJobPriority": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Job": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Updates an existing job's priority.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_UpdateJobPriority.html"
  },
  "s3:UpdateJobStatus": {
    "Access": "Write",
    "Affects": {
      "AWS::S3::Job": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Updates the status for the specified job.",
    "Reference": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_UpdateJobStatus.html"
  },
  "sts:AssumeRole": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Returns a set of temporary security credentials that you can use to access AWS resources that you might not normally have access to",
    "Reference": "https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html"
  },
  "sts:AssumeRoleWithSAML": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Returns a set of temporary security credentials for users who have been authenticated via a SAML authentication response",
    "Reference": "https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithSAML.html"
  },
  "sts:AssumeRoleWithWebIdentity": {
    "Access": "Write",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Returns a set of temporary security credentials for users who have been authenticated in a mobile or web application with a web identity provider",
    "Reference": "https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithWebIdentity.html"
  },
  "sts:DecodeAuthorizationMessage": {
    "Access": "Write",
    "Affects": {},
    "Description": "Decodes additional information about the authorization status of a request from an encoded message returned in response to an AWS request",
    "Reference": "https://docs.aws.amazon.com/STS/latest/APIReference/API_DecodeAuthorizationMessage.html"
  },
  "sts:GetAccessKeyInfo": {
    "Access": "Read",
    "Affects": {},
    "Description": "Returns details about the access key id passed as a parameter to the request.",
    "Reference": "https://docs.aws.amazon.com/STS/latest/APIReference/API_GetAccessKeyInfo.html"
  },
  "sts:GetCallerIdentity": {
    "Access": "Read",
    "Affects": {},
    "Description": "Returns details about the IAM identity whose credentials are used to call the API",
    "Reference": "https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html"
  },
  "sts:GetFederationToken": {
    "Access": "Read",
    "Affects": {
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Returns a set of temporary security credentials (consisting of an access key ID, a secret access key, and a security token) for a federated user",
    "Reference": "https://docs.aws.amazon.com/STS/latest/APIReference/API_GetFederationToken.html"
  },
  "sts:GetSessionToken": {
    "Access": "Read",
    "Affects": {},
    "Description": "Returns a set of temporary security credentials (consisting of an access key ID, a secret access key, and a security token) for an AWS account or IAM user",
    "Reference": "https://docs.aws.amazon.com/STS/latest/APIReference/API_GetSessionToken.html"
  },
  "sts:TagSession": {
    "Access": "Tagging",
    "Affects": {
      "AWS::Iam::Role": {
        "Condition Keys": [],
        "Dependant Actions": []
      },
      "AWS::Iam::User": {
        "Condition Keys": [],
        "Dependant Actions": []
      }
    },
    "Description": "Grants permission to add tags to a STS session",
    "Reference": "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html"
  }
}
