Name: libiscsi
Summary: iSCSI client library
Version: 1.9.0
Release: 3%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
URL: https://github.com/sahlberg/%{name}

Source: https://github.com/downloads/sahlberg/%{name}/%{name}-%{version}.tar.gz
Patch1: 0001-do-not-reconnect-if-reconnect-is-already-defered.patch
Patch2: 0002-fix-leak-of-iscsi_context-in-iscsi_reconnect.patch
Patch3: 0003-Add-ASCQ-codes-related-to-thin-provisioning.patch
Patch4: 0004-Create-safe-16-32-64-bit-accessors-for-reading-from-.patch
Patch5: 0005-fix-bug-in-md5-code.patch
Patch6: 0006-use-libgcrypt-for-MD5.patch
Patch7: 0007-URL-encoded-Targetnames.patch
Patch8: 0008-SCSI-add-a-safe-function-to-read-a-byte-from-the-dat.patch
Patch9: 0009-scsi-lowlevel-do-not-use-unsafe-pointer-casts.patch
Patch10: 0010-Add-a-cast-to-ssize_t.patch
Patch11: 0011-do-not-build-test-tool.patch
Patch12: 0012-bump-soname.patch
Patch13: 0013-disable-ld_iscsi.patch
Patch14: 0014-fix-another-aliasing-problem.patch
Patch15: 0015-fix-arm-aliasing-problem.patch
Patch16: 0016-avoid-casting-struct-sockaddr.patch
Patch18: 0018-cleanup-rename-pdu-written.patch
Patch19: 0019-fix-iovec-short-reads.patch
Patch20: 0020-iscsi_reconnect-Fix-a-use-after-free.patch
Patch21: 0021-Dont-reference-pdu-after-it-has-been-freed.patch
Patch22: 0022-lib-Make-scsi_free_scsi_task-accept-a-NULL-task-pointer.patch
Patch23: 0023-lib-Fix-a-memory-leak-in-scsi_cdb_persistent_reserve_out.patch
Patch24: 0024-reconnect-do-not-initialize-iscsi-to-old_iscsi-use-old_iscsi-if-appropriate.patch
Patch25: 0025-log-failures-typically-malloc-of-iscsi_create_context-during-reconnect.patch
Patch26: 0026-exit-after-malloc-failure-when-allocating-sense-data-blob.patch
Patch27: 0027-do-not-test-arrays-against-NULL.patch
Patch28: 0028-handle-bad-iscsi--fd-in-iscsi_service.patch
Patch29: 0029-rework-login-and-discovery-code-to-avoid-strlen-beyond-end-of-data.patch
Patch30: 0030-check-for-a-target-being-there-before-processing-TargetAddress.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: popt-devel
BuildRequires: libgcrypt-devel

%description
libiscsi is a library for attaching to iSCSI resources across
a network.


#######################################################################

# Conflict with iscsi-initiator-utils.

%global libiscsi_includedir %{_includedir}/iscsi
%global libiscsi_libdir %{_libdir}/iscsi

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1

%build
sh autogen.sh
%configure --libdir=%{libiscsi_libdir}
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install pkgconfigdir=%{_libdir}/pkgconfig %{?_smp_mflags}
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo %{libiscsi_libdir} > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf
rm $RPM_BUILD_ROOT/%{libiscsi_libdir}/libiscsi.a
rm $RPM_BUILD_ROOT/%{libiscsi_libdir}/libiscsi.la

# Remove "*.old" files
find $RPM_BUILD_ROOT -name "*.old" -exec rm -f {} \;

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING LICENCE-LGPL-2.1.txt README TODO
%{libiscsi_libdir}/libiscsi.so.*
/etc/ld.so.conf.d/*

%package utils
Summary: iSCSI Client Utilities
Group: Applications/System
License: GPLv2+
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
The libiscsi-utils package provides a set of assorted utilities to connect
to iSCSI servers without having to set up the Linux iSCSI initiator.

%files utils
%doc COPYING LICENCE-GPL-2.txt LICENCE-LGPL-2.1.txt README TODO
%{_bindir}/iscsi-ls
%{_bindir}/iscsi-inq
%{_bindir}/iscsi-readcapacity16

%package devel
Summary: iSCSI client development libraries
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The libiscsi-devel package includes the header files for libiscsi.

%files devel
%defattr(-,root,root)
%doc COPYING LICENCE-LGPL-2.1.txt README TODO
%{libiscsi_includedir}/iscsi.h
%{libiscsi_includedir}/scsi-lowlevel.h
%{libiscsi_libdir}/libiscsi.so
%{_libdir}/pkgconfig/libiscsi.pc

%changelog
* Thu Nov 07 2013 Miroslav Rezanina <mrezanin@redhat.com> - 1.9.0-3
- Fixed issues reported by coverity (bz #1026820)
- Do not mark /etc/ld.so.conf.d/ as config (bz #1011126)
- Resolves: #1026820 
- Resolves: #1011126 

* Tue Aug 27 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.9.0-2
- Add missing patch 11
- Resolves: #979953

* Tue Aug 27 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.9.0-1
- Rebase to 1.9.0
- Cherry-pick selected patches from upstream
- Resolves: #979953

* Thu Aug 1 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-6
- Add patch 6 to properly support escaped URIs produced by libvirt

* Mon Jul 1 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-5
- Add patch 5 to silence strict aliasing warnings

* Fri May 3 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-4
- Add patch 2 for FIPS mode
- Add patch 3 to avoid segmentation fault on iscsi-tools

* Thu Mar 7 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-3
- Correct license for libiscsi-utils, prefer %%global to %%define
- Add Requires
- Remove %clean section

* Fri Feb 22 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-2
- Use %config for ld.so.conf.d file.

* Fri Feb 22 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-1
- Initial version (bug 914752)
