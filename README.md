<h1>Azure RM Storage Account Keys module</h1>
<p>In a lot of automation scenarios there is need to create a new storage account and pass on the 'key' to subsequent tasks. Currently, there is no azure module that retrieves the keys. The way around is to run a powershell command or make a call to the ARM REST api.</p>
<p>This modules demonstrates how to create a custom module for Ansible.</p>
<ol>
  <li>
    <h3><strong>azure_rm_storageaccount_keys.py</strong></h3>
    <p>Demostrates how to create a custom module for ansible using the standard Ansible module structure <a href="http://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html">New module development</a>.
    </p>
  </li>
  <li>
    <h3><strong>azure_rm_storageaccountkeys_facts.py</strong></h3>
    <p>
      This implementation follows the same pattern as other Azure modules built for Ansible. It uses base functionality of azure_rm_common.py to handle common functionality like authentication, error handling, exceptions and instantiation of resource clients.
    </p>
  </li>
</ol>
