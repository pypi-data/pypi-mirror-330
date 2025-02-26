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

__all__ = ['VolumeArgs', 'Volume']

@pulumi.input_type
class VolumeArgs:
    def __init__(__self__, *,
                 size: pulumi.Input[int],
                 automount: Optional[pulumi.Input[bool]] = None,
                 delete_protection: Optional[pulumi.Input[bool]] = None,
                 format: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 server_id: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a Volume resource.
        :param pulumi.Input[int] size: Size of the volume (in GB).
        :param pulumi.Input[bool] automount: Automount the volume upon attaching it (server_id must be provided).
        :param pulumi.Input[bool] delete_protection: Enable or disable delete protection. See "Delete Protection" in the Provider Docs for details.
               
               **Note:** When you want to attach multiple volumes to a server, please use the `VolumeAttachment` resource and the `location` argument instead of the `server_id` argument.
        :param pulumi.Input[str] format: Format volume after creation. `xfs` or `ext4`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: User-defined labels (key-value pairs).
        :param pulumi.Input[str] location: The location name of the volume to create, not allowed if server_id argument is passed. See the [Hetzner Docs](https://docs.hetzner.com/cloud/general/locations/#what-locations-are-there) for more details about locations.
        :param pulumi.Input[str] name: Name of the volume to create (must be unique per project).
        :param pulumi.Input[int] server_id: Server to attach the Volume to, not allowed if location argument is passed.
        """
        pulumi.set(__self__, "size", size)
        if automount is not None:
            pulumi.set(__self__, "automount", automount)
        if delete_protection is not None:
            pulumi.set(__self__, "delete_protection", delete_protection)
        if format is not None:
            pulumi.set(__self__, "format", format)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if server_id is not None:
            pulumi.set(__self__, "server_id", server_id)

    @property
    @pulumi.getter
    def size(self) -> pulumi.Input[int]:
        """
        Size of the volume (in GB).
        """
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: pulumi.Input[int]):
        pulumi.set(self, "size", value)

    @property
    @pulumi.getter
    def automount(self) -> Optional[pulumi.Input[bool]]:
        """
        Automount the volume upon attaching it (server_id must be provided).
        """
        return pulumi.get(self, "automount")

    @automount.setter
    def automount(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "automount", value)

    @property
    @pulumi.getter(name="deleteProtection")
    def delete_protection(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable or disable delete protection. See "Delete Protection" in the Provider Docs for details.

        **Note:** When you want to attach multiple volumes to a server, please use the `VolumeAttachment` resource and the `location` argument instead of the `server_id` argument.
        """
        return pulumi.get(self, "delete_protection")

    @delete_protection.setter
    def delete_protection(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "delete_protection", value)

    @property
    @pulumi.getter
    def format(self) -> Optional[pulumi.Input[str]]:
        """
        Format volume after creation. `xfs` or `ext4`
        """
        return pulumi.get(self, "format")

    @format.setter
    def format(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "format", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        User-defined labels (key-value pairs).
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location name of the volume to create, not allowed if server_id argument is passed. See the [Hetzner Docs](https://docs.hetzner.com/cloud/general/locations/#what-locations-are-there) for more details about locations.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the volume to create (must be unique per project).
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> Optional[pulumi.Input[int]]:
        """
        Server to attach the Volume to, not allowed if location argument is passed.
        """
        return pulumi.get(self, "server_id")

    @server_id.setter
    def server_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "server_id", value)


@pulumi.input_type
class _VolumeState:
    def __init__(__self__, *,
                 automount: Optional[pulumi.Input[bool]] = None,
                 delete_protection: Optional[pulumi.Input[bool]] = None,
                 format: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 linux_device: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 server_id: Optional[pulumi.Input[int]] = None,
                 size: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering Volume resources.
        :param pulumi.Input[bool] automount: Automount the volume upon attaching it (server_id must be provided).
        :param pulumi.Input[bool] delete_protection: Enable or disable delete protection. See "Delete Protection" in the Provider Docs for details.
               
               **Note:** When you want to attach multiple volumes to a server, please use the `VolumeAttachment` resource and the `location` argument instead of the `server_id` argument.
        :param pulumi.Input[str] format: Format volume after creation. `xfs` or `ext4`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: User-defined labels (key-value pairs).
        :param pulumi.Input[str] linux_device: (string) Device path on the file system for the Volume.
        :param pulumi.Input[str] location: The location name of the volume to create, not allowed if server_id argument is passed. See the [Hetzner Docs](https://docs.hetzner.com/cloud/general/locations/#what-locations-are-there) for more details about locations.
        :param pulumi.Input[str] name: Name of the volume to create (must be unique per project).
        :param pulumi.Input[int] server_id: Server to attach the Volume to, not allowed if location argument is passed.
        :param pulumi.Input[int] size: Size of the volume (in GB).
        """
        if automount is not None:
            pulumi.set(__self__, "automount", automount)
        if delete_protection is not None:
            pulumi.set(__self__, "delete_protection", delete_protection)
        if format is not None:
            pulumi.set(__self__, "format", format)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if linux_device is not None:
            pulumi.set(__self__, "linux_device", linux_device)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if server_id is not None:
            pulumi.set(__self__, "server_id", server_id)
        if size is not None:
            pulumi.set(__self__, "size", size)

    @property
    @pulumi.getter
    def automount(self) -> Optional[pulumi.Input[bool]]:
        """
        Automount the volume upon attaching it (server_id must be provided).
        """
        return pulumi.get(self, "automount")

    @automount.setter
    def automount(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "automount", value)

    @property
    @pulumi.getter(name="deleteProtection")
    def delete_protection(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable or disable delete protection. See "Delete Protection" in the Provider Docs for details.

        **Note:** When you want to attach multiple volumes to a server, please use the `VolumeAttachment` resource and the `location` argument instead of the `server_id` argument.
        """
        return pulumi.get(self, "delete_protection")

    @delete_protection.setter
    def delete_protection(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "delete_protection", value)

    @property
    @pulumi.getter
    def format(self) -> Optional[pulumi.Input[str]]:
        """
        Format volume after creation. `xfs` or `ext4`
        """
        return pulumi.get(self, "format")

    @format.setter
    def format(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "format", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        User-defined labels (key-value pairs).
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter(name="linuxDevice")
    def linux_device(self) -> Optional[pulumi.Input[str]]:
        """
        (string) Device path on the file system for the Volume.
        """
        return pulumi.get(self, "linux_device")

    @linux_device.setter
    def linux_device(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "linux_device", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location name of the volume to create, not allowed if server_id argument is passed. See the [Hetzner Docs](https://docs.hetzner.com/cloud/general/locations/#what-locations-are-there) for more details about locations.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the volume to create (must be unique per project).
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> Optional[pulumi.Input[int]]:
        """
        Server to attach the Volume to, not allowed if location argument is passed.
        """
        return pulumi.get(self, "server_id")

    @server_id.setter
    def server_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "server_id", value)

    @property
    @pulumi.getter
    def size(self) -> Optional[pulumi.Input[int]]:
        """
        Size of the volume (in GB).
        """
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "size", value)


class Volume(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 automount: Optional[pulumi.Input[bool]] = None,
                 delete_protection: Optional[pulumi.Input[bool]] = None,
                 format: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 server_id: Optional[pulumi.Input[int]] = None,
                 size: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Provides a Hetzner Cloud volume resource to manage volumes.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_hcloud as hcloud

        node1 = hcloud.Server("node1",
            name="node1",
            image="debian-11",
            server_type="cx22")
        master = hcloud.Volume("master",
            name="volume1",
            size=50,
            server_id=node1.id,
            automount=True,
            format="ext4")
        ```

        ## Import

        Volumes can be imported using their `id`:

        ```sh
        $ pulumi import hcloud:index/volume:Volume example "$VOLUME_ID"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] automount: Automount the volume upon attaching it (server_id must be provided).
        :param pulumi.Input[bool] delete_protection: Enable or disable delete protection. See "Delete Protection" in the Provider Docs for details.
               
               **Note:** When you want to attach multiple volumes to a server, please use the `VolumeAttachment` resource and the `location` argument instead of the `server_id` argument.
        :param pulumi.Input[str] format: Format volume after creation. `xfs` or `ext4`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: User-defined labels (key-value pairs).
        :param pulumi.Input[str] location: The location name of the volume to create, not allowed if server_id argument is passed. See the [Hetzner Docs](https://docs.hetzner.com/cloud/general/locations/#what-locations-are-there) for more details about locations.
        :param pulumi.Input[str] name: Name of the volume to create (must be unique per project).
        :param pulumi.Input[int] server_id: Server to attach the Volume to, not allowed if location argument is passed.
        :param pulumi.Input[int] size: Size of the volume (in GB).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VolumeArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Hetzner Cloud volume resource to manage volumes.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_hcloud as hcloud

        node1 = hcloud.Server("node1",
            name="node1",
            image="debian-11",
            server_type="cx22")
        master = hcloud.Volume("master",
            name="volume1",
            size=50,
            server_id=node1.id,
            automount=True,
            format="ext4")
        ```

        ## Import

        Volumes can be imported using their `id`:

        ```sh
        $ pulumi import hcloud:index/volume:Volume example "$VOLUME_ID"
        ```

        :param str resource_name: The name of the resource.
        :param VolumeArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VolumeArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 automount: Optional[pulumi.Input[bool]] = None,
                 delete_protection: Optional[pulumi.Input[bool]] = None,
                 format: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 server_id: Optional[pulumi.Input[int]] = None,
                 size: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VolumeArgs.__new__(VolumeArgs)

            __props__.__dict__["automount"] = automount
            __props__.__dict__["delete_protection"] = delete_protection
            __props__.__dict__["format"] = format
            __props__.__dict__["labels"] = labels
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["server_id"] = server_id
            if size is None and not opts.urn:
                raise TypeError("Missing required property 'size'")
            __props__.__dict__["size"] = size
            __props__.__dict__["linux_device"] = None
        super(Volume, __self__).__init__(
            'hcloud:index/volume:Volume',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            automount: Optional[pulumi.Input[bool]] = None,
            delete_protection: Optional[pulumi.Input[bool]] = None,
            format: Optional[pulumi.Input[str]] = None,
            labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            linux_device: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            server_id: Optional[pulumi.Input[int]] = None,
            size: Optional[pulumi.Input[int]] = None) -> 'Volume':
        """
        Get an existing Volume resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] automount: Automount the volume upon attaching it (server_id must be provided).
        :param pulumi.Input[bool] delete_protection: Enable or disable delete protection. See "Delete Protection" in the Provider Docs for details.
               
               **Note:** When you want to attach multiple volumes to a server, please use the `VolumeAttachment` resource and the `location` argument instead of the `server_id` argument.
        :param pulumi.Input[str] format: Format volume after creation. `xfs` or `ext4`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: User-defined labels (key-value pairs).
        :param pulumi.Input[str] linux_device: (string) Device path on the file system for the Volume.
        :param pulumi.Input[str] location: The location name of the volume to create, not allowed if server_id argument is passed. See the [Hetzner Docs](https://docs.hetzner.com/cloud/general/locations/#what-locations-are-there) for more details about locations.
        :param pulumi.Input[str] name: Name of the volume to create (must be unique per project).
        :param pulumi.Input[int] server_id: Server to attach the Volume to, not allowed if location argument is passed.
        :param pulumi.Input[int] size: Size of the volume (in GB).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _VolumeState.__new__(_VolumeState)

        __props__.__dict__["automount"] = automount
        __props__.__dict__["delete_protection"] = delete_protection
        __props__.__dict__["format"] = format
        __props__.__dict__["labels"] = labels
        __props__.__dict__["linux_device"] = linux_device
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["server_id"] = server_id
        __props__.__dict__["size"] = size
        return Volume(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def automount(self) -> pulumi.Output[Optional[bool]]:
        """
        Automount the volume upon attaching it (server_id must be provided).
        """
        return pulumi.get(self, "automount")

    @property
    @pulumi.getter(name="deleteProtection")
    def delete_protection(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable or disable delete protection. See "Delete Protection" in the Provider Docs for details.

        **Note:** When you want to attach multiple volumes to a server, please use the `VolumeAttachment` resource and the `location` argument instead of the `server_id` argument.
        """
        return pulumi.get(self, "delete_protection")

    @property
    @pulumi.getter
    def format(self) -> pulumi.Output[Optional[str]]:
        """
        Format volume after creation. `xfs` or `ext4`
        """
        return pulumi.get(self, "format")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        User-defined labels (key-value pairs).
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter(name="linuxDevice")
    def linux_device(self) -> pulumi.Output[str]:
        """
        (string) Device path on the file system for the Volume.
        """
        return pulumi.get(self, "linux_device")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location name of the volume to create, not allowed if server_id argument is passed. See the [Hetzner Docs](https://docs.hetzner.com/cloud/general/locations/#what-locations-are-there) for more details about locations.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the volume to create (must be unique per project).
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> pulumi.Output[int]:
        """
        Server to attach the Volume to, not allowed if location argument is passed.
        """
        return pulumi.get(self, "server_id")

    @property
    @pulumi.getter
    def size(self) -> pulumi.Output[int]:
        """
        Size of the volume (in GB).
        """
        return pulumi.get(self, "size")

