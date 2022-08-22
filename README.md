# Modules for in-place upgrade to RHEL8

The gopa-modules-rhel8 package provides a base set of modules to support in-place upgrade to RHEL8 using the [Gopa](https://github.com/swapdisk/gopa) framework. These modules require that [Gopa playbooks](https://github.com/swapdisk/gopa-playbooks) are used to automate the preupgrade and the OS upgrade with the required [Leapp](https://leapp.readthedocs.io/en/latest/) integration. Additional modules can be introduced by building a [gopa-modules-custom](https://github.com/swapdisk/gopa-modules-custom) package tailored to suit the requirements of your environment.

## Included modules

The package includes two modules required to integrate with the Gopa playbooks for OS upgrade to RHEL8.

### Leapp Preupgrade Results module

This module verifies that the Leapp preupgrade completed successfully and that no inhibitors were reported. Consecutive playbook tasks run the Leapp preupgrade immediately followed by the Gopa preupgrade which then triggers this module. If the Leapp preupgrade results are missing or are too old, the module will exit with failed result status and the solution text will explain that the Leapp report could not be found or is stale. 

If the Leapp report was generated successfully, the module next checks for any inhibitors, that is, any actors listed as a "high (inhibitor)" risk factor. If any inhibitors are found, the module will exit with failed result status. If no inhibitors are indicated, the module will exit with fixed result status. In either case, the generated Leapp report will be included in the solution text. 

### Snapshot Space module

This module verifies if there is sufficient free space in the root volume group to create LVM snapshots. If there is not sufficient space, the module exits with needs action result status and the solution text warns that rolling back using LVM snapshots will not be possible.

If there is enough space for snapshots, the snapshots sizes that will be created are reported in the solution text. Space requirement calculations are for demonstration purposes only and  should be reviewed based on the requirements of your unique environment.

If snapshots will be created, the module goes on to verify that the LVM snapshot autoextend option is enabled and recommended autoextend settings are configured. If the settings will be changed, this is reported with fixed result status. If the settings do not need to be changed, the module reports with passed result status.

