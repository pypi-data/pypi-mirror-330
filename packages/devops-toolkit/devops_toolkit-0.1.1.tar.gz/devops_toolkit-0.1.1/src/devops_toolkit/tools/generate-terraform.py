# This file should be created as src/devops_toolkit/tools/terraform_generator.py

"""
DevOps Toolkit - Terraform Generator Module

This module provides functionality for generating Terraform code from infrastructure templates.
"""
import os
import json
from typing import Dict, Any, List
from datetime import datetime

# Import logger
from devops_toolkit.logging import get_logger

# Initialize logger
logger = get_logger(__name__)

class TerraformGenerationError(Exception):
    """Raised when Terraform generation encounters an error."""
    pass

def generate_azure_terraform(template: Dict[str, Any], output_dir: str) -> None:
    """
    Generate Azure-specific Terraform code from template.
    
    Args:
        template: Parsed template data
        output_dir: Directory to output Terraform code
    """
    # Generate providers.tf
    providers_tf = """# Azure Provider Configuration
provider "azurerm" {
  features {}
}

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  
  backend "local" {
    path = "./terraform.tfstate"
  }
}
"""
    
    # Generate variables.tf
    variables_tf = """# Variables

"""
    
    # Process template variables
    if "variables" in template:
        for var_name, var_def in template["variables"].items():
            var_type = var_def.get("type", "string")
            var_default = var_def.get("default", None)
            var_desc = var_def.get("description", f"Variable for {var_name}")
            
            # Map YAML types to Terraform types
            tf_type = {
                "string": "string",
                "number": "number",
                "boolean": "bool",
                "list": "list(string)", 
                "map": "map(string)"
            }.get(var_type, "string")
            
            # Format default value based on type
            default_val = ""
            if var_default is not None:
                if var_type == "string":
                    default_val = f'default = "{var_default}"'
                elif var_type in ["number", "boolean"]:
                    default_val = f'default = {var_default}'
                elif var_type == "list" and isinstance(var_default, list):
                    default_val = f'default = {json.dumps(var_default)}'
                elif var_type == "map" and isinstance(var_default, dict):
                    default_val = f'default = {json.dumps(var_default)}'
            
            variables_tf += f"""
variable "{var_name}" {{
  description = "{var_desc}"
  type        = {tf_type}
  {default_val}
}}
"""
    
    # Generate main.tf
    main_tf = f"""# Main Terraform Configuration
# Generated from template: {template.get("metadata", {}).get("name", "app-stack")}

"""
    
    # Generate resource group
    if "resource_group" in template.get("resources", {}):
        rg = template["resources"]["resource_group"]
        rg_name = rg.get("name", "${var.app_name}-${var.environment}-rg")
        rg_location = rg.get("location", "${var.location}")
        
        main_tf += f"""
# Resource Group
resource "azurerm_resource_group" "main" {{
  name     = "{rg_name}"
  location = "{rg_location}"
  
  tags = {{
    application = var.app_name
    environment = var.environment
    managed_by  = "terraform"
  }}
}}

"""
    
    # Generate Virtual Network
    if "virtual_network" in template.get("resources", {}):
        vnet = template["resources"]["virtual_network"]
        vnet_name = vnet.get("name", "${var.app_name}-${var.environment}-vnet")
        address_space = vnet.get("properties", {}).get("address_space", ["10.0.0.0/16"])
        subnets = vnet.get("properties", {}).get("subnets", [])
        
        main_tf += f"""
# Virtual Network
resource "azurerm_virtual_network" "main" {{
  name                = "{vnet_name}"
  address_space       = {json.dumps(address_space)}
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}}

"""
        
        # Generate Subnets
        for idx, subnet in enumerate(subnets):
            subnet_name = subnet.get("name", f"subnet-{idx}")
            subnet_prefix = subnet.get("address_prefix", "10.0.0.0/24")
            
            main_tf += f"""
resource "azurerm_subnet" "{subnet_name.replace('-', '_')}" {{
  name                 = "{subnet_name}"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["{subnet_prefix}"]
}}
"""
    
    # Generate AKS Cluster
    if "kubernetes_cluster" in template.get("resources", {}):
        aks = template["resources"]["kubernetes_cluster"]
        aks_name = aks.get("name", "${var.app_name}-${var.environment}-aks")
        
        main_tf += f"""
# AKS Cluster
resource "azurerm_kubernetes_cluster" "main" {{
  name                = "{aks_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "{aks_name}"
  
  default_node_pool {{
    name       = "default"
    node_count = var.node_count
    vm_size    = var.vm_size
    vnet_subnet_id = azurerm_subnet.kubernetes_subnet.id
    
    enable_auto_scaling = true
    min_count           = 1
    max_count           = 5
  }}
  
  identity {{
    type = "SystemAssigned"
  }}
  
  network_profile {{
    network_plugin = "azure"
    network_policy = "calico"
    service_cidr   = "10.1.0.0/16"
    dns_service_ip = "10.1.0.10"
  }}
  
  role_based_access_control_enabled = true
}}
"""
    
    # Generate Container Registry
    if "container_registry" in template.get("resources", {}):
        acr = template["resources"]["container_registry"]
        acr_name = acr.get("name", "${var.app_name}${var.environment}acr")
        
        main_tf += f"""
# Azure Container Registry
resource "azurerm_container_registry" "main" {{
  name                = "{acr_name}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Standard"
  admin_enabled       = true
}}

# Grant AKS access to ACR
resource "azurerm_role_assignment" "aks_to_acr" {{
  principal_id                     = azurerm_kubernetes_cluster.main.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.main.id
  skip_service_principal_aad_check = true
}}
"""
    
    # Generate Application Gateway
    if "application_gateway" in template.get("resources", {}):
        appgw = template["resources"]["application_gateway"]
        appgw_name = appgw.get("name", "${var.app_name}-${var.environment}-appgw")
        
        main_tf += f"""
# Public IP for Application Gateway
resource "azurerm_public_ip" "app_gateway" {{
  name                = "{appgw_name}-ip"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  allocation_method   = "Static"
  sku                 = "Standard"
}}

# Application Gateway
resource "azurerm_application_gateway" "main" {{
  name                = "{appgw_name}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  sku {{
    name     = "Standard_v2"
    tier     = "Standard_v2"
    capacity = 2
  }}

  gateway_ip_configuration {{
    name      = "appGatewayIpConfig"
    subnet_id = azurerm_subnet.gateway_subnet.id
  }}

  frontend_port {{
    name = "httpPort"
    port = 80
  }}

  frontend_port {{
    name = "httpsPort"
    port = 443
  }}

  frontend_ip_configuration {{
    name                 = "appGatewayFrontendIP"
    public_ip_address_id = azurerm_public_ip.app_gateway.id
  }}

  backend_address_pool {{
    name = "defaultBackendPool"
  }}

  backend_http_settings {{
    name                  = "defaultHttpSettings"
    cookie_based_affinity = "Disabled"
    port                  = 80
    protocol              = "Http"
    request_timeout       = 30
  }}

  http_listener {{
    name                           = "httpListener"
    frontend_ip_configuration_name = "appGatewayFrontendIP"
    frontend_port_name             = "httpPort"
    protocol                       = "Http"
  }}

  request_routing_rule {{
    name                       = "defaultRule"
    rule_type                  = "Basic"
    http_listener_name         = "httpListener"
    backend_address_pool_name  = "defaultBackendPool"
    backend_http_settings_name = "defaultHttpSettings"
    priority                   = 100
  }}
}}
"""
    
    # Generate SQL Database
    if "sql_server" in template.get("resources", {}) and "sql_database" in template.get("resources", {}):
        sql = template["resources"]["sql_server"]
        db = template["resources"]["sql_database"]
        sql_name = sql.get("name", "${var.app_name}-${var.environment}-sqlserver")
        db_name = db.get("name", "${var.app_name}-${var.environment}-db")
        
        main_tf += f"""
# SQL Server
resource "azurerm_mssql_server" "main" {{
  name                         = "{sql_name}"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = azurerm_resource_group.main.location
  version                      = "12.0"
  administrator_login          = var.admin_username
  administrator_login_password = var.admin_password
  
  public_network_access_enabled = false
}}

# SQL Database
resource "azurerm_mssql_database" "main" {{
  name           = "{db_name}"
  server_id      = azurerm_mssql_server.main.id
  sku_name       = "S1"
  max_size_gb    = 250
  zone_redundant = false
}}

# Private Endpoint for SQL
resource "azurerm_private_endpoint" "sql" {{
  name                = "{sql_name}-pe"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.database_subnet.id

  private_service_connection {{
    name                           = "sqlprivatelink"
    private_connection_resource_id = azurerm_mssql_server.main.id
    is_manual_connection           = false
    subresource_names              = ["sqlServer"]
  }}
}}
"""
    
    # Generate Redis Cache
    if "redis_cache" in template.get("resources", {}):
        redis = template["resources"]["redis_cache"]
        redis_name = redis.get("name", "${var.app_name}-${var.environment}-redis")
        
        main_tf += f"""
# Redis Cache
resource "azurerm_redis_cache" "main" {{
  name                = "{redis_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  capacity            = 1
  family              = "C"
  sku_name            = "Standard"
  enable_non_ssl_port = false
  minimum_tls_version = "1.2"
  
  subnet_id           = azurerm_subnet.redis_subnet.id
}}
"""
    
    # Generate Storage Account
    if "storage_account" in template.get("resources", {}):
        sa = template["resources"]["storage_account"]
        sa_name = sa.get("name", "${var.app_name}${var.environment}storage")
        
        main_tf += f"""
# Storage Account
resource "azurerm_storage_account" "main" {{
  name                     = "{sa_name}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  access_tier              = "Hot"
  
  enable_https_traffic_only = true
  min_tls_version           = "TLS1_2"
  
  network_rules {{
    default_action = "Deny"
    virtual_network_subnet_ids = [
      azurerm_subnet.function_subnet.id
    ]
  }}
}}
"""
    
    # Generate Key Vault
    if "key_vault" in template.get("resources", {}):
        kv = template["resources"]["key_vault"]
        kv_name = kv.get("name", "${var.app_name}-${var.environment}-kv")
        
        main_tf += f"""
# Key Vault
resource "azurerm_key_vault" "main" {{
  name                       = "{kv_name}"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days = 7
  purge_protection_enabled   = false
  sku_name                   = "standard"
  
  access_policy {{
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id
    
    key_permissions = [
      "Get", "List", "Create", "Delete"
    ]
    
    secret_permissions = [
      "Get", "List", "Set", "Delete"
    ]
    
    certificate_permissions = [
      "Get", "List", "Create", "Delete"
    ]
  }}
}}

# Get current Azure credentials
data "azurerm_client_config" "current" {{}}
"""
    
    # Generate Function App
    if "function_app" in template.get("resources", {}):
        fn = template["resources"]["function_app"]
        fn_name = fn.get("name", "${var.app_name}-${var.environment}-function")
        plan_name = template["resources"].get("function_app_plan", {}).get("name", "${var.app_name}-${var.environment}-asp")
        
        main_tf += f"""
# App Service Plan
resource "azurerm_app_service_plan" "main" {{
  name                = "{plan_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true
  
  sku {{
    tier = "PremiumV2"
    size = "P1v2"
  }}
}}

# Function App
resource "azurerm_function_app" "main" {{
  name                       = "{fn_name}"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  app_service_plan_id        = azurerm_app_service_plan.main.id
  storage_account_name       = azurerm_storage_account.main.name
  storage_account_access_key = azurerm_storage_account.main.primary_access_key
  os_type                    = "linux"
  version                    = "~4"
  
  app_settings = {{
    FUNCTIONS_WORKER_RUNTIME       = "dotnet"
    WEBSITE_RUN_FROM_PACKAGE       = "1"
    APPINSIGHTS_INSTRUMENTATIONKEY = azurerm_application_insights.main.instrumentation_key
  }}
  
  site_config {{
    linux_fx_version = "DOTNET|6.0"
  }}
}}
"""
    
    # Generate Log Analytics and Application Insights
    if "log_analytics_workspace" in template.get("resources", {}) and "application_insights" in template.get("resources", {}):
        law = template["resources"]["log_analytics_workspace"]
        ai = template["resources"]["application_insights"]
        law_name = law.get("name", "${var.app_name}-${var.environment}-logs")
        ai_name = ai.get("name", "${var.app_name}-${var.environment}-appinsights")
        
        main_tf += f"""
# Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "main" {{
  name                = "{law_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}}

# Application Insights
resource "azurerm_application_insights" "main" {{
  name                = "{ai_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  workspace_id        = azurerm_log_analytics_workspace.main.id
  application_type    = "web"
}}
"""
    
    # Generate outputs.tf
    outputs_tf = """# Outputs

"""
    
    # Process template outputs
    if "outputs" in template:
        for out_name, out_def in template["outputs"].items():
            out_desc = out_def.get("description", f"Output for {out_name}")
            out_value = out_def.get("value", "")
            
            # Map template output references to Terraform
            # This is a simplified version and would need enhancement for real use
            out_value = out_value.replace("${resources.kubernetes_cluster.name}", "azurerm_kubernetes_cluster.main.name")
            out_value = out_value.replace("${resources.container_registry.login_server}", "azurerm_container_registry.main.login_server")
            out_value = out_value.replace("${resources.app_gateway_public_ip.ip_address}", "azurerm_public_ip.app_gateway.ip_address")
            out_value = out_value.replace("${resources.application_insights.instrumentation_key}", "azurerm_application_insights.main.instrumentation_key")
            out_value = out_value.replace("${resources.sql_server.fully_qualified_domain_name}", "azurerm_mssql_server.main.fully_qualified_domain_name")
            out_value = out_value.replace("${resources.redis_cache.hostname}", "azurerm_redis_cache.main.hostname")
            out_value = out_value.replace("${resources.function_app.default_hostname}", "azurerm_function_app.main.default_hostname")
            
            outputs_tf += f"""
output "{out_name}" {{
  description = "{out_desc}"
  value       = {out_value}
}}
"""
    
    # Default outputs
    outputs_tf += """
output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.main.name
}

output "aks_kube_config" {
  description = "Kubernetes configuration for AKS"
  value       = azurerm_kubernetes_cluster.main.kube_config_raw
  sensitive   = true
}
"""
    
    # Write files
    with open(os.path.join(output_dir, "providers.tf"), "w") as f:
        f.write(providers_tf)
    
    with open(os.path.join(output_dir, "variables.tf"), "w") as f:
        f.write(variables_tf)
    
    with open(os.path.join(output_dir, "main.tf"), "w") as f:
        f.write(main_tf)
    
    with open(os.path.join(output_dir, "outputs.tf"), "w") as f:
        f.write(outputs_tf)
    
    # Additional file: README.md with basic usage instructions
    readme_md = f"""# Terraform for Azure Application Stack

This Terraform configuration deploys a comprehensive application stack on Azure including:

* Resource Group
* Virtual Network with multiple subnets
* AKS Cluster
* Container Registry
* Application Gateway
* SQL Database
* Redis Cache
* Storage Account
* Key Vault
* Function App
* Application Insights

## Prerequisites

* Azure CLI
* Terraform 1.0+
* Azure subscription

## Usage

1. Initialize Terraform:
   ```
   terraform init
   ```

2. Create or edit the `terraform.tfvars` file with your variable values:
   ```
   app_name       = "myapp"
   environment    = "dev"
   location       = "eastus"
   admin_username = "azureadmin"
   admin_password = "YourSecurePassword123!"
   node_count     = 3
   vm_size        = "Standard_DS2_v2"
   ```

3. Preview the changes:
   ```
   terraform plan
   ```

4. Apply the changes:
   ```
   terraform apply
   ```

5. Clean up when done:
   ```
   terraform destroy
   ```

## Notes

* This configuration creates Azure resources that may incur costs.
* The private IP ranges used are for demonstration only.
* Production deployments may require additional security configurations.
"""
    
    with open(os.path.join(output_dir, "README.md"), "w") as f:
        f.write(readme_md)
    
    # Create terraform.tfvars file for easy customization
    tfvars = """# Customize these variables for your deployment
app_name       = "myapp"
environment    = "dev"
location       = "eastus"
admin_username = "azureadmin"
admin_password = "YourSecurePassword123!"
node_count     = 3
vm_size        = "Standard_DS2_v2"
"""
    
    with open(os.path.join(output_dir, "terraform.tfvars"), "w") as f:
        f.write(tfvars)


