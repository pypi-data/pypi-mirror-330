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
from .. import _utilities

__all__ = ['OceanExtendedResourceDefinitionArgs', 'OceanExtendedResourceDefinition']

@pulumi.input_type
class OceanExtendedResourceDefinitionArgs:
    def __init__(__self__, *,
                 resource_mapping: pulumi.Input[Mapping[str, pulumi.Input[str]]],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a OceanExtendedResourceDefinition resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] resource_mapping: A mapping between AWS instanceType or * as default and its value for the given extended resource.
        :param pulumi.Input[str] name: The extended resource name as should be requested by your pods and registered to the nodes. Cannot be updated.
               The name should be a valid Kubernetes extended resource name.
        """
        pulumi.set(__self__, "resource_mapping", resource_mapping)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="resourceMapping")
    def resource_mapping(self) -> pulumi.Input[Mapping[str, pulumi.Input[str]]]:
        """
        A mapping between AWS instanceType or * as default and its value for the given extended resource.
        """
        return pulumi.get(self, "resource_mapping")

    @resource_mapping.setter
    def resource_mapping(self, value: pulumi.Input[Mapping[str, pulumi.Input[str]]]):
        pulumi.set(self, "resource_mapping", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The extended resource name as should be requested by your pods and registered to the nodes. Cannot be updated.
        The name should be a valid Kubernetes extended resource name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _OceanExtendedResourceDefinitionState:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_mapping: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering OceanExtendedResourceDefinition resources.
        :param pulumi.Input[str] name: The extended resource name as should be requested by your pods and registered to the nodes. Cannot be updated.
               The name should be a valid Kubernetes extended resource name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] resource_mapping: A mapping between AWS instanceType or * as default and its value for the given extended resource.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_mapping is not None:
            pulumi.set(__self__, "resource_mapping", resource_mapping)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The extended resource name as should be requested by your pods and registered to the nodes. Cannot be updated.
        The name should be a valid Kubernetes extended resource name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceMapping")
    def resource_mapping(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping between AWS instanceType or * as default and its value for the given extended resource.
        """
        return pulumi.get(self, "resource_mapping")

    @resource_mapping.setter
    def resource_mapping(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "resource_mapping", value)


class OceanExtendedResourceDefinition(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_mapping: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a Spotinst Ocean AWS Extended Resource Definition resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_spotinst as spotinst

        example = spotinst.aws.OceanExtendedResourceDefinition("example",
            name="terraform_extended_resource_definition",
            resource_mapping={
                "c3.large": "2Ki",
                "c3.xlarge": "4Ki",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The extended resource name as should be requested by your pods and registered to the nodes. Cannot be updated.
               The name should be a valid Kubernetes extended resource name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] resource_mapping: A mapping between AWS instanceType or * as default and its value for the given extended resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OceanExtendedResourceDefinitionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Spotinst Ocean AWS Extended Resource Definition resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_spotinst as spotinst

        example = spotinst.aws.OceanExtendedResourceDefinition("example",
            name="terraform_extended_resource_definition",
            resource_mapping={
                "c3.large": "2Ki",
                "c3.xlarge": "4Ki",
            })
        ```

        :param str resource_name: The name of the resource.
        :param OceanExtendedResourceDefinitionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OceanExtendedResourceDefinitionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_mapping: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OceanExtendedResourceDefinitionArgs.__new__(OceanExtendedResourceDefinitionArgs)

            __props__.__dict__["name"] = name
            if resource_mapping is None and not opts.urn:
                raise TypeError("Missing required property 'resource_mapping'")
            __props__.__dict__["resource_mapping"] = resource_mapping
        super(OceanExtendedResourceDefinition, __self__).__init__(
            'spotinst:aws/oceanExtendedResourceDefinition:OceanExtendedResourceDefinition',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_mapping: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'OceanExtendedResourceDefinition':
        """
        Get an existing OceanExtendedResourceDefinition resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The extended resource name as should be requested by your pods and registered to the nodes. Cannot be updated.
               The name should be a valid Kubernetes extended resource name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] resource_mapping: A mapping between AWS instanceType or * as default and its value for the given extended resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _OceanExtendedResourceDefinitionState.__new__(_OceanExtendedResourceDefinitionState)

        __props__.__dict__["name"] = name
        __props__.__dict__["resource_mapping"] = resource_mapping
        return OceanExtendedResourceDefinition(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The extended resource name as should be requested by your pods and registered to the nodes. Cannot be updated.
        The name should be a valid Kubernetes extended resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceMapping")
    def resource_mapping(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A mapping between AWS instanceType or * as default and its value for the given extended resource.
        """
        return pulumi.get(self, "resource_mapping")

