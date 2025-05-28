# AI_Bot

# devops06

pipeline{
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/AnnaBinoy09/demo_devops'
            }
        }
       
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
       
        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
       
        stage('Archive artifacts') {
            steps {
                archiveArtifacts artifacts: '**/target/*.jar', allowEmptyArchive: true
            }
        }
       
        stage('Deploy') {
            steps {
                sh """
                    export ANSIBLE_HOST_KEY_CHECKING=False
                    ansible-playbook -i hosts.ini deploy.yml --extra-vars "ansible_become_pass=exam@cse"
                """
            }
        }
    }
}


---
- name: Deploy Artifact to Localhost
  hosts: localhost
  tasks:
  - name: Copy the artifact to the target location
    become: true
    become_user: student
    become_method: su
    copy:
          src: "/var/lib/jenkins/workspace/HelloMaven-CI/target/my-app-1.0-SNAPSHOT.jar"
          dest: "/home/student/priti1/t.jar"

- name: First Playbook 
  hosts: local 
  connection: local 
  tasks: 
    - name: My first task 
      debug: 
        msg: "Ansible is a config mgmt tool"

#!/usr/bin/python 
from ansible.module_utils.basic import AnsibleModule 
def walk(): 
module_args = dict( 
name=dict(type='str', required=True) 
) 
module = AnsibleModule(argument_spec=module_args) 
 result = {"changed": False, "message": f"Welcome, {module.params['name']}!"} module.exit_json(**result) 
if __name__ == '__main__': 
walk() 


--- 
- name: Ansible with one module 
  hosts: localhost 
  gather_facts: no 
  tasks: 
    - name: Welcome friends 
      firstmodule: 
        name: "Ansible" 
      register: result 
    - name: Show message 
      debug:
        msg: "{{ result.message }}" 

****