def generate_terraform(template: Dict[str, Any], output_dir: str, provider: str) -> Dict[str, Any]:
    """
    Generate Terraform code from a template dictionary.
    
    Args:
        template: Template data
        output_dir: Directory to output Terraform code
        provider: Infrastructure provider (aws, azure, gcp, kubernetes)
        
    Returns:
        Dict with generation status and details
    """
    # Define the standard files we'll be generating
    files = [
        "main.tf",
        "variables.tf",
        "outputs.tf",
        "providers.tf"
    ]
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate based on provider
    if provider.lower() == "azure" and "resources" in template and len(template["resources"]) > 3:
        # This appears to be a complex Azure template
        try:
            logger.info(f"Generating complex Azure template")
            # Call the specialized Azure generator
            generate_azure_terraform(template, output_dir)
            # Add README.md and terraform.tfvars to the files list
            files.extend(["README.md", "terraform.tfvars"])
            return {
                "status": "success",
                "provider": provider,
                "template_name": template.get("metadata", {}).get("name", "template"),
                "output_dir": output_dir,
                "files": files,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error generating Azure Terraform: {str(e)}", exc_info=True)
            raise TerraformGenerationError(f"Failed to generate Azure Terraform: {str(e)}")
    else:
        # Basic generation for other providers (stub)
        logger.warning(f"Complex generation for {provider} not implemented")
        # Write basic files
        with open(os.path.join(output_dir, "main.tf"), "w") as f:
            f.write(f"# Basic {provider} Terraform configuration\n# TODO: Implement detailed generation\n")
        
        with open(os.path.join(output_dir, "variables.tf"), "w") as f:
            f.write("# Variables\n")
        
        with open(os.path.join(output_dir, "outputs.tf"), "w") as f:
            f.write("# Outputs\n")
        
        with open(os.path.join(output_dir, "providers.tf"), "w") as f:
            f.write(f"# Provider configuration for {provider}\n")
        
        return {
            "status": "partial",
            "provider": provider,
            "template_name": template.get("metadata", {}).get("name", "template"),
            "output_dir": output_dir,
            "files": files,
            "generated_at": datetime.now().isoformat(),
            "message": f"Basic template generated. Detailed {provider} generation not implemented."
        }
