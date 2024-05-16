from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import VirtualMachine,VirtualMachineExtension
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

#managed_identity_client_id = ''
#credential = ManagedIdentityCredential(client_id=managed_identity_client_id)

credential = DefaultAzureCredential()

subscription_id = "xxxx"
compute_client = ComputeManagementClient(credential, subscription_id)

# List all VMs in the subscription
vm_list = compute_client.virtual_machines.list_all()

def reset_password(resource_group_name, vm_name, new_password):
    try:
        # Get the VM
        vm = compute_client.virtual_machines.get(resource_group_name, vm_name)
        
        # Reset the password
        print(f"Password reset for VM {vm_name} in resource group {resource_group_name} for : {vm.os_profile.admin_username} which is {vm.storage_profile.os_disk.os_type}")
        if (vm.storage_profile.os_disk.os_type).lower=='linux':
            print('Linux')
            response = compute_client.virtual_machine_extensions.begin_create_or_update(
                resource_group_name=resource_group_name, 
                vm_name=vm_name, 
                vm_extension_name='enablevmaccess', 
                extension_parameters=VirtualMachineExtension(
                    location=vm.location,
                    protected_settings={'username':  vm.os_profile.admin_username, 'password': new_password}))
        else:
            print('Windows')
    except Exception as e:
        print(f"An error occurred: {e}")
# Call the function to reset the password
          reset_password('resource-grp', 'vm name', 'pwd')
