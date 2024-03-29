%global pkg_name %{name}

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           gopa-modules-rhel8
Version:        0.9.1
Release:        1%{?dist}
Summary:        Set of modules to support in-place upgrade to RHEL8
Group:          System Environment/Libraries
License:        GPLv3+
URL:            https://github.com/swapdisk/gopa-modules-rhel8
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       gopa >= 2.6.2
BuildRequires:  gopa-tools >= 2.6.2


############################
# Per module requirements #
############################

# Why those requirements?
# /usr/bin/python and /usr/bin/python2 are already present.
Requires:       bash
Requires:       python
Requires:       coreutils

#do not require php even in presence of php scripts
#dependency filtering: https://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering
%if 0%{?fedora} || 0%{?rhel} > 6
%global __requires_exclude_from ^%{_datadir}
%else
%filter_requires_in %{_datadir}
%filter_setup
%endif

##############################
#  PATCHES HERE
##############################

####### PATCHES END ##########

# We do not want any autogenerated requires/provides based on content
%global __requires_exclude .*
%global __requires_exclude_from .*
%global __provides_exclude .*
%global __provides_exclude_from .*

%description
This package provides a base set of modules to support in-place
upgrade to RHEL8. These modules require that Gopa playbooks are
used to automate the upgrade with the required Leapp integration.


%prep
%setup -q -n %{name}-%{version}


%build
# This is all we need here. The RHEL8-results dir will be created
# with XCCDF files for Preupgrade Assistant and OpenSCAP
preupg-xccdf-compose RHEL8


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p -m 755 $RPM_BUILD_ROOT%{_datadir}/doc/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/preupgrade
mv LICENSE README.md $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/
mv RHEL8-results $RPM_BUILD_ROOT%{_datadir}/preupgrade/RHEL8

rm -rf $RPM_BUILD_ROOT/%{_datadir}/preupgrade/common

# General cleanup
find $RPM_BUILD_ROOT%{_datadir}/preupgrade/RHEL8 -regex ".*/\(module\|group\)\.ini$" -regextype grep -delete
find $RPM_BUILD_ROOT%{_datadir}/preupgrade/ -name "READY" -delete
find $RPM_BUILD_ROOT -name '.gitignore' -delete
find $RPM_BUILD_ROOT -name 'module_spec' -delete


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{_datadir}/doc/%{name}/
%doc %{_datadir}/doc/%{name}/LICENSE
%doc %{_datadir}/doc/%{name}/README.md
%dir %{_datadir}/preupgrade/RHEL8/
%{_datadir}/preupgrade/RHEL8/


%changelog
* Thu Jul 14 2022 Bob Mader <bmader@redhat.com> - 0.9.1-1
- Repackaging for fork to gopa-modules-rhel8

* Thu Aug 10 2017 Petr Stodulka <pstodulk@redhat.com> - 0.8.0-3
- Initial spec file created for modules of Preupgrade Assistant for
  upgrade&migration from RHEL 6.x system to RHEL 7.x system

