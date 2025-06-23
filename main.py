#!/usr/bin/env python3
"""
Main orchestration script for Multi-Cloud Landing Zone deployment
Handles end-to-end provisioning and configuration
"""
# main.py
import os
import subprocess
import logging
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.monitor import MonitorManagementClient
import boto3
from botocore.exceptions import NoCredentialsError
from aws_manager import AWSManager
from azure_manager import AzureManager
from security_baselines import SecurityBaselines
from observability import ObservabilitySetup
from documentation import DocumentationGenerator
import logging
import json

class MultiCloudLandingZone:
    def __init__(self):
        self._setup_logging()
        self.config = self._load_config()
        self.aws = AWSManager(self.config['aws'])
        self.azure = AzureManager(self.config['azure'])
        self.security = SecurityBaselines(self.config['security'])
        self.observability = ObservabilitySetup(self.config['monitoring'])
        self.docs = DocumentationGenerator()

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("MultiCloudLandingZone")

    def _load_config(self):
        with open('config/landing_zone_config.json') as f:
            return json.load(f)

    def deploy(self):
        try:
            self.logger.info("Starting multi-cloud deployment")
            
            # Infrastructure deployment
            self.aws.deploy_foundation()
            self.azure.deploy_foundation()
            
            # Security and compliance
            self.security.apply_baselines()
            
            # Observability
            self.observability.setup_monitoring()
            
            # Documentation
            self.docs.generate_all()
            
            self.logger.info("Deployment completed successfully")
            return True
        except Exception as e:
            self.logger.error(f"Deployment failed: {str(e)}")
            raise

if __name__ == "__main__":
    landing_zone = MultiCloudLandingZone()
    landing_zone.deploy()
