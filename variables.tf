variable "SECRET_KEY" {
    
}

variable "CLIENT_ID" {

}

variable "CLIENT_SECRET" {
sensitive   = true
}

variable "LOGGLY_TOKEN" {
sensitive   = true
}

variable "LOG_LEVEL" {
default   = "INFO"
}