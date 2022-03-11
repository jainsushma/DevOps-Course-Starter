output "webapp_url" { 
    value = "https://${azurerm_app_service.main.default_site_hostname}"
 }

output "cd_webhook" {
    value = "https://${azurerm_app_service.main.site_credential[0].username}:${azurerm_app_service.main.site_credential[0].password}@${azurerm_app_service.main.name}.scm.azurewebsites.net/docker/hook"
    sensitive = true
}

# https://$module12-azure-terraform-sj:cqqHTnbisgShLtde2QMFqqdYA6pnWf797Ab3F5patRwbM55tszc8ondJqNy1@module12-azure-terraform-sj.scm.azurewebsites.net/docker/hook