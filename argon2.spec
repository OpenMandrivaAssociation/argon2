%define major 1
%define libname %mklibname %{name}_ %{major}
%define develname %mklibname %{name} -d

%ifarch %{ix86}
# Required for various inline assembly bits
%global optflags %{optflags} -mmmx -msse -msse2
%endif

Summary:	The reference C implementation of Argon2
Name:		argon2
Version:	20171227
Release:	1
License:	ASL 2.0
Group:		System/Libraries
Url:		https://github.com/P-H-C/phc-winner-argon2
Source0:	https://github.com/P-H-C/phc-winner-argon2/archive/%{version}/phc-winner-%{name}-%{version}.tar.gz
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
%setup -q -n phc-winner-%{name}-%{version}

sed -i s,"LIBRARY_REL = lib","LIBRARY_REL = %{_lib}", Makefile
sed -i -e "s|@UPSTREAM_VER@|%{version}|" libargon2.pc
sed -i -e "s|lib/@HOST_MULTIARCH@|%{_lib}|" libargon2.pc

%build
%setup_compile_flags
%make

%install
%makeinstall_std

# we don't want these
find %{buildroot} -name '*.a' -delete

install -D -m 644 man/argon2.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -D -m 644 libargon2.pc %{buildroot}%{_libdir}/pkgconfig/lib%{name}.pc

%check
make test

%files
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{develname}
%doc CHANGELOG.md README.md LICENSE
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc
