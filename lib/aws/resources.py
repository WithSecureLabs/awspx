
import re


class Resources(dict):

    # https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-aws-service-namespaces

    types = {
        "AWS::Account":                                                        "arn:aws:iam::{Account}:root",
        "AWS::Ec2::CapacityReservation":                                       "arn:aws:ec2:{Region}:{Account}:capacity-reservation/{ReservationId}",
        "AWS::Ec2::CarrierGateway":                                            "arn:aws:ec2:{Region}:{Account}:carrier-gateway/{CarrierGatewayId}",
        "AWS::Ec2::Certificate":                                               "arn:aws:acm:{Region}:{Account}:certificate/{CertificateId}",
        "AWS::Ec2::ClientVpnEndpoint":                                         "arn:aws:ec2:{Region}:{Account}:client-vpn-endpoint/{EndpointId}",
        "AWS::Ec2::CustomerGateway":                                           "arn:aws:ec2:{Region}:{Account}:customer-gateway/{CgwId}",
        "AWS::Ec2::DedicatedHost":                                             "arn:aws:ec2:{Region}:{Account}:dedicated-host/{DedicatedHostId}",
        "AWS::Ec2::DhcpOptions":                                               "arn:aws:ec2:{Region}:{Account}:dhcp-options/{DhcpOptionsId}",
        "AWS::Ec2::EgressOnlyInternetGateway":                                 "arn:aws:ec2:{Region}:{Account}:egress-only-internet-gateway/{EgressOnlyInternetGatewayId}",
        "AWS::Ec2::ElasticGpu":                                                "arn:aws:ec2:{Region}:{Account}:elastic-gpu/{ElasticGpuId}",
        "AWS::Ec2::ElasticIp":                                                 "arn:aws:ec2:{Region}:{Account}:elastic-ip/{AllocationId}",
        "AWS::Ec2::ExportImageTask":                                           "arn:aws:ec2:{Region}:{Account}:export-image-task/{ExportImageTaskId}",
        "AWS::Ec2::ExportInstanceTask":                                        "arn:aws:ec2:{Region}:{Account}:export-instance-task/{ExportTaskId}",
        "AWS::Ec2::Fleet":                                                     "arn:aws:ec2:{Region}:{Account}:fleet/{FleetId}",
        "AWS::Ec2::FpgaImage":                                                 "arn:aws:ec2:{Region}::fpga-image/{Name}",
        "AWS::Ec2::HostReservation":                                           "arn:aws:ec2:{Region}:{Account}:host-reservation/{HostReservationId}",
        "AWS::Ec2::Image":                                                     "arn:aws:ec2:{Region}:({Account})?:image/{ImageId}",
        "AWS::Ec2::ImportImageTask":                                           "arn:aws:ec2:{Region}:{Account}:import-image-task/{ImportImageTaskId}",
        "AWS::Ec2::ImportSnapshotTask":                                        "arn:aws:ec2:{Region}:{Account}:import-snapshot-task/{ImportSnapshotTaskId}",
        "AWS::Ec2::Instance":                                                  "arn:aws:ec2:{Region}:{Account}:instance/{InstanceId}",
        "AWS::Ec2::InternetGateway":                                           "arn:aws:ec2:{Region}:{Account}:internet-gateway/{InternetGatewayId}",
        "AWS::Ec2::Ipv4PoolEc2":                                               "arn:aws:ec2:{Region}:{Account}:ipv4pool-ec2/{Ipv4PoolEc2Id}",
        "AWS::Ec2::Ipv6PoolEc2":                                               "arn:aws:ec2:{Region}:{Account}:ipv6pool-ec2/{Ipv6PoolEc2Id}",
        "AWS::Ec2::KeyPair":                                                   "arn:aws:ec2:{Region}:{Account}:key-pair/{KeyName}",
        "AWS::Ec2::LaunchTemplate":                                            "arn:aws:ec2:{Region}:{Account}:launch-template/{LaunchTemplateId}",
        "AWS::Ec2::LocalGateway":                                              "arn:aws:ec2:{Region}:{Account}:local-gateway/{LocalGatewayId}",
        "AWS::Ec2::LocalGatewayRouteTable":                                    "arn:aws:ec2:{Region}:{Account}:local-gateway-route-table/{LocalGatewayRouteTableId}",
        "AWS::Ec2::LocalGatewayRouteTableVirtualInterfaceGroupAssociation":    "arn:aws:ec2:{Region}:{Account}:local-gateway-route-table-virtual-interface-group-association/{LocalGatewayRouteTableVirtualInterfaceGroupAssociationId}",
        "AWS::Ec2::LocalGatewayRouteTableVpcAssociation":                      "arn:aws:ec2:{Region}:{Account}:local-gateway-route-table-vpc-association/{LocalGatewayRouteTableVpcAssociationId}",
        "AWS::Ec2::LocalGatewayVirtualInterface":                              "arn:aws:ec2:{Region}:{Account}:local-gateway-virtual-interface/{LocalGatewayVirtualInterfaceId}",
        "AWS::Ec2::LocalGatewayVirtualInterfaceGroup":                         "arn:aws:ec2:{Region}:{Account}:local-gateway-virtual-interface-group/{LocalGatewayVirtualInterfaceGroupId}",
        "AWS::Ec2::NatGateway":                                                "arn:aws:ec2:{Region}:{Account}:natgateway/{NatGatewayId}",
        "AWS::Ec2::NetworkAcl":                                                "arn:aws:ec2:{Region}:{Account}:network-acl/{NetworkAclId}",
        "AWS::Ec2::NetworkInsightsAnalysis":                                   "arn:aws:ec2:{Region}:{Account}:network-insights-analysis/{NetworkInsightsAnalysisId}",
        "AWS::Ec2::NetworkInsightsPath":                                       "arn:aws:ec2:{Region}:{Account}:network-insights-path/{NetworkInsightsPathId}",
        "AWS::Ec2::NetworkInterface":                                          "arn:aws:ec2:{Region}:{Account}:network-interface/{NetworkInterfaceId}",
        "AWS::Ec2::PlacementGroup":                                            "arn:aws:ec2:{Region}:{Account}:placement-group/{GroupName}",
        "AWS::Ec2::PrefixList":                                                "arn:aws:ec2:{Region}:{Account}:prefix-list/{PrefixListId}",
        "AWS::Ec2::ReservedInstances":                                         "arn:aws:ec2:{Region}:{Account}:reserved-instances/{ReservationId}",
        "AWS::Ec2::RouteTable":                                                "arn:aws:ec2:{Region}:{Account}:route-table/{RouteTableId}",
        "AWS::Ec2::SecurityGroup":                                             "arn:aws:ec2:{Region}:{Account}:security-group/{GroupId}",
        "AWS::Ec2::Snapshot":                                                  "arn:aws:ec2:{Region}::snapshot/{SnapshotId}",
        "AWS::Ec2::SpotFleetRequest":                                          "arn:aws:ec2:{Region}:{Account}:spot-fleet-request/{SpotFleetRequestId}",
        "AWS::Ec2::SpotInstanceRequest":                                       "arn:aws:ec2:{Region}::spot-instance-request/{Name}",
        "AWS::Ec2::SpotInstancesRequest":                                      "arn:aws:ec2:{Region}:{Account}:spot-instances-request/{SpotInstanceRequestId}",
        "AWS::Ec2::Subnet":                                                    "arn:aws:ec2:{Region}:{Account}:subnet/{SubnetId}",
        "AWS::Ec2::TrafficMirrorFilter":                                       "arn:aws:ec2:{Region}:{Account}:traffic-mirror-filter/{TrafficMirrorFilterId}",
        "AWS::Ec2::TrafficMirrorFilterRule":                                   "arn:aws:ec2:{Region}:{Account}:traffic-mirror-filter-rule/{TrafficMirrorFilterRuleId}",
        "AWS::Ec2::TrafficMirrorSession":                                      "arn:aws:ec2:{Region}:{Account}:traffic-mirror-session/{TrafficMirrorSessionId}",
        "AWS::Ec2::TrafficMirrorTarget":                                       "arn:aws:ec2:{Region}:{Account}:traffic-mirror-target/{TrafficMirrorTargetId}",
        "AWS::Ec2::TransitGateway":                                            "arn:aws:ec2:{Region}:{Account}:transit-gateway/{TgwId}",
        "AWS::Ec2::TransitGatewayAttachment":                                  "arn:aws:ec2:{Region}:{Account}:transit-gateway-attachment/{TgwattachmentId}",
        "AWS::Ec2::TransitGatewayConnectPeer":                                 "arn:aws:ec2:{Region}:{Account}:transit-gateway-connect-peer/{TransitGatewayConnectPeerId}",
        "AWS::Ec2::TransitGatewayMulticastDomain":                             "arn:aws:ec2:{Region}:{Account}:transit-gateway-multicast-domain/{TransitGatewayMulticastDomainId}",
        "AWS::Ec2::TransitGatewayRouteTable":                                  "arn:aws:ec2:{Region}:{Account}:transit-gateway-route-table/{TgwroutetableId}",
        "AWS::Ec2::Volume":                                                    "arn:aws:ec2:{Region}:{Account}:volume/{VolumeId}",
        "AWS::Ec2::Vpc":                                                       "arn:aws:ec2:{Region}:{Account}:vpc/{VpcId}",
        "AWS::Ec2::VpcEndpoint":                                               "arn:aws:ec2:{Region}:{Account}:vpc-endpoint/{VpcEndpointId}",
        "AWS::Ec2::VpcEndpointService":                                        "arn:aws:ec2:{Region}:{Account}:vpc-endpoint-service/{VpcEndpointServiceId}",
        "AWS::Ec2::VpcFlowLog":                                                "arn:aws:ec2:{Region}:{Account}:vpc-flow-log/{VpcFlowLogId}",
        "AWS::Ec2::VpcPeeringConnection":                                      "arn:aws:ec2:{Region}:{Account}:vpc-peering-connection/{VpcPeeringConnectionId}",
        "AWS::Ec2::VpnConnection":                                             "arn:aws:ec2:{Region}:{Account}:vpn-connection/{VpnConnectionId}",
        "AWS::Ec2::VpnGateway":                                                "arn:aws:ec2:{Region}:{Account}:vpn-gateway/{VpnGatewaygwId}",
        "AWS::ElasticInference::Accelerator":                                  "arn:aws:elastic-inference:{Region}:{Account}:elastic-inference-accelerator/{ElasticInferenceAcceleratorId}",
        "AWS::Iam::AccessReport":                                              "arn:aws:iam::{Account}:access-report/{EntityPath}",
        "AWS::Iam::AssumedRole":                                               "arn:aws:iam::{Account}:assumed-role/{Role}/{RoleSessionName}",
        "AWS::Iam::FederatedUser":                                             "arn:aws:iam::{Account}:federated-user/{User}",
        "AWS::Iam::Group":                                                     "arn:aws:iam::{Account}:group/{Group}",
        "AWS::Iam::InstanceProfile":                                           "arn:aws:iam::{Account}:instance-profile/{InstanceProfile}",
        "AWS::Iam::MfaDevice":                                                 "arn:aws:iam::{Account}:u2f/user/{UserName}/{MfaDevice}",
        "AWS::Iam::OidcProvider":                                              "arn:aws:iam::{Account}:oidc-provider/{Provider}",
        "AWS::Iam::Policy":                                                    "arn:aws:iam::{Account}:policy/{Policy}",
        "AWS::Iam::Role":                                                      "arn:aws:iam::{Account}:role/{Role}",
        "AWS::Iam::SamlProvider":                                              "arn:aws:iam::{Account}:saml-provider/{Provider}",
        "AWS::Iam::ServerCertificate":                                         "arn:aws:iam::{Account}:server-certificate/{Certificate}",
        "AWS::Iam::SmsMfa":                                                    "arn:aws:iam::{Account}:sms-mfa/{MfaTokenIdWithPath}",
        "AWS::Iam::U2f":                                                       "arn:aws:iam::{Account}:u2f/{U2FTokenId}",
        "AWS::Iam::User":                                                      "arn:aws:iam::{Account}:user/{UserName}",
        "AWS::Iam::VirtualMfaDevice":                                          "arn:aws:iam::{Account}:mfa/{UserName}",
        "AWS::Lambda::CodeSigningConfig":                                      "arn:aws:lambda:{Region}:{Account}:codesigningconfig:{CodeSigningConfigId}",
        "AWS::Lambda::EventSourceMapping":                                     "arn:aws:lambda:{Region}:{Account}:event-source-mapping:{EventSourceMappingId}",
        "AWS::Lambda::Function":                                               "arn:aws:lambda:{Region}:{Account}:function:{Function}(:{Alias})?",
        "AWS::Lambda::Layer":                                                  "arn:aws:lambda:{Region}:{Account}:layer:{Layer}$",
        "AWS::Lambda::LayerVersion":                                           "arn:aws:lambda:{Region}:{Account}:layer:{Layer}:{Version}",
        "AWS::S3::AccessPoint":                                                "arn:aws:s3:{Region}:{Account}:accesspoint/{AccessPoint}",
        "AWS::S3::Bucket":                                                     "arn:aws:s3:::{Name}",
        "AWS::S3::Job":                                                        "arn:aws:s3:{Region}:{Account}:job/{JobId}",
        "AWS::S3::Object":                                                     "arn:aws:s3:::{Name}/{Key}",
        "AWS::S3::ObjectLambdaAccessPoint":                                    "arn:aws:s3-object-lambda:{Region}:{Account}:accesspoint/{AccessPointName}",
        "AWS::S3::StorageLensConfiguration":                                   "arn:aws:s3:{Region}:{Account}:storage-lens/{ConfigId}"
    }
    regex = {
        "Region":   r"([a-z0-9-]*)",
        "Account":  r"(\d{12})?",
        "Provider": r"(.*)",
        "Key":      r"(.*)",
        "Default":  r"([A-Za-z0-9-_]*)",
    }

    def __init__(self):

        format_string = re.compile("{([A-Za-z]+)}")
        for k, v in self.types.items():
            self[k] = self.types[k]
            for placeholder in set(format_string.findall(v)):
                self[k] = self[k].replace(f"{{{placeholder}}}", "(?P<{placeholder}>{regex})".format(
                    placeholder=placeholder,
                    regex=str(self.regex[placeholder] if placeholder in self.regex
                              else self.regex["Default"])))
            self[k] += '$'

    def definition(self, k):
        if k not in self.types:
            return ""
        elif self.types[k][-1] == "$":
            return self.types[k][0:-1]
        else:
            return self.types[k]

    def label(self, arn):
        for k, v in self.items():
            if re.match(v, arn):
                return k
        return None


RESOURCES = Resources()
