from mcp.server.fastmcp import FastMCP
from kubernetes import client, config
import json
from typing import Optional, List, Dict, Any

# Create an MCP server
mcp = FastMCP("Kubernetes Manager")

# Initialize Kubernetes client
try:
    # Try to load from within cluster first
    config.load_incluster_config()
except config.ConfigException:
    # Fall back to local kubeconfig
    config.load_kube_config()

# Create API clients
core_v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()
batch_v1 = client.BatchV1Api()

# ---- CRUD Operations ----

@mcp.tool()
def get_resources(resource_type: str, namespace: str = "default", name: Optional[str] = None) -> str:
    """
    Get Kubernetes resources of specified type.
    
    Args:
        resource_type: Type of resource (pod, deployment, service, job)
        namespace: Kubernetes namespace
        name: Optional specific resource name
    
    Returns:
        JSON string with resource information
    """
    try:
        if resource_type.lower() == "pod":
            if name:
                result = core_v1.read_namespaced_pod(name, namespace)
                return json.dumps(client.ApiClient().sanitize_for_serialization(result))
            else:
                result = core_v1.list_namespaced_pod(namespace)
                items = [{"name": i.metadata.name, "status": i.status.phase} for i in result.items]
                return json.dumps(items)
                
        elif resource_type.lower() == "deployment":
            if name:
                result = apps_v1.read_namespaced_deployment(name, namespace)
                return json.dumps(client.ApiClient().sanitize_for_serialization(result))
            else:
                result = apps_v1.list_namespaced_deployment(namespace)
                items = [{"name": i.metadata.name, "replicas": i.spec.replicas} for i in result.items]
                return json.dumps(items)
                
        elif resource_type.lower() == "service":
            if name:
                result = core_v1.read_namespaced_service(name, namespace)
                return json.dumps(client.ApiClient().sanitize_for_serialization(result))
            else:
                result = core_v1.list_namespaced_service(namespace)
                items = [{"name": i.metadata.name, "type": i.spec.type, "cluster_ip": i.spec.cluster_ip} for i in result.items]
                return json.dumps(items)
                
        elif resource_type.lower() == "job":
            if name:
                result = batch_v1.read_namespaced_job(name, namespace)
                return json.dumps(client.ApiClient().sanitize_for_serialization(result))
            else:
                result = batch_v1.list_namespaced_job(namespace)
                items = [{"name": i.metadata.name, "completions": i.spec.completions} for i in result.items]
                return json.dumps(items)
        else:
            return f"Unsupported resource type: {resource_type}"
    except Exception as e:
        return f"Error retrieving {resource_type}: {str(e)}"

@mcp.tool()
def create_resource(resource_type: str, namespace: str, manifest: str) -> str:
    """
    Create a Kubernetes resource from a JSON manifest.
    
    Args:
        resource_type: Type of resource (pod, deployment, service, job)
        namespace: Kubernetes namespace
        manifest: JSON string with resource definition
    
    Returns:
        Result of creation operation
    """
    try:
        manifest_dict = json.loads(manifest)
        if resource_type.lower() == "pod":
            result = core_v1.create_namespaced_pod(namespace, manifest_dict)
            return f"Pod {result.metadata.name} created"
            
        elif resource_type.lower() == "deployment":
            result = apps_v1.create_namespaced_deployment(namespace, manifest_dict)
            return f"Deployment {result.metadata.name} created"
            
        elif resource_type.lower() == "service":
            result = core_v1.create_namespaced_service(namespace, manifest_dict)
            return f"Service {result.metadata.name} created"
            
        elif resource_type.lower() == "job":
            result = batch_v1.create_namespaced_job(namespace, manifest_dict)
            return f"Job {result.metadata.name} created"
        else:
            return f"Unsupported resource type: {resource_type}"
    except Exception as e:
        return f"Error creating {resource_type}: {str(e)}"

@mcp.tool()
def delete_resource(resource_type: str, name: str, namespace: str = "default") -> str:
    """
    Delete a Kubernetes resource.
    
    Args:
        resource_type: Type of resource (pod, deployment, service, job)
        name: Name of the resource to delete
        namespace: Kubernetes namespace
    
    Returns:
        Result of deletion operation
    """
    try:
        if resource_type.lower() == "pod":
            core_v1.delete_namespaced_pod(name, namespace)
            return f"Pod {name} deleted"
            
        elif resource_type.lower() == "deployment":
            apps_v1.delete_namespaced_deployment(name, namespace)
            return f"Deployment {name} deleted"
            
        elif resource_type.lower() == "service":
            core_v1.delete_namespaced_service(name, namespace)
            return f"Service {name} deleted"
            
        elif resource_type.lower() == "job":
            batch_v1.delete_namespaced_job(name, namespace)
            return f"Job {name} deleted"
        else:
            return f"Unsupported resource type: {resource_type}"
    except Exception as e:
        return f"Error deleting {resource_type}: {str(e)}"

# ---- Observability ----

@mcp.tool()
def get_pod_logs(pod_name: str, namespace: str = "default", container: Optional[str] = None, tail_lines: int = 100) -> str:
    """
    Get logs from a pod.
    
    Args:
        pod_name: Name of the pod
        namespace: Kubernetes namespace
        container: Optional container name (if pod has multiple containers)
        tail_lines: Number of lines to return from the end
    
    Returns:
        Pod logs
    """
    try:
        return core_v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            container=container,
            tail_lines=tail_lines
        )
    except Exception as e:
        return f"Error getting logs for pod {pod_name}: {str(e)}"

@mcp.tool()
def describe_resource(resource_type: str, name: str, namespace: str = "default") -> str:
    """
    Get detailed information about a Kubernetes resource.
    
    Args:
        resource_type: Type of resource (pod, deployment, service, job)
        name: Name of the resource
        namespace: Kubernetes namespace
    
    Returns:
        Detailed description of the resource
    """
    try:
        if resource_type.lower() == "pod":
            result = core_v1.read_namespaced_pod(name, namespace)
        elif resource_type.lower() == "deployment":
            result = apps_v1.read_namespaced_deployment(name, namespace)
        elif resource_type.lower() == "service":
            result = core_v1.read_namespaced_service(name, namespace)
        elif resource_type.lower() == "job":
            result = batch_v1.read_namespaced_job(name, namespace)
        else:
            return f"Unsupported resource type: {resource_type}"
            
        # Convert to dict and then to formatted JSON
        resource_dict = client.ApiClient().sanitize_for_serialization(result)
        return json.dumps(resource_dict, indent=2)
    except Exception as e:
        return f"Error describing {resource_type} {name}: {str(e)}"

@mcp.tool()
def get_namespaces() -> str:
    """
    List all namespaces in the cluster.
    
    Returns:
        JSON string with namespace information
    """
    try:
        result = core_v1.list_namespace()
        namespaces = [{"name": item.metadata.name, "status": item.status.phase} for item in result.items]
        return json.dumps(namespaces)
    except Exception as e:
        return f"Error listing namespaces: {str(e)}"

if __name__ == "__main__":
    mcp.run()
