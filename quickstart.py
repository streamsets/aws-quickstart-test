import os
import sys
from streamsets.sdk import ControlHub

sch = ControlHub(credential_id=sys.argv[1], token=sys.argv[2])
print(sch.version)

environment_builder = sch.get_environment_builder(environment_type='SELF')
environment = environment_builder.build(environment_name='Self-Managed-Env-AWS_QuickStart',
                                        environment_tags=['self-managed-tag'],
                                        allow_nightly_engine_builds=False)
sch.add_environment(environment)
sch.activate_environment(environment)

deployment_builder = sch.get_deployment_builder(deployment_type='SELF')
deployment = deployment_builder.build(deployment_name='Self-Managed-Deployment-AWS_QuickStart',
                                      environment=environment,
                                      engine_type='DC',
                                      engine_version='5.0.0',
                                      deployment_tags=['self-managed-tag'])
deployment.install_type = 'TARBALL'
# deployment.install_type = 'DOCKER'
sch.add_deployment(deployment)
# equivalent to clicking on 'Start & Generate Install Script'
sch.start_deployment(deployment)
# add sample stage libs
# deployment.engine_configuration.stage_libs = ['dataformats', 'basic', 'dev', 'jdbc', 'aws']
# update deployment with stage libs
# sch.update_deployment(deployment)

install_script = sch.get_self_managed_deployment_install_script(
    deployment, install_mechanism="BACKGROUND")
agent_install_script = install_script.replace('--background', '--no-prompt --background').replace(
    '--background', '--install-dir=~/.streamsets/install --background').replace('--background', '--download-dir=~/.streamsets/download --background')
# prints install script
print(agent_install_script)
# deploys engine

os.system(agent_install_script)
