%define __debug_install_post : > %{_builddir}/%{?buildsubdir}/debugfiles.list
%define debug_package %{nil}

%if 0%{?fedora} || 0%{?rhel} >= 7
%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))")}
%else
%global luaver  5.3
%global luanext 5.4
%endif

%global luapkgdir %{_libdir}/lua/%{luaver}
%global prever rc2


%if 0%{?el5}
# For some reason find-debuginfo.sh is still triggered on RHEL 5, despite
# BuildArch being noarch -- the script then fails. Explicitly disable it
%global debug_package %{nil}
%endif

Name:           luarocks
Version:        2.2.3
Release:        0.3.%{prever}%{?dist}
Summary:        A deployment and management system for Lua modules

License:        MIT
%if 0%{?rhel} <= 6
# RHEL 5's rpm requires this field
# RHEL 6's rpmlint warns if it is unspecified
Group:          Development/Tools
%endif
URL:            http://luarocks.org
Source0:        http://luarocks.org/releases/luarocks-%{version}-%{prever}.tar.gz

%if 0%{?el5}
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%endif

BuildRequires:  lua-devel
%if 0%{?fedora} || 0%{?rhel} >= 7
Requires:       lua(abi) = %{luaver}
%else
Requires:       lua >= %{luaver}
Requires:       lua <  %{luanext}
%endif
Requires:       unzip
Requires:       zip

%description
LuaRocks allows you to install Lua modules as self-contained packages
called "rocks", which also contain version dependency
information. This information is used both during installation, so
that when one rock is requested all rocks it depends on are installed
as well, and at run time, so that when a module is required, the
correct version is loaded. LuaRocks supports both local and remote
repositories, and multiple local rocks trees.


%prep
%setup -q
# Remove DOS line endings
for file in ; do
 sed "s|\r||g" $file > $file.new && \
 touch -r $file $file.new && \
 mv $file.new $file
done

sed -i 's|LUAROCKS_ROCKS_SUBDIR=/lib/luarocks/rocks|LUAROCKS_ROCKS_SUBDIR=/%{_lib}/luarocks/rocks|g' configure
sed -i 's|lib_modules_path = "/lib/lua/"..cfg.lua_version,|lib_modules_path = "/%{_lib}/lua/"..cfg.lua_version,|g' src/luarocks/cfg.lua

%build
./configure --prefix=%{_prefix}  --with-lua-lib=%{luapkgdir}
#{?_smp_mflags} -- luarocks makefile is not thread-safe
make


%install
%if 0%{?el5}
rm -rf $RPM_BUILD_ROOT
%endif
make install DESTDIR=$RPM_BUILD_ROOT LUADIR=%{luapkgdir}
# fix symlinks to versioned binaries
#for f in luarocks{,-admin};
#do
#  mv -f $RPM_BUILD_ROOT%{_bindir}/$f{-%{luaver},}
#done


%check
# TODO - find how to run this without having to pre-download entire rocks tree
# ./test/run_tests.sh


%files
%doc COPYING* README.md
%dir %{_sysconfdir}/luarocks
%config(noreplace) %{_sysconfdir}/luarocks/config-%{luaver}.lua
%{_bindir}/luarocks
%{_bindir}/luarocks-%{luaver}
%{_bindir}/luarocks-admin
%{_bindir}/luarocks-admin-%{luaver}
%{luapkgdir}/luarocks


%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-0.3.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 10 2015 Tom Callaway <spot@fedoraproject.org> - 2.2.3-0.2.rc2
- update to 2.2.3-rc2
- fix another case of /usr/lib pathing

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  2 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2
- Add runtime dependencies on unzip and zip (h/t Ignacio Burgueño)

* Thu Jan 15 2015 Tom Callaway <spot@fedoraproject.org> - 2.2.0-2
- rebuild for lua 5.3

* Fri Oct 17 2014 Michel Alexandre Salim <salimma@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 16 2014 Michel Salim <salimma@fedoraproject.org> - 2.1.2-1
- Update to 2.1.2

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 12 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.13-2
- rebuild for lua 5.2

* Mon Apr 22 2013 Michel Salim <salimma@fedoraproject.org> - 2.0.13-1
- Update to 2.0.13

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov  5 2012 Michel Salim <salimma@fedoraproject.org> - 2.0.12-1.1
- Fix macro problem affecting EPEL builds

* Mon Nov  5 2012 Michel Salim <salimma@fedoraproject.org> - 2.0.12-1
- Update to 2.0.12

* Fri Sep 28 2012 Michel Salim <salimma@fedoraproject.org> - 2.0.11-1
- Update to 2.0.11

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 11 2012 Michel Salim <salimma@fedoraproject.org> - 2.0.8-2
- Add support for RHEL's older lua packaging

* Tue May  8 2012 Michel Salim <salimma@fedoraproject.org> - 2.0.8-1
- Initial package
