terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>2.0"
    }
  }
  
   backend "azurerm" {
        resource_group_name  = "AmericanExpress21Group1_SushmaJain_ProjectExercise"
        storage_account_name = "amex21group1pesj"
        container_name       = "amex21group1pesj"
        key                  = "terraform.tfstate"
    }
}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name = "AmericanExpress21Group1_SushmaJain_ProjectExercise"
}

resource "azurerm_app_service_plan" "main" {
 name = "terraformed-asp"
 location = data.azurerm_resource_group.main.location
 resource_group_name = data.azurerm_resource_group.main.name
 kind = "Linux"
 reserved = true
 sku {
 tier = "Basic"
 size = "B1"
 }
}

resource "azurerm_app_service" "main" {
 name = "module13-azure-terraform-sj"
 location = data.azurerm_resource_group.main.location
 resource_group_name = data.azurerm_resource_group.main.name
 app_service_plan_id = azurerm_app_service_plan.main.id
 
 site_config {
 app_command_line = ""
 linux_fx_version = "DOCKER|sjain309/todo-app-prod:latest"
 }

 app_settings = {
  "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
  "CLIENT" = azurerm_cosmosdb_account.main.connection_strings[0]
  "CLIENTID"= var.CLIENT_ID
  "CLIENTSECRET"=var.CLIENT_SECRET
  "SECRET_KEY" = var.SECRET_KEY
  "LOG_LEVEL" = var.LOG_LEVEL
  "LOGGLY_TOKEN" = var.LOGGLY_TOKEN
  "DBNAME"= azurerm_cosmosdb_mongo_database.main.name
  "OAUTHLIB_INSECURE_TRANSPORT"=1
 }
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "module12-azure-cosmos-account-sj"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  enable_automatic_failover = true

  capabilities {
    name = "MongoDBv3.4"
  }

  capabilities {
    name = "EnableMongo"
  }

  capabilities {
    name = "EnableServerless"
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "module12-cosmos-mongo-db-sj"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name

  lifecycle {
    prevent_destroy = true
  }
}