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
    'GetImageResult',
    'AwaitableGetImageResult',
    'get_image',
    'get_image_output',
]

@pulumi.output_type
class GetImageResult:
    """
    A collection of values returned by getImage.
    """
    def __init__(__self__, architecture=None, created=None, deprecated=None, description=None, id=None, include_deprecated=None, labels=None, most_recent=None, name=None, os_flavor=None, os_version=None, rapid_deploy=None, selector=None, type=None, with_architecture=None, with_selector=None, with_statuses=None):
        if architecture and not isinstance(architecture, str):
            raise TypeError("Expected argument 'architecture' to be a str")
        pulumi.set(__self__, "architecture", architecture)
        if created and not isinstance(created, str):
            raise TypeError("Expected argument 'created' to be a str")
        pulumi.set(__self__, "created", created)
        if deprecated and not isinstance(deprecated, str):
            raise TypeError("Expected argument 'deprecated' to be a str")
        pulumi.set(__self__, "deprecated", deprecated)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, int):
            raise TypeError("Expected argument 'id' to be a int")
        pulumi.set(__self__, "id", id)
        if include_deprecated and not isinstance(include_deprecated, bool):
            raise TypeError("Expected argument 'include_deprecated' to be a bool")
        pulumi.set(__self__, "include_deprecated", include_deprecated)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if most_recent and not isinstance(most_recent, bool):
            raise TypeError("Expected argument 'most_recent' to be a bool")
        pulumi.set(__self__, "most_recent", most_recent)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if os_flavor and not isinstance(os_flavor, str):
            raise TypeError("Expected argument 'os_flavor' to be a str")
        pulumi.set(__self__, "os_flavor", os_flavor)
        if os_version and not isinstance(os_version, str):
            raise TypeError("Expected argument 'os_version' to be a str")
        pulumi.set(__self__, "os_version", os_version)
        if rapid_deploy and not isinstance(rapid_deploy, bool):
            raise TypeError("Expected argument 'rapid_deploy' to be a bool")
        pulumi.set(__self__, "rapid_deploy", rapid_deploy)
        if selector and not isinstance(selector, str):
            raise TypeError("Expected argument 'selector' to be a str")
        pulumi.set(__self__, "selector", selector)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if with_architecture and not isinstance(with_architecture, str):
            raise TypeError("Expected argument 'with_architecture' to be a str")
        pulumi.set(__self__, "with_architecture", with_architecture)
        if with_selector and not isinstance(with_selector, str):
            raise TypeError("Expected argument 'with_selector' to be a str")
        pulumi.set(__self__, "with_selector", with_selector)
        if with_statuses and not isinstance(with_statuses, list):
            raise TypeError("Expected argument 'with_statuses' to be a list")
        pulumi.set(__self__, "with_statuses", with_statuses)

    @property
    @pulumi.getter
    def architecture(self) -> str:
        """
        (string) Architecture of the Image.
        """
        return pulumi.get(self, "architecture")

    @property
    @pulumi.getter
    def created(self) -> str:
        """
        (string) Date when the Image was created (in ISO-8601 format).
        """
        return pulumi.get(self, "created")

    @property
    @pulumi.getter
    def deprecated(self) -> str:
        """
        (string) Point in time when the image is considered to be deprecated (in ISO-8601 format).
        """
        return pulumi.get(self, "deprecated")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        (string) Description of the Image.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> int:
        """
        (int) Unique ID of the Image.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="includeDeprecated")
    def include_deprecated(self) -> Optional[bool]:
        return pulumi.get(self, "include_deprecated")

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter(name="mostRecent")
    def most_recent(self) -> Optional[bool]:
        return pulumi.get(self, "most_recent")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        (string) Name of the Image, only present when the Image is of type `system`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="osFlavor")
    def os_flavor(self) -> str:
        """
        (string) Flavor of operating system contained in the image, could be `ubuntu`, `centos`, `debian`, `fedora` or `unknown`.
        """
        return pulumi.get(self, "os_flavor")

    @property
    @pulumi.getter(name="osVersion")
    def os_version(self) -> str:
        """
        (string) Operating system version.
        """
        return pulumi.get(self, "os_version")

    @property
    @pulumi.getter(name="rapidDeploy")
    def rapid_deploy(self) -> bool:
        """
        (bool) Indicates that rapid deploy of the image is available.
        """
        return pulumi.get(self, "rapid_deploy")

    @property
    @pulumi.getter
    @_utilities.deprecated("""Please use the with_selector property instead.""")
    def selector(self) -> Optional[str]:
        return pulumi.get(self, "selector")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        (string) Type of the Image, could be `system`, `backup` or `snapshot`.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="withArchitecture")
    def with_architecture(self) -> Optional[str]:
        return pulumi.get(self, "with_architecture")

    @property
    @pulumi.getter(name="withSelector")
    def with_selector(self) -> Optional[str]:
        return pulumi.get(self, "with_selector")

    @property
    @pulumi.getter(name="withStatuses")
    def with_statuses(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "with_statuses")


class AwaitableGetImageResult(GetImageResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetImageResult(
            architecture=self.architecture,
            created=self.created,
            deprecated=self.deprecated,
            description=self.description,
            id=self.id,
            include_deprecated=self.include_deprecated,
            labels=self.labels,
            most_recent=self.most_recent,
            name=self.name,
            os_flavor=self.os_flavor,
            os_version=self.os_version,
            rapid_deploy=self.rapid_deploy,
            selector=self.selector,
            type=self.type,
            with_architecture=self.with_architecture,
            with_selector=self.with_selector,
            with_statuses=self.with_statuses)


def get_image(id: Optional[int] = None,
              include_deprecated: Optional[bool] = None,
              most_recent: Optional[bool] = None,
              name: Optional[str] = None,
              selector: Optional[str] = None,
              with_architecture: Optional[str] = None,
              with_selector: Optional[str] = None,
              with_statuses: Optional[Sequence[str]] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetImageResult:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_hcloud as hcloud

    image1 = hcloud.get_image(id=1234)
    image2 = hcloud.get_image(name="ubuntu-18.04",
        with_architecture="x86")
    image3 = hcloud.get_image(with_selector="key=value")
    main = hcloud.Server("main", image=image1.id)
    ```


    :param int id: ID of the Image.
    :param bool include_deprecated: Also return the image if it is marked as deprecated.
    :param bool most_recent: If more than one result is returned, use the most recent Image.
    :param str name: Name of the Image.
    :param str with_architecture: Select only images with this architecture, could be `x86` (default) or `arm`.
    :param str with_selector: [Label selector](https://docs.hetzner.cloud/#overview-label-selector)
    :param Sequence[str] with_statuses: Select only images with the specified status, could contain `creating` or `available`.
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['includeDeprecated'] = include_deprecated
    __args__['mostRecent'] = most_recent
    __args__['name'] = name
    __args__['selector'] = selector
    __args__['withArchitecture'] = with_architecture
    __args__['withSelector'] = with_selector
    __args__['withStatuses'] = with_statuses
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('hcloud:index/getImage:getImage', __args__, opts=opts, typ=GetImageResult).value

    return AwaitableGetImageResult(
        architecture=pulumi.get(__ret__, 'architecture'),
        created=pulumi.get(__ret__, 'created'),
        deprecated=pulumi.get(__ret__, 'deprecated'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        include_deprecated=pulumi.get(__ret__, 'include_deprecated'),
        labels=pulumi.get(__ret__, 'labels'),
        most_recent=pulumi.get(__ret__, 'most_recent'),
        name=pulumi.get(__ret__, 'name'),
        os_flavor=pulumi.get(__ret__, 'os_flavor'),
        os_version=pulumi.get(__ret__, 'os_version'),
        rapid_deploy=pulumi.get(__ret__, 'rapid_deploy'),
        selector=pulumi.get(__ret__, 'selector'),
        type=pulumi.get(__ret__, 'type'),
        with_architecture=pulumi.get(__ret__, 'with_architecture'),
        with_selector=pulumi.get(__ret__, 'with_selector'),
        with_statuses=pulumi.get(__ret__, 'with_statuses'))
def get_image_output(id: Optional[pulumi.Input[Optional[int]]] = None,
                     include_deprecated: Optional[pulumi.Input[Optional[bool]]] = None,
                     most_recent: Optional[pulumi.Input[Optional[bool]]] = None,
                     name: Optional[pulumi.Input[Optional[str]]] = None,
                     selector: Optional[pulumi.Input[Optional[str]]] = None,
                     with_architecture: Optional[pulumi.Input[Optional[str]]] = None,
                     with_selector: Optional[pulumi.Input[Optional[str]]] = None,
                     with_statuses: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                     opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetImageResult]:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_hcloud as hcloud

    image1 = hcloud.get_image(id=1234)
    image2 = hcloud.get_image(name="ubuntu-18.04",
        with_architecture="x86")
    image3 = hcloud.get_image(with_selector="key=value")
    main = hcloud.Server("main", image=image1.id)
    ```


    :param int id: ID of the Image.
    :param bool include_deprecated: Also return the image if it is marked as deprecated.
    :param bool most_recent: If more than one result is returned, use the most recent Image.
    :param str name: Name of the Image.
    :param str with_architecture: Select only images with this architecture, could be `x86` (default) or `arm`.
    :param str with_selector: [Label selector](https://docs.hetzner.cloud/#overview-label-selector)
    :param Sequence[str] with_statuses: Select only images with the specified status, could contain `creating` or `available`.
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['includeDeprecated'] = include_deprecated
    __args__['mostRecent'] = most_recent
    __args__['name'] = name
    __args__['selector'] = selector
    __args__['withArchitecture'] = with_architecture
    __args__['withSelector'] = with_selector
    __args__['withStatuses'] = with_statuses
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('hcloud:index/getImage:getImage', __args__, opts=opts, typ=GetImageResult)
    return __ret__.apply(lambda __response__: GetImageResult(
        architecture=pulumi.get(__response__, 'architecture'),
        created=pulumi.get(__response__, 'created'),
        deprecated=pulumi.get(__response__, 'deprecated'),
        description=pulumi.get(__response__, 'description'),
        id=pulumi.get(__response__, 'id'),
        include_deprecated=pulumi.get(__response__, 'include_deprecated'),
        labels=pulumi.get(__response__, 'labels'),
        most_recent=pulumi.get(__response__, 'most_recent'),
        name=pulumi.get(__response__, 'name'),
        os_flavor=pulumi.get(__response__, 'os_flavor'),
        os_version=pulumi.get(__response__, 'os_version'),
        rapid_deploy=pulumi.get(__response__, 'rapid_deploy'),
        selector=pulumi.get(__response__, 'selector'),
        type=pulumi.get(__response__, 'type'),
        with_architecture=pulumi.get(__response__, 'with_architecture'),
        with_selector=pulumi.get(__response__, 'with_selector'),
        with_statuses=pulumi.get(__response__, 'with_statuses')))
