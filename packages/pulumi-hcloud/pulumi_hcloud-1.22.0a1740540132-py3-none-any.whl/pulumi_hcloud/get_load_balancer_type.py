# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from . import _utilities

__all__ = [
    'GetLoadBalancerTypeResult',
    'AwaitableGetLoadBalancerTypeResult',
    'get_load_balancer_type',
    'get_load_balancer_type_output',
]

@pulumi.output_type
class GetLoadBalancerTypeResult:
    """
    A collection of values returned by getLoadBalancerType.
    """
    def __init__(__self__, description=None, id=None, max_assigned_certificates=None, max_connections=None, max_services=None, max_targets=None, name=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, int):
            raise TypeError("Expected argument 'id' to be a int")
        pulumi.set(__self__, "id", id)
        if max_assigned_certificates and not isinstance(max_assigned_certificates, int):
            raise TypeError("Expected argument 'max_assigned_certificates' to be a int")
        pulumi.set(__self__, "max_assigned_certificates", max_assigned_certificates)
        if max_connections and not isinstance(max_connections, int):
            raise TypeError("Expected argument 'max_connections' to be a int")
        pulumi.set(__self__, "max_connections", max_connections)
        if max_services and not isinstance(max_services, int):
            raise TypeError("Expected argument 'max_services' to be a int")
        pulumi.set(__self__, "max_services", max_services)
        if max_targets and not isinstance(max_targets, int):
            raise TypeError("Expected argument 'max_targets' to be a int")
        pulumi.set(__self__, "max_targets", max_targets)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the Load Balancer Type.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> int:
        """
        ID of the Load Balancer Type.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="maxAssignedCertificates")
    def max_assigned_certificates(self) -> int:
        """
        Maximum number of certificates that can be assigned for the Load Balancer of this type.
        """
        return pulumi.get(self, "max_assigned_certificates")

    @property
    @pulumi.getter(name="maxConnections")
    def max_connections(self) -> int:
        """
        Maximum number of simultaneous open connections for the Load Balancer of this type.
        """
        return pulumi.get(self, "max_connections")

    @property
    @pulumi.getter(name="maxServices")
    def max_services(self) -> int:
        """
        Maximum number of services for the Load Balancer of this type.
        """
        return pulumi.get(self, "max_services")

    @property
    @pulumi.getter(name="maxTargets")
    def max_targets(self) -> int:
        """
        Maximum number of targets for the Load Balancer of this type.
        """
        return pulumi.get(self, "max_targets")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the Load Balancer Type.
        """
        return pulumi.get(self, "name")


class AwaitableGetLoadBalancerTypeResult(GetLoadBalancerTypeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLoadBalancerTypeResult(
            description=self.description,
            id=self.id,
            max_assigned_certificates=self.max_assigned_certificates,
            max_connections=self.max_connections,
            max_services=self.max_services,
            max_targets=self.max_targets,
            name=self.name)


def get_load_balancer_type(id: Optional[int] = None,
                           name: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLoadBalancerTypeResult:
    """
    Provides details about a specific Hetzner Cloud Load Balancer Type.

    Use this resource to get detailed information about a specific Load Balancer Type.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_hcloud as hcloud

    by_id = hcloud.get_load_balancer_type(id=1)
    by_name = hcloud.get_load_balancer_type(name="lb11")
    main = hcloud.LoadBalancer("main",
        name="my-load-balancer",
        load_balancer_type=name,
        location="fsn1")
    ```


    :param int id: ID of the Load Balancer Type.
    :param str name: Name of the Load Balancer Type.
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('hcloud:index/getLoadBalancerType:getLoadBalancerType', __args__, opts=opts, typ=GetLoadBalancerTypeResult).value

    return AwaitableGetLoadBalancerTypeResult(
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        max_assigned_certificates=pulumi.get(__ret__, 'max_assigned_certificates'),
        max_connections=pulumi.get(__ret__, 'max_connections'),
        max_services=pulumi.get(__ret__, 'max_services'),
        max_targets=pulumi.get(__ret__, 'max_targets'),
        name=pulumi.get(__ret__, 'name'))
def get_load_balancer_type_output(id: Optional[pulumi.Input[Optional[int]]] = None,
                                  name: Optional[pulumi.Input[Optional[str]]] = None,
                                  opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetLoadBalancerTypeResult]:
    """
    Provides details about a specific Hetzner Cloud Load Balancer Type.

    Use this resource to get detailed information about a specific Load Balancer Type.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_hcloud as hcloud

    by_id = hcloud.get_load_balancer_type(id=1)
    by_name = hcloud.get_load_balancer_type(name="lb11")
    main = hcloud.LoadBalancer("main",
        name="my-load-balancer",
        load_balancer_type=name,
        location="fsn1")
    ```


    :param int id: ID of the Load Balancer Type.
    :param str name: Name of the Load Balancer Type.
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['name'] = name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('hcloud:index/getLoadBalancerType:getLoadBalancerType', __args__, opts=opts, typ=GetLoadBalancerTypeResult)
    return __ret__.apply(lambda __response__: GetLoadBalancerTypeResult(
        description=pulumi.get(__response__, 'description'),
        id=pulumi.get(__response__, 'id'),
        max_assigned_certificates=pulumi.get(__response__, 'max_assigned_certificates'),
        max_connections=pulumi.get(__response__, 'max_connections'),
        max_services=pulumi.get(__response__, 'max_services'),
        max_targets=pulumi.get(__response__, 'max_targets'),
        name=pulumi.get(__response__, 'name')))
