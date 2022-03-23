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

