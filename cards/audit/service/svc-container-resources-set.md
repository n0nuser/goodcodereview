---
id: svc-container-resources-set
level: service
tags: [reliability, performance, config]
severity: should-fix
status: stable
lang: core
applies_when: A change adds or edits a Kubernetes workload manifest or Helm values with containers.
context: [server]
tool_gate: An admission policy or manifest linter that rejects a container with no CPU request, memory request or memory limit; a namespace LimitRange that supplies defaults.
note: Microsoft says to set requests and limits on every pod, AWS says each container including sidecars needs its own, and Google says to give every container CPU and memory requests and to match memory requests to limits. Google advises leaving CPU limits unset, so the Rule asks for a memory limit only. The Kubernetes concepts page describes the mechanism and states no rule, so it is not counted
borrowed_from:
  - https://learn.microsoft.com/en-us/azure/aks/developer-best-practices-resource-management
  - https://docs.aws.amazon.com/eks/latest/best-practices/cost-opt-compute.html
  - https://cloud.google.com/kubernetes-engine/docs/best-practices/cost-optimization
---

**Rule.** Set a CPU request, a memory request and a memory limit on every container in the manifest, sidecars included.

**Why.** The scheduler places pods by their requests. A container with none looks free, so nodes get overpacked and neighbours starve each other. A cluster with quotas can also reject the deployment. Without a memory limit, one leak takes the whole node down instead of restarting one container. A CPU limit is left out on purpose: it throttles a container that has spare node capacity, so set the CPU request to what the service needs and leave the limit off unless you have a reason. Size the numbers from measured use, not a guess copied from another service.

**FAIL**

```yaml
containers:
  - name: api
    image: registry.example.com/api:1.8.2
  - name: log-shipper
    image: registry.example.com/shipper:0.4.0
```

**PASS**

```yaml
containers:
  - name: api
    image: registry.example.com/api:1.8.2
    resources:
      requests: { cpu: 250m, memory: 256Mi }
      limits: { memory: 256Mi }
  - name: log-shipper
    image: registry.example.com/shipper:0.4.0
    resources:
      requests: { cpu: 50m, memory: 64Mi }
      limits: { memory: 64Mi }
```

**Counterpoint.** "The namespace already has a LimitRange with defaults." Then the manifest can omit the block, as long as the repo shows that policy and the defaults fit the workload. Default values are one size for every container, so a service with a real profile still needs its own numbers.
