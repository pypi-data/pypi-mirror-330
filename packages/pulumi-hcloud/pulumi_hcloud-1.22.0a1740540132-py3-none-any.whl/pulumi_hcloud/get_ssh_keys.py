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
from . import outputs

__all__ = [
    'GetSshKeysResult',
    'AwaitableGetSshKeysResult',
    'get_ssh_keys',
    'get_ssh_keys_output',
]

@pulumi.output_type
class GetSshKeysResult:
    """
    A collection of values returned by getSshKeys.
    """
    def __init__(__self__, id=None, ssh_keys=None, with_selector=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ssh_keys and not isinstance(ssh_keys, list):
            raise TypeError("Expected argument 'ssh_keys' to be a list")
        pulumi.set(__self__, "ssh_keys", ssh_keys)
        if with_selector and not isinstance(with_selector, str):
            raise TypeError("Expected argument 'with_selector' to be a str")
        pulumi.set(__self__, "with_selector", with_selector)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of this resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="sshKeys")
    def ssh_keys(self) -> Sequence['outputs.GetSshKeysSshKeyResult']:
        return pulumi.get(self, "ssh_keys")

    @property
    @pulumi.getter(name="withSelector")
    def with_selector(self) -> Optional[str]:
        """
        Filter results using a [Label Selector](https://docs.hetzner.cloud/#label-selector)
        """
        return pulumi.get(self, "with_selector")


class AwaitableGetSshKeysResult(GetSshKeysResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSshKeysResult(
            id=self.id,
            ssh_keys=self.ssh_keys,
            with_selector=self.with_selector)


def get_ssh_keys(id: Optional[str] = None,
                 with_selector: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSshKeysResult:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_hcloud as hcloud

    all = hcloud.get_ssh_keys()
    by_label = hcloud.get_ssh_keys(with_selector="foo=bar")
    main = hcloud.Server("main", ssh_keys=[__item.name for __item in all.ssh_keys])
    ```


    :param str id: The ID of this resource.
    :param str with_selector: Filter results using a [Label Selector](https://docs.hetzner.cloud/#label-selector)
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['withSelector'] = with_selector
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('hcloud:index/getSshKeys:getSshKeys', __args__, opts=opts, typ=GetSshKeysResult).value

    return AwaitableGetSshKeysResult(
        id=pulumi.get(__ret__, 'id'),
        ssh_keys=pulumi.get(__ret__, 'ssh_keys'),
        with_selector=pulumi.get(__ret__, 'with_selector'))
def get_ssh_keys_output(id: Optional[pulumi.Input[Optional[str]]] = None,
                        with_selector: Optional[pulumi.Input[Optional[str]]] = None,
                        opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetSshKeysResult]:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_hcloud as hcloud

    all = hcloud.get_ssh_keys()
    by_label = hcloud.get_ssh_keys(with_selector="foo=bar")
    main = hcloud.Server("main", ssh_keys=[__item.name for __item in all.ssh_keys])
    ```


    :param str id: The ID of this resource.
    :param str with_selector: Filter results using a [Label Selector](https://docs.hetzner.cloud/#label-selector)
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['withSelector'] = with_selector
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('hcloud:index/getSshKeys:getSshKeys', __args__, opts=opts, typ=GetSshKeysResult)
    return __ret__.apply(lambda __response__: GetSshKeysResult(
        id=pulumi.get(__response__, 'id'),
        ssh_keys=pulumi.get(__response__, 'ssh_keys'),
        with_selector=pulumi.get(__response__, 'with_selector')))
