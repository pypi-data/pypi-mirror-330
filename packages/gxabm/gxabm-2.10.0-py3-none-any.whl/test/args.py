import sys
import argparse

#
# parser = argparse.ArgumentParser()
# parser.add_argument('input_dirs', nargs='+')
# parser.add_argument('-t', '--tsv', action='store_true')
# parser.add_argument('-c', '--csv', action='store_true')
# parser.add_argument('--markdown', action='store_true')
# parser.add_argument('-s', '--sort-by', choices=['cpu', 'runtime', 'memory'])
#
# args = parser.parse_args(sys.argv[1:])
# print('tsv', args.tsv)
# print('csv', args.csv)
# print('md', args.markdown)
# print('sort', args.sort_by)
# print('type', type(args.input_dirs))
# for p in args.input_dirs:
#     print('path', p)
#

DATA = '''Name
ID
Type
Private DNS Zone Contributor
b12aa53e-6015-4669-85d0-8515ebb3ae7f
BuiltInRole
Start and Stop VM_
2aeb0baf-603a-49d6-b0f4-860c38e52692
CustomRole
Virtual Machine Administrator Login
1c0163c0-47e6-4577-8991-ea5c82e286e4
BuiltInRole
Virtual Machine Contributor
9980e02c-c2be-4d73-94e8-173b1dc7cf3c
BuiltInRole
Virtual Machine Data Access Administrator (preview)
66f75aeb-eabe-4b70-9f1e-c350c4c9ad04
BuiltInRole
Virtual Machine Local User Login
602da2ba-a5c2-41da-b01d-5360126ab525
BuiltInRole
Virtual Machine User Login
fb879df8-f326-4884-b1cf-06f3ad86be52
BuiltInRole
Windows 365 Network User
7eabc9a4-85f7-4f71-b8ab-75daaccc1033
BuiltInRole
Azure Arc Enabled Kubernetes Cluster User Role
00493d72-78f6-4148-b6c5-d3ce8e4799dd
BuiltInRole
Azure Kubernetes Service RBAC Writer
a7ffa36f-339b-4b5c-8bdf-e2c188b2c0eb
BuiltInRole
Azure Arc Kubernetes Admin
dffb1e0c-446f-4dde-a09f-99eb5cc68b96
BuiltInRole
Azure Arc Kubernetes Cluster Admin
8393591c-06b9-48a2-a542-1bd6b377f6a2
BuiltInRole
Azure Arc Kubernetes Viewer
63f0a09d-1495-4db4-a681-037d84835eb4
BuiltInRole
Azure Arc Kubernetes Writer
5b999177-9696-4545-85c7-50de3797e5a1
BuiltInRole
Azure Kubernetes Fleet Manager Contributor Role
63bb64ad-9799-4770-b5c3-24ed299a07bf
BuiltInRole
Azure Kubernetes Fleet Manager RBAC Admin
434fb43a-c01c-447e-9f67-c3ad923cfaba
BuiltInRole
Azure Kubernetes Fleet Manager RBAC Cluster Admin
18ab4d3d-a1bf-4477-8ad9-8359bc988f69
BuiltInRole
Azure Kubernetes Fleet Manager RBAC Reader
30b27cfc-9c84-438e-b0ce-70e35255df80
BuiltInRole
Azure Kubernetes Fleet Manager RBAC Writer
5af6afb3-c06c-4fa4-8848-71a8aee05683
BuiltInRole
Azure Kubernetes Service Cluster Admin Role
0ab0b1a8-8aac-4efd-b8c2-3ee1fb270be8
BuiltInRole
Azure Kubernetes Service Cluster Monitoring User
1afdec4b-e479-420e-99e7-f82237c7c5e6
BuiltInRole
Azure Kubernetes Service Cluster User Role
4abbcc35-e782-43d8-92c5-2d3f1bd2253f
BuiltInRole
Azure Kubernetes Service Contributor Role
ed7f3fbd-7b88-4dd4-9017-9adb7ce333f8
BuiltInRole
Azure Kubernetes Service Hybrid Cluster User Role
fc3f91a1-40bf-4439-8c46-45edbd83563a
BuiltInRole
Azure Kubernetes Service Hybrid Cluster Admin Role
b5092dac-c796-4349-8681-1a322a31c3f9
BuiltInRole
Azure Kubernetes Service Hybrid Contributor Role
e7037d40-443a-4434-a3fb-8cd202011e1d
BuiltInRole
Azure Kubernetes Service Policy Add-on Deployment
18ed5180-3e48-46fd-8541-4ea054d57064
BuiltInRole
Azure Kubernetes Service RBAC Admin
3498e952-d568-435e-9b2c-8d77e338d7f7
BuiltInRole
Azure Kubernetes Service RBAC Cluster Admin
b1ff04bb-8a4e-4dc4-8eb5-8693973ce19b
BuiltInRole
Azure Kubernetes Service RBAC Reader
7f6c6a51-bcf8-42ba-9220-52d62157d7db
BuiltInRole
Storage Blob Data Contributor
ba92f5b4-2d11-453d-a403-e96b0029c9fe
BuiltInRole
Storage Blob Data Owner
b7e6dc6d-f1e8-4753-8033-0f276bb0955b
BuiltInRole
Storage Blob Data Reader
2a2b9908-6ea1-4ae2-8e65-a410df84e7d1
BuiltInRole
Storage Blob Delegator
db58b8e5-c6ad-4a2a-8342-4190687cbf4a
BuiltInRole
'''

def run():
    count = 0
    role = ''
    for line in DATA.splitlines(keepends=False):
        # print("LINE:", line)
        count += 1
        if count % 3 == 1:
            # print(line, end='')
            role = line
        elif count % 3 == 0:
            print(f"{line} - {role}")


if __name__ == '__main__':
    run()