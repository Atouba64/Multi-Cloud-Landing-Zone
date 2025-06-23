import json
import logging
import os
from diagrams import Diagram, Cluster
from diagrams.aws.general import Account
from diagrams.azure.general import ManagementGroups
import terraform_docs

class DocumentationGenerator:
    def __init__(self):
        self.logger = logging.getLogger("DocumentationGenerator")

    def generate_all(self):
        self.logger.info("Generating documentation")
        self._generate_terraform_docs()
        self._generate_architecture_diagrams()
        self._generate_compliance_report()

    def _generate_terraform_docs(self):
        self.logger.info("Generating Terraform documentation")
        terraform_docs.generate(
            output_dir="docs/terraform",
            module_paths=["modules/aws", "modules/azure"]
        )

    def _generate_architecture_diagrams(self):
        self.logger.info("Generating architecture diagrams")
        with Diagram("Multi-Cloud Landing Zone", show=False, filename="docs/architecture"):
            with Cluster("AWS"):
                aws_account = Account("AWS Account")
                
            with Cluster("Azure"):
                azure_mg = ManagementGroups("Azure Management Group")
            
            aws_account >> azure_mg

    def _generate_compliance_report(self):
        self.logger.info("Generating compliance report")
        # Generate FedRAMP/NIST compliance documentation
        pass
