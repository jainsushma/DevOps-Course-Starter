
variable "location" {
description = "The Azure location where all resources in thisdeployment should be created" 
default = "uksouth"
}

variable "SECRET_KEY" {
    
}

variable "CLIENT_ID" {

}

variable "CLIENT_SECRET" {
sensitive   = true
}

variable "DB_NAME" {
    default ="module12-azure-cosmos-account-sj"
}

variable "OAUTHLIB_INSECURE_TRANSPORT"{
    default =1
}

