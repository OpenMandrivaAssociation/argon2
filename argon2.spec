%define major 1
%define libname %mklibname %{name}_ %{major}
%define develname %mklibname %{name} -d

%global optflags %{optflags} -O3

Summary:	The reference C implementation of Argon2
Name:		argon2
Version:	20190702
Release:	5
License:	ASL 2.0
Group:		System/Libraries
Url:		https://github.com/P-H-C/phc-winner-argon2
Source0:	https://github.com/P-H-C/phc-winner-argon2/archive/%{version}/phc-winner-%{name}-%{version}.tar.gz
Patch0:		argon2-optflags.patch
Requires:	%{libname} = %{EVRD}

%description
This is the reference C implementation of Argon2, the password-hashing
function that won the Password Hashing Competition (PHC).

Argon2 is a password-hashing function that summarizes the state of the
art in the design of memory-hard functions and can be used to hash
passwords for credential storage, key derivation, or other applications.

#----------------------------------------------------

%package -n %{libname}
Summary:	The reference C implementation of Argon2
Group:		System/Libraries

%description -n %{libname}
Reference C implementation of Argon2, the password-hashing function
that won the Password Hashing Competition (PHC).

#----------------------------------------------------

%package -n %{develname}
Summary:	Development files for argon2
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{develname}
Headers for argon2, the reference C implementation of Argon2, the
password-hashing function that won the Password Hashing Competition (PHC).

#----------------------------------------------------

%prep
%autosetup -n phc-winner-%{name}-%{version} -p1

sed -i s,"LIBRARY_REL ?= lib.*","LIBRARY_REL = %{_lib}", Makefile
sed -i -e "s|@UPSTREAM_VER@|%{version}|" libargon2.pc.in
sed -i -e "s|lib/@HOST_MULTIARCH@|%{_lib}|" libargon2.pc.in

%build
%set_build_flags
%make_build RPM_OPT_FLAGS="%{optflags}"

%install
%make_install

# we don't want these
find %{buildroot} -name '*.a' -delete

install -D -m 644 man/argon2.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -D -m 644 libargon2.pc %{buildroot}%{_libdir}/pkgconfig/lib%{name}.pc

%if ! %{cross_compiling}
%check
make test
%endif

%files
%{_bindir}/%{name}
%doc %{_mandir}/man1/%{name}.1*

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{develname}
%doc CHANGELOG.md README.md LICENSE
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc
