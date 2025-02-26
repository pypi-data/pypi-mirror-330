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
from ._inputs import *

__all__ = ['OceanRightSizingRuleArgs', 'OceanRightSizingRule']

@pulumi.input_type
class OceanRightSizingRuleArgs:
    def __init__(__self__, *,
                 recommendation_application_intervals: pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationIntervalArgs']]],
                 rule_name: pulumi.Input[str],
                 attach_workloads: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleAttachWorkloadArgs']]]] = None,
                 detach_workloads: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleDetachWorkloadArgs']]]] = None,
                 exclude_preliminary_recommendations: Optional[pulumi.Input[bool]] = None,
                 ocean_id: Optional[pulumi.Input[str]] = None,
                 recommendation_application_boundaries: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationBoundaryArgs']]]] = None,
                 recommendation_application_hpas: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationHpaArgs']]]] = None,
                 recommendation_application_min_thresholds: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationMinThresholdArgs']]]] = None,
                 recommendation_application_overhead_values: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationOverheadValueArgs']]]] = None,
                 restart_replicas: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a OceanRightSizingRule resource.
        """
        pulumi.set(__self__, "recommendation_application_intervals", recommendation_application_intervals)
        pulumi.set(__self__, "rule_name", rule_name)
        if attach_workloads is not None:
            pulumi.set(__self__, "attach_workloads", attach_workloads)
        if detach_workloads is not None:
            pulumi.set(__self__, "detach_workloads", detach_workloads)
        if exclude_preliminary_recommendations is not None:
            pulumi.set(__self__, "exclude_preliminary_recommendations", exclude_preliminary_recommendations)
        if ocean_id is not None:
            pulumi.set(__self__, "ocean_id", ocean_id)
        if recommendation_application_boundaries is not None:
            pulumi.set(__self__, "recommendation_application_boundaries", recommendation_application_boundaries)
        if recommendation_application_hpas is not None:
            pulumi.set(__self__, "recommendation_application_hpas", recommendation_application_hpas)
        if recommendation_application_min_thresholds is not None:
            pulumi.set(__self__, "recommendation_application_min_thresholds", recommendation_application_min_thresholds)
        if recommendation_application_overhead_values is not None:
            pulumi.set(__self__, "recommendation_application_overhead_values", recommendation_application_overhead_values)
        if restart_replicas is not None:
            pulumi.set(__self__, "restart_replicas", restart_replicas)

    @property
    @pulumi.getter(name="recommendationApplicationIntervals")
    def recommendation_application_intervals(self) -> pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationIntervalArgs']]]:
        return pulumi.get(self, "recommendation_application_intervals")

    @recommendation_application_intervals.setter
    def recommendation_application_intervals(self, value: pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationIntervalArgs']]]):
        pulumi.set(self, "recommendation_application_intervals", value)

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "rule_name")

    @rule_name.setter
    def rule_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "rule_name", value)

    @property
    @pulumi.getter(name="attachWorkloads")
    def attach_workloads(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleAttachWorkloadArgs']]]]:
        return pulumi.get(self, "attach_workloads")

    @attach_workloads.setter
    def attach_workloads(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleAttachWorkloadArgs']]]]):
        pulumi.set(self, "attach_workloads", value)

    @property
    @pulumi.getter(name="detachWorkloads")
    def detach_workloads(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleDetachWorkloadArgs']]]]:
        return pulumi.get(self, "detach_workloads")

    @detach_workloads.setter
    def detach_workloads(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleDetachWorkloadArgs']]]]):
        pulumi.set(self, "detach_workloads", value)

    @property
    @pulumi.getter(name="excludePreliminaryRecommendations")
    def exclude_preliminary_recommendations(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "exclude_preliminary_recommendations")

    @exclude_preliminary_recommendations.setter
    def exclude_preliminary_recommendations(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "exclude_preliminary_recommendations", value)

    @property
    @pulumi.getter(name="oceanId")
    def ocean_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "ocean_id")

    @ocean_id.setter
    def ocean_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ocean_id", value)

    @property
    @pulumi.getter(name="recommendationApplicationBoundaries")
    def recommendation_application_boundaries(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationBoundaryArgs']]]]:
        return pulumi.get(self, "recommendation_application_boundaries")

    @recommendation_application_boundaries.setter
    def recommendation_application_boundaries(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationBoundaryArgs']]]]):
        pulumi.set(self, "recommendation_application_boundaries", value)

    @property
    @pulumi.getter(name="recommendationApplicationHpas")
    def recommendation_application_hpas(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationHpaArgs']]]]:
        return pulumi.get(self, "recommendation_application_hpas")

    @recommendation_application_hpas.setter
    def recommendation_application_hpas(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationHpaArgs']]]]):
        pulumi.set(self, "recommendation_application_hpas", value)

    @property
    @pulumi.getter(name="recommendationApplicationMinThresholds")
    def recommendation_application_min_thresholds(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationMinThresholdArgs']]]]:
        return pulumi.get(self, "recommendation_application_min_thresholds")

    @recommendation_application_min_thresholds.setter
    def recommendation_application_min_thresholds(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationMinThresholdArgs']]]]):
        pulumi.set(self, "recommendation_application_min_thresholds", value)

    @property
    @pulumi.getter(name="recommendationApplicationOverheadValues")
    def recommendation_application_overhead_values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationOverheadValueArgs']]]]:
        return pulumi.get(self, "recommendation_application_overhead_values")

    @recommendation_application_overhead_values.setter
    def recommendation_application_overhead_values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationOverheadValueArgs']]]]):
        pulumi.set(self, "recommendation_application_overhead_values", value)

    @property
    @pulumi.getter(name="restartReplicas")
    def restart_replicas(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "restart_replicas")

    @restart_replicas.setter
    def restart_replicas(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "restart_replicas", value)


@pulumi.input_type
class _OceanRightSizingRuleState:
    def __init__(__self__, *,
                 attach_workloads: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleAttachWorkloadArgs']]]] = None,
                 detach_workloads: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleDetachWorkloadArgs']]]] = None,
                 exclude_preliminary_recommendations: Optional[pulumi.Input[bool]] = None,
                 ocean_id: Optional[pulumi.Input[str]] = None,
                 recommendation_application_boundaries: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationBoundaryArgs']]]] = None,
                 recommendation_application_hpas: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationHpaArgs']]]] = None,
                 recommendation_application_intervals: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationIntervalArgs']]]] = None,
                 recommendation_application_min_thresholds: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationMinThresholdArgs']]]] = None,
                 recommendation_application_overhead_values: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationOverheadValueArgs']]]] = None,
                 restart_replicas: Optional[pulumi.Input[str]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering OceanRightSizingRule resources.
        """
        if attach_workloads is not None:
            pulumi.set(__self__, "attach_workloads", attach_workloads)
        if detach_workloads is not None:
            pulumi.set(__self__, "detach_workloads", detach_workloads)
        if exclude_preliminary_recommendations is not None:
            pulumi.set(__self__, "exclude_preliminary_recommendations", exclude_preliminary_recommendations)
        if ocean_id is not None:
            pulumi.set(__self__, "ocean_id", ocean_id)
        if recommendation_application_boundaries is not None:
            pulumi.set(__self__, "recommendation_application_boundaries", recommendation_application_boundaries)
        if recommendation_application_hpas is not None:
            pulumi.set(__self__, "recommendation_application_hpas", recommendation_application_hpas)
        if recommendation_application_intervals is not None:
            pulumi.set(__self__, "recommendation_application_intervals", recommendation_application_intervals)
        if recommendation_application_min_thresholds is not None:
            pulumi.set(__self__, "recommendation_application_min_thresholds", recommendation_application_min_thresholds)
        if recommendation_application_overhead_values is not None:
            pulumi.set(__self__, "recommendation_application_overhead_values", recommendation_application_overhead_values)
        if restart_replicas is not None:
            pulumi.set(__self__, "restart_replicas", restart_replicas)
        if rule_name is not None:
            pulumi.set(__self__, "rule_name", rule_name)

    @property
    @pulumi.getter(name="attachWorkloads")
    def attach_workloads(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleAttachWorkloadArgs']]]]:
        return pulumi.get(self, "attach_workloads")

    @attach_workloads.setter
    def attach_workloads(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleAttachWorkloadArgs']]]]):
        pulumi.set(self, "attach_workloads", value)

    @property
    @pulumi.getter(name="detachWorkloads")
    def detach_workloads(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleDetachWorkloadArgs']]]]:
        return pulumi.get(self, "detach_workloads")

    @detach_workloads.setter
    def detach_workloads(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleDetachWorkloadArgs']]]]):
        pulumi.set(self, "detach_workloads", value)

    @property
    @pulumi.getter(name="excludePreliminaryRecommendations")
    def exclude_preliminary_recommendations(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "exclude_preliminary_recommendations")

    @exclude_preliminary_recommendations.setter
    def exclude_preliminary_recommendations(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "exclude_preliminary_recommendations", value)

    @property
    @pulumi.getter(name="oceanId")
    def ocean_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "ocean_id")

    @ocean_id.setter
    def ocean_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ocean_id", value)

    @property
    @pulumi.getter(name="recommendationApplicationBoundaries")
    def recommendation_application_boundaries(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationBoundaryArgs']]]]:
        return pulumi.get(self, "recommendation_application_boundaries")

    @recommendation_application_boundaries.setter
    def recommendation_application_boundaries(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationBoundaryArgs']]]]):
        pulumi.set(self, "recommendation_application_boundaries", value)

    @property
    @pulumi.getter(name="recommendationApplicationHpas")
    def recommendation_application_hpas(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationHpaArgs']]]]:
        return pulumi.get(self, "recommendation_application_hpas")

    @recommendation_application_hpas.setter
    def recommendation_application_hpas(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationHpaArgs']]]]):
        pulumi.set(self, "recommendation_application_hpas", value)

    @property
    @pulumi.getter(name="recommendationApplicationIntervals")
    def recommendation_application_intervals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationIntervalArgs']]]]:
        return pulumi.get(self, "recommendation_application_intervals")

    @recommendation_application_intervals.setter
    def recommendation_application_intervals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationIntervalArgs']]]]):
        pulumi.set(self, "recommendation_application_intervals", value)

    @property
    @pulumi.getter(name="recommendationApplicationMinThresholds")
    def recommendation_application_min_thresholds(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationMinThresholdArgs']]]]:
        return pulumi.get(self, "recommendation_application_min_thresholds")

    @recommendation_application_min_thresholds.setter
    def recommendation_application_min_thresholds(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationMinThresholdArgs']]]]):
        pulumi.set(self, "recommendation_application_min_thresholds", value)

    @property
    @pulumi.getter(name="recommendationApplicationOverheadValues")
    def recommendation_application_overhead_values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationOverheadValueArgs']]]]:
        return pulumi.get(self, "recommendation_application_overhead_values")

    @recommendation_application_overhead_values.setter
    def recommendation_application_overhead_values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanRightSizingRuleRecommendationApplicationOverheadValueArgs']]]]):
        pulumi.set(self, "recommendation_application_overhead_values", value)

    @property
    @pulumi.getter(name="restartReplicas")
    def restart_replicas(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "restart_replicas")

    @restart_replicas.setter
    def restart_replicas(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "restart_replicas", value)

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "rule_name")

    @rule_name.setter
    def rule_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rule_name", value)


class OceanRightSizingRule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attach_workloads: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleAttachWorkloadArgs', 'OceanRightSizingRuleAttachWorkloadArgsDict']]]]] = None,
                 detach_workloads: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleDetachWorkloadArgs', 'OceanRightSizingRuleDetachWorkloadArgsDict']]]]] = None,
                 exclude_preliminary_recommendations: Optional[pulumi.Input[bool]] = None,
                 ocean_id: Optional[pulumi.Input[str]] = None,
                 recommendation_application_boundaries: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleRecommendationApplicationBoundaryArgs', 'OceanRightSizingRuleRecommendationApplicationBoundaryArgsDict']]]]] = None,
                 recommendation_application_hpas: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleRecommendationApplicationHpaArgs', 'OceanRightSizingRuleRecommendationApplicationHpaArgsDict']]]]] = None,
                 recommendation_application_intervals: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleRecommendationApplicationIntervalArgs', 'OceanRightSizingRuleRecommendationApplicationIntervalArgsDict']]]]] = None,
                 recommendation_application_min_thresholds: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleRecommendationApplicationMinThresholdArgs', 'OceanRightSizingRuleRecommendationApplicationMinThresholdArgsDict']]]]] = None,
                 recommendation_application_overhead_values: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleRecommendationApplicationOverheadValueArgs', 'OceanRightSizingRuleRecommendationApplicationOverheadValueArgsDict']]]]] = None,
                 restart_replicas: Optional[pulumi.Input[str]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a OceanRightSizingRule resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OceanRightSizingRuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a OceanRightSizingRule resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param OceanRightSizingRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OceanRightSizingRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attach_workloads: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleAttachWorkloadArgs', 'OceanRightSizingRuleAttachWorkloadArgsDict']]]]] = None,
                 detach_workloads: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleDetachWorkloadArgs', 'OceanRightSizingRuleDetachWorkloadArgsDict']]]]] = None,
                 exclude_preliminary_recommendations: Optional[pulumi.Input[bool]] = None,
                 ocean_id: Optional[pulumi.Input[str]] = None,
                 recommendation_application_boundaries: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleRecommendationApplicationBoundaryArgs', 'OceanRightSizingRuleRecommendationApplicationBoundaryArgsDict']]]]] = None,
                 recommendation_application_hpas: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleRecommendationApplicationHpaArgs', 'OceanRightSizingRuleRecommendationApplicationHpaArgsDict']]]]] = None,
                 recommendation_application_intervals: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleRecommendationApplicationIntervalArgs', 'OceanRightSizingRuleRecommendationApplicationIntervalArgsDict']]]]] = None,
                 recommendation_application_min_thresholds: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleRecommendationApplicationMinThresholdArgs', 'OceanRightSizingRuleRecommendationApplicationMinThresholdArgsDict']]]]] = None,
                 recommendation_application_overhead_values: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleRecommendationApplicationOverheadValueArgs', 'OceanRightSizingRuleRecommendationApplicationOverheadValueArgsDict']]]]] = None,
                 restart_replicas: Optional[pulumi.Input[str]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OceanRightSizingRuleArgs.__new__(OceanRightSizingRuleArgs)

            __props__.__dict__["attach_workloads"] = attach_workloads
            __props__.__dict__["detach_workloads"] = detach_workloads
            __props__.__dict__["exclude_preliminary_recommendations"] = exclude_preliminary_recommendations
            __props__.__dict__["ocean_id"] = ocean_id
            __props__.__dict__["recommendation_application_boundaries"] = recommendation_application_boundaries
            __props__.__dict__["recommendation_application_hpas"] = recommendation_application_hpas
            if recommendation_application_intervals is None and not opts.urn:
                raise TypeError("Missing required property 'recommendation_application_intervals'")
            __props__.__dict__["recommendation_application_intervals"] = recommendation_application_intervals
            __props__.__dict__["recommendation_application_min_thresholds"] = recommendation_application_min_thresholds
            __props__.__dict__["recommendation_application_overhead_values"] = recommendation_application_overhead_values
            __props__.__dict__["restart_replicas"] = restart_replicas
            if rule_name is None and not opts.urn:
                raise TypeError("Missing required property 'rule_name'")
            __props__.__dict__["rule_name"] = rule_name
        super(OceanRightSizingRule, __self__).__init__(
            'spotinst:index/oceanRightSizingRule:OceanRightSizingRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            attach_workloads: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleAttachWorkloadArgs', 'OceanRightSizingRuleAttachWorkloadArgsDict']]]]] = None,
            detach_workloads: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleDetachWorkloadArgs', 'OceanRightSizingRuleDetachWorkloadArgsDict']]]]] = None,
            exclude_preliminary_recommendations: Optional[pulumi.Input[bool]] = None,
            ocean_id: Optional[pulumi.Input[str]] = None,
            recommendation_application_boundaries: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleRecommendationApplicationBoundaryArgs', 'OceanRightSizingRuleRecommendationApplicationBoundaryArgsDict']]]]] = None,
            recommendation_application_hpas: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleRecommendationApplicationHpaArgs', 'OceanRightSizingRuleRecommendationApplicationHpaArgsDict']]]]] = None,
            recommendation_application_intervals: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleRecommendationApplicationIntervalArgs', 'OceanRightSizingRuleRecommendationApplicationIntervalArgsDict']]]]] = None,
            recommendation_application_min_thresholds: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleRecommendationApplicationMinThresholdArgs', 'OceanRightSizingRuleRecommendationApplicationMinThresholdArgsDict']]]]] = None,
            recommendation_application_overhead_values: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OceanRightSizingRuleRecommendationApplicationOverheadValueArgs', 'OceanRightSizingRuleRecommendationApplicationOverheadValueArgsDict']]]]] = None,
            restart_replicas: Optional[pulumi.Input[str]] = None,
            rule_name: Optional[pulumi.Input[str]] = None) -> 'OceanRightSizingRule':
        """
        Get an existing OceanRightSizingRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _OceanRightSizingRuleState.__new__(_OceanRightSizingRuleState)

        __props__.__dict__["attach_workloads"] = attach_workloads
        __props__.__dict__["detach_workloads"] = detach_workloads
        __props__.__dict__["exclude_preliminary_recommendations"] = exclude_preliminary_recommendations
        __props__.__dict__["ocean_id"] = ocean_id
        __props__.__dict__["recommendation_application_boundaries"] = recommendation_application_boundaries
        __props__.__dict__["recommendation_application_hpas"] = recommendation_application_hpas
        __props__.__dict__["recommendation_application_intervals"] = recommendation_application_intervals
        __props__.__dict__["recommendation_application_min_thresholds"] = recommendation_application_min_thresholds
        __props__.__dict__["recommendation_application_overhead_values"] = recommendation_application_overhead_values
        __props__.__dict__["restart_replicas"] = restart_replicas
        __props__.__dict__["rule_name"] = rule_name
        return OceanRightSizingRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="attachWorkloads")
    def attach_workloads(self) -> pulumi.Output[Optional[Sequence['outputs.OceanRightSizingRuleAttachWorkload']]]:
        return pulumi.get(self, "attach_workloads")

    @property
    @pulumi.getter(name="detachWorkloads")
    def detach_workloads(self) -> pulumi.Output[Optional[Sequence['outputs.OceanRightSizingRuleDetachWorkload']]]:
        return pulumi.get(self, "detach_workloads")

    @property
    @pulumi.getter(name="excludePreliminaryRecommendations")
    def exclude_preliminary_recommendations(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "exclude_preliminary_recommendations")

    @property
    @pulumi.getter(name="oceanId")
    def ocean_id(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "ocean_id")

    @property
    @pulumi.getter(name="recommendationApplicationBoundaries")
    def recommendation_application_boundaries(self) -> pulumi.Output[Optional[Sequence['outputs.OceanRightSizingRuleRecommendationApplicationBoundary']]]:
        return pulumi.get(self, "recommendation_application_boundaries")

    @property
    @pulumi.getter(name="recommendationApplicationHpas")
    def recommendation_application_hpas(self) -> pulumi.Output[Optional[Sequence['outputs.OceanRightSizingRuleRecommendationApplicationHpa']]]:
        return pulumi.get(self, "recommendation_application_hpas")

    @property
    @pulumi.getter(name="recommendationApplicationIntervals")
    def recommendation_application_intervals(self) -> pulumi.Output[Sequence['outputs.OceanRightSizingRuleRecommendationApplicationInterval']]:
        return pulumi.get(self, "recommendation_application_intervals")

    @property
    @pulumi.getter(name="recommendationApplicationMinThresholds")
    def recommendation_application_min_thresholds(self) -> pulumi.Output[Optional[Sequence['outputs.OceanRightSizingRuleRecommendationApplicationMinThreshold']]]:
        return pulumi.get(self, "recommendation_application_min_thresholds")

    @property
    @pulumi.getter(name="recommendationApplicationOverheadValues")
    def recommendation_application_overhead_values(self) -> pulumi.Output[Optional[Sequence['outputs.OceanRightSizingRuleRecommendationApplicationOverheadValue']]]:
        return pulumi.get(self, "recommendation_application_overhead_values")

    @property
    @pulumi.getter(name="restartReplicas")
    def restart_replicas(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "restart_replicas")

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "rule_name")

