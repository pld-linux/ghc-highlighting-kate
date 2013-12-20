#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	highlighting-kate
Summary:	Syntax highlighting
Summary(pl.UTF-8):	Podświetlanie składni
Name:		ghc-%{pkgname}
Version:	0.5.5.1
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/highlighting-kate
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	f29f4356fbee734c06dbbe18d332f61a
URL:		http://hackage.haskell.org/package/highlighting-kate
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-blaze-html >= 0.4.2
BuildRequires:	ghc-blaze-html < 0.7
BuildRequires:	ghc-containers
BuildRequires:	ghc-filepath
BuildRequires:	ghc-mtl
BuildRequires:	ghc-parsec
BuildRequires:	ghc-pcre-light
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-blaze-html-prof >= 0.4.2
BuildRequires:	ghc-blaze-html-prof < 0.7
BuildRequires:	ghc-containers-prof
BuildRequires:	ghc-filepath-prof
BuildRequires:	ghc-mtl-prof
BuildRequires:	ghc-parsec-prof
BuildRequires:	ghc-pcre-light-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 3
Requires:	ghc-base < 5
Requires:	ghc-blaze-html >= 0.4.2
Requires:	ghc-blaze-html < 0.7
Requires:	ghc-containers
Requires:	ghc-filepath
Requires:	ghc-mtl
Requires:	ghc-parsec
Requires:	ghc-pcre-light
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
highlighting-kate is a syntax highlighting library with support for
nearly one hundred languages. The syntax parsers are automatically
generated from Kate syntax descriptions (<http://kate-editor.org/>),
so any syntax supported by Kate can be added. An (optional)
command-line program is provided, along with a utility for generating
new parsers from Kate XML syntax descriptions.

%description -l pl.UTF-8
highlighting-kate to biblioteka do podświetlania składni z obsługą
prawie setki języków. Analizatory składni są automatycznie generowane
z opisów składni edytora Kate (<http://kate-editor.org/>), więc można
dodać dowolną składnię obsługiwaną przez Kate. Dostępny jest
(opcjonalny) działający z linii poleceń program wraz z narzędziem do
generowania nowych analizatorów z XML-owych opisów składni edytora
Kate.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 3
Requires:	ghc-base-prof < 5
Requires:	ghc-blaze-html-prof >= 0.4.2
Requires:	ghc-blaze-html-prof < 0.7
Requires:	ghc-containers-prof
Requires:	ghc-filepath-prof
Requires:	ghc-mtl-prof
Requires:	ghc-parsec-prof
Requires:	ghc-pcre-light-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc README
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HShighlighting-kate-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHShighlighting-kate-%{version}.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Paths_highlighting_kate.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Highlighting
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Highlighting/Kate.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Highlighting/Kate
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Highlighting/Kate/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Highlighting/Kate/Format
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Highlighting/Kate/Format/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Highlighting/Kate/Syntax
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Highlighting/Kate/Syntax/*.hi


%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHShighlighting-kate-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Paths_highlighting_kate.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Highlighting/Kate.p_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Highlighting/Kate
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Highlighting/Kate/*.p_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Highlighting/Kate/Format
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Highlighting/Kate/Format/*.p_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Highlighting/Kate/Syntax
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Highlighting/Kate/Syntax/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
